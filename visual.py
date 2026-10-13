"""Identidade visual do Laboratório de Biomecânica Aplicada."""
from pathlib import Path
import base64
import streamlit as st


def cabecalho(root: Path):
    st.markdown('''<style>
    .block-container {max-width:1320px;padding-top:4.5rem;padding-bottom:3rem;}
    [data-testid="stAppViewContainer"] {background:#f4f6fa;}
    h1,h2,h3 {color:#222746;letter-spacing:-.025em;}
    h1 {font-size:2rem !important;font-weight:750 !important;}
    [data-testid="stCaptionContainer"] {color:#68748a;}
    [data-testid="stTabs"] [role="tablist"] {gap:.6rem;background:#e9edf4;padding:.4rem;border-radius:14px;}
    [data-testid="stTabs"] [role="tab"] {padding:.7rem 1rem;border-radius:10px;font-weight:600;height:auto;}
    [data-testid="stTabs"] [aria-selected="true"] {background:white;color:#24284d;box-shadow:0 3px 12px #23304710;}
    [data-testid="stTabs"] [data-baseweb="tab-highlight"] {display:none;}
    [data-testid="stTabs"] [role="tabpanel"] {padding-top:1.5rem;}
    [data-testid="stFileUploader"] {background:white;padding:1rem;border:1px solid #e0e5ee;border-radius:16px;}
    [data-testid="stFileUploaderDropzone"] {border-radius:12px;background:#f8f9fc;}
    [data-testid="stVerticalBlockBorderWrapper"] {border-color:#e0e5ee;border-radius:14px;background:white;}
    [data-testid="stMetric"] {background:white;border:1px solid #e0e5ee;border-radius:14px;padding:1rem;}
    [data-testid="stMetricValue"] {color:#282c52;}
    button[kind="primary"] {background:#ed7857;border-color:#ed7857;border-radius:10px;font-weight:650;box-shadow:0 4px 12px #ee785720;}
    button[kind="secondary"] {border-radius:10px;}
    [data-testid="stSidebar"] {background:#222746;}
    [data-testid="stSidebar"] h3,[data-testid="stSidebar"] p,[data-testid="stSidebar"] label {color:#f5f6fb;}
    .lba-eyebrow {white-space:normal;overflow-wrap:anywhere;line-height:1.65;font-size:.75rem;letter-spacing:.16em;color:#68748a;font-weight:700;margin-top:.25rem;}
    .lba-subtitle {color:#68748a;font-size:.97rem;margin-top:.6rem;line-height:1.5;}
    .lba-divider {height:1px;background:#dde3ed;margin:1.2rem 0 1.4rem;}
    </style>''',unsafe_allow_html=True)
    left,right=st.columns([.65,3],vertical_alignment='center')
    with left:
        source=base64.b64encode((root/'assets/logo_lba.png').read_bytes()).decode()
        st.markdown(f'<div style="width:136px;max-width:100%;aspect-ratio:1;overflow:hidden;border-radius:14px;background:white"><img alt="Símbolo do Laboratório de Biomecânica Aplicada" src="data:image/png;base64,{source}" style="width:100%;height:auto;display:block"></div>',unsafe_allow_html=True)
    with right:
        st.markdown('''<div class="lba-header"><div class="lba-eyebrow">LABORATÓRIO DE BIOMECÂNICA APLICADA</div><h1 style="margin:0;padding:.4rem 0;line-height:1.25">Análise da marcha</h1><div class="lba-subtitle">Das tentativas ao laudo: reúna ciclos, confira as curvas e exporte suas figuras.</div></div>''',unsafe_allow_html=True)
    st.markdown('<div class="lba-divider"></div>',unsafe_allow_html=True)
