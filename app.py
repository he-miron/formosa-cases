import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fpdf import FPDF
import base64

# --- CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="SGE PRO - Gestão Escolar", layout="wide", page_icon="🎓")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stButton>button { border-radius: 5px; height: 3em; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); background-color: #1e40af; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM GOOGLE SHEETS ---
def conectar_google():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    try:
        if "gcp_service_account" in st.secrets:
            creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
        else:
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        return client.open_by_key("1yurzw28SK7rF6LPpbKYShICY0QgexeFbv0ShVbwUkjc")
    except Exception as e:
        st.error(f"Erro de Conexão: {e}")
        return None

# --- GERADOR DE BOLETIM PDF ---
def gerar_pdf(aluno_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "BOLETIM ESCOLAR OFICIAL", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Aluno: {aluno_data['nome']}", ln=True)
    pdf.cell(200, 10, f"Turma: {aluno_data['turma']}", ln=True)
    pdf.ln(5)
    pdf.cell(100, 10, f"Frequência: {aluno_data['frequencia']}%", border=1)
    pdf.cell(100, 10, f"Média Geral: {aluno_data['notas']}", border=1, ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Observações: {aluno_data['observacoes']}")
    return pdf.output(dest='S').encode('latin-1')

# --- AUTENTICAÇÃO ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 SGE PRO - Login")
    u = st.text_input("Usuário").strip().lower()
    p = st.text_input("Senha", type="password")
    if st.button("Acessar Painel"):
        db = conectar_google()
        if db:
            ws = db.worksheet("servidores")
            servidores = pd.DataFrame(ws.get_all_records())
            valid = servidores[(servidores['usuario'].astype(str) == u) & (servidores['senha'].astype(str) == p)]
            if not valid.empty:
                st.session_state.auth = True
                st.session_state.user = valid.iloc[0].to_dict()
                st.rerun()
            else: st.error("Acesso Negado.")
else:
    db = conectar_google()
    st.sidebar.title("🎓 Gestão Escolar")
    st.sidebar.write(f"Olá, **{st.session_state.user['nome']}**")
    
    aba = st.sidebar.radio("Menu", ["📊 Dashboard Geral", "📝 Lançamentos", "📋 Chamada", "📄 Boletins"])

    # --- ABA DASHBOARD ---
    if aba == "📊 Dashboard Geral":
        st.header("Visão Geral da Escola")
        df_alunos = pd.DataFrame(db.worksheet("alunos").get_all_records())
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total de Alunos", len(df_alunos))
        c2.metric("Média da Escola", round(pd.to_numeric(df_alunos['notas']).mean(), 1))
        c3.metric("Frequência Média", f"{round(pd.to_numeric(df_alunos['frequencia']).mean())}%")
        
        st.subheader("Lista de Alunos")
        st.dataframe(df_alunos, use_container_width=True)

    # --- ABA LANÇAMENTOS ---
    elif aba == "📝 Lançamentos":
        st.header("Lançamento de Notas e Observações")
        ws_alunos = db.worksheet("alunos")
        df_alunos = pd.DataFrame(ws_alunos.get_all_records())
        
        aluno_sel = st.selectbox("Selecione o Aluno", df_alunos['nome'].tolist())
        dados = df_alunos[df_alunos['nome'] == aluno_sel].iloc[0]
        linha = df_alunos[df_alunos['nome'] == aluno_sel].index[0] + 2
        
        with st.form("edit_form"):
            nota = st.number_input("Nota", value=float(dados['notas']), min_value=0.0, max_value=10.0)
            obs = st.text_area("Observações Pedagógicas", value=str(dados['observacoes']))
            if st.form_submit_button("Salvar no Sistema"):
                ws_alunos.update_cell(linha, 5, nota) # Coluna E
                ws_alunos.update_cell(linha, 6, obs)  # Coluna F
                st.success("Dados salvos com sucesso!")

    # --- ABA CHAMADA ---
    elif aba == "📋 Chamada":
        st.header("Controle de Frequência Diária")
        ws_alunos = db.worksheet("alunos")
        df_alunos = pd.DataFrame(ws_alunos.get_all_records())
        
        st.write("Marque 'Presente' para os alunos da turma selecionada:")
        turma_sel = st.selectbox("Turma", df_alunos['turma'].unique())
        alunos_turma = df_alunos[df_alunos['turma'] == turma_sel]
        
        for i, row in alunos_turma.iterrows():
            col_a, col_b = st.columns([3, 1])
            col_a.write(row['nome'])
            if col_b.button("Presença ✅", key=f"pres_{i}"):
                nova_f = min(int(row['frequencia']) + 1, 100)
                ws_alunos.update_cell(i + 2, 4, nova_f) # Coluna D
                st.toast(f"Presença de {row['nome']} registrada!")

    # --- ABA BOLETINS ---
    elif aba == "📄 Boletins":
        st.header("Emissão de Documentos")
        df_alunos = pd.DataFrame(db.worksheet("alunos").get_all_records())
        aluno_doc = st.selectbox("Gerar boletim para:", df_alunos['nome'].tolist())
        aluno_final = df_alunos[df_alunos['nome'] == aluno_doc].iloc[0]
        
        if st.button("Gerar PDF do Boletim"):
            pdf_bytes = gerar_pdf(aluno_final)
            st.download_button(label="📥 Baixar Boletim PDF", 
                             data=pdf_bytes, 
                             file_name=f"Boletim_{aluno_doc}.pdf",
                             mime="application/pdf")

    if st.sidebar.button("Sair"):
        st.session_state.auth = False
        st.rerun()
