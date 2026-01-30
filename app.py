import streamlit as st

# Configuração da página
st.set_page_config(page_title="Formosa Case Express", page_icon="📱")

st.title("📱 Formosa Case Express")
st.subheader("As melhores capinhas e películas em Formosa-GO")

# Simulação de Banco de Dados
produtos = [
    {"nome": "Capinha Silicone MagSafe", "preco": 45.00, "tipo": "Capinha"},
    {"nome": "Película de Cerâmica Privativa", "preco": 30.00, "tipo": "Película"},
    {"nome": "Capinha Anti-Impacto Transparente", "preco": 35.00, "tipo": "Capinha"},
    {"nome": "Película de Vidro 3D", "preco": 20.00, "tipo": "Película"}
]

# Carrinho de compras
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []

# Interface
tab1, tab2 = st.tabs(["🛒 Loja", "📦 Meu Carrinho"])

with tab1:
    st.write("### Escolha seus itens:")
    for produto in produtos:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**{produto['nome']}** - R$ {produto['preco']:.2f}")
        with col2:
            if st.button(f"Adicionar", key=produto['nome']):
                st.session_state.carrinho.append(produto)
                st.toast(f"{produto['nome']} adicionado!")

with tab2:
    if len(st.session_state.carrinho) == 0:
        st.write("Seu carrinho está vazio.")
    else:
        total = sum(item['preco'] for item in st.session_state.carrinho)
        for item in st.session_state.carrinho:
            st.write(f"- {item['nome']}: R$ {item['preco']:.2f}")
        
        st.write(f"### Total: R$ {total:.2f}")
        
        # Finalização via WhatsApp (O segredo para rodar rápido)
        endereco = st.text_input("Endereço de Entrega em Formosa:")
        if st.button("Finalizar Pedido via WhatsApp"):
            msg = f"Olá! Gostaria de pedir: {len(st.session_state.carrinho)} itens. Total: R${total}. Entrega em: {endereco}"
            link_whatsapp = f"https://wa.me/5561999999999?text={msg.replace(' ', '%20')}"
            st.markdown(f"[CLIQUE AQUI PARA ENVIAR O PEDIDO]({link_whatsapp})")
