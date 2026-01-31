import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DO LINK DA PLANILHA
# Use exatamente este formato abaixo:
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQhJW43nfokHKiBwhu64dORzbzD8m8Haxy8tEbGRsysr8JG1Wq8s7qgRfHT5ZLLUBkAuHzUJFKODEDZ/pub?output=csv"

@st.cache_data(ttl=60)
def carregar_dados():
    # O comando abaixo lê o link da planilha
    return pd.read_csv(SHEET_URL)

# --- RESTO DO SEU CÓDIGO ABAIXO ---
try:
    df = carregar_dados()
    st.success("Dados carregados com sucesso!")
except Exception as e:
    st.error(f"Erro ao conectar com a planilha: {e}")
    st.stop()

# Aqui continua a parte visual (o grid de produtos que te passei antes)
