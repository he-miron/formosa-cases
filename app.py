import streamlit as st
import pandas as pd

# 1. Configurações de página e Estilo Visual
st.set_page_config(page_title="Formosa Cases", layout="wide", page_icon="📱")

st.markdown("""
    <style>
    /* Estilo Fundo e Fontes */
    .stApp { background-color: #f5f5f5; }
    
    /* Header Estilo Shopee */
    .shopee-header {
        background-color: #ee4d2d;
        padding: 15px;
        color: white;
        text-align: center;
        font-family: 'Arial';
        border-radius: 0 0 20px 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* Card de Produto */
    .product-card {
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid #eee;
    }
    
    .price-tag {
        color: #ee4d2d;
        font-size: 1.3rem;
        font-weight: bold;
    }

    /* Botão de Compra */
    .stButton>button {
        background-color: #ee4d2d;
        color: white;
        border-radius: 5px;
        border: none;
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Conexão com sua Planilha
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQhJW43nfokHKiBwhu64dORzbzD8m8Haxy8tEbGRsysr8JG1Wq8s7qgRfHT5ZLLUBkAuHzUJFKODEDZ/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

# Cabeçalho
st.markdown('<div class="shopee-header"><h1>📱 FORMOSA CASES</h1><p>Entrega Ultra Rápida em Formosa-GO</p></div>', unsafe_allow_html=True)

try:
    df = load_data()
    
    # Grid de Produtos
    cols = st.columns(2) # 2 colunas igual na Shopee
    
    for index, row in df.iterrows():
        with cols[index % 2]:
            st.markdown(f"""
                <div class="product-card">
                    <img src="{row['img']}" style="width:100%; border-radius:5px; height:150px; object-fit:cover;">
                    <p style="font-size:14px; margin-top:10px; height:40px; overflow:hidden;"><b>{row['nome']}</b></p>
                    <p class="price-tag">R$ {row['preco']:.2f}</p>
                    <p style="font-size:10px; color:#25D366;">⚡ Entrega Hoje</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"PEDIR AGORA", key=f"btn_{index}"):
                # Link do seu WhatsApp (Coloque seu número abaixo)
                seu_numero = "5561999999999" 
                msg = f"Olá! Vi no App e quero: {row['nome']} (R$ {row['preco']:.2f})"
                link_zap = f"https://wa.me/{seu_numero}?text={msg.replace(' ', '%20')}"
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={link_zap}">', unsafe_allow_html=True)

except Exception as e:
    st.error("Adicione produtos na sua planilha para eles aparecerem aqui!")

st.markdown("<br><br><p style='text-align:center; color:gray; font-size:10px;'>Formosa Cases Express © 2026</p>", unsafe_allow_html=True)
