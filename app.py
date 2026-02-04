import streamlit as st
import barcode
from barcode.writer import ImageWriter
import qrcode
from io import BytesIO
import base64
from datetime import datetime

# 1. Configurações da Página
st.set_page_config(page_title="Gerador MAD - FSA Market", layout="centered")

# URL da Logo Gerada (Usando a última versão tecnológica)
URL_LOGO = "https://raw.githubusercontent.com/fsa-market/assets/main/logo.png" # Substitua pelo link real da imagem ou caminho local

# 2. Funções de Geração de Imagem
def gerar_imagem_barcode(dados):
    COD = barcode.get_barcode_class('code128')
    buffer = BytesIO()
    writer = ImageWriter()
    options = {'dpi': 300, 'module_height': 15.0, 'write_text': False}
    codigo = COD(dados, writer=writer)
    codigo.write(buffer, options=options)
    return buffer

def gerar_imagem_qrcode(dados):
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
    qr.add_data(dados)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer

# 3. Interface de Entrada com Identidade Visual
# Layout do Topo
col_l, col_t = st.columns([1, 4])
with col_l:
    # Exibe a logo no App (Versão Circular/Dark que criamos)
    st.image("https://r.jina.ai/i/6f9a0c...", width=100) # Link da imagem gerada anteriormente
with col_t:
    st.title("FSA MARKET")
    st.subheader("🏷️ Criador de Etiquetas MAD")

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
    
    gerar = st.form_submit_button("GERAR ETIQUETA PROFISSIONAL")

# 4. Lógica de Exibição e Impressão
if gerar:
    dados_qr = f"PEDIDO: {id_pedido}\nCLIENTE: {cliente}\nEND: {endereco}\nCEP: {cep}\nITEM: {item_declarado}"
    img_bar = gerar_imagem_barcode(rastreio)
    img_qr = gerar_imagem_qrcode(dados_qr)
    
    bar_b64 = base64.b64encode(img_bar.getvalue()).decode()
    qr_b64 = base64.b64encode(img_qr.getvalue()).decode()
    hoje = datetime.now().strftime("%d/%m/%Y")

    html_content = f"""
    <div id="etiqueta-container">
        <div style="background-color: white; padding: 15px; border: 3px solid black; color: black; font-family: Arial, sans-serif; width: 340px; margin: auto;" id="printable-area">
            
            <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid black; padding-bottom: 8px; margin-bottom: 10px;">
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 18px; font-weight: 900; letter-spacing: -1px;">FSA MARKET</div>
                </div>
                <div style="background: black; color: white; padding: 4px 10px; font-size: 11px; font-weight: bold; border-radius: 3px;">
                    MAD LOG 🚚
                </div>
            </div>
            
            <div style="text-align: center; font-size: 22px; font-weight: bold; margin-bottom: 10px; border: 1px solid #ccc; padding: 5px;">
                PEDIDO: #{id_pedido}
            </div>
            
            <div style="font-size: 12px; line-height: 1.4;">
                <b style="color: #555;">DESTINATÁRIO:</b><br>
                <span style="font-size: 15px; font-weight: bold; text-transform: uppercase;">{cliente}</span><br>
                {endereco}<br>
                <b style="font-size: 14px;">CEP: {cep}</b>
            </div>
            
            <div style="border: 1px solid black; padding: 6px; font-size: 11px; margin: 12px 0; background: #f9f9f9; border-left: 5px solid black;">
                <b>CONTEÚDO DECLARADO:</b><br>
                {item_declarado}
            </div>
            
            <div style="text-align: center; margin-top: 10px;">
                <img src="data:image/png;base64,{bar_b64}" style="width: 100%; height: 65px; image-rendering: pixelated;"><br>
                <b style="font-size: 16px; letter-spacing: 3px;">{rastreio}</b><br><br>
                
                <div style="display: flex; align-items: center; justify-content: center; gap: 15px;">
                    <img src="data:image/png;base64,{qr_b64}" width="85" style="image-rendering: pixelated;">
                    <div style="text-align: left; font-size: 9px; line-height: 1.2; font-weight: bold;">
                        RASTREIO DIGITAL<br>FSA MARKET SYNC<br>🔒 PROTOCOLO SEGURO
                    </div>
                </div>
            </div>

            <div style="margin-top: 20px; border-top: 1px dashed #000; padding-top: 10px;">
                <div style="font-size: 10px; margin-bottom: 18px;"><b>RECEBIDO POR:</b></div>
                <div style="border-bottom: 1px solid black; width: 100%; height: 1px; margin-bottom: 5px;"></div>
                <div style="display: flex; justify-content: space-between; font-size: 9px;">
                    <span>NOME: __________________________</span>
                    <span>DOC: ________________</span>
                </div>
            </div>
            
            <div style="text-align: center; font-size: 9px; border-top: 1px solid black; margin-top: 15px; padding-top: 5px; color: #666;">
                {hoje} | FORMOSA-GO | 🛒 FSA MARKET ONLINE
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 25px;">
            <button onclick="window.print()" style="padding: 12px 30px; background-color: #000; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                🖨️ IMPRIMIR ETIQUETA AGORA
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

    st.components.v1.html(html_content, height=900, scrolling=True)
