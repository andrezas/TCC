import pandas as pd
from repository import execute_query 

df_reference = pd.read_json("questions/responses.json")

arquivos = ["results2/results_edit/deepseek.json", 
            "results2/results_edit/gemma.json", 
            "results2/results_edit/llama.json", 
            "results2/results_edit/mistral.json", 
            "results2/results_edit/phi4.json", 
            "results2/results_edit/gpt4.json"]

resultados = []

for arquivo in arquivos:
    df = pd.read_json(arquivo)
    for _, row in df.iterrows():
        id_pergunta = row["ID"]
        consulta_sql = row["Consulta_SQL"]
        modelo = row["Modelo"]

        resultado_modelo = execute_query(consulta_sql)

        if "Erro" in resultado_modelo:
            resultado = "Erro"
        else:
            query = df_reference.loc[df_reference["id_pergunta"] == id_pergunta, "sql_reference"]
            if not query.empty:
                query = query.values[0]
                resultado_esperado = execute_query(query)
                print("Id pergunta: ", id_pergunta)
                print("Esperado: ", resultado_esperado)
                print("Modelo: ", resultado_modelo)
                print("--------------------------\n")
                resultado = "Correto" if resultado_modelo == resultado_esperado else "Incorreto"
            else:
                resultado = "Sem referência"
            
        resultados.append({
            "ID_Pergunta": id_pergunta,
            "Consulta_SQL": consulta_sql,
            "Resultado": resultado,
            "Modelo": modelo
        })

    pd.DataFrame(resultados).to_csv(f"results2/avaliacao/avalicao_{modelo}.csv", index=False)


