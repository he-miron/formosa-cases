import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configurações Iniciais
st.set_page_config(page_title="Formosa Cases Express", layout="wide", page_icon="📱")

# Inicializar memória de seleção
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = None

# 2. Estilo Visual (CSS Shopee Dark/Orange)
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; }
    .header { background-color: #ee4d2d; padding: 20px; color: white; text-align: center; border-radius: 0 0 20px 20px; margin-bottom: 20px; }
    .card { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 20px; }
    .price { color: #ee4d2d; font-size: 1.4rem; font-weight: bold; }
    .stButton>button { background-color: #ee4d2d; color: white; width: 100%; border-radius: 8px; height: 45px; }
    .log-card { background: #2d2d2d; color: #fff; padding: 15px; border-radius: 10px; border-left: 5px solid #ee4d2d; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Conexão com Dados
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQhJW43nfokHKiBwhu64dORzbzD8m8Haxy8tEbGRsysr8JG1Wq8s7qgRfHT5ZLLUBkAuHzUJFKODEDZ/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

# --- LÓGICA DE NAVEGAÇÃO ---
query_params = st.query_params
modo_logistica = query_params.get("p") == "moto"

if modo_logistica:
    # ---------------- QUEBRA DE PÁGINA: LOGÍSTICA ----------------
    st.markdown('<div class="header"><h1>🚚 PAINEL ENTREGADOR</h1><p>Logística Formosa Cases</p></div>', unsafe_allow_html=True)
    
    try:
        df = load_data()
        st.subheader("Pedidos Pendentes para Entrega")
        
        for i in range(3): 
            st.markdown(f"""
                <div class="log-card">
                    <p><b>📦 PEDIDO #102{i}</b></p>
                    <p>📍 Rua 14, Centro - Próximo à Praça</p>
                    <p>💰 Receber: R$ 59,90 (PIX)</p>
                </div>
            """, unsafe_allow_html=True)
            col_gps, col_ok = st.columns(2)
            with col_gps:
                st.link_button("🗺️ Abrir GPS", "https://www.google.com/maps/search/Formosa+GO")
            with col_ok:
                if st.button("✅ Entregue", key=f"ent_{i}"):
                    st.toast("Entrega confirmada!")
    except:
        st.error("Erro ao carregar mapa de entregas.")

else:
    # ---------------- QUEBRA DE PÁGINA: LOJA (CLIENTE) ----------------
    st.markdown('<div class="header"><h1>📱 FORMOSA CASES</h1><p>Entrega em até 24h em Formosa</p></div>', unsafe_allow_html=True)

# Sidebar de Checkout (Otimizado para Celular)
    with st.sidebar:
        st.header("🛒 Seu Pedido")
        if st.session_state.carrinho:
            st.write(f"**Item:** {st.session_state.carrinho['nome']}")
            st.write(f"**Total:** R$ {st.session_state.carrinho['preco']:.2f}")
            
            nome = st.text_input("Nome Completo")
            endereco = st.text_input("Rua e Número")
            bairro = st.selectbox("Bairro", ["Centro", "Formosinha", "Setor Sul", "Parque Lago"])
            
            if nome and endereco:
                zap_num = "5561991937857"
                msg = f"*NOVO PEDIDO - FORMOSA CASES*\n\n" \
                      f"*Produto:* {st.session_state.carrinho['nome']}\n" \
                      f"*Cliente:* {nome}\n" \
                      f"*Endereço:* {endereco}\n" \
                      f"*Bairro:* {bairro}\n" \
                      f"*Total:* R$ {st.session_state.carrinho['preco']:.2f}"
                
                # Mudamos de wa.me para api.whatsapp.com que é mais compatível com navegadores mobile
                link_whatsapp = f"https://api.whatsapp.com/send?phone={zap_num}&text={msg.replace(' ', '%20').replace('\n', '%0A')}"
                
                # Usando o link_button com um ícone para melhorar o clique no touch
                st.link_button("📲 FINALIZAR NO WHATSAPP", link_whatsapp, use_container_width=True)
                
                st.info("👆 Se o WhatsApp não abrir automaticamente, ligue 61 9 9193-7857.")
            else:
                st.warning("Preencha Nome e Endereço.")
        else:
            st.write("Toque em um produto para comprar.")

    # Vitrine de Produtos (INDENTAÇÃO CORRIGIDA)
    try:
        df = load_data()
        cols = st.columns(2)
        for idx, row in df.iterrows():
            with cols[idx % 2]:
                st.markdown(f"""
                    <div class="card">
                        <img src="{row['img']}" style="width:100%; border-radius:10px; height:150px; object-fit:cover;">
                        <p style="margin:10px 0 5px 0;"><b>{row['nome']}</b></p>
                        <p class="price">R$ {row['preco']:.2f}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Eu Quero", key=f"venda_{idx}"):
                    st.session_state.carrinho = {"nome": row['nome'], "preco": row['preco']}
                    st.rerun()
    except Exception as e:
        st.error(f"Erro ao carregar vitrine: {e}")

st.markdown("---")
st.caption("Formosa Cases Express - Sistema Integrado 2026")
