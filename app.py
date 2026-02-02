import streamlit as st
import barcode
from barcode.writer import ImageWriter
import qrcode
from io import BytesIO
import base64
from datetime import datetime

# 1. Configurações Iniciais
st.set_page_config(page_title="Gerador MAD", layout="centered")

def gerar_imagem_barcode(dados):
    COD = barcode.get_barcode_class('code128')
    buffer = BytesIO()
    # Usando writer com fundo branco e sem texto embaixo (o texto colocamos via HTML)
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

with st.expander("📝 Dados do Pedido", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        id_pedido = st.text_input("ID do Pedido", "10258")
        rastreio = st.text_input("Código de Rastreio", "MAD789456123")
    with col2:
        cliente = st.text_input("Nome do Cliente", "MIRON DE AQUINO DIAS")
        cep = st.text_input("CEP", "73800-000")
    
    endereco = st.text_area("Endereço Completo", "Rua 15, Casa 200, Setor Central, Formosa-GO")
    item_declarado = st.text_input("Conteúdo Declarado", "1x Capinha iPhone 13 Pro Max")

# 3. Lógica de Geração
if st.button("GERAR ETIQUETA AGORA", use_container_width=True):
    # Preparar Dados
    dados_qr = f"PEDIDO: {id_pedido}\nCLIENTE: {cliente}\nEND: {endereco}\nCEP: {cep}\nITEM: {item_declarado}"
    
    # Gerar Imagens em Memória
    img_bar = gerar_imagem_barcode(rastreio)
    img_qr = gerar_imagem_qrcode(dados_qr)
    
    # Converter para Base64
    bar_b64 = base64.b64encode(img_bar.getvalue()).decode()
    qr_b64 = base64.b64encode(img_qr.getvalue()).decode()
    hoje = datetime.now().strftime("%d/%m/%Y")

    # Montagem do HTML (Design Limpo para Impressão)
    etiqueta_html = f"""
    <div style="background-color: white; padding: 15px; border: 3px solid black; color: black; font-family: 'Arial', sans-serif; width: 360px; margin: auto; line-height: 1.2;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid black; padding-bottom: 5px;">
            <span style="font-size: 18px; font-weight: bold;">FSA MARKET</span>
            <span style="background: black; color: white; padding: 3px 10px; font-size: 12px; font-weight: bold;">MAD LOG</span>
        </div>

        <div style="text-align: center; font-size: 22px; font-weight: bold; margin: 10px 0;">
            PEDIDO: {id_pedido}
        </div>

        <div style="font-size: 13px; margin-bottom: 10px;">
            <b style="font-size: 11px; text-transform: uppercase;">Destinatário:</b><br>
            <span style="font-size: 16px; font-weight: bold;">{cliente}</span><br>
            {endereco}<br>
            <b>CEP: {cep}</b>
        </div>

        <div style="border: 1px solid black; padding: 5px; font-size: 11px; background: #f2f2f2; margin-bottom: 10px;">
            <b>CONTEÚDO DECLARADO:</b><br>
            {item_declarado}
        </div>

        <div style="text-align: center;">
            <img src="data:image/png;base64,{bar_b64}" style="width: 100%; max-height: 60px;">
            <p style="font-size: 13px; font-weight: bold; margin: 2px 0;">{rastreio}</p>
            
            <div style="margin-top: 10px;">
                <img src="data:image/png;base64,{qr_b64}" width="100">
                <p style="font-size: 9px; color: #555; margin: 0;">SCAN PARA CONFERÊNCIA</p>
            </div>
        </div>

        <div style="border-top: 1px solid black; margin-top: 10px; padding-top: 5px; font-size: 9px; text-align: center; color: #444;">
            EMISSÃO: {hoje} | ORIGEM: FORMOSA-GO | SPX EXPRESS
        </div>
    </div>
    """

    # EXIBIÇÃO DA ETIQUETA
    st.divider()
    st.markdown(etiqueta_html, unsafe_allow_html=True)
    st.divider()
    
    st.info("💡 Dica: Para imprimir, clique com o botão direito na etiqueta e selecione 'Imprimir' ou tire um print da tela.")
