import streamlit as st
import barcode
from barcode.writer import ImageWriter
import qrcode
from io import BytesIO
import base64
from datetime import datetime

# 1. Configurações
st.set_page_config(page_title="Gerador MAD", layout="centered")

def gerar_imagem_barcode(dados):
    COD = barcode.get_barcode_class('code300')
    buffer = BytesIO()
    codigo = COD(dados, writer=ImageWriter())
    codigo.write(buffer)
    return buffer

def gerar_imagem_qrcode(dados):
    qr = qrcode.QRCode(version=None, box_size=10, border=2, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(dados)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer

# 2. Interface
st.title("🏷️ Criador de Etiquetas MAD")

with st.form("dados_etiqueta"):
    col1, col2 = st.columns(2)
    with col1:
        id_pedido = st.text_input("ID do Pedido", "10258")
        rastreio = st.text_input("Código de Rastreio", "MAD789456123")
    with col2:
        cliente = st.text_input("Nome do Cliente", "MIRON DE AQUINO DIAS")
        cep = st.text_input("CEP", "73800-000")
    
    endereco = st.text_area("Endereço Completo", "Rua 15, Casa 200, Setor Central, Formosa-GO")
    item_declarado = st.text_input("Conteúdo Declarado", "1x Capinha iPhone 13 Pro Max")
    gerar = st.form_submit_button("GERAR ETIQUETA")

if gerar:
    # Preparar Dados e Imagens
    dados_qr = f"PEDIDO: {id_pedido}\nCLIENTE: {cliente}\nEND: {endereco}\nCEP: {cep}\nITEM: {item_declarado}"
    img_bar = gerar_imagem_barcode(rastreio)
    img_qr = gerar_imagem_qrcode(dados_qr)
    
    bar_b64 = base64.b64encode(img_bar.getvalue()).decode()
    qr_b64 = base64.b64encode(img_qr.getvalue()).decode()
    hoje = datetime.now().strftime("%d/%m/%Y")

    # HTML DA ETIQUETA (Formatado para não quebrar)
    html_content = f"""
    <div style="background-color: white; padding: 10px; border: 2px solid black; color: black; font-family: sans-serif; width: 320px; height: auto;">
        <div style="display: flex; justify-content: space-between; border-bottom: 2px solid black;">
            <b style="font-size: 16px;">FSA MARKET</b>
            <span style="background: black; color: white; padding: 0 5px; font-size: 12px;">MAD LOG</span>
        </div>
        <div style="text-align: center; font-size: 20px; font-weight: bold; margin: 10px 0;">PEDIDO: {id_pedido}</div>
        <div style="font-size: 12px;">
            <b>DESTINATÁRIO:</b><br>
            <span style="font-size: 14px; font-weight: bold;">{cliente}</span><br>
            {endereco}<br>
            <b>CEP: {cep}</b>
        </div>
        <div style="border: 1px solid black; padding: 5px; font-size: 11px; margin: 10px 0; background: #f0f0f0;">
            <b>CONTEÚDO:</b> {item_declarado}
        </div>
        <div style="text-align: center;">
            <img src="data:image/png;base64,{bar_b64}" width="280" height="60"><br>
            <b style="font-size: 12px;">{rastreio}</b><br><br>
            <img src="data:image/png;base64,{qr_b64}" width="100"><br>
            <span style="font-size: 9px;">CONFERÊNCIA DE SEGURANÇA</span>
        </div>
        <div style="text-align: center; font-size: 9px; border-top: 1px solid black; margin-top: 10px;">
            {hoje} | ORIGEM: FORMOSA-GO
        </div>
    </div>
    """

    # O SEGREDO: Usar um componente de HTML fixo (Iframe)
    st.components.v1.html(html_content, height=550, scrolling=True)
    
    st.success("Etiqueta pronta para impressão!")
