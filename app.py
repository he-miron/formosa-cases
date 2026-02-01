import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Busca Aluno - FSA", page_icon="🔍")

st.markdown("""
    <style>
    .resultado {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #1e3a8a;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        color: #1e3a8a;
        margin-top: 20px;
    }
    .label { font-weight: bold; color: #555; font-size: 0.9em; }
    .valor { font-size: 1.4em; font-weight: bold; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS ---
# Usando o link CSV para máxima velocidade de busca
SHEET_ID = "1yurzw28SK7rF6LPpbKYShICY0QgexeFbv0ShVbwUkjc"
GID = "672132072"
URL = f"https://docs.google.com/spreadsheets/d/e/2PACX-1vQV4Cj-QnWSfJLD5I5TwNfEW6F0Ti_YFPve0yyzqOAW9clUyLlRvohv9ZKm7kGD7x6xTVo0qKlYohKl/pub?output=csv"

@st.cache_data(ttl=60) # Atualiza a cada 1 minuto
def carregar_dados():
    df = pd.read_csv(URL)
    # Padroniza nomes das colunas (tira espaços e deixa minúsculo)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

# --- INTERFACE ---
st.title("🔍 Conferência de Alunos")
st.write("Digite o nome abaixo para consultar os dados imediatamente.")

try:
    df = carregar_dados()
    
    # BARRA DE PESQUISA (A LUPA)
    busca = st.text_input("Pesquisar Nome do Aluno", placeholder="Ex: João Silva...").strip().lower()

    if busca:
        # Filtra o DataFrame onde o nome contém o texto digitado
        resultado = df[df['nome'].astype(str).str.lower().str.contains(busca)]

        if not resultado.empty:
            for _, aluno in resultado.iterrows():
                # Exibição em "Card" elegante
                st.markdown(f"""
                    <div class="resultado">
                        <div class="label">NOME COMPLETO:</div>
                        <div class="valor">{aluno['nome'].upper()}</div>
                        
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <div class="label">SÉRIE / TURMA:</div>
                                <div class="valor">{aluno.get('turma', aluno.get('serie', 'Não inf.'))}</div>
                            </div>
                            <div>
                                <div class="label">SITUAÇÃO:</div>
                                <div class="valor" style="color: green;">ATIVO</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Nenhum aluno encontrado com esse nome.")
    else:
        st.info("Aguardando digitação para busca...")

except Exception as e:
    st.error("Erro ao conectar com a planilha. Verifique se ela está publicada na web.")
    st.info("Para publicar: Arquivo > Compartilhar > Publicar na Web (formato CSV).")
