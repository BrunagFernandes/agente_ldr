

# 🤖 Agente LDR: Automação Inteligente de Geração de Leads

**Um assistente de software que transforma listas de contatos brutas em bases de leads qualificados, limpas e prontas para a ação.**

![Streamlit](https://img.shields.io/badge/Feito%20com-Streamlit-red?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-blueviolet?style=for-the-badge&logo=pandas)

---

## 🎯 Sobre o Projeto

O Agente LDR nasceu da necessidade de otimizar e automatizar o pré-processamento de listas para geração de leads, especialmente as exportadas de plataformas como o **Apollo.io**. O objetivo é eliminar horas de trabalho manual, reduzir erros humanos e garantir que a equipe de vendas possa focar no que realmente importa: conectar-se com os contatos certos.

Este projeto utiliza uma arquitetura de software moderna, separando a lógica de processamento da interface do usuário para garantir manutenibilidade e escalabilidade.

---

## ✨ Funcionalidades Atuais (Estação 1: Limpeza)

A primeira estação do nosso agente é uma poderosa ferramenta de limpeza e padronização de dados, realizando as seguintes tarefas com apenas um clique:

* **Leitura Inteligente:** Interpreta arquivos `.csv` com diferentes separadores.
* **Padronização de Nomes:**
    * Cria um campo de nome completo a partir do nome e sobrenome.
    * Limpa nomes de empresas, removendo sufixos corporativos (LTDA, S/A, etc.).
* **Validação de Telefones:**
    * Descarta números 0800 e telefones internacionais.
    * Formata todos os contatos válidos do Brasil para o padrão `(XX) XXXXX-XXXX`.
* **Tradução e Contextualização:**
    * Converte segmentos de mercado do inglês para o português.
    * Padroniza nomes de cidades e estados brasileiros com base nos dados oficiais do IBGE, corrigindo inconsistências.
* **Formatação de Dados:** Garante que dados numéricos, como o número de funcionários, sejam exibidos como inteiros, sem casas decimais.

---

## 🗺️ Roadmap Futuro (Próximas Estações)

O Agente LDR está em constante evolução. As próximas fases do projeto incluem o desenvolvimento de funcionalidades de inteligência para a geração de leads:

* **[ ] Estação de Geração Ativa de Leads:**
    * **Integração Direta com API do Apollo:** Permitirá buscar leads diretamente da interface do agente, sem precisar subir arquivos.
    * **Busca por ICP:** O usuário poderá definir o Perfil de Cliente Ideal (cargos, segmentos, localização) e o agente buscará os contatos.
    * **Busca Hierárquica e Inteligente:** O agente buscará cargos em ordem de prioridade (ex: Gerente > Coordenador) e garantirá apenas um contato por empresa.
* **[ ] Estação de Análise (Estação 2):**
    * **Análise de Potencial:** Calculará o total de leads únicos disponíveis para um determinado ICP antes da extração.
    * **Análise de Mercado:** Gerará insights sobre os segmentos e cargos mais encontrados.
* **[ ] Sistema de Campanhas com Memória:**
    * **Salvar Buscas:** Permitirá salvar e nomear campanhas de geração de leads.
    * **Prevenção de Duplicados:** O agente terá uma "memória" para nunca baixar um contato que já foi extraído na mesma campanha, garantindo listas sempre novas.

---

## 🛠️ Como Usar a Estação 1

1.  **Acesse a Aplicação:** Abra o link do projeto.
2.  **Navegue:** No menu lateral, clique em **"1 Limpeza"**.
3.  **Carregue:** Faça o upload do seu arquivo `.csv` exportado do Apollo.
4.  **Processe:** Clique em **"Iniciar Limpeza e Padronização"**.
5.  **Baixe:** Após a pré-visualização, clique em **"Baixar CSV Limpo"** para obter sua lista pronta.

---

## ⚙️ Configuração do Ambiente de Desenvolvimento

Para contribuir com o projeto ou rodá-lo em um novo ambiente (como o GitHub Codespaces):

1.  **Clone o repositório:**
    ```bash
    git clone URL_DO_SEU_REPOSITORIO
    cd NOME_DO_REPOSITORIO
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute o aplicativo Streamlit:**
    ```bash
    streamlit run app.py

