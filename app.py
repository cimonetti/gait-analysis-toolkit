"""Execute: python -m streamlit run app.py"""
import io
import json
import zipfile
import hashlib
import warnings
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from marcha import ROOT, reference, make_figure, make_comparison
from multiplos import chave_par, ciclos_cabecalho, carregar_condicao
from revisao import identificar_ciclos, remover_ciclos, ciclos_incompletos
from visual import cabecalho
from apoio import saida_do_pe
from marcha import load_record
import indices
import gdi

st.set_page_config(page_title='LBA · Análise da marcha',page_icon=str(ROOT/'assets/logo_lba.png'),layout='wide')
cabecalho(ROOT)
plots=json.loads((ROOT/'plots.json').read_text(encoding='utf-8'))
config=json.loads((ROOT/'config.json').read_text(encoding='utf-8'))
ss=st.session_state
# Sufixos das chaves de estado: '' = condição 1 (ou avaliação única), '_b' = condição 2.
CONDICOES=('','_b')

@st.cache_data(show_spinner='Carregando grupo controle...')
def reference_cached(records, base, dp_mode, fingerprint):
    return reference(records, Path(base), dp_mode)


@st.cache_data(show_spinner='Carregando a base do GDI...')
def gdi_base_cached(raiz, assinatura):
    return gdi.carregar_base(raiz)


@st.cache_data(show_spinner='Calculando a referência do GPS...')
def gps_ref_cached(records, base, fingerprint):
    return indices.referencia([load_record(r, Path(base), allow_unilateral=True) for r in records])


def parse_ticks(text):
    if not text.strip():
        return None
    values=[float(v) for v in text.replace(';',',').split(',')]
    if not all(np.isfinite(values)) or any(a >= b for a,b in zip(values,values[1:])):
        raise ValueError('Informe valores numéricos crescentes separados por vírgula.')
    return values


def nome_condicao(suf):
    padrao='Condição 1' if suf=='' else 'Condição 2'
    return (ss.get('nome_c1' if suf=='' else 'nome_c2') or padrao).strip() or padrao


def estado_condicao(suf):
    loaded=ss.get('loaded'+suf)
    provenance=loaded['provenance'] if loaded else []
    ids=identificar_ciclos(provenance)
    lookup={r['id']:r for rows in ids.values() for r in rows}
    labels={key:f"{key} — tentativa {r['tentativa']}, ciclo {r['ciclo_local']} — {r['qjt']}" for key,r in lookup.items()}
    incompletos=ss.get('incompletos'+suf,[])
    # Ciclos incompletos ficam fora da edição e sempre fora das figuras.
    editaveis={side:[r for r in rows if r['id'] not in incompletos] for side,rows in ids.items()}
    excluded=[k for k in ss.get('excluded'+suf,[]) if k in lookup and k not in incompletos]
    return {'curves':loaded['curves'] if loaded else None,'provenance':provenance,'ids':ids,
            'editaveis':editaveis,'lookup':lookup,'labels':labels,'excluded':excluded,
            'incompletos':incompletos,'fora':excluded+incompletos}

# Modelo compartilhado: não depende da ordem de renderização das abas.
title=ss.get('titulo','Avaliação')
controls=ss.get('controls',True)
both=ss.get('both',True)
individual=ss.get('individual',True)
comparar=ss.get('comparar',False)
MODO_TEMPOS='Tempos (s)'
MODO_PERCENTUAL='% do ciclo'


def apoio_do_estado(side, suf):
    """[média, DP] da saída do pé em % do ciclo, ou None se desligado/incompleto."""
    if not ss.get('apoio_enable_'+side+suf,False):
        return None
    if ss.get('apoio_modo_'+side+suf,MODO_TEMPOS)==MODO_PERCENTUAL:
        return [ss.get('apoio_media_'+side+suf,60.),ss.get('apoio_dp_'+side+suf,2.)]
    try:
        r=saida_do_pe(ss.get('t_apoio_'+side+suf,0.),ss.get('dp_apoio_'+side+suf,0.),ss.get('t_ciclo_'+side+suf,0.),
                      ss.get('t_balanco_'+side+suf,0.),ss.get('dp_balanco_'+side+suf,0.))
    except ValueError:
        return None
    return [round(r['media'],2),round(r['dp'],2)]


stance={suf:{side:apoio_do_estado(side,suf) for side in ('D','E')} for suf in CONDICOES}
axes_errors=[]
for key,spec in plots.items():
    spec['ylim']=[ss.get(key+'min',float(spec['ylim'][0])),ss.get(key+'max',float(spec['ylim'][1]))]
    try:
        spec['yticks']=parse_ticks(ss.get(key+'ticks',','.join(str(v) for v in spec['yticks'])))
        if spec['ylim'][0]>=spec['ylim'][1]: raise ValueError('Mínimo deve ser menor que máximo.')
    except ValueError as exc:
        axes_errors.append(spec['title']+': '+str(exc))
groups=config['grupos_controle']
group_name=ss.get('grupo_controle',config['grupo_controle_padrao'])
group_path=ROOT/groups[group_name]
group=json.loads(group_path.read_text(encoding='utf-8'))
ref=None
gps_ref=None
fingerprint=None
control_error=None
if controls:
    if not group['controles']:
        control_error=group.get('status','Grupo controle sem arquivos cadastrados.')
    else:
        try:
            fingerprint=tuple((str(path),path.stat().st_mtime_ns,path.stat().st_size)
                              for r in group['controles'] for path in (group_path.parent/r['qjt'],group_path.parent/r['pp']))
            ref=reference_cached(group['controles'],str(group_path.parent),'ambos' if both else 'esquerdo',fingerprint)
            gps_ref=gps_ref_cached(group['controles'],str(group_path.parent),fingerprint)
        except (ValueError,FileNotFoundError) as exc:
            control_error=str(exc)
conds={suf:estado_condicao(suf) for suf in CONDICOES}
gdi_erro=None
try:
    _arqs=[ROOT/gdi.PASTA/a for a in (gdi.ARQ_FEATURES,gdi.ARQ_CONTROLES)]
    gdi_base=gdi_base_cached(str(ROOT),tuple((str(a),a.stat().st_mtime_ns) for a in _arqs if a.exists()))
except ValueError as exc:
    gdi_base,gdi_erro=None,str(exc)
duas_condicoes=comparar and 'loaded_b' in ss
ABAS=['Arquivos e opções','Figuras','Editar ciclos','Ajustar eixos Y']


def ir_para(aba):
    ss['aba_ativa']=aba


signature=ss.get('input_signature','')
if ss.pop('ir_para_figuras',False):
    ss['aba_ativa']='Figuras'
# A navegação fica na barra lateral; a barra de abas do topo é escondida.
# As abas continuam existindo para que todos os campos permaneçam carregados.
st.markdown('<style>[data-testid="stTabs"] [role="tablist"]{display:none;}'
            '[data-testid="stSidebar"] button[kind="secondary"]{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.22);}'
            '[data-testid="stSidebar"] button[kind="secondary"]:hover{background:rgba(255,255,255,.16);border-color:rgba(255,255,255,.45);}'
            '[data-testid="stSidebar"] button[kind="secondary"] p{color:#f5f6fb !important;}'
            '[data-testid="stSidebar"] button[kind="primary"] p{color:white !important;}'
            '[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] *,'
            '[data-testid="stSidebarHeader"] button *{color:#f5f6fb !important;fill:#f5f6fb !important;}'
            '</style>',unsafe_allow_html=True)
with st.sidebar:
    st.markdown('### Navegação')
    atual=ss.get('aba_ativa',ABAS[0])
    for i,aba in enumerate(ABAS,1):
        st.button(f'{i}. {aba}',key='nav_'+str(i),on_click=ir_para,args=(aba,),
                  type='primary' if aba==atual else 'secondary',width='stretch')
data_tab, figure_tab, review_tab, axes_tab=st.tabs(ABAS,key='aba_ativa',on_change='rerun')


# A lista de exclusões fica em 'excluded'+suf, fora de qualquer widget: o Streamlit
# apaga o estado de widgets que não são desenhados (ex.: a lista da outra condição).
def _nova_versao(suf):
    ss['versao_exclusoes'+suf]=ss.get('versao_exclusoes'+suf,0)+1
    ss.pop('resultado',None)


def excluir_selecionado(cycle, suf):
    ss['excluded'+suf]=list(dict.fromkeys(ss.get('excluded'+suf,[])+[cycle]))
    _nova_versao(suf)


def restaurar_todos(suf):
    ss['excluded'+suf]=[]
    _nova_versao(suf)


def sincronizar_exclusoes(suf, chave):
    ss['excluded'+suf]=list(ss.get(chave,[]))
    _nova_versao(suf)


def selecionar_pares(suf):
    """Uploaders e pareamento QJT/PP de uma condição. Retorna (qjt, pp, nd, ne) por tentativa."""
    q_files=st.file_uploader('TXT Quadril / Joelho / Tornozelo (QJT) — selecione uma ou várias tentativas',type=['txt'],accept_multiple_files=True,key='q_files'+suf)
    p_files=st.file_uploader('TXT Pelve / Pé (PP) — selecione os pares correspondentes',type=['txt'],accept_multiple_files=True,key='p_files'+suf)
    st.caption('Você pode selecionar vários arquivos com Ctrl. Confirme abaixo qual PP corresponde a cada QJT; os ciclos serão reunidos na mesma figura.')
    records=[]
    if q_files and p_files:
        st.markdown('**Pares de arquivos e ciclos por tentativa**')
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
                    key=f'pair{suf}_{identity}_{hashlib.sha256(chr(0).join(p.name for p in p_files).encode()).hexdigest()[:12]}')
                c1,c2=st.columns(2)
                nd=c1.number_input('Ciclos direitos desta tentativa',min_value=0,
                    value=inferred[0] if inferred else 1,step=1,key=f'nd{suf}_{identity}')
                ne=c2.number_input('Ciclos esquerdos desta tentativa',min_value=0,
                    value=inferred[1] if inferred else 1,step=1,key=f'ne{suf}_{identity}')
                if inferred:
                    st.caption(f'Cabeçalho QJT: {inferred[0]} ciclos direitos e {inferred[1]} esquerdos.')
                else:
                    st.warning('Não foi possível identificar os ciclos no cabeçalho. Informe as quantidades manualmente.')
                records.append((q,p_files[selection] if selection is not None else None,int(nd),int(ne)))
        st.write(f"**Total selecionado: {sum(r[2] for r in records)} ciclos direitos e {sum(r[3] for r in records)} esquerdos.**")
    return records


def campos_apoio(suf):
    a,b=st.columns(2)
    for side,col in [('D',a),('E',b)]:
        with col:
            with st.container(border=True):
                name='Direito' if side=='D' else 'Esquerdo'
                st.markdown('**Lado '+name.lower()+'**')
                enable=st.checkbox('Marcar a saída do pé — '+name.lower(),value=False,key='apoio_enable_'+side+suf,
                    help='Mostra uma linha vertical na média da saída do pé e uma faixa de ± 1 DP. Desligado, nenhuma marcação aparece no laudo.')
                modo=st.radio('Informar por',[MODO_TEMPOS,MODO_PERCENTUAL],horizontal=True,key='apoio_modo_'+side+suf,disabled=not enable,
                    help='Tempos: digite os valores do relatório temporal (apoio, balanço e ciclo) e a % é calculada. % do ciclo: digite a média e o DP já em porcentagem.')
                if modo==MODO_TEMPOS:
                    c1,c2=st.columns(2)
                    c1.number_input('Tempo de apoio (s)',min_value=0.,value=0.,step=.001,format='%.3f',key='t_apoio_'+side+suf,disabled=not enable)
                    c2.number_input('DP do apoio (s)',min_value=0.,value=0.,step=.001,format='%.3f',key='dp_apoio_'+side+suf,disabled=not enable)
                    c1.number_input('Tempo de balanço (s)',min_value=0.,value=0.,step=.001,format='%.3f',key='t_balanco_'+side+suf,disabled=not enable,
                        help='Fase aérea do membro. Usado para conferir se apoio + balanço ≈ ciclo e para informar o balanço em %.')
                    c2.number_input('DP do balanço (s)',min_value=0.,value=0.,step=.001,format='%.3f',key='dp_balanco_'+side+suf,disabled=not enable)
                    st.number_input('Duração do ciclo (s)',min_value=0.,value=0.,step=.001,format='%.3f',key='t_ciclo_'+side+suf,disabled=not enable)
                    if enable:
                        try:
                            r=saida_do_pe(ss['t_apoio_'+side+suf],ss['dp_apoio_'+side+suf],ss['t_ciclo_'+side+suf],
                                          ss['t_balanco_'+side+suf],ss['dp_balanco_'+side+suf])
                            st.caption(f"Saída do pé: {r['media']:.1f}% ± {r['dp']:.1f} (apoio ÷ ciclo; DP do apoio ÷ ciclo)."
                                       +(f" Balanço: {r['balanco'][0]:.1f}% ± {r['balanco'][1]:.1f}." if r['balanco'] else ''))
                            if r['aviso']: st.warning(r['aviso'])
                        except ValueError as exc:
                            st.caption(str(exc)+' Sem marcação enquanto os tempos estiverem incompletos.')
                else:
                    st.number_input('Saída do pé: média (% do ciclo)',min_value=0.,max_value=100.,value=60.,key='apoio_media_'+side+suf,disabled=not enable,
                        help='Percentual do ciclo em que o pé deixa o solo, em média. Por exemplo, 60,19 significa 60,19% do ciclo.')
                    st.number_input('DP (pontos percentuais)',min_value=0.,value=2.,key='apoio_dp_'+side+suf,disabled=not enable,
                        help='Desvio-padrão da saída do pé entre os ciclos, em % do ciclo. Não é o DP dos ângulos nem o DP do controle.')
                stance[suf][side]=apoio_do_estado(side,suf)
                if stance[suf][side]:
                    mean,sd=stance[suf][side]
                    st.caption(f'No laudo: linha em {mean:g}% e faixa de {mean-sd:g}% a {mean+sd:g}% do ciclo.')
                elif not enable:
                    st.caption('Sem marcação de saída do pé nos gráficos deste lado.')


with data_tab:
    st.subheader('Prepare sua avaliação')
    st.caption('Carregue os dois conjuntos de arquivos e confira os pares antes de gerar.')
    comparar=st.checkbox('Comparar duas condições (ex.: sem órtese × com órtese)',value=False,key='comparar',
        help='Abre um segundo conjunto de arquivos. Cada condição gera suas próprias figuras e, além delas, figuras com as médias das duas condições sobrepostas.')
    records={}
    if comparar:
        st.caption('Cada condição tem seus arquivos, sua marcação de apoio e sua edição de ciclos. Na comparação, a condição 1 aparece em azul/vermelho e a condição 2 em verde/laranja.')
        for suf,padrao in (('','Condição 1'),('_b','Condição 2')):
            with st.container(border=True):
                st.text_input('Nome da condição '+('1' if suf=='' else '2'),padrao,key='nome_c1' if suf=='' else 'nome_c2',
                    help='Aparece nos títulos e na legenda das figuras. Exemplos: Sem órtese, Com órtese, Pré, Pós.')
                records[suf]=selecionar_pares(suf)
    else:
        records['']=selecionar_pares('')
    title=st.text_input('Título da avaliação','Avaliação',key='titulo')
    st.subheader('Saída do pé')
    st.caption('Opcional. Mostra quando o pé deixa o solo e começa o balanço: uma linha vertical na média e uma faixa de ± 1 desvio-padrão (DP), separadamente para cada lado.')
    st.caption('Com "Tempos (s)", digite apoio, balanço e ciclo do relatório temporal: a média é apoio ÷ ciclo e o DP é o DP do apoio ÷ ciclo, em % do ciclo. Com "% do ciclo", digite os valores já calculados.')
    if comparar:
        for suf in CONDICOES:
            st.markdown('**'+nome_condicao(suf)+'**')
            campos_apoio(suf)
    else:
        campos_apoio('')
    st.subheader('Referência para comparação')
    controls=st.checkbox('Mostrar curvas do grupo controle ao fundo',value=True,key='controls',
        help='Adiciona a média e a faixa de ± 1 DP da referência. As curvas da avaliação continuam sendo mostradas por cima.')
    st.caption('A linha cinza representa a média do controle; a faixa cinza mostra a variação de ± 1 DP. Desmarque para mostrar apenas a avaliação.')
    st.selectbox('Grupo controle',list(groups),key='grupo_controle',disabled=not controls,
        help='Escolha uma referência cadastrada em config.json. A demonstração sintética não tem significado normativo.')
    if controls:
        if group_name=='Adulto (Millene)':
            st.caption('Adulto: 4 tentativas da Millene, com 6 ciclos direitos e 6 esquerdos. É uma referência de uma participante.')
        else:
            registros=group['controles']
            st.caption(f"{group_name}: {len(registros)} tentativas, com {sum(r['ciclos_d'] for r in registros)} ciclos direitos e {sum(r['ciclos_e'] for r in registros)} esquerdos.")
        if group.get('origem'):
            st.caption(group['origem'])
    if control_error: st.warning(control_error)
    both=st.checkbox('Pelve sagital: usar os dois lados no DP do controle',value=True,key='both',disabled=not controls,
        help='Marcado: DP calculado com ciclos direitos e esquerdos. Desmarcado: DP só dos ciclos esquerdos, para reproduzir a rotina antiga. A média permanece bilateral.')
    st.caption('Esta opção altera somente a largura da faixa cinza da pelve sagital. Marcada, usa os ciclos dos dois lados; desmarcada, usa apenas os esquerdos. Não altera as curvas do paciente.')
    st.subheader('Curvas da avaliação')
    individual=st.checkbox('Mostrar cada ciclo individualmente',value=True,key='individual',
        help='Marcado: uma curva para cada ciclo mantido. Desmarcado: uma única curva média por lado, considerando os ciclos mantidos.')
    st.caption('Marcado: todas as curvas dos arquivos selecionados, azul à direita e vermelho à esquerda. Desmarcado: apenas a média dos ciclos mantidos de cada lado. Você pode excluir ciclos depois na aba Editar ciclos.')
    signature=hashlib.sha256(str(comparar).encode())
    for suf,recs in records.items():
        signature.update(suf.encode())
        for q,p,nd,ne in recs:
            signature.update(q.name.encode()); signature.update(q.getvalue())
            if p is not None:
                signature.update(p.name.encode()); signature.update(p.getvalue())
            signature.update(f'{nd}/{ne}'.encode())
    signature=signature.hexdigest()
    if ss.get('input_signature') != signature:
        for suf in CONDICOES:
            ss.pop('loaded'+suf,None)
            ss.pop('aviso_incompletos'+suf,None)
            ss.pop('incompletos'+suf,None)
            ss.pop('excluded'+suf,None)
        ss.pop('previews',None)
        ss.pop('resultado',None)
        ss['input_signature']=signature
    if st.button('Gerar figuras',type='primary'):
        for suf in CONDICOES:
            ss.pop('loaded'+suf,None)
        ss.pop('previews',None)
        if control_error or axes_errors:
            st.error(control_error or '\n'.join(axes_errors))
        elif any(not recs or any(p is None for q,p,nd,ne in recs) for recs in records.values()):
            st.error('Selecione os arquivos QJT e PP e confirme todos os pares'+(' das duas condições.' if comparar else '.'))
        else:
            novos={}
            for suf,recs in records.items():
                try:
                    novos[suf]=carregar_condicao([(q.name,q.getvalue(),p.name,p.getvalue(),nd,ne) for q,p,nd,ne in recs])
                except Exception as exc:
                    st.error((nome_condicao(suf)+': ' if comparar else '')+str(exc))
                    novos=None
                    break
            if novos:
                for suf,(curves,provenance) in novos.items():
                    ss['loaded'+suf]={'curves':curves,'provenance':provenance}
                    incompletos=ciclos_incompletos(curves,identificar_ciclos(provenance))
                    ss['excluded'+suf]=[]
                    ss['incompletos'+suf]=incompletos
                    ss['aviso_incompletos'+suf]=incompletos
                    _nova_versao(suf)
                ss.pop('resultado',None)
                ss['auto_generate']=True
                ss['ir_para_figuras']=True
                st.rerun()

duas_condicoes=comparar and 'loaded_b' in ss
with axes_tab:
    st.subheader('Ajustes dos gráficos')
    st.caption('Defina a escala e as marcações. Os mesmos limites são usados nos dois lados e nas duas condições.')
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
    if 'loaded' not in ss:
        st.info('Selecione os pares na aba Arquivos e opções e clique em Gerar figuras.')
    else:
        suf=''
        if duas_condicoes:
            suf=st.radio('Condição para revisar',list(CONDICOES),format_func=nome_condicao,horizontal=True,key='revisar_condicao')
        cond=conds[suf]
        curves,ids,labels=cond['curves'],cond['editaveis'],cond['labels']
        lookup={r['id']:r for rows in ids.values() for r in rows}
        st.caption('Passe o mouse para identificar a curva. Use a ferramenta de seleção de pontos para selecionar um ciclo e clique em Excluir ciclo selecionado. A exclusão afeta todos os segmentos daquele ciclo e pode ser desfeita.')
        if cond['incompletos']:
            st.caption('Ciclos incompletos descartados (não aparecem aqui): '+', '.join(labels.get(k,k) for k in cond['incompletos'])+'.')
        chave_lista=f"lista_exclusoes{suf}_{ss.get('versao_exclusoes'+suf,0)}"
        excluded=st.multiselect('Ciclos excluídos — retire um item para restaurá-lo',list(lookup),default=cond['excluded'],
                                format_func=lambda key:labels[key],key=chave_lista,
                                on_change=sincronizar_exclusoes,args=(suf,chave_lista))
        st.button('Restaurar todos os ciclos',on_click=restaurar_todos,args=(suf,),key='restaurar'+suf)
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
        chart.update_layout(height=470,title=plots[variable]['title']+(' — '+nome_condicao(suf) if duas_condicoes else ''),dragmode='select',
                            xaxis_title='Ciclo (%)',yaxis_title='Graus (°)',hovermode='closest')
        chart.update_xaxes(range=[0,100]); chart.update_yaxes(range=plots[variable]['ylim'],tickmode='array' if plots[variable].get('yticks') else 'auto',tickvals=plots[variable].get('yticks'))
        event=st.plotly_chart(chart,width='stretch',on_select='rerun',
            selection_mode=('points','box','lasso'),key='revision_chart'+suf+'_'+side+'_'+variable+'_'+signature)
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
                key='target'+suf+'_'+side+'_'+hashlib.sha256(repr((selected,excluded)).encode()).hexdigest()[:12])
            st.button('Excluir ciclo selecionado',on_click=excluir_selecionado,args=(selected_cycle,suf),key='excluir'+suf)
        m1,m2=st.columns(2)
        m1.metric('Ciclos direitos mantidos',sum(r['id'] not in excluded for r in ids['D']))
        m2.metric('Ciclos esquerdos mantidos',sum(r['id'] not in excluded for r in ids['E']))
        st.write('**Mantidos:** '+', '.join(f"{sum(r['id'] not in excluded for r in ids[s])} ciclos {'direitos' if s=='D' else 'esquerdos'}" for s in ('D','E')))


def salvar(archive, previews, fig, arquivo, grupo, rotulo):
    for ext in ('png','svg'):
        data=io.BytesIO(); fig.savefig(data,format=ext,dpi=300)
        archive.writestr(f'{arquivo}.{ext}',data.getvalue())
        if ext=='png': previews.append((grupo,rotulo,data.getvalue()))
    plt.close(fig)


with figure_tab:
    st.subheader('Figuras do laudo')
    ativas=CONDICOES if duas_condicoes else ('',)
    for suf in ativas:
        if ss.get('aviso_incompletos'+suf) and 'loaded'+suf in ss:
            st.warning((nome_condicao(suf)+' — ' if duas_condicoes else '')
                       +'Ciclos com pontos ausentes na exportação foram descartados: '
                       +', '.join(conds[suf]['labels'].get(k,k) for k in ss['aviso_incompletos'+suf])
                       +'. Eles não entram nas figuras nem aparecem em Editar ciclos.')
    if 'loaded' not in ss:
        st.info('Selecione os arquivos e clique em Gerar figuras na primeira aba.')
    else:
        nomes=(nome_condicao(''),nome_condicao('_b'))
        # Exportação é invalidada quando opções, eixos ou exclusões mudam.
        output_signature=hashlib.sha256(json.dumps([signature,title,plots,stance,controls,group_name,fingerprint if ref is not None else None,both,individual,
            duas_condicoes,nomes,[conds[s]['fora'] for s in CONDICOES]],sort_keys=True).encode()).hexdigest()
        pending=ss.get('output_signature') != output_signature
        if pending and ss.get('previews'):
            st.info('Há alterações pendentes. Clique em Gerar figuras novamente para aplicá-las.')
        regenerate=st.button('Gerar figuras novamente',type='primary')
        auto=ss.pop('auto_generate',False)
        if (regenerate or auto) and (control_error or axes_errors):
            st.error(control_error or '\n'.join(axes_errors))
        elif regenerate or auto:
            try:
                kept={suf:remover_ciclos(conds[suf]['curves'],conds[suf]['ids'],conds[suf]['fora']) for suf in ativas}
                bundle=io.BytesIO()
                previews=[]
                with warnings.catch_warnings(record=True) as registro:
                    warnings.simplefilter('always')
                    with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as archive:
                        for n,suf in enumerate(ativas,1):
                            prefixo=f'condicao{n}_' if duas_condicoes else ''
                            titulo=f'{title} — {nomes[n-1]}' if duas_condicoes else title
                            grupo=nomes[n-1] if duas_condicoes else 'Avaliação'
                            for s in ('D','E'):
                                salvar(archive,previews,make_figure(kept[suf],s,plots,ref,stance[suf][s],titulo,individual),
                                       f'{prefixo}avaliacao_{s}',grupo,'Direito' if s=='D' else 'Esquerdo')
                            salvar(archive,previews,make_comparison(kept[suf],plots,ref,titulo),
                                   f'{prefixo}comparacao_medias',grupo,'Comparação das médias')
                        if duas_condicoes:
                            grupo='Comparação entre condições'
                            salvar(archive,previews,make_comparison(kept[''],plots,ref,title,kept['_b'],nomes),
                                   'comparacao_condicoes',grupo,'Dois lados')
                            for s in ('D','E'):
                                salvar(archive,previews,make_comparison(kept[''],plots,ref,title,kept['_b'],nomes,lados=(s,)),
                                       f'comparacao_condicoes_{s}',grupo,'Direito' if s=='D' else 'Esquerdo')
                        linhas_ind,frases_ind,gdi_resumo=[],[],[]
                        nomes_ind=list(nomes[:len(ativas)]) if duas_condicoes else ['Avaliação']
                        if gdi_base is not None:
                            res_gdi=[gdi.calcular(kept[suf],gdi_base) for suf in ativas]
                            salvar(archive,previews,gdi.figura(res_gdi,nomes_ind,title),'gdi','Índices (GDI, GPS e MAP)','GDI')
                            linhas_ind+=gdi.tabela(res_gdi,nomes_ind)
                            if duas_condicoes: frases_ind+=gdi.resumo_comparacao(res_gdi,nomes_ind)
                            gdi_resumo=[(n,r) for n,r in zip(nomes_ind,res_gdi)]
                        if gps_ref is not None:
                            resultados=[indices.calcular(kept[suf],gps_ref['medias']) for suf in ativas]
                            nomes_ind=list(nomes[:len(ativas)]) if duas_condicoes else ['Avaliação']
                            salvar(archive,previews,indices.figura_map(resultados,nomes_ind,gps_ref,title),
                                   'map_gps','Índices (GDI, GPS e MAP)','MAP')
                            linhas_ind=indices.tabela(resultados,nomes_ind,gps_ref)+linhas_ind
                            if duas_condicoes: frases_ind=indices.resumo_comparacao(resultados,nomes_ind)+frases_ind
                        if linhas_ind:
                            archive.writestr('indices_gps_gdi.csv',indices.csv_texto(linhas_ind))
                            ss['indices']={'linhas':linhas_ind,'frases':frases_ind,'gdi':[(n,{s:(float(r[s].mean()),float(r[s].std(ddof=1)) if len(r[s])>1 else 0.) for s in 'DE'}) for n,r in gdi_resumo],
                                           'geral':[(n,r['geral']) for n,r in zip(nomes_ind,resultados)] if gps_ref is not None else []}
                        else:
                            ss.pop('indices',None)
                        archive.writestr('grupo_controle.json',json.dumps({'grupo':group_name if controls else None,'dp_pelve_sagital':'ambos' if both else 'esquerdo'},ensure_ascii=False,indent=2))
                        for n,suf in enumerate(ativas,1):
                            prefixo=f'condicao{n}_' if duas_condicoes else ''
                            c=conds[suf]
                            if duas_condicoes:
                                archive.writestr(f'{prefixo}nome.txt',nomes[n-1])
                            archive.writestr(f'{prefixo}tentativas.json',json.dumps(c['provenance'],ensure_ascii=False,indent=2))
                            archive.writestr(f'{prefixo}revisao_ciclos.json',json.dumps({'ciclos':c['ids'],'excluidos':c['excluded'],'incompletos_descartados':c['incompletos'],'mantidos':[key for key in c['lookup'] if key not in c['fora']]},ensure_ascii=False,indent=2))
                            arrays=io.BytesIO(); np.savez(arrays,**kept[suf])
                            archive.writestr(f'{prefixo}avaliacao_ciclos.npz',arrays.getvalue())
                        archive.writestr('plots.json',json.dumps(plots,ensure_ascii=False,indent=2))
                ss['avisos_eixos']=sorted({str(w.message) for w in registro})
                ss['resultado']=bundle.getvalue()
                ss['previews']=previews
                ss['output_signature']=output_signature
                pending=False
            except Exception as exc:
                st.error(str(exc))
        for aviso in ss.get('avisos_eixos',[]):
            st.warning(aviso+' Aumente os limites em Ajustar eixos Y para não cortar as curvas.')
        previews=ss.get('previews',[])
        for grupo in dict.fromkeys(g for g,_,_ in previews):
            itens=[(rotulo,png) for g,rotulo,png in previews if g==grupo]
            if len(dict.fromkeys(g for g,_,_ in previews))>1:
                st.markdown('### '+grupo)
            if grupo=='Comparação entre condições':
                st.caption(f'{nomes[0]}: azul (direito) e vermelho (esquerdo) · {nomes[1]}: verde (direito) e laranja (esquerdo) · Cinza: controle ± 1 DP.')
            pares=[i for i in itens if i[0] in ('Direito','Esquerdo')]
            outros=[i for i in itens if i[0] not in ('Direito','Esquerdo')]

            def mostrar_outros():
                for rotulo,png in outros:
                    st.markdown('#### '+rotulo)
                    if rotulo=='GDI':
                        st.caption('GDI de cada lado (média ± DP dos ciclos). 100 = média dos controles da planilha GDI-GPS; cada 10 pontos abaixo de 100 = 1 DP de desvio.')
                    if rotulo=='MAP':
                        st.caption('Barras: GVS médio de cada variável (distância RMS até a média do controle) e GPS de cada lado. Cinza: valor típico dos próprios controles.')
                    if rotulo=='Comparação das médias':
                        st.caption('Azul: média direita · Vermelho: média esquerda · Cinza: média do controle ± 1 DP. Considera somente os ciclos mantidos.')
                    st.image(png)
            if grupo=='Comparação entre condições':
                mostrar_outros()
            colunas=st.columns(2)
            for i,(rotulo,png) in enumerate(pares):
                with colunas[i%2]:
                    st.markdown('#### '+rotulo)
                    st.image(png)
            if grupo!='Comparação entre condições':
                mostrar_outros()
        if ss.get('indices') and not pending:
            st.markdown('### Índices: GDI, GPS e GVS')
            for nome,r in ss['indices'].get('gdi',[]):
                f=lambda x:f'{x:.1f}'.replace('.',',')
                st.write(f"**GDI{' — '+nome if duas_condicoes else ''}: direito {f(r['D'][0])} ± {f(r['D'][1])} · esquerdo {f(r['E'][0])} ± {f(r['E'][1])}**")
            for nome,geral in ss['indices']['geral']:
                st.write(f"**GPS geral{' — '+nome if duas_condicoes else ''}: {geral:.1f}°**".replace('.',','))
            if gps_ref and gps_ref['gps']:
                st.caption(f"Referência do grupo {group_name}: GPS {gps_ref['gps'][0]:.1f}° ± {gps_ref['gps'][1]:.1f}° "
                           f"({gps_ref['n']} ciclos, cada um comparado à média das demais tentativas).".replace('.',',',2))
            for frase in ss['indices']['frases']:
                st.write(frase)
            st.dataframe(ss['indices']['linhas'],hide_index=True)
        if ref is None and 'loaded' in ss:
            st.caption('GPS e MAP exigem o grupo controle: ative "Mostrar curvas do grupo controle". O GDI usa o controle fixo da planilha GDI-GPS.')
        if gdi_erro:
            st.warning('GDI: '+gdi_erro)
        elif gdi_base is None and 'loaded' in ss:
            st.caption('GDI indisponível: faltam gillette.txt e dados_con_GDI_orig.txt na pasta dados_gdi.')
        if 'resultado' in ss and not pending:
            st.download_button('Baixar figuras PNG + SVG',ss['resultado'],'figuras_marcha.zip','application/zip')

# Assinatura discreta do desenvolvedor no fim da página (só na interface; não entra nas figuras exportadas).
_cimo=ROOT/'assets/cimonetti_cor.svg'
if _cimo.exists():
    import base64
    st.markdown('<div style="margin:4rem 0 .5rem;padding-top:1rem;border-top:1px solid #e3e7ef;opacity:.5;display:flex;'
                'justify-content:center;align-items:center;gap:.45rem;font-size:.7rem;letter-spacing:.06em;color:#68748a">'
                'desenvolvido por<img alt="CIMONETTI" style="height:18px;width:auto" src="data:image/svg+xml;base64,'
                f'{base64.b64encode(_cimo.read_bytes()).decode()}"></div>',unsafe_allow_html=True)
