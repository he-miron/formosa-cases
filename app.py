import streamlit as st
import barcode
from barcode.writer import ImageWriter
import qrcode
from io import BytesIO
import base64

# Configuração da Página
st.set_page_config(page_title="Gerador de Etiquetas MAD", page_icon="🏷️")

def gerar_imagem_barcode(dados):
    COD = barcode.get_barcode_class('code128')
    buffer = BytesIO()
    codigo = COD(dados, writer=ImageWriter())
    codigo.write(buffer)
    return buffer

def gerar_imagem_qrcode(dados):
    # Aumentamos o 'version' para comportar mais texto se necessário
    qr = qrcode.QRCode(version=None, box_size=10, border=2, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(dados)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer

# Interface
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

if st.button("Gerar Etiqueta"):
    # --- NOVIDADE AQUI: String completa para o QR Code ---
    dados_qr = f"PEDIDO: {id_pedido}\nCLIENTE: {cliente}\nENDERECO: {endereco}\nCEP: {cep}"
    
    # Geração dos códigos
    img_bar = gerar_imagem_barcode(rastreio)
    img_qr = gerar_imagem_qrcode(dados_qr)

    # Layout da Etiqueta em HTML/CSS
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border: 2px solid #000; color: black; font-family: 'Courier New', Courier, monospace; width: 380px; margin: auto;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <b style="font-size: 20px;">FSA MARKET</b>
            <span style="border: 1px solid black; padding: 2px 5px;">PADRÃO VIP</span>
        </div>
        <hr style="border: 1px solid black;">
        <div style="text-align: center;">
            <p style="margin: 0;">PEDIDO: {id_pedido}</p>
        </div>
        <br>
        <p style="margin: 0; font-size: 14px;"><b>DESTINATÁRIO:</b></p>
        <p style="margin: 0; font-size: 16px;">{cliente}</p>
        <p style="margin: 0; font-size: 13px;">{endereco}</p>
        <p style="margin: 0; font-size: 14px;"><b>CEP: {cep}</b></p>
        <hr style="border: 0.5px dashed black;">
        <div style="display: flex; flex-direction: column; align-items: center; gap: 10px;">
            <img src="data:image/png;base64,{base64.b64encode(img_bar.getvalue()).decode()}" width="300">
            <p style="margin: 0; font-size: 12px;">{rastreio}</p>
            <img src="data:image/png;base64,{base64.b64encode(img_qr.getvalue()).decode()}" width="120">
            <p style="font-size: 8px; margin-top: -5px;">Escaneie para detalhes do cliente</p>
        </div>
        <br>
        <div style="border-top: 1px solid black; padding-top: 5px; font-size: 10px; text-align: center;">
            DATA: 02/02/2026 | ROTA: FSA-CITY
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("Etiqueta gerada com sucesso!")
