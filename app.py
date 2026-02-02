import streamlit as st
import barcode
from barcode.writer import ImageWriter
import qrcode
from io import BytesIO
import base64
from datetime import datetime

# 1. Configuração da Página
st.set_page_config(page_title="Gerador de Etiquetas MAD", page_icon="🏷️")

def gerar_imagem_barcode(dados):
    COD = barcode.get_barcode_class('code128')
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

# 2. Interface de Entrada
st.title("🏷️ Criador de Etiquetas MAD")
st.write("Preencha os dados abaixo para gerar a etiqueta de envio.")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        id_pedido = st.text_input("ID do Pedido", "10258")
        rastreio = st.text_input("Código de Rastreio", "MAD789456123")
    with col2:
        cliente = st.text_input("Nome do Cliente", "MIRON DE AQUINO DIAS")
        cep = st.text_input("CEP", "73800-000")

    endereco = st.text_area("Endereço Completo", "Rua 15, Casa 200, Setor Central, Formosa-GO")
    item_declarado = st.text_input("Conteúdo / Item Declarado", "1x Capinha iPhone 13 Pro Max")

# 3. Geração da Etiqueta
if st.button("Gerar Etiqueta"):
    # Dados para o QR Code
    dados_qr = f"PEDIDO: {id_pedido}\nCLIENTE: {cliente}\nENDERECO: {endereco}\nCEP: {cep}\nITEM: {item_declarado}"
    
    # Gerar Imagens
    img_bar = gerar_imagem_barcode(rastreio)
    img_qr = gerar_imagem_qrcode(dados_qr)
    
    # Converter para Base64 para exibir no HTML
    bar_base64 = base64.b64encode(img_bar.getvalue()).decode()
    qr_base64 = base64.b64encode(img_qr.getvalue()).decode()
    data_atual = datetime.now().strftime("%d/%m/%Y")

    # Layout HTML corrigido (FECHAMENTO NA LINHA 80)
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border: 2px solid #000; color: black; font-family: monospace; width: 380px; margin: auto;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <b style="font-size: 20px;">FSA MARKET</b>
            <span style="border: 1px solid black; padding: 2px 5px; font-weight: bold;">MAD LOG</span>
        </div>
