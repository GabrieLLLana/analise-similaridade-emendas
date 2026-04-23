import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

# Tenta carregar as stop words em português, se não estiverem disponíveis, baixa e tenta novamente
try:
    stop_words_pt = stopwords.words('portuguese') # Carrega as stop words em português  
except LookupError:
    import nltk
    nltk.download('stopwords')
    stop_words_pt = stopwords.words('portuguese') # Tenta carregar novamente após baixar as stop words      
    
      
def agrupar_emendas(caminho_entrada='emendas_mpv_1348_26.xlsx', caminho_saida='emendas_agrupadas_resultado.xlsx', limite_similaridade=0.70):
    """
    Lê um quadro de emendas parlamentares, analisa o conteúdo textual
    usando TF-IDF e Similaridade de Cosseno, e agrupa as emendas similares.
    
    Parâmetros:
    - caminho_entrada (str): Caminho para o arquivo Excel original.
    - caminho_saida (str): Caminho onde o Excel com os resultados será salvo.
    - limite_similaridade (float): Nota de corte (0.0 a 1.0) para considerar duas emendas do mesmo grupo.
    """
    
    # ---------------------------------------------------------
    # PASSO 1: Leitura do Arquivo Excel
    # ---------------------------------------------------------
    print("1. Lendo o arquivo Excel...")
    df = pd.read_excel(caminho_entrada)
    
    df.columns = df.columns.str.strip() # Remove espaços em branco do início e fim dos nomes das colunas
    
    textos_emendas = df['Inteiro teor'].fillna('') # Evita que células vazias quebrem a vetorização
    numeros_emendas = df['Emenda'].tolist()

    # ---------------------------------------------------------
    # PASSO 2: Contagem de Palavras e Pesos (TF-IDF)
    # ---------------------------------------------------------
    print("2. Analisando o vocabulário das emendas...")     
    
    # Criação do vetorizador: token_pattern garante que apenas palavras (letras) sejam extraídas, ignorando pontuações e números.
    vetorizador = TfidfVectorizer(stop_words=stop_words_pt, token_pattern=r'(?u)\b[a-zA-Zà-úÀ-Ú]{2,}\b') 
    matriz_tfidf = vetorizador.fit_transform(textos_emendas)

    # ---------------------------------------------------------
    # PASSO 3: Criar a Matriz de Similaridade
    # ---------------------------------------------------------
    print("3. Calculando a similaridade entre todas as emendas...")
    # Retorna uma matriz simétrica relacionando cada texto com todos os outros
    matriz_similaridade = cosine_similarity(matriz_tfidf)

    # ---------------------------------------------------------
    # PASSO 4: Agrupar as emendas similares
    # ---------------------------------------------------------
    print("4. Separando em grupos...")
    
    emendas_processadas = set() # Estrutura de busca rápida (O(1)) para emendas já agrupadas
    grupos = [] 
    emendas_unicas = [] 

    # Lógica de agrupamento "Greedy" (Guloso): Agrupa com base na primeira emenda que bater o limite
    for i in range(len(numeros_emendas)):
        if i in emendas_processadas:
            continue 
            
        grupo_atual = [numeros_emendas[i]]
        emendas_processadas.add(i)
        
        # Compara apenas com as emendas seguintes (j > i) para evitar cálculos duplicados
        for j in range(i + 1, len(numeros_emendas)):
            if j not in emendas_processadas:
                if matriz_similaridade[i][j] >= limite_similaridade:
                    grupo_atual.append(numeros_emendas[j])
                    emendas_processadas.add(j)
        
        # Validação: Se achou pares, salva como grupo; se não, salva como única
        if len(grupo_atual) > 1:
            grupos.append(grupo_atual)
        else:
            emendas_unicas.append(grupo_atual[0])

    # ---------------------------------------------------------
    # PASSO 5: Mostrar os Resultados no Console
    # ---------------------------------------------------------
    print("\n=== RESULTADOS DA ANÁLISE ===")
    print(f"Total de emendas analisadas: {len(numeros_emendas)}")
    print(f"\nGrupos de Emendas Similares (Acima de {limite_similaridade*100}% de igualdade):")
    
    for idx, grupo in enumerate(grupos):
        print(f"Grupo {idx + 1}: Emendas {grupo}")
        
    print(f"\nEmendas Únicas (Sem similaridade forte):")
    print(emendas_unicas)

    # ---------------------------------------------------------
    # PASSO 6: Salvar Resultados em um Novo Excel
    # ---------------------------------------------------------
    print("\n5. Gerando nova planilha com os resultados...")
    
    mapa_grupos = {}
    
    for idx, grupo in enumerate(grupos):
        nome_grupo = f"Grupo {idx + 1}"
        for numero_emenda in grupo:
            mapa_grupos[numero_emenda] = nome_grupo
            
    for numero_emenda in emendas_unicas:
        mapa_grupos[numero_emenda] = "Única"

    # Mapeia a coluna 'Emenda' original de volta para o nome do grupo correspondente
    df['Classificação de Similaridade'] = df['Emenda'].map(mapa_grupos)
    
    df.to_excel(caminho_saida, index=False) 
    
    print(f"Pronto! O arquivo '{caminho_saida}' foi criado com sucesso.")

# Bloco de execução principal
if __name__ == "__main__":
    agrupar_emendas()