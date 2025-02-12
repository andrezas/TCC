import pyodbc

server = 'localhost,1433'
database = 'LICON_DEV'
username = 'sa'  
password = 'Oil2005iGIS'  
path = '/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.4.so.1.1'

conn_str = (
    f"DRIVER={path};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=yes;"
)

def execute_query(sql_query):
    try: 
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute(sql_query)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows
    except Exception as e:
        return f"Erro ao executar consulta: {e}"