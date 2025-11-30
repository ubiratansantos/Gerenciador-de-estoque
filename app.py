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
        cursor.execute(
            "SELECT ID, Nome, Descricao, Quantidade, Preco FROM Produtos")
        rows = cursor.fetchall()

        for row in rows:
            # --- Lógica de Verificação de Estoque Baixo ---
            # Se a quantidade for menor que 5, define alerta como True
            tem_estoque_baixo = row.Quantidade < 5

            produtos.append({
                "ID": row.ID,
                "Nome": row.Nome,
                "Descricao": row.Descricao,
                "Quantidade": row.Quantidade,
                "Preco": row.Preco,
                "Alerta": tem_estoque_baixo  # Adicionamos essa nova informação ao dicionário
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
            conn.commit()  # Confirma a transação
        except Exception as e:
            print(f"Erro ao inserir produto: {e}")
        finally:
            if conn:
                conn.close()

        # Redireciona o usuário de volta para a página inicial
        return redirect(url_for('index'))

    # Se o método for GET, apenas exibe a página com o formulário
    return render_template('adicionar.html')

# (O código anterior do Flask, pyodbc, get_produtos(), index() e adicionar() permanece aqui em cima)
# ...

# --- NOVO CÓDIGO DA ETAPA 3 ---

# Rota para REMOVER um produto


@app.route('/remover/<int:id>')
def remover(id):
    conn = None
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        # Query SQL para deletar o produto com o ID_Produto_Ativo
        sql_query = "DELETE FROM Produtos WHERE ID = ?"
        cursor.execute(sql_query, id)
        conn.commit()
    except Exception as e:
        print(f"Erro ao remover produto: {e}")
    finally:
        if conn:
            conn.close()

    # Redireciona de volta para a página inicial
    return redirect(url_for('index'))

# Rota para carregar a página de EDIÇÃO (Método GET)


@app.route('/editar/<int:id>')
def editar(id):
    produto = None
    conn = None
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        # Busca o produto específico pelo ID
        sql_query = "SELECT ID, Nome, Descricao, Quantidade, Preco FROM Produtos WHERE ID = ?"
        cursor.execute(sql_query, id)
        row = cursor.fetchone()  # Pega apenas um resultado
        if row:
            # Converte o resultado (tuple) em um dicionário
            produto = {
                "ID": row.ID, "Nome": row.Nome, "Descricao": row.Descricao,
                "Quantidade": row.Quantidade, "Preco": row.Preco
            }
    except Exception as e:
        print(f"Erro ao buscar produto para edição: {e}")
    finally:
        if conn:
            conn.close()

    # Se o produto foi encontrado, renderiza a página 'editar.html' com os dados dele
    if produto:
        return render_template('editar.html', produto=produto)
    else:
        # Se não encontrou o produto, volta para a home
        return redirect(url_for('index'))

# Rota para processar a ATUALIZAÇÃO de um produto (Método POST)


@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    if request.method == 'POST':
        # Pega os dados atualizados do formulário
        nome = request.form['nome']
        descricao = request.form['descricao']
        quantidade = request.form['quantidade']
        preco = request.form['preco']

        conn = None
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            # Query SQL para atualizar o produto
            sql_query = """
                UPDATE Produtos
                SET Nome = ?, Descricao = ?, Quantidade = ?, Preco = ?
                WHERE ID = ?
            """
            cursor.execute(sql_query, nome, descricao, quantidade, preco, id)
            conn.commit()
        except Exception as e:
            print(f"Erro ao atualizar produto: {e}")
        finally:
            if conn:
                conn.close()

        # Redireciona de volta para a página inicial
        return redirect(url_for('index'))

# --- FIM DO CÓDIGO DA ETAPA 3 ---


# Permite que a aplicação seja executada diretamente
if __name__ == '__main__':
    app.run(debug=True)
