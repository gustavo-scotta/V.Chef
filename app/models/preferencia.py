from app.models.conexao import db

class PreferenciasModel:
    @staticmethod
    def obtem_preferencias_ativas():
        conn = db.get_conexao()
        cur = conn.cursor()
        preferencias = []

        cur.execute("""
            SELECT r.nome FROM restricao r
            INNER JOIN usuario_restricao ur ON ur.id_restricao = r.id
            WHERE ur.id_usuario = ? AND ur.status = 1
            ORDER BY r.nome
        """, (1,))
        preferencias.extend([linha[0] for linha in cur.fetchall()])

        cur.execute("""
            SELECT nome FROM observacao
            WHERE id_usuario = ? AND status = 1
            ORDER BY nome
        """, (1,))
        preferencias.extend([linha[0] for linha in cur.fetchall()])

        return preferencias

    @staticmethod
    def lista_restricoes():
        conn = db.get_conexao()
        cur = conn.cursor()
        cur.execute("""
            SELECT r.id, r.nome, ur.status, r.padrao FROM restricao r
            INNER JOIN usuario_restricao ur ON ur.id_restricao = r.id
            WHERE ur.id_usuario = ?
            ORDER BY r.id
        """, (1,))
        return [{"id": l[0], "nome": l[1], "status": bool(l[2]), "padrao": bool(l[3])} for l in cur.fetchall()]

    @staticmethod
    def lista_observacoes():
        conn = db.get_conexao()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nome, status, padrao FROM observacao
            WHERE id_usuario = ?
            ORDER BY id
        """, (1,))
        return [{"id": l[0], "nome": l[1], "status": bool(l[2]), "padrao": bool(l[3])} for l in cur.fetchall()]

    @staticmethod
    def cadastra_nao_gosta(nome_ingrediente):
        conn = db.get_conexao()
        cur = conn.cursor()
        nome_ingrediente = nome_ingrediente.strip()
        if not nome_ingrediente:
            return None

        cur.execute("SELECT id FROM ingrediente WHERE nome = ?", (nome_ingrediente,))
        ingrediente = cur.fetchone()

        if ingrediente:
            id_ingrediente = ingrediente[0]
        else:
            cur.execute("INSERT OR IGNORE INTO categoria_ingrediente (nome) VALUES (?)", ("Outros",))
            cur.execute("SELECT id FROM categoria_ingrediente WHERE nome = ?", ("Outros",))
            id_categoria = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO ingrediente (nome, id_categoria, unidade_medida, codigo_icone) VALUES (?, ?, ?, ?)",
                (nome_ingrediente, id_categoria, "un", "")
            )
            id_ingrediente = cur.lastrowid

        cur.execute(
            "INSERT OR IGNORE INTO nao_gosta (id_usuario, id_ingrediente) VALUES (?, ?)",
            (1, id_ingrediente)
        )
        conn.commit()
        return id_ingrediente

    @staticmethod
    def lista_nao_gosta():
        conn = db.get_conexao()
        cur = conn.cursor()
        cur.execute("""
            SELECT i.id, i.nome FROM nao_gosta ng
            INNER JOIN ingrediente i ON i.id = ng.id_ingrediente
            WHERE ng.id_usuario = ?
            ORDER BY i.nome
        """, (1,))
        return [{"id": l[0], "nome": l[1]} for l in cur.fetchall()]

    @staticmethod
    def cadastra_restricao(nome_restricao, status=True):
        conn = db.get_conexao()
        cur = conn.cursor()
        nome_restricao = nome_restricao.strip()
        if not nome_restricao:
            return None

        cur.execute("SELECT id FROM restricao WHERE nome = ?", (nome_restricao,))
        restricao = cur.fetchone()

        if restricao:
            id_restricao = restricao[0]
        else:
            cur.execute("INSERT INTO restricao (nome) VALUES (?)", (nome_restricao,))
            id_restricao = cur.lastrowid

        cur.execute(
            "INSERT OR REPLACE INTO usuario_restricao (id_usuario, id_restricao, status) VALUES (?, ?, ?)",
            (1, id_restricao, status)
        )
        conn.commit()
        return id_restricao

    @staticmethod
    def cadastra_observacao(nome_observacao, status=True):
        conn = db.get_conexao()
        cur = conn.cursor()
        if not nome_observacao:
            return None
        nome_observacao = nome_observacao.strip()
        if not nome_observacao:
            return None

        cur.execute("SELECT id FROM observacao WHERE nome = ?", (nome_observacao,))
        observacao = cur.fetchone()

        if observacao:
            id_observacao = observacao[0]
            cur.execute("UPDATE observacao SET status = ? WHERE id = ?", (status, id_observacao))
        else:
            cur.execute("INSERT INTO observacao (id_usuario, nome, status) VALUES (?, ?, ?)", (1, nome_observacao, status))
            id_observacao = cur.lastrowid

        conn.commit()
        return id_observacao
    
    @staticmethod
    def salvar_preferencias(nao_gosta, restricoes, observacoes):
        conn = db.get_conexao()
        cur = conn.cursor()

        cur.execute("DELETE FROM nao_gosta WHERE id_usuario = ?", (1,))
        cur.execute("DELETE FROM usuario_restricao WHERE id_usuario = ? AND id_restricao IN (SELECT id FROM restricao WHERE padrao = 0)", (1,))
        cur.execute("UPDATE usuario_restricao SET status = 0 WHERE id_usuario = ?", (1,))
        cur.execute("DELETE FROM observacao WHERE id_usuario = ? AND padrao = 0", (1,))
        cur.execute("UPDATE observacao SET status = 0 WHERE id_usuario = ?", (1,))
        conn.commit()

        for nome in nao_gosta:
            nome = nome.strip()
            if nome:
                PreferenciasModel.cadastra_nao_gosta(nome)

        for restricao in restricoes:
            nome = restricao.get("nome", "").strip()
            status = restricao.get("status", False)
            if nome:
                PreferenciasModel.cadastra_restricao(nome, status)

        for observacao in observacoes:
            nome = observacao.get("nome", "").strip()
            status = observacao.get("status", False)
            if nome:
                PreferenciasModel.cadastra_observacao(nome, status)

        conn.commit()

    @staticmethod
    def cadastra_preferencias_padrao():
        conn = db.get_conexao()
        cur = conn.cursor()
        restricoes = ["Lactose", "Glúten", "Amendoim", "Frutos do mar"]
        observacoes = ["Vegetariano", "Vegano", "Low carb", "Sem açúcar"]

        for nome in restricoes:
            cur.execute("INSERT OR IGNORE INTO restricao (nome, padrao) VALUES (?, ?)", (nome, 1))
            cur.execute("UPDATE restricao SET padrao = 1 WHERE nome = ?", (nome,))
            cur.execute("SELECT id FROM restricao WHERE nome = ?", (nome,))
            id_restricao = cur.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO usuario_restricao (id_usuario, id_restricao, status) VALUES (?, ?, ?)", (1, id_restricao, 0))

        for nome in observacoes:
            cur.execute("INSERT OR IGNORE INTO observacao (id_usuario, nome, status, padrao) VALUES (?, ?, ?, ?)", (1, nome, 0, 1))
            cur.execute("UPDATE observacao SET padrao = 1 WHERE id_usuario = ? AND nome = ?", (1, nome))

        conn.commit()