# Arquivo: src/logic/data_cleaning.py
import pandas as pd
import re
import unicodedata

# Tenta importar o dicionário de segmentos. Se não encontrar, cria um dicionário vazio.
try:
    from dados_traducao import DICIONARIO_SEGMENTOS
except ImportError:
    DICIONARIO_SEGMENTOS = {}

# --- FUNÇÕES DE PADRONIZAÇÃO DA ESTAÇÃO 1 ---

def normalizar_texto_para_comparacao(texto):
    """Remove acentos e converte para minúsculo para comparações internas."""
    if pd.isna(texto): return ""
    s = str(texto).lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def title_case_com_excecoes(s, excecoes):
    palavras = str(s).split()
    if not palavras:
        return ""
    resultado = [palavras[0].capitalize()]
    for palavra in palavras[1:]:
        if palavra.lower() in excecoes:
            resultado.append(palavra.lower())
        else:
            resultado.append(palavra.capitalize())
    return ' '.join(resultado)

def padronizar_nome_contato(row, df_columns):
    nome_col = next((col for col in df_columns if 'first name' in col.lower() or 'nome_lead' in col.lower()), None)
    sobrenome_col = next((col for col in df_columns if 'last name' in col.lower() or 'sobrenome_lead' in col.lower()), None)
    if not nome_col or pd.isna(row.get(nome_col)): return ''
    primeiro_nome = str(row[nome_col]).split()[0]
    sobrenome_completo = str(row.get(sobrenome_col, ''))
    conectivos = ['de', 'da', 'do', 'dos', 'das']
    partes_sobrenome = [p for p in sobrenome_completo.split() if p.lower() not in conectivos]
    ultimo_sobrenome = partes_sobrenome[-1] if partes_sobrenome else ''
    nome_final = f"{primeiro_nome} {ultimo_sobrenome}".strip()
    return nome_final.title()

def padronizar_nome_empresa(nome_empresa):
    if pd.isna(nome_empresa): return ''
    nome_limpo = str(nome_empresa)
    siglas = [r'\sS/A', r'\sS\.A', r'\sSA\b', r'\sLTDA', r'\sLtda', r'\sME\b', r'\sEIRELI', r'\sEPP', r'\sMEI\b']
    for sigla in siglas:
        nome_limpo = re.sub(sigla, '', nome_limpo, flags=re.IGNORECASE)
    return title_case_com_excecoes(nome_limpo.strip(), ['de', 'da', 'do', 'dos', 'das', 'e'])

def padronizar_localidade_geral(valor, tipo, mapa_cidades, mapa_estados):
    if pd.isna(valor): return ''
    mapa_paises = { 'br': 'Brasil', 'bra': 'Brasil', 'brazil': 'Brasil' }
    chave_busca = normalizar_texto_para_comparacao(str(valor))
    if tipo == 'cidade':
        return mapa_cidades.get(chave_busca, title_case_com_excecoes(str(valor), ['de', 'da', 'do', 'dos', 'das']))
    elif tipo == 'estado':
        chave_busca_estado = re.sub(r'state of ', '', chave_busca).strip()
        return mapa_estados.get(chave_busca_estado, title_case_com_excecoes(str(valor), ['de', 'do']))
    elif tipo == 'pais':
        return mapa_paises.get(chave_busca, str(valor).capitalize())
    return valor

def padronizar_site(site):
    if pd.isna(site) or str(site).strip() == '': return ''
    site_limpo = str(site).strip()
    site_limpo = re.sub(r'^(https?://)?', '', site_limpo)
    site_limpo = site_limpo.rstrip('/')
    if not site_limpo.lower().startswith('www.'):
        site_limpo = 'www.' + site_limpo
    return site_limpo

def padronizar_telefone(telefone):
    if pd.isna(telefone):
        return ''
    tel_str = str(telefone).strip()
    if tel_str.startswith('+') and not tel_str.startswith('+55'):
        return ''
    apenas_digitos = re.sub(r'\D', '', tel_str)
    if apenas_digitos.startswith('55'):
        apenas_digitos = apenas_digitos[2:]
    if apenas_digitos.startswith('0800'):
        return ''
    if len(apenas_digitos) == 11 and apenas_digitos.startswith('0'):
        apenas_digitos = apenas_digitos[1:]
    if len(apenas_digitos) not in [10, 11]:
        return ''
    if len(apenas_digitos) == 11:
        return f"({apenas_digitos[:2]}) {apenas_digitos[2:7]}-{apenas_digitos[7:]}"
    elif len(apenas_digitos) == 10:
        if apenas_digitos.startswith('800'):
            return ''
        return f"({apenas_digitos[:2]}) {apenas_digitos[2:6]}-{apenas_digitos[6:]}"
    return ''

def padronizar_segmento(segmento):
    """Traduz o segmento usando o dicionário interno."""
    if pd.isna(segmento): return ''
    segmento_norm = str(segmento).lower().strip()
    return DICIONARIO_SEGMENTOS.get(segmento_norm, title_case_com_excecoes(segmento, []))

def padronizar_numero_funcionarios(valor):
    """Converte o número de funcionários para um inteiro (removendo o .0) e depois para string."""
    if pd.isna(valor) or str(valor).strip() == '':
        return ''
    try:
        # Tenta converter o valor para float, depois para inteiro, e finalmente para string
        return str(int(float(valor)))
    except (ValueError, TypeError):
        # Se não for um número conversível, retorna o valor como está (em formato string)
        return str(valor)