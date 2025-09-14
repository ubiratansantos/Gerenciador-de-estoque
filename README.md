# Gerenciador-de-estoque

Aplicação web simples para gerenciamento de estoque, com funcionalidades completas de CRUD (Create, Read, Update, Delete). Desenvolvido para fins acadêmicos para demonstrar conceitos de desenvolvimento full-stack.

✨ Tecnologias
- Backend: Python 3, Flask, pyodbc
- Frontend: HTML, CSS
- Banco de Dados: SQL Server

📋 Funcionalidades
- Cadastro de novos produtos. (CREATE)
- Visualização de todos os produtos do estoque. (READ)
- Edição das informações de produtos existentes. (UPDATE)
- Remoção de produtos. (DELETE)
- **EXTRA**: Busca simples por nome do produto.

🚀 Como Executar
1. Banco de Dados:

    1. Crie um banco de dados no seu SQL Server (ex: EstoqueDB).
    ```
    CREATE DATABASE EstoqueDB;
    ```
    2. Crie a tabela
    ```
    CREATE TABLE Produtos (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        Nome VARCHAR(100) NOT NULL,
        Descricao VARCHAR(255),
        Quantidade INT NOT NULL,
        Preco DECIMAL(10, 2) NOT NULL
        );
    ```


2. Ambiente Python:
```
# Instale as bibliotecas

pip install flask
pip install pyodbc
```
3. Configure a Conexão:

    - Abra o arquivo app.py.

    - Altere a CONNECTION_STRING com os dados do seu servidor SQL Server e do banco de dados criado.

4. Execute a Aplicação:
```
# Inicie o servidor Flask

python app.py
```