from groq import Groq
import csv
import re
from repository import execute_query 
import os

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

modelos = ["deepseek-r1-distill-llama-70b"]

default_prompt = """
You are an assistant specialized in converting natural language questions into SQL queries,
focused on a public transparency system of the Court of Accounts of the State of Acre (TCE-AC).
Based on the natural language question and the provided database context, you must generate
executable SQL queries for SQL SERVER (Microsoft).

Instructions:

1. Use the correct SQL Server syntax.
2. Identify the relevant columns from the provided context.
3. Return only the SQL query, without explanations.
"""

def get_context():
    with open('descriptionsTables/licitacaoEnglish.txt', 'r', encoding='utf-8') as arquivo:
        return arquivo.read()

def read_questions_csv():
    perguntas = []
    with open('./questions/questionsEnglish.csv', mode='r', encoding='utf-8') as arquivo_csv:
        reader = csv.reader(arquivo_csv)
        next(reader) 
        for row in reader:
            if len(row) >= 0:
                perguntas.append((row[0], row[1]))  
    return perguntas
    
def write_result_csv(id_pergunta, pergunta, resultado, modelo):
    caminho_pasta = "./results/"
    os.makedirs(caminho_pasta, exist_ok=True)

    nome_arquivo = f"results_{modelo}.csv"

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