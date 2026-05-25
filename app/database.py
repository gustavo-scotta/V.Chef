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
                nome VARCHAR(200) NOT NULL,
                status BOOLEAN NOT NULL DEFAULT(FALSE),
                padrao BOOLEAN NOT NULL DEFAULT(FALSE),

                UNIQUE(id_usuario, nome),
                    
                FOREIGN KEY (id_usuario)
                REFERENCES usuario(id)
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

        self.cadastra_preferencias_padrao()

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


    ####################################
    ##########
    ########## ALTERADO
    ###################################

    def obtem_preferencias_ativas(self):
        cur = self.connection.cursor()

        preferencias = []

        cur.execute(
            """
            SELECT r.nome
            FROM restricao r
            INNER JOIN usuario_restricao ur
                ON ur.id_restricao = r.id
            WHERE ur.id_usuario = ?
            AND ur.status = 1
            ORDER BY r.nome
            """,
            (1,)
        )

        preferencias.extend([linha[0] for linha in cur.fetchall()])

        cur.execute(
            """
            SELECT nome
            FROM observacao
            WHERE id_usuario = ?
            AND status = 1
            ORDER BY nome
            """,
            (1,)
        )

        preferencias.extend([linha[0] for linha in cur.fetchall()])

        return preferencias

    # Aumenta a quantidade de um ingrediente na despensa.
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

    def lista_restricoes(self):
        cur = self.connection.cursor()

        cur.execute(
            """
            SELECT r.id, r.nome, ur.status, r.padrao
            FROM restricao r
            INNER JOIN usuario_restricao ur
                ON ur.id_restricao = r.id
            WHERE ur.id_usuario = ?
            ORDER BY r.id
            """,
            (1,)
        )

        return [
            {
                "id": linha[0],
                "nome": linha[1],
                "status": bool(linha[2]),
                "padrao": bool(linha[3])
            }
            for linha in cur.fetchall()
        ]

    def lista_observacoes(self):
        cur = self.connection.cursor()

        cur.execute(
            """
            SELECT id, nome, status, padrao
            FROM observacao
            WHERE id_usuario = ?
            ORDER BY id
            """,
            (1,)
        )

        return [
            {
                "id": linha[0],
                "nome": linha[1],
                "status": bool(linha[2]),
                "padrao": bool(linha[3])
            }
            for linha in cur.fetchall()
        ]

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

    def lista_nao_gosta(self):
        cur = self.connection.cursor()

        cur.execute(
            """
            SELECT i.id, i.nome
            FROM nao_gosta ng
            INNER JOIN ingrediente i
                ON i.id = ng.id_ingrediente
            WHERE ng.id_usuario = ?
            ORDER BY i.nome
            """,
            (1,)
        )

        return [
            {
                "id": linha[0],
                "nome": linha[1]
            }
            for linha in cur.fetchall()
        ]

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

    def cadastra_observacao(self, nome_observacao, status=True):
        cur = self.connection.cursor()

        if not nome_observacao:
            return None

        nome_observacao = nome_observacao.strip()

        if not nome_observacao:
            return None

        cur.execute(
            "SELECT id FROM observacao WHERE nome = ?",
            (nome_observacao,)
        )

        observacao = cur.fetchone()

        if observacao:
            id_observacao = observacao[0]

            cur.execute(
                """
                UPDATE observacao
                SET status = ?
                WHERE id = ?
                """,
                (status, id_observacao)
            )
        else:
            cur.execute(
                """
                INSERT INTO observacao (id_usuario, nome, status)
                VALUES (?, ?, ?)
                """,
                (1, nome_observacao, status)
            )

            id_observacao = cur.lastrowid

        self.connection.commit()

        return id_observacao
    
    def salvar_preferencias(self, nao_gosta, restricoes, observacoes):
        cur = self.connection.cursor()

        # Limpa alimentos que o usuário não gosta.
        cur.execute(
            """
            DELETE FROM nao_gosta
            WHERE id_usuario = ?
            """,
            (1,)
        )

        # Remove restrições personalizadas do usuário.
        cur.execute(
            """
            DELETE FROM usuario_restricao
            WHERE id_usuario = ?
            AND id_restricao IN (
                SELECT id FROM restricao WHERE padrao = 0
            )
            """,
            (1,)
        )

        # Desmarca todas as restrições padrão.
        cur.execute(
            """
            UPDATE usuario_restricao
            SET status = 0
            WHERE id_usuario = ?
            """,
            (1,)
        )

        # Remove observações personalizadas.
        cur.execute(
            """
            DELETE FROM observacao
            WHERE id_usuario = ?
            AND padrao = 0
            """,
            (1,)
        )

        # Desmarca todas as observações padrão.
        cur.execute(
            """
            UPDATE observacao
            SET status = 0
            WHERE id_usuario = ?
            """,
            (1,)
        )

        self.connection.commit()

        # Salva novamente alimentos "não gosto".
        for nome in nao_gosta:
            nome = nome.strip()

            if nome:
                self.cadastra_nao_gosta(nome)

        # Salva novamente restrições que estão na tela.
        for restricao in restricoes:
            nome = restricao.get("nome", "").strip()
            status = restricao.get("status", False)

            if nome:
                self.cadastra_restricao(nome, status)

        # Salva novamente observações que estão na tela.
        for observacao in observacoes:
            nome = observacao.get("nome", "").strip()
            status = observacao.get("status", False)

            if nome:
                self.cadastra_observacao(nome, status)

        self.connection.commit()

    def cadastra_preferencias_padrao(self):
        cur = self.connection.cursor()

        restricoes = [
            "Lactose",
            "Glúten",
            "Amendoim",
            "Frutos do mar"
        ]

        observacoes = [
            "Vegetariano",
            "Vegano",
            "Low carb",
            "Sem açúcar"
        ]

        for nome in restricoes:
            cur.execute(
                """
                INSERT OR IGNORE INTO restricao (nome, padrao)
                VALUES (?, ?)
                """,
                (nome, 1)
            )

            cur.execute(
                """
                UPDATE restricao
                SET padrao = 1
                WHERE nome = ?
                """,
                (nome,)
            )

            cur.execute(
                "SELECT id FROM restricao WHERE nome = ?",
                (nome,)
            )

            id_restricao = cur.fetchone()[0]

            cur.execute(
                """
                INSERT OR IGNORE INTO usuario_restricao
                (id_usuario, id_restricao, status)
                VALUES (?, ?, ?)
                """,
                (1, id_restricao, 0)
            )

        for nome in observacoes:
            cur.execute(
                """
                INSERT OR IGNORE INTO observacao
                (id_usuario, nome, status, padrao)
                VALUES (?, ?, ?, ?)
                """,
                (1, nome, 0, 1)
            )

            cur.execute(
                """
                UPDATE observacao
                SET padrao = 1
                WHERE id_usuario = ? AND nome = ?
                """,
                (1, nome)
            )

        self.connection.commit()
    
banco = DB()