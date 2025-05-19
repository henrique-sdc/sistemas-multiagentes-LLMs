from agenteA_alienista import agenteA_buscar
from agenteD_resumidor import agenteD_resumir
from agenteB_alienista import agenteB_responder
from agenteC_avaliador import agenteC_avaliar

def executar_fluxo_completo(pergunta_usuario: str):
    print(f"\n--- Iniciando fluxo para a pergunta: '{pergunta_usuario}' ---")
    
    # Agente A: Busca o contexto original, tentando pegar 2 blocos
    contexto_original = agenteA_buscar(pergunta_usuario, k_resultados=2) 
    if "Nenhum bloco encontrado" in contexto_original or not contexto_original.strip():
        print("[Orquestrador] Agente A não retornou contexto válido. Encerrando fluxo.")
        return "Falha na recuperação de contexto", "", "", "Contexto não encontrado"

    # Agente D: Resume o contexto original
    contexto_resumido = agenteD_resumir(contexto_original)
    if not contexto_resumido.strip():
        print("[Orquestrador] Agente D não retornou resumo válido. Usando contexto original para Agente B.")
        contexto_para_b = contexto_original 
    else:
        contexto_para_b = contexto_resumido

    # Agente B: Gera a resposta
    resposta_gerada = agenteB_responder(pergunta_usuario, contexto_para_b)

    # Agente C: Avalia a resposta
    avaliacao_final = agenteC_avaliar(resposta_gerada)
    
    print(f"--- Fluxo finalizado para: '{pergunta_usuario}' ---")
    # Ajuste nos prints para serem mais concisos
    print(f"Pergunta: {pergunta_usuario}")
    print(f"Contexto Original (Primeiros 250 caracteres do primeiro bloco): {contexto_original.split('---')[0].strip()[:250]}...")
    print(f"Contexto Resumido: {contexto_resumido}")
    print(f"Resposta: {resposta_gerada}")
    print(f"Avaliação: {avaliacao_final}")
    print("---------------------------------------------------\n")
    return contexto_original, contexto_resumido, resposta_gerada, avaliacao_final

if __name__ == "__main__":
    perguntas_teste = [
        "Por que o personagem Simão Bacamarte decide internar a esposa no hospício?",
        "Qual era a principal ocupação de Simão Bacamarte?",
        "O que era a Casa Verde?",
        "Quem foi o boticario Crispim Soares na trama?",
        "Ao final da história, quem Simão Bacamarte concluiu ser o único louco e onde ele se internou?",
        "Onde Simão Bacamarte estudou antes de retornar ao Brasil?"
    ]

    print("AVISO: Certifique-se de ter executado 'python indexador_alienista.py' após qualquer alteração no indexador ou no texto base.\n")

    resultados_para_relatorio = []

    for pergunta in perguntas_teste:
        resultado_fluxo = executar_fluxo_completo(pergunta)
        if resultado_fluxo: # Garante que houve retorno
            contexto_original_completo, resumo, resposta, avaliacao = resultado_fluxo
            resultados_para_relatorio.append({
                "pergunta": pergunta,
                # "contexto_original_completo": contexto_original_completo, 
                "contexto_resumido": resumo,
                "resposta_gerada": resposta,
                "avaliacao": avaliacao
            })
    
    print("\n\n========= RESUMO DOS RESULTADOS =========")
    for i, res in enumerate(resultados_para_relatorio):
        print(f"\nEXECUÇÃO {i+1}:")
        print(f"Pergunta: {res['pergunta']}")
        # print(f"Contexto Original (Completo): {res['contexto_original_completo']}") 
        print(f"Contexto Resumido: {res['contexto_resumido']}")
        print(f"Resposta Gerada: {res['resposta_gerada']}")
        print(f"Avaliação do Agente C: {res['avaliacao']}")