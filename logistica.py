import streamlit as st
import pandas as pd

# Conecte ao link da aba de "Vendas" da sua planilha
SHEET_URL = "SEU_LINK_AQUI"

try:
    df = pd.read_csv(SHEET_URL)
    
    # Filtro de Segurança: Só mostra pedidos que tenham Endereço e Bairro preenchidos
    # Isso evita o "pedido ruim" no painel do motoboy
    entregas_validas = df.dropna(subset=['endereco', 'bairro'])
    
    st.title("🚚 Entregas em Formosa")
    
    for i, row in entregas_validas.iterrows():
        with st.expander(f"📍 Pedido para {row['bairro']} - Ver Detalhes"):
            st.write(f"**Cliente:** {row['cliente']}")
            st.write(f"**Endereço:** {row['endereco']}")
            st.write(f"**Produto:** {row['nome_produto']}")
            
            # Botão de Rota Direta
            maps_url = f"https://www.google.com/maps/search/?api=1&query={row['endereco']}+Formosa+GO"
            st.link_button("Abrir no GPS", maps_url)
            
except Exception as e:
    st.error("Aguardando novas vendas entrarem na planilha...")
