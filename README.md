# Sistema Multiagente para Análise de "O Alienista"

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Transformers](https://img.shields.io/badge/🤗%20Transformers-Usado-yellow.svg)
![SentenceTransformers](https://img.shields.io/badge/SentenceTransformers-Usado-orange.svg)
![HNSWLib](https://img.shields.io/badge/hnswlib-Usado-lightgrey.svg)
![Pandas](https://img.shields.io/badge/Pandas-Usado-blue.svg)

## 📌 Visão Geral

Este projeto implementa um sistema multiagente utilizando Modelos de Linguagem de Grande Escala (LLMs) para realizar a análise textual da obra "O Alienista" de Machado de Assis. O sistema adota uma arquitetura de **Retrieval-Augmented Generation (RAG)** e é composto por quatro agentes distintos que colaboram para responder perguntas sobre o texto:

1.  **Agente A (Recuperador):** Localiza e extrai os blocos de texto mais relevantes da obra com base na pergunta do usuário.
2.  **Agente D (Resumidor):** Recebe os blocos recuperados e gera um resumo conciso, visando focar na informação essencial.
3.  **Agente B (Gerador de Resposta):** Formula uma resposta textual à pergunta, utilizando o resumo fornecido pelo Agente D como contexto.
4.  **Agente C (Avaliador):** Realiza uma avaliação heurística da qualidade da resposta gerada.

O objetivo é demonstrar a implementação de um pipeline multiagente, observar o comportamento dos agentes e analisar o impacto da etapa de sumarização na qualidade das respostas.

## 🛠️ Tecnologias Utilizadas

-   **Python 3.10+**
-   **sentence-transformers:** Para gerar embeddings semânticos (`all-MiniLM-L6-v2`).
-   **transformers (Hugging Face):**
    -   Para o pipeline de Question Answering (Agente B - `deepset/roberta-base-squad2`).
    -   Para o pipeline de Sumarização (Agente D - `t5-small`).
-   **hnswlib:** Para criar e consultar o índice de busca vetorial eficiente.
-   **pandas:** Para manipulação de dados tabulares (ex: blocos de texto).
-   **re (regex):** Para pré-processamento e divisão do texto.

## 📋 Pré-requisitos

Antes de executar o projeto, certifique-se de ter:
-   Python 3.10 ou superior instalado.
-   `pip` (gerenciador de pacotes Python).
-   **(Apenas Windows) Microsoft C++ Build Tools:** A biblioteca `hnswlib` pode requerer compilação C++. Se você estiver no Windows e encontrar problemas na instalação do `hnswlib`, instale as "Build Tools for Visual Studio" a partir [deste link](https://visualstudio.microsoft.com/visual-cpp-build-tools/), certificando-se de selecionar a carga de trabalho "Desenvolvimento para desktop com C++".

## 📂 Estrutura do Projeto

```
sistema-multiagente-alienista/
│   ├── Logs CMD/             # Prints de respostas geradas no CMD
├── Documento de Evidência dos Resultados.pdf #Documentação do Projeto 
├── o_alienista.txt           # Texto completo da obra "O Alienista" (e outras de "Papeis Avulsos")
├── indexador_alienista.py    # Script para processar o texto, gerar embeddings e criar o índice
├── agenteA_alienista.py      # Implementação do Agente A (Recuperador)
├── agenteB_alienista.py      # Implementação do Agente B (Gerador de Resposta)
├── agenteC_avaliador.py      # Implementação do Agente C (Avaliador)
├── agenteD_resumidor.py      # Implementação do Agente D (Resumidor)
├── orquestrador_alienista.py # Script principal que coordena os agentes
├── requirements.txt          # Arquivo com as dependências do projeto
└── README.md                 # Este arquivo
```
*(Nota: Após a execução do `indexador_alienista.py`, serão criados os arquivos `blocos_alienista.csv` e `indice_alienista.bin`)*

## ⚙️ Configuração e Instalação

1.  **Clone o repositório (ou crie a estrutura de pastas e adicione os arquivos):**
    ```bash
    git clone https://github.com/henrique-sdc/sistemas-multiagentes-LLMs.git
    ```

2.  **Instale as dependências a partir do `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Baixe o texto:**
    Certifique-se de que o arquivo `o_alienista.txt` esteja na raiz do projeto.
    Link para download: `https://www.gutenberg.org/cache/epub/57001/pg57001.txt` (salve como `o_alienista.txt`).

## ▶️ Executando o Sistema

O sistema deve ser executado em duas etapas principais:

1.  **Executar o Indexador (apenas uma vez ou sempre que o texto base ou a lógica de blocos mudar):**
    Este script processa `o_alienista.txt`, isola a obra "O Alienista", divide-a em blocos, gera embeddings e salva o índice e os blocos.
    ```bash
    python indexador_alienista.py
    ```
    Aguarde a mensagem "Indexação de 'O Alienista' finalizada com sucesso."

2.  **Executar o Orquestrador:**
    Este script carrega os modelos dos agentes, o índice e processa as perguntas de teste.
    ```bash
    python orquestrador_alienista.py
    ```
    O script irá:
    - Baixar os modelos da Hugging Face (pode levar um tempo na primeira execução de cada modelo).
    - Para cada pergunta de teste:
        - Acionar o Agente A para buscar contexto.
        - Acionar o Agente D para resumir o contexto.
        - Acionar o Agente B para gerar uma resposta.
        - Acionar o Agente C para avaliar a resposta.
    - Imprimir o fluxo de interações e os resultados finais.

## 🚀 Exemplo de Saída Esperada no Terminal (para uma pergunta)

```
--- Iniciando fluxo para a pergunta: 'Quem foi o boticario Crispim Soares na trama?' ---
[Agente A] Buscando contexto para: 'Quem foi o boticario Crispim Soares na trama?' (k=2)
[Agente A] Contexto recuperado com 1259 caracteres de 2 bloco(s).
[Agente D] Iniciando sumarização para texto de 1259 caracteres.
[Agente D] Sumarização concluída. Texto resumido para 237 caracteres.
[Agente D DEBUG - Resumo Gerado]: Crispim Soares derretia-se todo interrogar da gente inquieta e curiosa, dos amigos attonitos, era para elle uma consagraço publica . o privado do alienista era elle, Crispim, o boticario e o riso discreto, porque elle no respondia nada .
[Agente B] Gerando resposta para: 'Quem foi o boticario Crispim Soares na trama?'
[Agente B] Resposta gerada: 'o privado do alienista'
[Agente C] Avaliando resposta: 'o privado do alienista'
[Agente C] Avaliação: Resposta satisfatória.
--- Fluxo finalizado para: 'Quem foi o boticario Crispim Soares na trama?' ---
Pergunta: Quem foi o boticario Crispim Soares na trama?
Contexto Original (Primeiros 250 caracteres do primeiro bloco): Crispim Soares derretia-se todo. Esse interrogar da gente inquieta e
curiosa, dos amigos attonitos, era para elle uma consagração publica.
Não havia duvidar; toda a povoação sabia emfim que o privado do
alienista era elle, Crispim, o boticario, o col...
Contexto Resumido: Crispim Soares derretia-se todo interrogar da gente inquieta e curiosa, dos amigos attonitos, era para elle uma consagraço publica . o privado do alienista era elle, Crispim, o boticario e o riso discreto, porque elle no respondia nada .
Resposta: o privado do alienista
Avaliação: Resposta satisfatória.
---------------------------------------------------
```
*(Nota: A qualidade e exatidão das respostas dependem da relevância do contexto recuperado, da qualidade do resumo e da capacidade do modelo de QA.)*

## 📜 Modelos Utilizados

-   **Embedding Model (Agente A):** `all-MiniLM-L6-v2` (de `sentence-transformers`)
-   **Summarization Model (Agente D):** `t5-small` (de `transformers`)
-   **Question Answering Model (Agente B):** `deepset/roberta-base-squad2` (de `transformers`)
