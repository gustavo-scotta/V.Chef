from app.models.conexao import db

class DespensaModel:
    @staticmethod
    def cadastra_ingrediente_na_despensa(nome_ingrediente, nome_categoria, unidade_medida, quantidade, codigo_icone=""):
        conn = db.get_conexao()
        cur = conn.cursor()

        # categoria
        cur.execute("SELECT id FROM categoria_ingrediente WHERE nome = ?", (nome_categoria,))
        categoria = cur.fetchone()
        if categoria:
            id_categoria = categoria[0]
        else:
            cur.execute("INSERT INTO categoria_ingrediente (nome) VALUES (?)", (nome_categoria,))
            id_categoria = cur.lastrowid

        # ingrediente
        cur.execute("SELECT id FROM ingrediente WHERE nome = ?", (nome_ingrediente,))
        ingrediente = cur.fetchone()
        if ingrediente:
            id_ingrediente = ingrediente[0]
        else:
            cur.execute(
                "INSERT INTO ingrediente (nome, id_categoria, unidade_medida, codigo_icone) VALUES (?, ?, ?, ?)",
                (nome_ingrediente, id_categoria, unidade_medida, codigo_icone)
            )
            id_ingrediente = cur.lastrowid

        # verifica se já existe na despensa
        cur.execute(
            "SELECT id, quantidade FROM despensa WHERE id_usuario = ? AND id_ingrediente = ?",
            (1, id_ingrediente)
        )
        item = cur.fetchone()

        if item:
            cur.execute("UPDATE despensa SET quantidade = quantidade + ? WHERE id = ?", (quantidade, item[0]))
        else:
            cur.execute(
                "INSERT INTO despensa (id_usuario, id_ingrediente, quantidade) VALUES (?, ?, ?)",
                (1, id_ingrediente, quantidade)
            )

        conn.commit()

    @staticmethod
    def obtem_ingredientes_despensa():
        conn = db.get_conexao()
        cur = conn.cursor()
        cur.execute("""
            SELECT d.id, i.nome, d.quantidade, ci.nome, i.unidade_medida, i.codigo_icone
            FROM despensa d
            LEFT JOIN ingrediente i ON i.id = d.id_ingrediente
            LEFT JOIN categoria_ingrediente ci ON ci.id = i.id_categoria
            WHERE d.id_usuario = 1
            ORDER BY i.nome
        """)
        return cur.fetchall()

    @staticmethod
    def aumentar_ingrediente_despensa(id_despensa):
        conn = db.get_conexao()
        cur = conn.cursor()
        cur.execute("UPDATE despensa SET quantidade = quantidade + 1 WHERE id = ?", (id_despensa,))
        conn.commit()

    @staticmethod
    def diminuir_ingrediente_despensa(id_despensa):
        conn = db.get_conexao()
        cur = conn.cursor()
        cur.execute("SELECT quantidade FROM despensa WHERE id = ?", (id_despensa,))
        item = cur.fetchone()

        if not item:
            return

        nova_quantidade = item[0] - 1
        if nova_quantidade <= 0:
            cur.execute("DELETE FROM despensa WHERE id = ?", (id_despensa,))
        else:
            cur.execute("UPDATE despensa SET quantidade = ? WHERE id = ?", (nova_quantidade, id_despensa))

        conn.commit()