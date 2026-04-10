import pandas as pd
import string

def generate_full_csv(data_list, output_file):
    # Definir a ordem das colunas
    base_cols = ["classificacao", "nome_fonte", "resolucao", "peso", "manual?"]
    
    # Gerar colunas dinâmicas: Ae, Ad... Ze, Zd, ae, ad... ze, zd
    char_cols = []
    for char in string.ascii_uppercase + string.ascii_lowercase:
        char_cols.append(f"{char}e")
        char_cols.append(f"{char}d")
    
    full_columns = base_cols + char_cols
    
    df = pd.DataFrame(data_list)
    
    # Reordenar colunas para garantir que o CSV seja idêntico à referência
    df = df.reindex(columns=full_columns)
    
    df.to_csv(output_file, index=False, sep=",", encoding="utf-8")