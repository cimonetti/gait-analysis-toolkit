"""Execute: python -m streamlit run app.py"""
import io
import json
import zipfile
import hashlib
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from marcha import ROOT, read_txt, extract, reference, make_figure, make_comparison
from multiplos import chave_par, ciclos_cabecalho, reunir_ciclos
from revisao import identificar_ciclos, remover_ciclos
from visual import cabecalho

st.set_page_config(page_title='LBA · Análise da marcha',page_icon=str(ROOT/'assets/logo_lba.png'),layout='wide')
cabecalho(ROOT)
plots=json.loads((ROOT/'plots.json').read_text(encoding='utf-8'))
config=json.loads((ROOT/'config.json').read_text(encoding='utf-8'))

@st.cache_data(show_spinner='Carregando grupo controle...')
def reference_cached(records, base, dp_mode, fingerprint):
    return reference(records, Path(base), dp_mode)


def parse_ticks(text):
    if not text.strip():
        return None
    values=[float(v) for v in text.replace(';',',').split(',')]
    if not all(np.isfinite(values)) or any(a >= b for a,b in zip(values,values[1:])):
        raise ValueError('Informe valores numéricos crescentes separados por vírgula.')
    return values

# Modelo compartilhado: não depende da ordem de renderização das abas.
title=st.session_state.get('titulo','Avaliação')
controls=st.session_state.get('controls',True)
both=st.session_state.get('both',True)
individual=st.session_state.get('individual',True)
stance={side: [st.session_state.get('apoio_media_'+side,60.),st.session_state.get('apoio_dp_'+side,2.)]
        if st.session_state.get('apoio_enable_'+side,False) else None for side in ('D','E')}
axes_errors=[]
for key,spec in plots.items():
    spec['ylim']=[st.session_state.get(key+'min',float(spec['ylim'][0])),st.session_state.get(key+'max',float(spec['ylim'][1]))]
    try:
        spec['yticks']=parse_ticks(st.session_state.get(key+'ticks',','.join(str(v) for v in spec['yticks'])))
        if spec['ylim'][0]>=spec['ylim'][1]: raise ValueError('Mínimo deve ser menor que máximo.')
    except ValueError as exc:
        axes_errors.append(spec['title']+': '+str(exc))
groups=config['grupos_controle']
group_name=st.session_state.get('grupo_controle',config['grupo_controle_padrao'])
group_path=ROOT/groups[group_name]
group=json.loads(group_path.read_text(encoding='utf-8'))
ref=None
control_error=None
if controls:
    if not group['controles']:
        control_error=group.get('status','Grupo controle sem arquivos cadastrados.')
    else:
        try:
            fingerprint=tuple((str(path),path.stat().st_mtime_ns,path.stat().st_size)
                              for r in group['controles'] for path in (group_path.parent/r['qjt'],group_path.parent/r['pp']))
            ref=reference_cached(group['controles'],str(group_path.parent),'ambos' if both else 'esquerdo',fingerprint)
        except (ValueError,FileNotFoundError) as exc:
            control_error=str(exc)
loaded_state=st.session_state.get('loaded')
curves=loaded_state['curves'] if loaded_state else None
provenance=loaded_state['provenance'] if loaded_state else []
ids=identificar_ciclos(provenance)
lookup={r['id']:r for rows in ids.values() for r in rows}
labels={key:f"{key} — tentativa {r['tentativa']}, ciclo {r['ciclo_local']} — {r['qjt']}" for key,r in lookup.items()}
excluded=st.session_state.get('excluded',[])
with st.sidebar:
    st.markdown('### Seu laudo')
    st.write('**Referência selecionada**')
    st.write(group_name if controls else 'Sem grupo controle')
    if controls and group['controles']:
        total_d=sum(r['ciclos_d'] for r in group['controles'])
        total_e=sum(r['ciclos_e'] for r in group['controles'])
        st.write(f"{len(group['controles'])} tentativas · {total_d} ciclos D · {total_e} ciclos E")
    st.divider()
    st.write('**Fluxo de trabalho**')
    st.write('1. Selecione suas tentativas')
    st.write('2. Gere e confira as figuras')
    st.write('3. Edite ciclos, se necessário')
    st.write('4. Exporte para o laudo')
    if group_name=='Demonstração sintética' and controls:
        st.caption('Referência sintética criada apenas para demonstração.')

signature=st.session_state.get('input_signature','')
if st.session_state.pop('ir_para_figuras',False):
    st.session_state['aba_ativa']='Figuras'
data_tab, figure_tab, review_tab, axes_tab=st.tabs(['Arquivos e opções','Figuras','Editar ciclos','Ajustar eixos Y'],key='aba_ativa',on_change='rerun')


def excluir_selecionado(cycle):
    st.session_state['excluded']=list(dict.fromkeys(st.session_state.get('excluded',[])+[cycle]))
    st.session_state.pop('resultado',None)


def restaurar_todos():
    st.session_state['excluded']=[]
    st.session_state.pop('resultado',None)

with data_tab:
    st.subheader('Prepare sua avaliação')
    st.caption('Carregue os dois conjuntos de arquivos e confira os pares antes de gerar.')
    q_files=st.file_uploader('TXT Quadril / Joelho / Tornozelo (QJT) — selecione uma ou várias tentativas',type=['txt'],accept_multiple_files=True)
    p_files=st.file_uploader('TXT Pelve / Pé (PP) — selecione os pares correspondentes',type=['txt'],accept_multiple_files=True)
    st.caption('Você pode selecionar vários arquivos com Ctrl. Confirme abaixo qual PP corresponde a cada QJT; os ciclos serão reunidos na mesma figura.')
    records=[]
    if q_files and p_files:
        st.subheader('Pares de arquivos e ciclos por tentativa')
        for i,q in enumerate(q_files):
            identity=hashlib.sha256(q.name.encode()+q.getvalue()).hexdigest()[:16]
            inferred=ciclos_cabecalho(q.getvalue())
            matches=[j for j,p in enumerate(p_files) if chave_par(p.name)==chave_par(q.name)]
            choices=[None]+list(range(len(p_files)))
            default=matches[0]+1 if len(matches)==1 else 0
            with st.container(border=True):
                st.write(f'**Tentativa {i+1}: {q.name}**')
                selection=st.selectbox('Arquivo PP correspondente',choices,index=default,
                    format_func=lambda j:'Selecione o par PP' if j is None else p_files[j].name,
                    key=f'pair_{identity}_{hashlib.sha256(chr(0).join(p.name for p in p_files).encode()).hexdigest()[:12]}')
                c1,c2=st.columns(2)
                nd=c1.number_input('Ciclos direitos desta tentativa',min_value=0,
                    value=inferred[0] if inferred else 1,step=1,key=f'nd_{identity}')
                ne=c2.number_input('Ciclos esquerdos desta tentativa',min_value=0,
                    value=inferred[1] if inferred else 1,step=1,key=f'ne_{identity}')
                if inferred:
                    st.caption(f'Cabeçalho QJT: {inferred[0]} ciclos direitos e {inferred[1]} esquerdos.')
                else:
                    st.warning('Não foi possível identificar os ciclos no cabeçalho. Informe as quantidades manualmente.')
                records.append((q,p_files[selection] if selection is not None else None,int(nd),int(ne)))
        st.write(f"**Total selecionado: {sum(r[2] for r in records)} ciclos direitos e {sum(r[3] for r in records)} esquerdos.**")
    title=st.text_input('Título da avaliação','Avaliação',key='titulo')
    st.subheader('Marcação da fase de apoio')
    st.caption('Opcional. Mostra quando o pé deixa o solo e começa a fase de balanço: uma linha vertical na média do final do apoio e uma faixa correspondente à média ± 1 desvio-padrão (DP).')
    st.caption('Informe os valores obtidos na avaliação, separadamente para cada lado. Exemplo: média 60% e DP 2 representam uma linha em 60% do ciclo e uma faixa de 58% a 62%. Esses valores não são calculados a partir dos TXT angulares.')
    a,b=st.columns(2)
    stance={}
    for side,col in [('D',a),('E',b)]:
        with col:
            with st.container(border=True):
                name='Direito' if side=='D' else 'Esquerdo'
                st.markdown('**Lado '+name.lower()+'**')
                enable=st.checkbox('Marcar o final do apoio — '+name.lower(),value=False,key='apoio_enable_'+side,
                    help='Ative somente quando tiver a média e o DP da fase de apoio deste lado. Desligado, nenhuma linha ou faixa de apoio aparece no laudo.')
                mean=st.number_input('Final do apoio: média (% do ciclo)',min_value=0.,max_value=100.,value=60.,key='apoio_media_'+side,disabled=not enable,
                    help='Percentual do ciclo em que o pé deixa o solo, em média. Por exemplo, 60,19 significa 60,19% do ciclo.')
                sd=st.number_input('Variação entre ciclos: DP (pontos percentuais)',min_value=0.,value=2.,key='apoio_dp_'+side,disabled=not enable,
                    help='Desvio-padrão do final do apoio entre os ciclos. Não é o DP dos ângulos nem o DP do controle.')
                if enable:
                    st.caption(f'No laudo: linha em {mean:g}% e faixa de {mean-sd:g}% a {mean+sd:g}% do ciclo.')
                else:
                    st.caption('Sem marcação de apoio nos gráficos deste lado.')
                stance[side]=[mean,sd] if enable else None
    st.subheader('Referência para comparação')
    controls=st.checkbox('Mostrar curvas do grupo controle ao fundo',value=True,key='controls',
        help='Adiciona a média e a faixa de ± 1 DP da referência. As curvas da avaliação continuam sendo mostradas por cima.')
    st.caption('A linha cinza representa a média do controle; a faixa cinza mostra a variação de ± 1 DP. Desmarque para mostrar apenas a avaliação.')
    st.selectbox('Grupo controle',list(groups),key='grupo_controle',disabled=not controls,
        help='A versão pública inclui somente a referência sintética de demonstração.')
    if controls:
        if group_name=='Demonstração sintética':
            st.caption('Demonstração: 2 tentativas sintéticas, com 4 ciclos de cada lado. Sem valores normativos.')
        else:
            st.caption('Referência definida na configuração local.')
    if control_error: st.warning(control_error)
    both=st.checkbox('Pelve sagital: usar os dois lados no DP do controle',value=True,key='both',disabled=not controls,
        help='Marcado: DP calculado com ciclos direitos e esquerdos. Desmarcado: DP só dos ciclos esquerdos, para reproduzir a rotina antiga. A média permanece bilateral.')
    st.caption('Esta opção altera somente a largura da faixa cinza da pelve sagital. Marcada, usa os ciclos dos dois lados; desmarcada, usa apenas os esquerdos. Não altera as curvas do paciente.')
    st.subheader('Curvas da avaliação')
    individual=st.checkbox('Mostrar cada ciclo individualmente',value=True,key='individual',
        help='Marcado: uma curva para cada ciclo mantido. Desmarcado: uma única curva média por lado, considerando os ciclos mantidos.')
    st.caption('Marcado: todas as curvas dos arquivos selecionados, azul à direita e vermelho à esquerda. Desmarcado: apenas a média dos ciclos mantidos de cada lado. Você pode excluir ciclos depois na aba Editar ciclos.')
    signature=hashlib.sha256()
    for q,p,nd,ne in records:
        signature.update(q.name.encode()); signature.update(q.getvalue())
        if p is not None:
            signature.update(p.name.encode()); signature.update(p.getvalue())
        signature.update(f'{nd}/{ne}'.encode())
    signature=signature.hexdigest()
    if st.session_state.get('input_signature') != signature:
        st.session_state.pop('loaded',None)
        st.session_state.pop('previews',None)
        st.session_state.pop('resultado',None)
        st.session_state['input_signature']=signature
    if st.button('Gerar figuras',type='primary'):
        st.session_state.pop('loaded',None)
        st.session_state.pop('previews',None)
        if control_error or axes_errors:
            st.error(control_error or '\n'.join(axes_errors))
        elif not records or any(p is None for q,p,nd,ne in records):
            st.error('Selecione os arquivos QJT e PP e confirme todos os pares.')
        elif len({p.name for q,p,nd,ne in records}) != len(records):
            st.error('Um mesmo PP foi associado a mais de um QJT. Revise os pares.')
        elif len({q.name for q,p,nd,ne in records}) != len(records):
            st.error('Há nomes QJT repetidos. Renomeie as tentativas para identificá-las sem ambiguidade.')
        else:
            try:
                import tempfile
                loaded=[]
                provenance=[]
                with tempfile.TemporaryDirectory() as folder:
                    for i,(q,p,nd,ne) in enumerate(records):
                        if nd+ne==0:
                            raise ValueError(f'{q.name}: informe pelo menos um ciclo.')
                        inferred=ciclos_cabecalho(q.getvalue())
                        if inferred is not None and inferred != (nd,ne):
                            raise ValueError(f'{q.name}: quantidades informadas divergem do cabeçalho {inferred}.')
                        qp=Path(folder)/f'qjt_{i}.txt'; pp=Path(folder)/f'pp_{i}.txt'
                        qp.write_bytes(q.getvalue()); pp.write_bytes(p.getvalue())
                        qdata,pdata=read_txt(qp),read_txt(pp)
                        if qdata.shape[1] != 1+9*(nd+ne) or pdata.shape[1] != 1+6*(nd+ne):
                            raise ValueError(f'{q.name} / {p.name}: colunas incompatíveis com os ciclos informados.')
                        loaded.append(extract(qdata,pdata,nd,ne))
                        provenance.append({'qjt':q.name,'pp':p.name,'ciclos_d':nd,'ciclos_e':ne})
                curves=reunir_ciclos(loaded)
                st.session_state['loaded']={'curves':curves,'provenance':provenance}
                st.session_state['excluded']=[]
                st.session_state.pop('resultado',None)
                st.session_state['auto_generate']=True
                st.session_state['ir_para_figuras']=True
                st.rerun()
            except Exception as exc:
                st.error(str(exc))
with axes_tab:
    st.subheader('Ajustes dos gráficos')
    st.caption('Defina a escala e as marcações. Os mesmos limites são usados nos dois lados.')
    if axes_errors:
        for error in axes_errors: st.error(error)
    for key,spec in plots.items():
        c1,c2,c3=st.columns([2,1,1])
        c1.write(spec['title'])
        lo=c2.number_input('Mínimo',value=float(spec['ylim'][0]),key=key+'min')
        hi=c3.number_input('Máximo',value=float(spec['ylim'][1]),key=key+'max')
        spec['ylim']=[lo,hi]
        st.text_input('Marcações Y (separadas por vírgula; vazio = automático)',value=','.join(str(v) for v in spec.get('yticks') or []),key=key+'ticks')
    st.download_button('Salvar configuração dos eixos',json.dumps(plots,ensure_ascii=False,indent=2),'plots.json','application/json')

with review_tab:
    if 'loaded' not in st.session_state:
        st.info('Selecione os pares na aba Arquivos e opções e clique em Gerar figuras.')
    else:
        st.caption('Passe o mouse para identificar a curva. Use a ferramenta de seleção de pontos para selecionar um ciclo e clique em Excluir ciclo selecionado. A exclusão afeta todos os segmentos daquele ciclo e pode ser desfeita.')
        excluded=st.multiselect('Ciclos excluídos — retire um item para restaurá-lo',list(lookup),
                                format_func=lambda key:labels[key],key='excluded')
        st.button('Restaurar todos os ciclos',on_click=restaurar_todos)
        c1,c2=st.columns(2)
        side=c1.radio('Lado para revisar',['D','E'],format_func=lambda x:'Direito' if x=='D' else 'Esquerdo',horizontal=True)
        variable=c2.selectbox('Gráfico para revisar',list(plots),format_func=lambda key:plots[key]['title'])
        chart=go.Figure()
        x=np.arange(101)
        if ref:
            mean,sd=ref[variable]
            chart.add_trace(go.Scatter(x=x,y=mean-sd,mode='lines',line={'width':0},showlegend=False,hoverinfo='skip'))
            chart.add_trace(go.Scatter(x=x,y=mean+sd,mode='lines',line={'width':0},fill='tonexty',fillcolor='rgba(150,150,150,.25)',name='Controle ± DP',hoverinfo='skip'))
            chart.add_trace(go.Scatter(x=x,y=mean,mode='lines',line={'color':'gray','width':1},name='Média controle',hoverinfo='skip'))
        values=curves[variable.replace('_',side+'_',1)]
        for r in ids[side]:
            removed=r['id'] in excluded
            chart.add_trace(go.Scatter(x=x,y=values[:,r['coluna']],mode='lines+markers',
                name=r['id']+(' (excluído)' if removed else ''),
                line={'width':1 if removed else 2,'dash':'dot' if removed else 'solid'},
                marker={'size':3},opacity=.2 if removed else .85,
                customdata=[[r['id']]]*101,
                hovertemplate=labels[r['id']]+'<br>Ciclo: %{x}%<br>Ângulo: %{y:.2f}°<extra></extra>'))
        chart.update_layout(height=470,title=plots[variable]['title'],dragmode='select',
                            xaxis_title='Ciclo (%)',yaxis_title='Graus (°)',hovermode='closest')
        chart.update_xaxes(range=[0,100]); chart.update_yaxes(range=plots[variable]['ylim'],tickmode='array' if plots[variable].get('yticks') else 'auto',tickvals=plots[variable].get('yticks'))
        event=st.plotly_chart(chart,width='stretch',on_select='rerun',
            selection_mode=('points','box','lasso'),key='revision_chart_'+side+'_'+variable+'_'+signature)
        selected=[]
        for point in event.selection.points:
            custom=point.get('customdata')
            key=custom[0] if isinstance(custom,(tuple,list)) and custom else custom
            if key in lookup and key not in selected:
                selected.append(key)
        available=[r['id'] for r in ids[side] if r['id'] not in excluded]
        if available:
            candidates=[key for key in selected if key in available]
            selected_cycle=st.selectbox('Ciclo selecionado para excluir',available,
                index=available.index(candidates[-1]) if candidates else 0,
                format_func=lambda key:labels[key],
                key='target_'+side+'_'+hashlib.sha256(repr((selected,excluded)).encode()).hexdigest()[:12])
            st.button('Excluir ciclo selecionado',on_click=excluir_selecionado,args=(selected_cycle,))
        m1,m2=st.columns(2)
        m1.metric('Ciclos direitos mantidos',sum(r['id'] not in excluded for r in ids['D']))
        m2.metric('Ciclos esquerdos mantidos',sum(r['id'] not in excluded for r in ids['E']))
        st.write('**Mantidos:** '+', '.join(f"{sum(r['id'] not in excluded for r in ids[s])} ciclos {'direitos' if s=='D' else 'esquerdos'}" for s in ('D','E')))

with figure_tab:
    st.subheader('Figuras do laudo')
    if 'loaded' not in st.session_state:
        st.info('Selecione os arquivos e clique em Gerar figuras na primeira aba.')
    else:
        # Exportação é invalidada quando opções, eixos ou exclusões mudam.
        output_signature=hashlib.sha256(json.dumps([signature,title,plots,stance,controls,group_name,fingerprint if ref is not None else None,both,individual,excluded],sort_keys=True).encode()).hexdigest()
        pending=st.session_state.get('output_signature') != output_signature
        if pending and st.session_state.get('previews'):
            st.info('Há alterações pendentes. Clique em Gerar figuras novamente para aplicá-las.')
        regenerate=st.button('Gerar figuras novamente',type='primary')
        auto=st.session_state.pop('auto_generate',False)
        if (regenerate or auto) and (control_error or axes_errors):
            st.error(control_error or '\n'.join(axes_errors))
        elif regenerate or auto:
            try:
                kept=remover_ciclos(curves,ids,excluded)
                bundle=io.BytesIO()
                previews=[]
                with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as archive:
                    for s in ('D','E'):
                        fig=make_figure(kept,s,plots,ref,stance[s],title,individual)
                        for ext in ('png','svg'):
                            data=io.BytesIO(); fig.savefig(data,format=ext,dpi=300)
                            archive.writestr(f'avaliacao_{s}.{ext}',data.getvalue())
                            if ext=='png': previews.append(data.getvalue())
                        plt.close(fig)
                    fig=make_comparison(kept,plots,ref,title)
                    for ext in ('png','svg'):
                        data=io.BytesIO(); fig.savefig(data,format=ext,dpi=300)
                        archive.writestr(f'comparacao_medias.{ext}',data.getvalue())
                        if ext=='png': previews.append(data.getvalue())
                    plt.close(fig)
                    archive.writestr('grupo_controle.json',json.dumps({'grupo':group_name if controls else None,'dp_pelve_sagital':'ambos' if both else 'esquerdo'},ensure_ascii=False,indent=2))
                    archive.writestr('tentativas.json',json.dumps(provenance,ensure_ascii=False,indent=2))
                    archive.writestr('revisao_ciclos.json',json.dumps({'ciclos':ids,'excluidos':excluded,'mantidos':[key for key in lookup if key not in excluded]},ensure_ascii=False,indent=2))
                    arrays=io.BytesIO(); np.savez(arrays,**kept)
                    archive.writestr('avaliacao_ciclos.npz',arrays.getvalue())
                    archive.writestr('plots.json',json.dumps(plots,ensure_ascii=False,indent=2))
                st.session_state['resultado']=bundle.getvalue()
                st.session_state['previews']=previews
                st.session_state['output_signature']=output_signature
                pending=False
            except Exception as exc:
                st.error(str(exc))
        preview_columns=st.columns(2)
        for i,preview in enumerate(st.session_state.get('previews',[])[:2]):
            with preview_columns[i]:
                st.markdown('#### '+('Direito' if i==0 else 'Esquerdo'))
                st.image(preview)
        if len(st.session_state.get('previews',[]))>2:
            st.markdown('#### Comparação das médias')
            st.caption('Azul: média direita · Vermelho: média esquerda · Cinza: média do controle ± 1 DP. Considera somente os ciclos mantidos.')
            st.image(st.session_state['previews'][2])
        if 'resultado' in st.session_state and not pending:
            st.download_button('Baixar figuras PNG + SVG',st.session_state['resultado'],'figuras_marcha.zip','application/zip')
