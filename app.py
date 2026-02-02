if st.button("Gerar Etiqueta"):
    # 1. Preparar Dados
    dados_qr = f"PEDIDO: {id_pedido}\nCLIENTE: {cliente}\nENDERECO: {endereco}\nCEP: {cep}\nITEM: {item_declarado}"
    img_bar = gerar_imagem_barcode(rastreio)
    img_qr = gerar_imagem_qrcode(dados_qr)
    bar_b64 = base64.b64encode(img_bar.getvalue()).decode()
    qr_b64 = base64.b64encode(img_qr.getvalue()).decode()
    hoje = datetime.now().strftime("%d/%m/%Y")

    # 2. Criar o HTML em uma variável separada para evitar erro de sintaxe
    html_etiqueta = f"""
    <div style="background-color: white; padding: 20px; border: 3px solid black; color: black; font-family: monospace; width: 350px; margin: auto;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid black; padding-bottom: 10px;">
            <b style="font-size: 20px;">FSA MARKET</b>
            <span style="background: black; color: white; padding: 2px 8px;">MAD LOG</span>
        </div>
        
        <div style="text-align: center; font-size: 22px; font-weight: bold; margin: 15px 0;">
            PEDIDO: {id_pedido}
        </div>

        <div style="font-size: 14px; line-height: 1.2;">
            <b>DESTINATÁRIO:</b><br>
            {cliente}<br>
            {endereco}<br>
            <b>CEP: {cep}</b>
        </div>

        <div style="border: 1px solid black; margin: 10px 0; padding: 5px; font-size: 12px; background: #eee;">
            <b>CONTEÚDO:</b> {item_declarado}
        </div>

        <div style="text-align: center; margin-top: 15px;">
            <img src="data:image/png;base64,{bar_b64}" width="280">
            <p style="font-size: 14px; font-weight: bold; margin: 0;">{rastreio}</p>
            <br>
            <img src="data:image/png;base64,{qr_b64}" width="120">
            <p style="font-size: 10px;">SCAN PARA CONFERÊNCIA</p>
        </div>

        <div style="border-top: 1px solid black; margin-top: 10px; padding-top: 5px; font-size: 10px; text-align: center;">
            EMISSÃO: {hoje} | ORIGEM: FORMOSA-GO
        </div>
    </div>
    """
    
    # 3. Exibir sem risco de SyntaxError
    st.markdown(html_etiqueta, unsafe_allow_html=True)
    st.success("Etiqueta gerada com sucesso!")
