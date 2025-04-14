from ollama import chat
import csv
import re
import os
from repository import execute_query

modelos = ["phi4"]  # adapte conforme os modelos disponíveis no seu Ollama

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
            if len(row) >= 2:
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

def generate_sql(pergunta, modelo):
    contexto = get_context()

    messages = [
        {"role": "system", "content": f"{default_prompt}\n\nContexto da tabela:\n{contexto}"},
        {"role": "user", "content": f"Pergunta: {pergunta}"}
    ]

    response = chat(model=modelo, messages=messages)
    resultado = response['message']['content'].strip()

    if "deepseek" in modelo:
        resultado = re.sub(r"<think>.*?</think>", "", resultado, flags=re.DOTALL).strip()

    return resultado

if __name__ == "__main__":
    perguntas = read_questions_csv()

    for modelo in modelos:
        print("*********", modelo, "*********\n")
        for id_pergunta, pergunta in perguntas:
            sql_query = generate_sql(pergunta, modelo)
            print(f"Query gerada:\n{sql_query}\n\n")
            sql_executed = execute_query(sql_query)
            print(f"\n Resultado da consulta: {sql_executed}")
            print("\n-------------------------------\n")            
            write_result_csv(id_pergunta, pergunta, sql_query, modelo)
