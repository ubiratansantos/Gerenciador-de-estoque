from flask import Flask, render_template
import pyodbc

app = Flask(__name__)

SERVER = 'Junior'
DATABASE = 'EstoqueDB'

CONNECTION_STRING = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes'


def get_produtos():
    produtos = []
    conn = None
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT ID, Nome, Descricao, Quantidade, Preco FROM Produtos")

        rows = cursor.fetchall()

        for row in rows:
            produtos.append({
                "ID": row.ID,
                "Nome": row.Nome,
                "Descricao": row.Descricao,
                "Quantidade": row.Quantidade,
                "Preco": row.Preco
            })

    except Exception as e:
        print(f"Erro ao conectar ou buscar dados: {e}")

    finally:
        if conn:
            conn.close()

    return produtos


@app.route('/')
def index():
    lista_produtos = get_produtos()
    return render_template('index.html', produtos=lista_produtos)


if __name__ == '__main__':
    app.run(debug=True)
