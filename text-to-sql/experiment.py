from groq import Groq
import csv
import re
from repository import execute_query 
import os

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

modelos = ["llama3-8b-8192", "deepseek-r1-distill-llama-70b"]
pergunta = "Qual o número da licitação com maior valor do ano de 2024?"

default_prompt = """
Você é um assistente especializado em converter perguntas em linguagem natural para consultas SQL, 
focado em um sistema de transparência pública do Tribunal de Contas do Estado do Acre (TCE-AC).
Com base na pergunta em linguagem natural e o contexto da base de dados fornecido, você deve gerar 
consultas SQL executáveis para SQL SERVER (Microsoft).

Instruções:
1. Utilize a sintaxe correta do SQL Server.
2. Identifique as colunas relevantes do contexto fornecido.
3. Retorne apenas a consulta SQL, sem explicações.
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
    caminho_pasta = "./results/"
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

    resultado = re.sub(r"```(?:sql)?\s*(.*?)\s*```", r"\1", resultado, flags=re.DOTALL)
    resultado = " ".join(resultado.split())

    return resultado

if __name__ == "__main__":
    perguntas = read_questions_csv()

    for id_pergunta, pergunta in perguntas:
        for modelo in modelos:
            sql_query = generate_sql(pergunta, modelo)
            print(f"Query gerada: {sql_query}")
            sql_executed = execute_query(sql_query)
            print(f"\n Resultado da consulta: {sql_executed}")
            write_result_csv(id_pergunta, pergunta, sql_query, modelo)