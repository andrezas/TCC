from groq import Groq
import csv
import re
from repository import execute_query 

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
    
def write_result_csv(resultado, modelo):
    with open("./questions/results.csv", mode='a', newline='', encoding='utf-8') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow([1, pergunta, resultado, modelo])

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

    write_result_csv(resultado, modelo)

    return resultado

if __name__ == "__main__":
    sql_query = generate_sql(pergunta, modelos[0])
    print(f"Query gerada: {sql_query}")
    sql_executed = execute_query(sql_query)
    print(f"\n Resultado da consulta: {sql_executed}")