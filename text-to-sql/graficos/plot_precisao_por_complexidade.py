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

df = pd.concat([pd.read_csv(arq) for arq in arquivos])

df['Modelo'] = df['Modelo'].str.extract(r'([a-zA-Z0-9\-]+)')

questions_df = pd.read_json("../questions/questions.json")

df = df.merge(questions_df[['id_pergunta', 'complexidade_pergunta']], left_on='ID_Pergunta', right_on='id_pergunta', how='left')

acuracia_modelo_complexidade = df.groupby(['Modelo', 'complexidade_pergunta'])['Resultado'].value_counts(normalize=True).unstack().fillna(0)
acuracia_modelo_complexidade['Correto (%)'] = acuracia_modelo_complexidade.get('Correto', 0) * 100

acuracia_modelo_complexidade = acuracia_modelo_complexidade.reset_index()

for modelo in acuracia_modelo_complexidade['Modelo'].unique():
    dados_modelo = acuracia_modelo_complexidade[acuracia_modelo_complexidade['Modelo'] == modelo]
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=dados_modelo, x='complexidade_pergunta', y='Correto (%)', color="#4F78B1")
    
    plt.title(f'Precisão para o Modelo {modelo} por Complexidade das Perguntas')
    plt.ylabel('Precisão (%)')
    plt.xlabel('Complexidade da Pergunta')
    plt.tight_layout()
    
    plt.savefig(f"precisao_por_complexidade/precisao_{modelo}_por_complexidade.png", dpi=300)
    





