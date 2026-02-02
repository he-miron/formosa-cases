import streamlit as st
import barcode
from barcode.writer import ImageWriter
import qrcode
from io import BytesIO
import base64
from datetime import datetime

# 1. Configurações Iniciais (DEVE VIR PRIMEIRO)
st.set_page_config(page_title="Gerador de Etiquetas MAD", page_icon="🏷️")

# 2. Definição de Funções (O Python precisa conhecê-las antes de usá-las)
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

# 3. Interface de Usuário
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

# 4. Lógica do Botão (SÓ NO FINAL)
if st.button("Gerar Etiqueta"):
    # Preparar Dados
    dados_qr = f"PEDIDO: {id_pedido}\nCLIENTE: {cliente}\nENDERECO: {endereco}\nCEP: {cep}\nITEM: {item_declarado}"
    img_bar = gerar_imagem_barcode(rastreio)
    img_qr = gerar_imagem_qrcode(dados_qr)
    bar_b64 = base64.b64encode(img_bar.getvalue()).decode()
    qr_b64 = base64.b64encode(img_qr.getvalue()).decode()
    hoje = datetime.now().strftime("%d/%m/%Y")

    # Criar o HTML
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
    
    st.markdown(html_etiqueta, unsafe_allow_html=True)
    st.success("Etiqueta gerada com sucesso!")
