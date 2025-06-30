# Arquivo: pages/1_Limpeza.py (Versão Corrigida)
import streamlit as st
import pandas as pd
import requests
import io

# --- Importa as funções de lógica do nosso novo arquivo ---
from src.logic.data_cleaning import (
    normalizar_texto_para_comparacao,
    padronizar_nome_contato,
    padronizar_nome_empresa,
    padronizar_localidade_geral,
    padronizar_site,
    padronizar_telefone,
    padronizar_segmento, # <-- VÍRGULA ADICIONADA AQUI
    padronizar_numero_funcionarios 
)

# --- LÓGICA DA PÁGINA (CARREGAMENTO DE DADOS) ---

@st.cache_data
def carregar_dados_ibge():
    """Carrega e prepara mapas otimizados de cidades e estados da API do IBGE."""
    try:
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
st.write("Faça o upload do seu arquivo de leads (exportado do Apollo ou similar) para limpá-lo e padronizá-lo.")

# Carrega os dados do IBGE e os mantém em cache
MAPA_CIDADES, MAPA_ESTADOS = carregar_dados_ibge()

uploaded_file = st.file_uploader("1. Selecione o arquivo de DADOS brutos (.csv)", type="csv")

if st.button("🧹 Iniciar Limpeza e Padronização"):
    if uploaded_file is not None:
        with st.spinner('Lendo e processando o arquivo... Por favor, aguarde.'):
            df = ler_csv_flexivel(uploaded_file)
            
            if df is not None:
                mapa_colunas = {
                    'First Name': 'Nome_Lead', 'Last Name': 'Sobrenome_Lead', 'Title': 'Cargo', 
                    'Company': 'Nome_Empresa', 'Email': 'Email_Lead', 'Corporate Phone': 'Telefone_Original',
                    'Industry': 'Segmento_Original', 'City': 'Cidade_Contato', 'State': 'Estado_Contato', 
                    'Country': 'Pais_Contato', 'Company City': 'Cidade_Empresa', 'Company State': 'Estado_Empresa',
                    'Company Country': 'Pais_Empresa', 'Website': 'Site_Original', '# Employees': 'Numero_Funcionarios',
                    'Person Linkedin Url': 'Linkedin_Contato', 'Company Linkedin Url': 'LinkedIn_Empresa', 
                    'Facebook Url': 'Facebook_Empresa'
                }
                
                colunas_para_renomear = {k: v for k, v in mapa_colunas.items() if k in df.columns}
                df_limpo = df.rename(columns=colunas_para_renomear)
                
                colunas_finais = list(colunas_para_renomear.values())
                df_limpo = df_limpo[[col for col in colunas_finais if col in df_limpo.columns]].copy()

                df_cols = list(df_limpo.columns)
                if 'Nome_Lead' in df_cols and 'Sobrenome_Lead' in df_cols:
                    df_limpo['Nome_Completo'] = df_limpo.apply(lambda row: padronizar_nome_contato(row, df_cols), axis=1)
                    df_limpo = df_limpo.drop(columns=['Nome_Lead', 'Sobrenome_Lead'])
                
                colunas_para_padronizar = {
                    'Nome_Empresa': padronizar_nome_empresa, 
                    'Site_Original': padronizar_site,
                    'Telefone_Original': padronizar_telefone,
                    'Segmento_Original': padronizar_segmento, 
                    'Numero_Funcionarios': padronizar_numero_funcionarios,
                    'Cidade_Contato': lambda x: padronizar_localidade_geral(x, 'cidade', MAPA_CIDADES, MAPA_ESTADOS),
                    'Estado_Contato': lambda x: padronizar_localidade_geral(x, 'estado', MAPA_CIDADES, MAPA_ESTADOS),
                    'Pais_Contato': lambda x: padronizar_localidade_geral(x, 'pais', MAPA_CIDADES, MAPA_ESTADOS),
                    'Cidade_Empresa': lambda x: padronizar_localidade_geral(x, 'cidade', MAPA_CIDADES, MAPA_ESTADOS),
                    'Estado_Empresa': lambda x: padronizar_localidade_geral(x, 'estado', MAPA_CIDADES, MAPA_ESTADOS),
                    'Pais_Empresa': lambda x: padronizar_localidade_geral(x, 'pais', MAPA_CIDADES, MAPA_ESTADOS),
                }
                
                for col, func in colunas_para_padronizar.items():
                    if col in df_limpo.columns:
                        df_limpo[col] = df_limpo[col].astype(str).apply(func)
                
                ordem_final_desejada = [
                    'Nome_Completo', 'Cargo', 'Email_Lead', 'Nome_Empresa', 'Site_Original',
                    'Telefone_Original', 'Cidade_Contato', 'Estado_Contato', 'Pais_Contato',
                    'Segmento_Original', 'Cidade_Empresa', 'Estado_Empresa', 'Pais_Empresa',
                    'Numero_Funcionarios', 'Linkedin_Contato', 'LinkedIn_Empresa', 'Facebook_Empresa'
                ]
                colunas_existentes_na_ordem = [col for col in ordem_final_desejada if col in df_limpo.columns]
                outras_colunas = [col for col in df_limpo.columns if col not in colunas_existentes_na_ordem]
                df_limpo = df_limpo[colunas_existentes_na_ordem + outras_colunas]
                
                # Limpeza final para garantir que não haja 'nan' ou valores nulos (Versão Corrigida)
                df_limpo.fillna('', inplace=True)
                for col in df_limpo.columns:
                    df_limpo[col] = df_limpo[col].astype(str).apply(lambda x: '' if x.strip().lower() == 'nan' else x)
                    
                st.success("Arquivo limpo e padronizado com sucesso!")
                st.dataframe(df_limpo.head(10))

                st.session_state['df_limpo'] = df_limpo
    else:
        st.warning("Por favor, faça o upload de um arquivo para começar.")

if 'df_limpo' in st.session_state:
    st.write("---")
    st.header("Próximo Passo")
    col1, col2 = st.columns(2)
    
    with col1:
        csv = st.session_state['df_limpo'].to_csv(sep=';', index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label="⬇️ Baixar CSV Limpo", data=csv, file_name='leads_limpos.csv', 
            mime='text/csv', use_container_width=True
        )
        
    with col2:
        if st.button("➡️ Enviar para Análise (Estação 2)", use_container_width=True):
            st.switch_page("pages/2_Analise_de_ICP.py")
