from transformers import pipeline

# Carrega o pipeline de Question Answering
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def agenteB_responder(pergunta: str, contexto_resumido: str) -> str:
    """Gera uma resposta para a pergunta com base no contexto resumido."""
    print(f"[Agente B] Gerando resposta para: '{pergunta}'")
    if not contexto_resumido or not contexto_resumido.strip():
        print("[Agente B] Contexto resumido está vazio. Não é possível gerar resposta.")
        return "Contexto para resposta estava vazio."

    try:
        resposta_qa = qa_pipeline(question=pergunta, context=contexto_resumido)
        print(f"[Agente B] Resposta gerada: '{resposta_qa['answer']}'")
        return resposta_qa["answer"]
    except Exception as e:
        print(f"[Agente B] Erro durante a geração da resposta: {e}")
        return f"Erro ao gerar resposta."