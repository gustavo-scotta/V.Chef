import sqlite3

class ConexaoDB:
    def __init__(self, db_name="banco.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(
            db_name,
            check_same_thread=False
        )
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.__setup_tables()

    def __setup_tables(self):
        cur = self.connection.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS categoria_ingrediente (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(50) NOT NULL UNIQUE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ingrediente (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(50) NOT NULL UNIQUE,
                id_categoria INTEGER NOT NULL,
                unidade_medida VARCHAR(20) NOT NULL,
                codigo_icone VARCHAR(50),
                FOREIGN KEY (id_categoria) REFERENCES categoria_ingrediente(id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS despensa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                id_ingrediente INTEGER NOT NULL,
                quantidade REAL NOT NULL,
                FOREIGN KEY (id_usuario) REFERENCES usuario(id),
                FOREIGN KEY (id_ingrediente) REFERENCES ingrediente(id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS nao_gosta (
                id_usuario INTEGER NOT NULL,
                id_ingrediente INTEGER NOT NULL,
                PRIMARY KEY (id_usuario, id_ingrediente),
                FOREIGN KEY (id_usuario) REFERENCES usuario(id),
                FOREIGN KEY (id_ingrediente) REFERENCES ingrediente(id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS restricao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(50) NOT NULL UNIQUE,
                padrao BOOLEAN NOT NULL DEFAULT(FALSE)
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuario_restricao (
                id_usuario INTEGER NOT NULL,
                id_restricao INTEGER NOT NULL,
                status BOOLEAN NOT NULL DEFAULT(FALSE),
                PRIMARY KEY(id_usuario, id_restricao),
                FOREIGN KEY (id_usuario) REFERENCES usuario(id),
                FOREIGN KEY (id_restricao) REFERENCES restricao(id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS observacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                nome VARCHAR(200) NOT NULL,
                status BOOLEAN NOT NULL DEFAULT(FALSE),
                padrao BOOLEAN NOT NULL DEFAULT(FALSE),
                UNIQUE(id_usuario, nome),
                FOREIGN KEY (id_usuario) REFERENCES usuario(id)
            )
        """)

        self.connection.commit()

        # cria usuário padrão
        cur.execute("SELECT id FROM usuario WHERE id = 1")
        cur.execute(
            """
            INSERT OR IGNORE INTO usuario (id, nome)
            VALUES (?, ?)
            """,
            (1, "Fabio")
        )
        self.connection.commit()

    def get_conexao(self):
        return self.connection

# Instância global para ser importada pelos outros models
db = ConexaoDB()