from sentence_transformers import SentenceTransformer
import hnswlib
import pandas as pd

# Carregamento de modelo, índice e blocos de texto
modelo = SentenceTransformer("all-MiniLM-L6-v2")
index = hnswlib.Index(space="cosine", dim=384) 
index.load_index("indice_alienista.bin")
df_blocos = pd.read_csv("blocos_alienista.csv")

def agenteA_buscar(pergunta: str, k_resultados: int = 1) -> str:
    """Recupera os k_resultados blocos de texto mais relevantes para a pergunta."""
    print(f"[Agente A] Buscando contexto para: '{pergunta}' (k={k_resultados})")
    emb_pergunta = modelo.encode([pergunta], convert_to_numpy=True)
    
    num_blocos_indexados = index.get_current_count()
    if num_blocos_indexados == 0:
        return "Nenhum bloco encontrado no índice. Reexecute o indexador."

    # Garante que k_resultados não seja maior que o número de itens no índice
    k_efetivo = min(k_resultados, num_blocos_indexados)
    if k_efetivo == 0 : # Caso especial se num_blocos_indexados for 0, mas já tratado acima.
        return "Nenhum bloco para buscar."

    idxs, _ = index.knn_query(emb_pergunta, k=k_efetivo)
    
    contextos_recuperados = [df_blocos.iloc[i].bloco for i in idxs[0]]
    
    # Concatena os blocos com um separador mais claro, se houver mais de um.
    contexto_final = "\n\n---\n\n".join(contextos_recuperados) 
    print(f"[Agente A] Contexto recuperado com {len(contexto_final)} caracteres de {len(contextos_recuperados)} bloco(s).")
    return contexto_final