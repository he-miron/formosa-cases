import streamlit as st
import pandas as pd

# 1. Configurações de página
st.set_page_config(page_title="Formosa Cases", layout="wide", page_icon="📱")

# 2. Estilo Visual Shopee
st.markdown("""
    <style>
    .stApp { background-color: #f5f5f5; }
    .shopee-header {
        background-color: #ee4d2d;
        padding: 15px;
        color: white;
        text-align: center;
        border-radius: 0 0 20px 20px;
        margin-bottom: 20px;
    }
    .product-card {
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .price-tag { color: #ee4d2d; font-size: 1.3rem; font-weight: bold; }
    .stButton>button { background-color: #ee4d2d; color: white; width: 100%; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 3. Conexão com a Planilha
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQhJW43nfokHKiBwhu64dORzbzD8m8Haxy8tEbGRsysr8JG1Wq8s7qgRfHT5ZLLUBkAuHzUJFKODEDZ/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

# Cabeçalho
st.markdown('<div class="shopee-header"><h1>📱 FORMOSA CASES</h1><p>O Shopping das Capinhas em Formosa</p></div>', unsafe_allow_html=True)

# 4. Bloco de Exibição de Produtos
try:
    df = load_data()
    cols = st.columns(2) 

    for index, row in df.iterrows():
        with cols[index % 2]:
            st.markdown(f"""
                <div class="product-card">
                    <img src="{row['img']}" style="width:100%; border-radius:5px; height:150px; object-fit:cover;">
                    <p style="font-size:14px; margin-top:10px; height:40px; overflow:hidden;"><b>{row['nome']}</b></p>
                    <p class="price-tag">R$ {row['preco']:.2f}</p>
                    <p style="font-size:10px; color:#25D366;">⚡ Entrega Expressa</p>
                </div>
            """, unsafe_allow_html=True)
            # Botão apenas para feedback visual (opcional)
            st.button(f"Ver detalhes", key=f"det_{index}")

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")

# 5. ÁREA DE CHECKOUT (Barra Lateral - Fora de qualquer bloco anterior)
with st.sidebar:
    st.header("🛒 Finalizar Pedido")
    nome = st.text_input("Seu Nome")
    endereco = st.text_input("Endereço (Rua e Número)")
    bairro = st.selectbox("Seu Bairro em Formosa", ["Centro", "Formosinha", "Planaltina", "Parque da Colina", "Jardim das Américas", "Outro"])
    
    if st.button("🚀 CONFIRMAR COMPRA"):
        if nome and endereco:
            # Substitua pelo SEU número real com DDD
            seu_numero = "5561991937857" 
            msg = f"*NOVO PEDIDO - FORMOSA CASES*\n\n👤 Cliente: {nome}\n📍 Endereço: {endereco}\n🏘️ Bairro: {bairro}"
            link_zap = f"https://wa.me/{seu_numero}?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
            
            st.success("Dados validados!")
            st.markdown(f'<a href="{link_zap}" target="_blank" style="background-color: #25D366; color: white; padding: 12px; text-decoration: none; border-radius: 5px; display: block; text-align: center; font-weight: bold;">ENVIAR PARA O WHATSAPP</a>', unsafe_allow_html=True)
        else:
            st.error("⚠️ Preencha nome e endereço!")
