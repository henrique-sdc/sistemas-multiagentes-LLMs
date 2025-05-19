import re
import pandas as pd
from sentence_transformers import SentenceTransformer
import hnswlib

# Leitura do texto de entrada completo
with open("o_alienista.txt", encoding="utf-8") as f:
    texto_completo = f.read()

# Marcadores para isolar "O Alienista"
inicio_alienista_marker = "O ALIENISTA\n\n\nI\n\nDE COMO ITAGUAHY GANHOU UMA CASA DE ORATES"
fim_alienista_marker = "THEORIA DO MEDALHÃO\n\nDIALOGO"

start_index = texto_completo.find(inicio_alienista_marker)
end_index = texto_completo.find(fim_alienista_marker)

texto_obra = ""
if start_index != -1 and end_index != -1 and start_index < end_index:
    texto_obra = texto_completo[start_index : end_index]
    print(f"Texto de 'O Alienista' isolado. Comprimento: {len(texto_obra)} caracteres.")
else:
    print("ERRO: Não foi possível isolar o texto de 'O Alienista' corretamente. Verifique os marcadores.")
    print(f"Debug: start_index={start_index}, end_index={end_index}")
    # Fallback para o texto completo se o isolamento falhar, mas idealmente deve funcionar.
    texto_obra = texto_completo 
    print("AVISO: Utilizando o texto completo pois 'O Alienista' não foi isolado.")

if not texto_obra.strip():
    print("ERRO CRÍTICO: Texto isolado para 'O Alienista' está vazio. Saindo.")
    exit()

# Inicializa modelo de embeddings
modelo = SentenceTransformer("all-MiniLM-L6-v2")

# Parâmetros para divisão de blocos
MAX_CARACTERES_POR_BLOCO = 1500
MIN_CARACTERES_POR_BLOCO = 150 

blocos_finais = []

# Estratégia de divisão: Primeiro por capítulos, depois subdivide capítulos longos por parágrafos.
# Regex para capítulos de "O Alienista" (ex: I, II, ... seguido de título em nova linha)
capitulos_matches = list(re.finditer(r"(?mi)^\s*([IVXLCDM]+)\s*\n\n(.*?)(?=\n\s*[IVXLCDM]+\s*\n\n|\Z)", texto_obra, re.DOTALL))

if capitulos_matches:
    print(f"Encontrados {len(capitulos_matches)} capítulos em 'O Alienista'.")
    for match in capitulos_matches:
        conteudo_cap = match.group(2).strip()
        
        if len(conteudo_cap) > MAX_CARACTERES_POR_BLOCO:
            # Subdivide capítulos longos em blocos menores baseados em parágrafos
            paragrafos_do_capitulo = [p.strip() for p in re.split(r'\n\s*\n', conteudo_cap) if p.strip()]
            bloco_atual = ""
            for paragrafo in paragrafos_do_capitulo:
                if len(bloco_atual) + len(paragrafo) + 2 < MAX_CARACTERES_POR_BLOCO: # +2 para possível \n\n
                    bloco_atual += ("\n\n" + paragrafo if bloco_atual else paragrafo)
                else:
                    if bloco_atual and len(bloco_atual) > MIN_CARACTERES_POR_BLOCO:
                        blocos_finais.append(bloco_atual)
                    bloco_atual = paragrafo # Inicia novo bloco com o parágrafo atual
            if bloco_atual and len(bloco_atual) > MIN_CARACTERES_POR_BLOCO: # Adiciona último bloco pendente
                blocos_finais.append(bloco_atual)
        elif len(conteudo_cap) > MIN_CARACTERES_POR_BLOCO: # Adiciona capítulo se não for muito longo e nem muito curto
            blocos_finais.append(conteudo_cap)
else:
    # Fallback: Se a divisão por capítulos não funcionar, divide o texto inteiro em blocos de parágrafos agrupados
    print("Divisão por capítulos não encontrou resultados. Dividindo 'O Alienista' por parágrafos agrupados.")
    paragrafos_todos = [p.strip() for p in re.split(r'\n\s*\n', texto_obra) if p.strip()]
    bloco_atual = ""
    for paragrafo in paragrafos_todos:
        if len(bloco_atual) + len(paragrafo) + 2 < MAX_CARACTERES_POR_BLOCO:
            bloco_atual += ("\n\n" + paragrafo if bloco_atual else paragrafo)
        else:
            if bloco_atual and len(bloco_atual) > MIN_CARACTERES_POR_BLOCO:
                blocos_finais.append(bloco_atual)
            bloco_atual = paragrafo
    if bloco_atual and len(bloco_atual) > MIN_CARACTERES_POR_BLOCO:
        blocos_finais.append(bloco_atual)

# Filtro final para garantir que todos os blocos tenham um tamanho mínimo significativo
blocos_finais = [b for b in blocos_finais if len(b.strip()) > MIN_CARACTERES_POR_BLOCO]

if not blocos_finais:
    print("Nenhum bloco significativo encontrado em 'O Alienista' após tentativas de divisão. Verifique a lógica e os parâmetros.")
    exit()

print(f"Número final de blocos de 'O Alienista' para indexação: {len(blocos_finais)}")

# Gera os embeddings
embeddings = modelo.encode(blocos_finais, convert_to_numpy=True, show_progress_bar=True)

# Indexa os embeddings
index = hnswlib.Index(space="cosine", dim=embeddings.shape[1]) # dim=384 para all-MiniLM-L6-v2
index.init_index(max_elements=len(blocos_finais), ef_construction=200, M=16)
index.add_items(embeddings)

# Salva o índice e os blocos
index.save_index("indice_alienista.bin")
pd.DataFrame({"bloco": blocos_finais}).to_csv("blocos_alienista.csv", index=False)

print("Indexação de 'O Alienista' finalizada com sucesso.")