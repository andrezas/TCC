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

total_por_modelo = df.groupby('Modelo')['Resultado'].count()

erros_sintaxe = df[df['Resultado'] == 'Erro'].groupby('Modelo')['Resultado'].count()
consultas_incorretas = df[df['Resultado'] == 'Incorreto'].groupby('Modelo')['Resultado'].count()

percentual_erro = (erros_sintaxe / total_por_modelo * 100).fillna(0).sort_values(ascending=False)
percentual_incorreto = (consultas_incorretas / total_por_modelo * 100).fillna(0).sort_values(ascending=False)

# Tamanhos de fonte personalizados
title_fontsize = 18
label_fontsize = 14
tick_fontsize = 12

# Gráfico: Percentual de Erros de Sintaxe por Modelo
plt.figure(figsize=(9, 9))
ax1 = sns.barplot(x=percentual_erro.index, y=percentual_erro.values, color="#D9534F")
ax1.yaxis.grid(True, linestyle='--', alpha=0.7)  # Linhas de grade no eixo Y

# Adiciona os valores nas barras
for p in ax1.patches:
    height = p.get_height()
    ax1.text(p.get_x() + p.get_width() / 2, height + 1, f'{height:.1f}%', 
             ha='center', va='bottom', fontsize=10, color='black')

plt.ylabel('Percentual de Erros de Sintaxe (%)', fontsize=label_fontsize)
plt.xlabel('Modelo', fontsize=label_fontsize)
plt.title('Erros de Sintaxe por Modelo', fontsize=title_fontsize)
plt.xticks(rotation=30, ha='right', fontsize=tick_fontsize)
plt.yticks(fontsize=tick_fontsize)
plt.tight_layout()
plt.savefig("erros_sintaxe_por_modelo.png", dpi=300)
plt.show()

# Gráfico: Percentual de Consultas Incorretas por Modelo
plt.figure(figsize=(9, 9))
ax2 = sns.barplot(x=percentual_incorreto.index, y=percentual_incorreto.values, color="#F0AD4E")
ax2.yaxis.grid(True, linestyle='--', alpha=0.7)  # Linhas de grade no eixo Y

# Adiciona os valores nas barras
for p in ax2.patches:
    height = p.get_height()
    ax2.text(p.get_x() + p.get_width() / 2, height + 1, f'{height:.1f}%', 
             ha='center', va='bottom', fontsize=10, color='black')

plt.ylabel('Percentual de Consultas Incorretas (%)', fontsize=label_fontsize)
plt.xlabel('Modelo', fontsize=label_fontsize)
plt.title('Consultas Incorretas por Modelo', fontsize=title_fontsize)
plt.xticks(rotation=30, ha='right', fontsize=tick_fontsize)
plt.yticks(fontsize=tick_fontsize)
plt.tight_layout()
plt.savefig("consultas_incorretas_por_modelo.png", dpi=300)
plt.show()
