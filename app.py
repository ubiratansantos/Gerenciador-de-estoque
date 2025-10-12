# Adicione 'request', 'redirect' e 'url_for' na linha de importação
from flask import Flask, render_template, request, redirect, url_for
import pyodbc

# Inicializa a aplicação Flask
app = Flask(__name__)

# --- Configuração da Conexão com o Banco de Dados SQL Server ---
SERVER = 'Junior'
DATABASE = 'EstoqueDB'
CONNECTION_STRING = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes'

# Função para obter os produtos do banco de dados (da Etapa 1)
def get_produtos():
    produtos = []
    conn = None
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Nome, Descricao, Quantidade, Preco FROM Produtos")
        rows = cursor.fetchall()
        for row in rows:
            produtos.append({
                "ID": row.ID, "Nome": row.Nome, "Descricao": row.Descricao,
                "Quantidade": row.Quantidade, "Preco": row.Preco
            })
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
    finally:
        if conn:
            conn.close()
    return produtos

# --- Definição das Rotas ---

# Rota principal que exibe a lista de produtos (da Etapa 1)
@app.route('/')
def index():
    lista_produtos = get_produtos()
    return render_template('index.html', produtos=lista_produtos)

# --- NOVO CÓDIGO DA ETAPA 2 ---

# Rota para adicionar novos produtos
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    # Se o método for POST, significa que o formulário foi enviado
    if request.method == 'POST':
        # Pega os dados do formulário
        nome = request.form['nome']
        descricao = request.form['descricao']
        quantidade = request.form['quantidade']
        preco = request.form['preco']

        conn = None
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            # Query SQL para inserir o novo produto
            sql_query = """
                INSERT INTO Produtos (Nome, Descricao, Quantidade, Preco)
                VALUES (?, ?, ?, ?)
            """
            # Executa a query com os dados do formulário
            cursor.execute(sql_query, nome, descricao, quantidade, preco)
            conn.commit() # Confirma a transação
        except Exception as e:
            print(f"Erro ao inserir produto: {e}")
        finally:
            if conn:
                conn.close()
        
        # Redireciona o usuário de volta para a página inicial
        return redirect(url_for('index'))

    # Se o método for GET, apenas exibe a página com o formulário
    return render_template('adicionar.html')


# Permite que a aplicação seja executada diretamente
if __name__ == '__main__':
    app.run(debug=True)