import streamlit as st
import pandas as pd

# 1. Configurações de página
st.set_page_config(page_title="Formosa Cases", layout="wide", page_icon="📱")

# Inicializar o item selecionado na memória do navegador
if 'item_selecionado' not in st.session_state:
    st.session_state.item_selecionado = None

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
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .product-card {
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid #eee;
        text-align: center;
    }
    .price-tag { color: #ee4d2d; font-size: 1.3rem; font-weight: bold; }
    .stButton>button { background-color: #ee4d2d; color: white; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. Conexão com a Planilha
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQhJW43nfokHKiBwhu64dORzbzD8m8Haxy8tEbGRsysr8JG1Wq8s7qgRfHT5ZLLUBkAuHzUJFKODEDZ/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

st.markdown('<div class="shopee-header"><h1>📱 FORMOSA CASES</h1><p>Entrega Ultra Rápida em Formosa-GO</p></div>', unsafe_allow_html=True)

# 3. Sidebar - Finalização do Pedido
with st.sidebar:
    st.header("🛒 Checkout")
    if st.session_state.item_selecionado:
        st.info(f"📌 Selecionado: **{st.session_state.item_selecionado['nome']}**")
        nome = st.text_input("Nome do Cliente")
        endereco = st.text_input("Endereço e Número")
        bairro = st.selectbox("Bairro em Formosa", ["Centro", "Formosinha", "Planaltina", "Parque da Colina", "Jardim das Américas", "Outro"])
        
        if st.button("✅ FINALIZAR NO WHATSAPP"):
            if nome and endereco:
                seu_numero = "5561991937857"
                texto_pedido = f"*NOVO PEDIDO - FORMOSA CASES*\n\n" \
                               f"📦 *Produto:* {st.session_state.item_selecionado['nome']}\n" \
                               f"💰 *Preço:* R$ {st.session_state.item_selecionado['preco']:.2f}\n" \
                               f"👤 *Cliente:* {nome}\n" \
                               f"📍 *Endereço:* {endereco}\n" \
                               f"🏘️ *Bairro:* {bairro}"
                
                link_zap = f"https://wa.me/{seu_numero}?text={texto_pedido.replace(' ', '%20').replace('\n', '%0A')}"
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={link_zap}">', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Preencha Nome e Endereço!")
    else:
        st.write("Escolha um produto na loja para finalizar.")

# 4. Grid de Produtos
try:
    df = load_data()
    cols = st.columns(2)
    
    for index, row in df.iterrows():
        with cols[index % 2]:
            st.markdown(f"""
                <div class="product-card">
                    <img src="{row['img']}" style="width:100%; border-radius:5px; height:140px; object-fit:cover;">
                    <p style="font-size:14px; margin-top:10px; height:35px; overflow:hidden;"><b>{row['nome']}</b></p>
                    <p class="price-tag">R$ {row['preco']:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"SELECIONAR", key=f"btn_{index}"):
                st.session_state.item_selecionado = {"nome": row['nome'], "preco": row['preco']}
                st.rerun()

except Exception as e:
    st.error("Erro ao carregar produtos. Verifique sua planilha.")

st.markdown("<br><br><p style='text-align:center; color:gray; font-size:10px;'>Formosa Cases Express © 2026</p>", unsafe_allow_html=True)
