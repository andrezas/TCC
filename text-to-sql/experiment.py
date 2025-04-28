from groq import Groq
import csv
import re
from repository import execute_query 
import os

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

modelos = ["llama3-8b-8192", "deepseek-r1-distill-llama-70b", "gemma2-9b-it", "mistral-saba-24b"] 
# "llama3-8b-8192", "deepseek-r1-distill-llama-70b", "gemma2-9b-it", "mixtral-8x7b-32768"

default_prompt = """
Você é um especialista em SQL Server e tem como tarefa a geração de consultas SQL sintaticamente corretas a partir 
de perguntas em linguagem natural. Você atua no contexto de um  sistema de transparência pública do Tribunal de 
Contas do Estado do Acre (TCE-AC). Com base na pergunta em linguagem natural e no contexto da base de dados 
fornecido, gere uma consulta SQL válida e executável no SQL Server.

Instruções:
1. Utilize a sintaxe correta do SQL Server.
2. Identifique as colunas relevantes do contexto fornecido.
3. Retorne apenas a consulta SQL, sem explicações, quebra de linhas, símbolos, aspas de modo que possibilite a execução 
da consulta diretamente no banco de dados.
"""

def get_context():
    with open('descriptionsTables/licitacao.txt', 'r', encoding='utf-8') as arquivo:
        return arquivo.read()

def read_questions_csv():
    perguntas = []
    with open('./questions/questions.csv', mode='r', encoding='utf-8') as arquivo_csv:
        reader = csv.reader(arquivo_csv)
        next(reader) 
        for row in reader:
            if len(row) >= 0:
                perguntas.append((row[0], row[1]))  
    return perguntas
    
def write_result_csv(id_pergunta, pergunta, resultado, modelo):
    caminho_pasta = "./results2/"
    os.makedirs(caminho_pasta, exist_ok=True)

    nome_arquivo = os.path.join(caminho_pasta, f"results_{modelo}.csv")

    if not os.path.exists(nome_arquivo):
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            writer.writerow(["ID", "Pergunta", "Consulta_SQL", "Modelo"])

    with open(nome_arquivo, mode='a', newline='', encoding='utf-8') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow([id_pergunta, pergunta, resultado, modelo])

def generate_sql (pergunta, modelo):
    contexto = get_context()

    chat_completion = client.chat.completions.create(
        messages=[ 
            {"role": "system", "content": f"{default_prompt}\n\nContexto da tabela:\n{contexto}"},
            {"role": "user", "content": f"Pergunta: {pergunta}"}
            ],
        model=modelo,
    )

    resultado = chat_completion.choices[0].message.content.strip()

    # resultado = re.sub(r"```(?:sql)?\s*(.*?)\s*```", r"\1", resultado, flags=re.DOTALL)
    # resultado = " ".join(resultado.split())

    if "deepseek" in modelo:
        resultado =  re.sub(r"<think>.*?</think>", "", resultado, flags=re.DOTALL).strip()

    return resultado

if __name__ == "__main__":
    perguntas = read_questions_csv()

    for modelo in modelos:
        print("*********", modelo, "*********\n")
        for id_pergunta, pergunta in perguntas:
            sql_query = generate_sql(pergunta, modelo)
            print(f"Query gerada:\n{sql_query}\n\n")
           