import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

arquivos = [
    "../results/avaliacao/avalicao_deepseek-r1-distill-llama-70b.csv", 
    "../results/avaliacao/avalicao_gemma2-9b-it.csv", 
    "../results/avaliacao/avalicao_gpt-4.csv", 
    "../results/avaliacao/avalicao_llama3-8b-8192.csv", 
    "../results/avaliacao/avalicao_mistral-saba-24b.csv", 
    "../results/avaliacao/avalicao_phi4.csv"
]

# Concatena os dados
df = pd.concat([pd.read_csv(arq) for arq in arquivos])

# Extrai apenas o nome do modelo
df['Modelo'] = df['Modelo'].str.extract(r'([a-zA-Z0-9\-]+)')

# Carrega perguntas
questions_df = pd.read_json("../questions/questions.json")

# Faz o merge
df = df.merge(questions_df[['id_pergunta', 'complexidade_pergunta']], left_on='ID_Pergunta', right_on='id_pergunta', how='left')

# Agrupa e calcula a precisão
acuracia_modelo_complexidade = df.groupby(['Modelo', 'complexidade_pergunta'])['Resultado']\
    .value_counts(normalize=True).unstack().fillna(0)

acuracia_modelo_complexidade['Correto (%)'] = acuracia_modelo_complexidade.get('Correto', 0) * 100
acuracia_modelo_complexidade = acuracia_modelo_complexidade.reset_index()

title_fontsize = 14
label_fontsize = 12
tick_fontsize = 10

# Geração dos gráficos individuais por modelo
modelos = acuracia_modelo_complexidade['Modelo'].unique()

for modelo in modelos:
    dados_modelo = acuracia_modelo_complexidade[acuracia_modelo_complexidade['Modelo'] == modelo]

    plt.figure(figsize=(9, 9))
    sns.barplot(data=dados_modelo, x='complexidade_pergunta', y='Correto (%)', color="#4F78B1")

    plt.title(f'Acurácia por Complexidade - {modelo}', fontsize=title_fontsize)
    plt.xlabel('Complexidade', fontsize=label_fontsize)
    plt.ylabel('Acurácia (%)', fontsize=label_fontsize)
    plt.xticks(fontsize=tick_fontsize)
    plt.yticks(fontsize=tick_fontsize)
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(f"acuracia_{modelo}_por_complexidade.png", dpi=300)
    plt.close()
