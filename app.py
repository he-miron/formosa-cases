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
            # Todo esse bloco abaixo deve ter o mesmo recuo (4 ou 8 espaços)
            st.markdown(f"""
                <div class="product-card">
                    <img src="{row['img']}" style="width:100%; border-radius:5px; height:150px; object-fit:cover;">
                    <p style="font-size:14px; margin-top:10px; height:40px; overflow:hidden;"><b>{row['nome']}</b></p>
                    <p class="price-tag">R$ {row['preco']:.2f}</p>
                    <p style="font-size:10px; color:#25D366;">⚡ Entrega Hoje em Formosa</p>
                </div>
            """, unsafe_allow_html=True)
            
            # ESTE BOTÃO DEVE ESTAR ALINHADO COM O st.markdown ACIMA
            if st.button(f"PEDIR AGORA", key=f"btn_{index}"):
                seu_numero = "5561999999999" 
                msg = f"Olá! Vi no App e quero: {row['nome']} (R$ {row['preco']:.2f})"
                link_zap = f"https://wa.me/{seu_numero}?text={msg.replace(' ', '%20')}"
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={link_zap}">', unsafe_allow_html=True)
st.sidebar.info("Dica: Salve nosso contato e n'ao percam ofertas no status.")
