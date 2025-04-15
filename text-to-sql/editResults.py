import pandas as pd
from repository import execute_query 

df_reference = pd.read_csv("questions/responses_edit.csv")
df = pd.read_csv("results2/results_edit/deepseek.csv")

print(df.head())

# arquivos = ["results2/results_edit/results_deepseek.csv"]
# # "results2/results_edit/results_gemma.csv",
# #     "results2/results_edit/results_llama.csv",
# #     "results2/results_edit/results_mistral.csv",
# #     "results2/results_edit/results_phi4.csv"

# resultados = []

# for arquivo in arquivos:
#     df = pd.read_csv(arquivo)

#     for _, row in df.iterrows():
#         id_pergunta = row["ID_Pergunta"]
#         consulta_sql = row["Consulta_SQL"]

#         resultado_modelo = execute_query(consulta_sql)

#         if "Erro" in resultado_modelo:
#             resultado = "Erro"
#         else:
#             reference_row = df_reference[df_reference["id_pergunta"] == id_pergunta]
#             if not reference_row.empty:
#                 resultado_esperado = reference_row["resultado"].values[0]
#                 resultado = "Correto" if resultado_modelo == resultado_esperado else "Incorreto"
#             else:
#                 resultado = "Sem referência"

#         resultados.append({
#             "comparacao": resultado
#         })

# # Salva tudo em CSV se quiser
# pd.DataFrame(resultados).to_csv("comparacao_resultados.csv", index=False)
