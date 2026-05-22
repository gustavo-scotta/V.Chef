import sqlite3


class DB:
    def __init__(self, db_name="banco.db"):
        self.db_name = db_name

        self.connection = sqlite3.connect(
            db_name,
            check_same_thread=False
        )

        self.connection.execute("PRAGMA foreign_keys = ON")

        self.__setupTables()

    def __setupTables(self):

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

                FOREIGN KEY (id_categoria)
                REFERENCES categoria_ingrediente(id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS despensa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                id_ingrediente INTEGER NOT NULL,
                quantidade REAL NOT NULL,

                FOREIGN KEY (id_usuario)
                REFERENCES usuario(id),

                FOREIGN KEY (id_ingrediente)
                REFERENCES ingrediente(id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS nao_gosta (
                id_usuario INTEGER NOT NULL,
                id_ingrediente INTEGER NOT NULL,

                PRIMARY KEY (id_usuario, id_ingrediente),
            
                FOREIGN KEY (id_usuario)
                REFERENCES usuario(id),

                FOREIGN KEY (id_ingrediente)
                REFERENCES ingrediente(id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS restricao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(50) NOT NULL UNIQUE
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuario_restricao (
                id_usuario INTEGER NOT NULL,
                id_restricao INTEGER NOT NULL,
                status BOOLEAN NOT NULL DEFAULT(FALSE),

                PRIMARY KEY(id_usuario, id_restricao),
            
                FOREIGN KEY (id_usuario)
                REFERENCES usuario(id),

                FOREIGN KEY (id_restricao)
                REFERENCES restricao(id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS observacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                nome VARCHAR(200) NOT NULL UNIQUE,
                status BOOLEAN NOT NULL DEFAULT(FALSE),

                FOREIGN KEY (id_usuario)
                REFERENCES usuario(id)
            )
        """)

        self.connection.commit()

        # cria usuário padrão
        cur.execute("SELECT id FROM usuario WHERE id = 1")

        if not cur.fetchone():
            cur.execute(
                "INSERT INTO usuario (nome) VALUES (?)",
                ("Fabio",)
            )

        self.connection.commit()

    def cadastra_ingrediente_na_despensa(
        self,
        nome_ingrediente,
        nome_categoria,
        unidade_medida,
        quantidade,
        codigo_icone=""
    ):

        cur = self.connection.cursor()

        # categoria
        cur.execute(
            "SELECT id FROM categoria_ingrediente WHERE nome = ?",
            (nome_categoria,)
        )

        categoria = cur.fetchone()

        if categoria:
            id_categoria = categoria[0]
        else:
            cur.execute(
                "INSERT INTO categoria_ingrediente (nome) VALUES (?)",
                (nome_categoria,)
            )

            id_categoria = cur.lastrowid

        # ingrediente
        cur.execute(
            "SELECT id FROM ingrediente WHERE nome = ?",
            (nome_ingrediente,)
        )

        ingrediente = cur.fetchone()

        if ingrediente:
            id_ingrediente = ingrediente[0]
        else:
            cur.execute(
                """
                INSERT INTO ingrediente
                (nome, id_categoria, unidade_medida, codigo_icone)
                VALUES (?, ?, ?, ?)
                """,
                (
                    nome_ingrediente,
                    id_categoria,
                    unidade_medida,
                    codigo_icone
                )
            )

            id_ingrediente = cur.lastrowid

        # verifica se já existe na despensa
        cur.execute(
            """
            SELECT id, quantidade
            FROM despensa
            WHERE id_usuario = ? AND id_ingrediente = ?
            """,
            (1, id_ingrediente)
        )

        item = cur.fetchone()

        if item:
            cur.execute(
                """
                UPDATE despensa
                SET quantidade = quantidade + ?
                WHERE id = ?
                """,
                (quantidade, item[0])
            )
        else:
            cur.execute(
                """
                INSERT INTO despensa
                (id_usuario, id_ingrediente, quantidade)
                VALUES (?, ?, ?)
                """,
                (1, id_ingrediente, quantidade)
            )

        self.connection.commit()

    def obtem_ingredientes_despensa(self):

        cur = self.connection.cursor()

        cur.execute("""
            SELECT
                d.id,
                i.nome,
                d.quantidade,
                ci.nome,
                i.unidade_medida,
                i.codigo_icone
            FROM despensa d

            LEFT JOIN ingrediente i
                ON i.id = d.id_ingrediente

            LEFT JOIN categoria_ingrediente ci
                ON ci.id = i.id_categoria

            WHERE d.id_usuario = 1

            ORDER BY i.nome
        """)

        return cur.fetchall()

    # ALTERADO: novo método para aumentar a quantidade de um ingrediente na despensa.
    def aumentar_ingrediente_despensa(self, id_despensa):

        cur = self.connection.cursor()

        cur.execute(
            """
            UPDATE despensa
            SET quantidade = quantidade + 1
            WHERE id = ?
            """,
            (id_despensa,)
        )

        self.connection.commit()

    # ALTERADO: novo método para diminuir a quantidade.
    # Se a quantidade chegar a zero, o item é excluído da despensa.
    def diminuir_ingrediente_despensa(self, id_despensa):

        cur = self.connection.cursor()

        cur.execute(
            "SELECT quantidade FROM despensa WHERE id = ?",
            (id_despensa,)
        )

        item = cur.fetchone()

        if not item:
            return

        nova_quantidade = item[0] - 1

        if nova_quantidade <= 0:
            cur.execute(
                "DELETE FROM despensa WHERE id = ?",
                (id_despensa,)
            )
        else:
            cur.execute(
                """
                UPDATE despensa
                SET quantidade = ?
                WHERE id = ?
                """,
                (nova_quantidade, id_despensa)
            )

        self.connection.commit()

    def cadastra_nao_gosta(self, nome_ingrediente):

        cur = self.connection.cursor()

        nome_ingrediente = nome_ingrediente.strip()

        if not nome_ingrediente:
            return None

        cur.execute(
            "SELECT id FROM ingrediente WHERE nome = ?",
            (nome_ingrediente,)
        )

        ingrediente = cur.fetchone()

        if ingrediente:
            id_ingrediente = ingrediente[0]

        else:
            # cria categoria "Outros" se não existir
            cur.execute(
                "INSERT OR IGNORE INTO categoria_ingrediente (nome) VALUES (?)",
                ("Outros",)
            )

            # busca id da categoria "Outros"
            cur.execute(
                "SELECT id FROM categoria_ingrediente WHERE nome = ?",
                ("Outros",)
            )

            id_categoria = cur.fetchone()[0]

            # cria ingrediente usando a categoria encontrada
            cur.execute(
                """
                INSERT INTO ingrediente
                (nome, id_categoria, unidade_medida, codigo_icone)
                VALUES (?, ?, ?, ?)
                """,
                (
                    nome_ingrediente,
                    id_categoria,
                    "un",
                    ""
                )
            )

            id_ingrediente = cur.lastrowid

        # vincula ingrediente ao usuário em nao_gosta
        cur.execute(
            """
            INSERT OR IGNORE INTO nao_gosta
            (id_usuario, id_ingrediente)
            VALUES (?, ?)
            """,
            (1, id_ingrediente)
        )


        self.connection.commit()

        return id_ingrediente
    
    def remove_nao_gosta(self, id_ingrediente):

        cur = self.connection.cursor()

        cur.execute(
            """
            DELETE FROM nao_gosta
            WHERE id_usuario = ? AND id_ingrediente = ?
            """,
            (1, id_ingrediente)
        )

        self.connection.commit()

    def cadastra_restricao(self, nome_restricao, status=True):

        cur = self.connection.cursor()

        nome_restricao = nome_restricao.strip()

        if not nome_restricao:
            return None

        cur.execute(
            "SELECT id FROM restricao WHERE nome = ?",
            (nome_restricao,)
        )

        restricao = cur.fetchone()

        if restricao:
            id_restricao = restricao[0]
        else:
            cur.execute(
                "INSERT INTO restricao (nome) VALUES (?)",
                (nome_restricao,)
            )

            id_restricao = cur.lastrowid

        cur.execute(
            """
            INSERT OR REPLACE INTO usuario_restricao
            (id_usuario, id_restricao, status)
            VALUES (?, ?, ?)
            """,
            (1, id_restricao, status)
        )

        self.connection.commit()

        return id_restricao
    
    
    def altera_status_restricao(self, id_restricao, status):

        cur = self.connection.cursor()

        status_db = 1 if status else 0

        cur.execute(
            """
            UPDATE usuario_restricao
            SET status = ?
            WHERE id_usuario = ? AND id_restricao = ?
            """,
            (status_db, 1, id_restricao)
        )

        self.connection.commit()

    def remove_restricao(self, id_restricao):

        cur = self.connection.cursor()

        cur.execute(
            """
            DELETE FROM usuario_restricao
            WHERE id_usuario = ? AND id_restricao = ?
            """,
            (1, id_restricao)
        )

        self.connection.commit()

banco = DB()