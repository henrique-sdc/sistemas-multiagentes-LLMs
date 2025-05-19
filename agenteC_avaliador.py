def agenteC_avaliar(resposta: str) -> str:
    """Avalia a qualidade da resposta gerada."""
    print(f"[Agente C] Avaliando resposta: '{resposta}'")
    palavras = resposta.split()
    num_palavras = len(palavras)

    if not resposta or not resposta.strip():
        avaliacao = "Resposta vazia. Necessário refazer."
    elif any(p in resposta.lower() for p in ["não sei", "desconhecido", "irrelevante", "não foi possível", "erro ao gerar", "contexto para resposta estava vazio"]):
        avaliacao = "Resposta vaga ou indica falha."
    elif num_palavras < 2 : # Se for só uma palavra, geralmente é insatisfatório
        avaliacao = "Resposta muito curta. Reavalie."
    elif num_palavras < 4 and not all(p.istitle() or p.islower() for p in palavras): # Se curta e não for um nome próprio ou frase simples
        avaliacao = "Resposta curta e possivelmente incompleta. Reavalie."
    else:
        avaliacao = "Resposta satisfatória."
    
    print(f"[Agente C] Avaliação: {avaliacao}")
    return avaliacao