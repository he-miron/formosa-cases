import streamlit as st
import barcode
from barcode.writer import ImageWriter
import qrcode
from io import BytesIO
import base64
from datetime import datetime

# 1. Configurações da Página
st.set_page_config(page_title="Gerador MAD", layout="centered")

# 2. Funções de Geração de Imagem (Alta Definição)
def gerar_imagem_barcode(dados):
    COD = barcode.get_barcode_class('code128')
    buffer = BytesIO()
    writer = ImageWriter()
    options = {
        'dpi': 300, 
        'module_height': 15.0, 
        'write_text': False 
    }
    codigo = COD(dados, writer=writer)
    codigo.write(buffer, options=options)
    return buffer

def gerar_imagem_qrcode(dados):
    qr = qrcode.QRCode(
        version=None, 
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10, 
        border=2
    )
    qr.add_data(dados)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer

# 3. Interface de Entrada
st.title("🏷️ Criador de Etiquetas MAD")

with st.form("meu_formulario"):
    col1, col2 = st.columns(2)
    with col1:
        id_pedido = st.text_input("ID do Pedido", "520")
        rastreio = st.text_input("Código de Rastreio", "5207417778")
    with col2:
        cliente = st.text_input("Nome do Cliente", "MIRON DE AQUINO DIAS")
        cep = st.text_input("CEP", "73803-277")
    
    endereco = st.text_area("Endereço Completo", "Rua 15, Casa 200, Setor Central, Formosa-GO")
    item_declarado = st.text_input("Conteúdo Declarado", "1x Capinha iPhone 13 Pro Max")
    
    gerar = st.form_submit_button("GERAR ETIQUETA")

# 4. Lógica de Exibição e Impressão
if gerar:
    dados_qr = f"PEDIDO: {id_pedido}\nCLIENTE: {cliente}\nEND: {endereco}\nCEP: {cep}\nITEM: {item_declarado}"
    img_bar = gerar_imagem_barcode(rastreio)
    img_qr = gerar_imagem_qrcode(dados_qr)
    
    bar_b64 = base64.b64encode(img_bar.getvalue()).decode()
    qr_b64 = base64.b64encode(img_qr.getvalue()).decode()
    hoje = datetime.now().strftime("%d/%m/%Y")

    # HTML com o Botão de Impressão e Campo de Assinatura
    html_content = f"""
    <div id="etiqueta-container">
        <div style="background-color: white; padding: 15px; border: 3px solid black; color: black; font-family: Arial, sans-serif; width: 320px; margin: auto;" id="printable-area">
            <div style="display: flex; justify-content: space-between; border-bottom: 2px solid black; padding-bottom: 5px;">
                <b style="font-size: 16px;">FSA MARKET</b>
                <span style="background: black; color: white; padding: 2px 8px; font-size: 12px; font-weight: bold;">MAD LOG</span>
            </div>
            
            <div style="text-align: center; font-size: 20px; font-weight: bold; margin: 15px 0;">PEDIDO: {id_pedido}</div>
            
            <div style="font-size: 12px; line-height: 1.4;">
                <b>DESTINATÁRIO:</b><br>
                <span style="font-size: 14px; font-weight: bold;">{cliente}</span><br>
                {endereco}<br>
                <b>CEP: {cep}</b>
            </div>
            
            <div style="border: 1px solid black; padding: 5px; font-size: 11px; margin: 10px 0; background: #f4f4f4;">
                <b>CONTEÚDO:</b> {item_declarado}
            </div>
            
            <div style="text-align: center;">
                <img src="data:image/png;base64,{bar_b64}" style="width: 100%; height: 60px; image-rendering: pixelated;"><br>
                <b style="font-size: 14px; letter-spacing: 2px;">{rastreio}</b><br><br>
                
                <img src="data:image/png;base64,{qr_b64}" width="80" style="image-rendering: pixelated;"><br>
                <span style="font-size: 9px; font-weight: bold;">CONFERÊNCIA DE SEGURANÇA</span>
            </div>

            <div style="margin-top: 20px; border-top: 1px dashed #000; padding-top: 10px;">
                <div style="font-size: 10px; margin-bottom: 20px;"><b>ASSINATURA DO RECEBEDOR:</b></div>
                <div style="border-bottom: 1px solid black; width: 100%; height: 20px;"></div>
                <div style="display: flex; justify-content: space-between; font-size: 9px; margin-top: 5px;">
                    <span>NOME: __________________________</span>
                    <span>DOC: ________________</span>
                </div>
            </div>
            
            <div style="text-align: center; font-size: 9px; border-top: 1px solid black; margin-top: 15px; padding-top: 5px;">
                {hoje} | ORIGEM: FORMOSA-GO 🛒 | MIRON DE AQUINO
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 20px;">
            <button onclick="window.print()" style="padding: 10px 20px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                🖨️ IMPRIMIR ETIQUETA
            </button>
        </div>
    </div>

    <style>
        @media print {{
            body * {{ visibility: hidden; }}
            #printable-area, #printable-area * {{ visibility: visible; }}
            #printable-area {{ position: absolute; left: 0; top: 0; width: 100%; border: none; }}
            button {{ display: none; }}
        }}
    </style>
    """

    st.components.v1.html(html_content, height=850, scrolling=True)
