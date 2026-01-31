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

with st.sidebar:
    st.header("🛒 Finalizar Pedido")
    nome = st.text_input("Seu Nome")
    endereco = st.text_input("Endereço (Rua e Número)")
    bairro = st.selectbox("Seu Bairro em Formosa", ["Centro", "Formosinha", "Planaltina", "Parque da Colina", "Jardim das Américas", "Outro"])
    
    if st.button("🚀 CONFIRMAR COMPRA"):
        if nome and endereco: # Só prossegue se tiver nome e endereço
            seu_numero = "5561999999999" 
            # Criamos uma mensagem organizada para o WhatsApp
            msg = f"*NOVO PEDIDO - FORMOSA CASES*\n\n" \
                  f"👤 *Cliente:* {nome}\n" \
                  f"📍 *Endereço:* {endereco}\n" \
                  f"🏘️ *Bairro:* {bairro}\n" \
                  f"--------------------------\n" \
                  f"Verifique os itens no carrinho acima."
            
            link_zap = f"https://wa.me/{seu_numero}?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
            st.success("Dados validados! Clique no botão abaixo para enviar o pedido.")
            st.markdown(f'[ENVIAR PARA O WHATSAPP]({link_zap})')
        else:
            st.error("⚠️ Por favor, preencha seu nome e endereço para entrega.")
