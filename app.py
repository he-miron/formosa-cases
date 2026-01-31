# --- ÁREA DE CHECKOUT NO APP ---
with st.sidebar:
    st.header("🛒 Finalizar Pedido")
    nome = st.text_input("Seu Nome")
    endereco = st.text_input("Endereço (Rua e Número)")
    bairro = st.selectbox("Seu Bairro em Formosa", ["Centro", "Formosinha"])
    
    if st.button("🚀 CONFIRMAR COMPRA"):
        if nome and endereco: # Só prossegue se tiver nome e endereço
            seu_numero = "5561991937857" 
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
