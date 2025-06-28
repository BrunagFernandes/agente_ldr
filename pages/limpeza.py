# Arquivo: pages/1_Limpeza.py
import streamlit as st
import pandas as pd
import requests

# --- Importa as funções de lógica do nosso novo arquivo ---
from src.logic.data_cleaning import (
    normalizar_texto_para_comparacao,
    padronizar_nome_contato,
    padronizar_nome_empresa,
    padronizar_localidade_geral,
    padronizar_site,
    padronizar_telefone,
    padronizar_segmento
)

# --- CARREGAMENTO DOS DADOS DE MUNICÍPIOS (FEITO UMA SÓ VEZ) ---
@st.cache_data
def carregar_dados_ibge():
    """Carrega e prepara mapas otimizados de cidades e estados da API do IBGE."""
    try:
        st.info("Carregando lista oficial de localidades do IBGE... (só na primeira vez)")
        url_municipios = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        response_municipios = requests.get(url_municipios)
        response_municipios.raise_for_status()
        municipios_json = response_municipios.json()
        mapa_cidades = {
            normalizar_texto_para_comparacao(m['nome']): m['nome']
            for m in municipios_json if 'nome' in m
        }
        mapa_estados = {}
        for m in municipios_json:
            try:
                uf_data = m['microrregiao']['mesorregiao']['UF']
                sigla = uf_data['sigla'].lower()
                nome = uf_data['nome']
                mapa_estados[sigla] = nome
                mapa_estados[normalizar_texto_para_comparacao(nome)] = nome
            except (KeyError, TypeError):
                continue
        return mapa_cidades, mapa_estados
    except Exception as e:
        st.error(f"Não foi possível carregar a lista de localidades do IBGE: {e}")
        return {}, {}

MAPA_CIDADES, MAPA_ESTADOS = carregar_dados_ibge()

def ler_csv_flexivel(arquivo_upado):
    try:
        arquivo_upado.seek(0)
        df = pd.read_csv(arquivo_upado, sep=',', encoding='utf-8', on_bad_lines='skip', low_memory=False)
        if df.shape[1] <= 1:
            arquivo_upado.seek(0)
            df = pd.read_csv(arquivo_upado, sep=';', encoding='utf-8', on_bad_lines='skip', low_memory=False)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro crítico ao ler o arquivo CSV: {e}")
        return None

# --- INTERFACE DA ESTAÇÃO 1 ---
st.set_page_config(layout="wide", page_title="Estação 1: Limpeza")
st.title("⚙️ Estação 1: Limpeza e Preparação de Dados")
# ... (cole aqui todo o resto do código da interface, do `st.write` em diante)
# ...
# ATENÇÃO: Na parte de 'colunas_para_padronizar', você precisará ajustar a chamada da função de localidade
# para passar os mapas como argumento:
# 'Cidade_Contato': lambda x: padronizar_localidade_geral(x, 'cidade', MAPA_CIDADES, MAPA_ESTADOS),
# 'Estado_Contato': lambda x: padronizar_localidade_geral(x, 'estado', MAPA_CIDADES, MAPA_ESTADOS),
# ... e assim por diante