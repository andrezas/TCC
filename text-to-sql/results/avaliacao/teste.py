import pandas as pd

df = pd.read_csv("avalicao_deepseek-r1-distill-llama-70b.csv")

acertos = (df["Resultado"] == "Incorreto").sum()

print(acertos)

# gemma-6, mistral-6, deepseek-2 - llama1, phi-1, 