from transformers import pipeline

# Carrega o pipeline de sumarização.
summarizer = None
try:
    print("[Agente D] Carregando modelo de sumarização: t5-small...")
    summarizer = pipeline("summarization", model="t5-small")
    print("[Agente D] Modelo de sumarização carregado com sucesso.")
except Exception as e:
    print(f"[Agente D] ERRO ao carregar modelo de sumarização t5-small: {e}")
    summarizer = None

def agenteD_resumir(texto_original: str, max_comprimento_resumo: int = 200, min_comprimento_resumo: int = 50) -> str:
    """
    Resume o texto original fornecido utilizando o modelo.
    Retorna o texto original se a sumarização falhar ou se o sumarizador não for inicializado.
    """
    if summarizer is None:
        print("[Agente D] Sumarizador não foi inicializado. Retornando texto original.")
        return texto_original
        
    if not texto_original or not texto_original.strip():
        print("[Agente D] Texto original para resumo está vazio. Retornando string vazia.")
        return ""

    print(f"[Agente D] Iniciando sumarização para texto de {len(texto_original)} caracteres.")
    
    try:
        # A pipeline de sumarização lida com truncamento se o texto de entrada
        # exceder o limite de tokens do modelo.
        resumo_gerado = summarizer(
            texto_original, 
            max_length=max_comprimento_resumo, 
            min_length=min_comprimento_resumo, 
            do_sample=False,
            truncation=True # Garante o truncamento se necessário
        )
        texto_resumido = resumo_gerado[0]['summary_text']
        print(f"[Agente D] Sumarização concluída. Texto resumido para {len(texto_resumido)} caracteres.")
        print(f"[Agente D DEBUG - Resumo Gerado]: {texto_resumido}")
        return texto_resumido
    except Exception as e:
        print(f"[Agente D] ERRO durante o processo de sumarização: {e}")
        print("[Agente D] Retornando texto original devido ao erro.")
        return texto_original