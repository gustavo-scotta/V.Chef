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


banco = DB()