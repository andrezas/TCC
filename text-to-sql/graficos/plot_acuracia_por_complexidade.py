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
acertos = df_acertos.groupby(['Modelo', 'complexidade_pergunta']).size().unstack(fill_value=0)

# Conta total de perguntas feitas por Modelo e Complexidade
total_perguntas = df.groupby(['Modelo', 'complexidade_pergunta']).size().unstack(fill_value=0)

# Calcula a porcentagem de acertos por complexidade
percentual = (acertos / total_perguntas) * 100

# Garante a ordem Simples -> Média -> Complexa
percentual = percentual[['Simples', 'Média', 'Complexa']]

# Define cores personalizadas
custom_colors = ['#4F78B1', '#A6BDD7', '#C4A5CF']

# Gráfico de barras lado a lado
fig, ax = plt.subplots(figsize=(14, 8))

x = range(len(percentual))  # Posições dos modelos
largura_barra = 0.25  # Largura de cada barra

# Plota cada grupo de complexidade
for i, complexidade in enumerate(['Simples', 'Média', 'Complexa']):
    ax.bar(
        [pos + i * largura_barra for pos in x], 
        percentual[complexidade], 
        width=largura_barra, 
        label=complexidade, 
        color=custom_colors[i],
        edgecolor='black'
    )

# Ajusta o eixo X para mostrar os nomes dos modelos no centro dos 3 grupos de barras
ax.set_xticks([pos + largura_barra for pos in x])
ax.set_xticklabels(percentual.index, rotation=45, ha='right', fontsize=11)

# Adiciona os valores nas barras
for i, complexidade in enumerate(['Simples', 'Média', 'Complexa']):
    for j, valor in enumerate(percentual[complexidade]):
        if not pd.isna(valor):
            ax.text(
                j + i * largura_barra, valor + 1, f'{valor:.1f}%', 
                ha='center', va='bottom', fontsize=9
            )

# Layout
plt.title('Acurácia por Modelo e Complexidade', fontsize=16, pad=20)  # Ajustando o espaçamento do título
plt.xlabel('Modelo', fontsize=14)
plt.ylabel('Acurácia (%)', fontsize=14)
plt.yticks(fontsize=11)
plt.ylim(0, 100)  # agora o limite máximo é 100% certinho

plt.legend(title='Complexidade', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout(pad=3.0)  # Ajusta o layout com mais espaço entre o gráfico e os rótulos

# Salva o gráfico
plt.savefig("grafico_barras_lado_a_lado_por_complexidade.png", dpi=300)
plt.show()
