import streamlit as st
import pandas as pd

# 1. Configurações Iniciais
st.set_page_config(page_title="Formosa Cases Admin", layout="wide")

# 2. Conexão com Google Sheets (Troque o ID abaixo pelo seu)
SHEET_ID = "COLOQUE_AQUI_O_ID_DA_SUA_PLANILHA"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=60) # Atualiza os dados a cada 60 segundos
def carregar_dados():
    return pd.read_csv(SHEET_URL)

try:
    df = carregar_dados()
except:
    st.error("Erro ao conectar com a planilha. Verifique o ID e a permissão de compartilhamento.")
    st.stop()

# 3. Estilização (Mesmo estilo Shopee anterior)
st.markdown("""
    <style>
    .product-card { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 20px; text-align: center; }
    .price { color: #ee4d2d; font-size: 22px; font-weight: bold; }
    .stButton>button { background-color: #ee4d2d; color: white; width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📱 Formosa Cases Online")
st.write("---")

# 4. Exibição dos Produtos vindos da Planilha
cols = st.columns(2)

for index, row in df.iterrows():
    with cols[index % 2]:
        st.markdown(f"""
            <div class="product-card">
                <img src="{row['img']}" style="width:100%; max-height:150px; object-fit: contain;">
                <h4>{row['nome']}</h4>
                <p style="font-size: 12px; color: gray;">{row['desc']}</p>
                <p class="price">R$ {row['preco']:.2f}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Comprar {row['nome']}", key=f"btn_{index}"):
            # Lógica de checkout simplificada para WhatsApp
            zap_link = f"https://wa.me/5561999999999?text=Quero%20o%20produto:%20{row['nome']}"
            st.success("Produto selecionado!")
            st.markdown(f"[CLIQUE AQUI PARA PEDIR NO WHATSAPP]({zap_link})")

st.sidebar.info("Dica: Para atualizar preços e fotos, basta editar sua Planilha do Google e atualizar esta página.")
