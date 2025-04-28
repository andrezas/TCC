import pandas as pd
import matplotlib.pyplot as plt

# Lê os arquivos
arquivos = [
    "../results/avaliacao/avalicao_deepseek-r1-distill-llama-70b.csv", 
    "../results/avaliacao/avalicao_gemma2-9b-it.csv", 
    "../results/avaliacao/avalicao_gpt-4.csv", 
    "../results/avaliacao/avalicao_llama3-8b-8192.csv", 
    "../results/avaliacao/avalicao_mistral-saba-24b.csv", 
    "../results/avaliacao/avalicao_phi4.csv"
]

df = pd.concat([pd.read_csv(arq) for arq in arquivos])

# Extrai apenas o nome do modelo
df['Modelo'] = df['Modelo'].str.extract(r'([a-zA-Z0-9\-]+)')

# Carrega as perguntas para pegar a complexidade
questions_df = pd.read_json("../questions/questions.json")
df = df.merge(questions_df[['id_pergunta', 'complexidade_pergunta']], left_on='ID_Pergunta', right_on='id_pergunta', how='left')

# Filtra apenas os acertos
df_acertos = df[df['Resultado'] == 'Correto']

# Conta acertos por Modelo e Complexidade
contagem = df_acertos.groupby(['Modelo', 'complexidade_pergunta']).size().unstack(fill_value=0)

# Conta total de perguntas feitas por modelo
total_perguntas = df.groupby('Modelo').size()

# Calcula a porcentagem de acertos
percentual = contagem.div(total_perguntas, axis=0) * 100

# Ordena as complexidades na ordem desejada
percentual = percentual[['Simples', 'Média', 'Complexa']]

# Define cores personalizadas
custom_colors = ['#4F78B1', '#A6BDD7', '#C4A5CF']

# Gráfico de barras empilhadas
fig, ax = plt.subplots(figsize=(12, 8))
percentual.plot(
    kind='bar', 
    stacked=True, 
    color=custom_colors, 
    edgecolor='black', 
    ax=ax
)

# Adiciona os valores de acurácia para cada barra
for p in ax.patches:
    height = p.get_height()
    width = p.get_width()
    x = p.get_x() + width / 2
    y = p.get_y() + height / 2
    ax.text(x, y, f'{height:.1f}%', ha='center', va='center', fontsize=10, color='black')

# Ajustes de layout
plt.title('Acurácia por Modelo e Complexidade', fontsize=16)
plt.xlabel('Modelo', fontsize=14)
plt.ylabel('Acurácia (%)', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=11)
plt.yticks(fontsize=11)
plt.ylim(0, 100)

# Adiciona a legenda ao lado do título
plt.legend(title='Complexidade', fontsize=12, loc='upper left', bbox_to_anchor=(1, 1), ncol=1)

plt.grid(axis='y', linestyle='--', alpha=0.7)

# Ajusta a distância do gráfico para não cobrir os nomes do eixo X
plt.tight_layout(rect=[0, 0, 0.9, 1])  # Ajusta o lado direito do gráfico para acomodar a legenda

plt.savefig("grafico_barras_empilhadas.png", dpi=300)
plt.show()
