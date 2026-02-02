import streamlit as st
import barcode
from barcode.writer import ImageWriter
import qrcode
from io import BytesIO
import base64
from datetime import datetime

# 1. Funções com Melhoria de Qualidade
def gerar_imagem_barcode(dados):
    COD = barcode.get_barcode_class('code128')
    buffer = BytesIO()
    # Aumentamos o DPI para 300 e removemos o texto nativo para ganhar nitidez
    writer = ImageWriter()
    options = {
        'dpi': 300, 
        'module_height': 15.0, 
        'text_distance': 1.0, 
        'write_text': False # Tiramos o texto da imagem para não borrar
    }
    codigo = COD(dados, writer=writer)
    codigo.write(buffer, options=options)
    return buffer

def gerar_imagem_qrcode(dados):
    # QR Code com correção de erro nível M para melhor leitura
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

# ... (Mantenha sua interface de entrada igual)

if gerar:
    dados_qr = f"PEDIDO: {id_pedido}\nCLIENTE: {cliente}\nEND: {endereco}\nCEP: {cep}\nITEM: {item_declarado}"
    img_bar = gerar_imagem_barcode(rastreio)
    img_qr = gerar_imagem_qrcode(dados_qr)
    
    bar_b64 = base64.b64encode(img_bar.getvalue()).decode()
    qr_b64 = base64.b64encode(img_qr.getvalue()).decode()
    hoje = datetime.now().strftime("%d/%m/%Y")

    # HTML OTIMIZADO PARA NITIDEZ
    html_content = f"""
    <div style="background-color: white; padding: 15px; border: 2px solid black; color: black; font-family: Arial, sans-serif; width: 330px; margin: auto;">
        <div style="display: flex; justify-content: space-between; border-bottom: 2px solid black; padding-bottom: 5px;">
            <b style="font-size: 16px;">FSA MARKET</b>
            <span style="background: black; color: white; padding: 2px 8px; font-size: 12px; font-weight: bold;">MAD LOG</span>
        </div>
        
        <div style="text-align: center; font-size: 20px; font-weight: bold; margin: 15px 0;">PEDIDO: {id_pedido}</div>
        
        <div style="font-size: 13px; line-height: 1.4;">
            <b>DESTINATÁRIO:</b><br>
            <span style="font-size: 15px; font-weight: bold;">{cliente}</span><br>
            {endereco}<br>
            <b>CEP: {cep}</b>
        </div>
        
        <div style="border: 1px solid black; padding: 8px; font-size: 12px; margin: 12px 0; background: #f4f4f4;">
            <b>CONTEÚDO:</b> {item_declarado}
        </div>
        
        <div style="text-align: center;">
            <img src="data:image/png;base64,{bar_b64}" style="width: 300px; height: 70px; image-rendering: pixelated;"><br>
            <b style="font-size: 14px; letter-spacing: 2px;">{rastreio}</b><br><br>
            
            <img src="data:image/png;base64,{qr_b64}" width="110" style="image-rendering: pixelated;"><br>
            <span style="font-size: 10px; font-weight: bold;">CONFERÊNCIA DE SEGURANÇA</span>
        </div>
        
        <div style="text-align: center; font-size: 10px; border-top: 1px solid black; margin-top: 15px; padding-top: 5px;">
            {hoje} | ORIGEM: FORMOSA-GO | SPX
        </div>
    </div>
    """

    st.components.v1.html(html_content, height=600, scrolling=True)
