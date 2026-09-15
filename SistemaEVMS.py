import sqlite3

#=============================
#CONEXÃO COM BANCO(BANCO.PY)
#=============================
conexao = sqlite3.connect("mercadinho.db")
cursor = conexao.cursor()

# =========================
# CRIAÇÃO DA TABELA(BANCO.PY)
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_barras TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    estoque INTEGER NOT NULL
)
""")

conexao.commit()

# =========================
# LEITURA DO CÓDIGO DE BARRAS
# =========================

def ler_codigo_barras():
     return input("Passe o código de barras: ").strip()

# =========================
# MENU PRINCIPAL
# =========================

while True:

    print("\n========================")
    print("     Mercadinho Santana")
    print("1 - Cadastrar produtos")
    print("2 - Procurar produtos")
    print("3 - Sair")

    opcao = input("\nEscolha uma opção: ")

    # =========================
    # CADASTRAR PRODUTO
    # =========================

    if opcao == "1":

        print("\n--- Cadastrar Produto ---")

        codigo = ler_codigo_barras()
        nome = input("Nome do Produto: ")
        preco = float(input("Preço do Produto: ").replace(",", "."))
        estoque = int(input("Estoque: "))

        try:
           
           cursor.execute("""
               INSERT INTO produtos (codigo_barras, nome, preco, estoque)
               VALUES (?, ?, ?, ?)
            """, (codigo, nome, preco, estoque))

           conexao.commit()

           print("\nProduto cadastrado com sucesso!")

        except sqlite3.IntegrityError:
           print("\nErro: esse código de barras já está cadastrado.")

    # =========================
    # PESQUISAR PRODUTO
    # =========================

    elif opcao == "2":

        print("\n---- Pesquusar Produto ---")
        print("1 - Pesquisar por código de barras")
        print("2 - Pesquisar por nome")

        tipo_pesquisa = input("\nEscolha uma opção: ")
        
        if tipo_pesquisa =="1":
        
            codigo = ler_codigo_barras()
        
            cursor.execute("""
                SELECT * FROM produtos
                WHERE codigo_barras = ?
            """, (codigo,))
        
            produto = cursor.fetchone()
        
            if produto:
                print("\n---Produto encontrado!---")
                print("Código:", produto[1])
                print("Nome:", produto[2])
                print("Preço: R$", produto[3])
                print("Estoque:", produto[4])
        
            else:
                print("\nProduto não encontrado.")
        
        elif tipo_pesquisa =="2":
            
                nome = input("\nDigite o Nome do Produto: ")
            
                cursor.execute("""
                    SELECT * FROM produtos
                    WHERE nome LIKE ?
                """, (f"%{nome}%",))
            
                produtos = cursor.fetchall()
            
                if produtos:
                    print("\n---Produto encontrado!---")
        
        
                    for produto in produtos:
                        print("\nCódigo:", produto[1])
                        print("Nome:", produto[2])
                        print("Preço: R$", produto[3])
                        print("Estoque:", produto[4])
        
                else:
                        print("\nProduto não encontrado.")
        
        else:
                 print("\nOpção Inálida.")

    # =========================
    # SAIR
    # =========================

    elif opcao == "3":
        print("\nSistema Encerrado.")
        break

    else:

         print("\nOpçaõ Inválida.")

conexao.close()





