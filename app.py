import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DO LINK DA PLANILHA
# Use exatamente este formato abaixo:
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQhJW43nfokHKiBwhu64dORzbzD8m8Haxy8tEbGRsysr8JG1Wq8s7qgRfHT5ZLLUBkAuHzUJFKODEDZ/pub?output=csv"

@st.cache_data(ttl=60)
def carregar_dados():
    # O comando abaixo lê o link da planilha
    return pd.read_csv(SHEET_URL)

# --- RESTO DO SEU CÓDIGO ABAIXO ---
try:
    df = carregar_dados()
    st.success("Dados carregados com sucesso!")
except Exception as e:
    st.error(f"Erro ao conectar com a planilha: {e}")
    st.stop()

# Aqui continua a parte visual (o grid de produtos que te passei antes)

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
