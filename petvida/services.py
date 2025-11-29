from typing import Optional, Dict, Any

import psycopg2
from psycopg2.extensions import connection as PgConnection

from config import DB_CONFIG, gerar_hash_senha, verificar_senha
from utils import (
    ler_numero,
    ler_letras,
    ler_senha_mascarada,
    senha_forte,
)

def criar_conexao() -> Optional[PgConnection]:
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = False
        return conn
    except Exception as e:
        print("Erro ao conectar ao banco:", e)
        return None


def criar_tabelas(conn: PgConnection) -> None:
    try:
        with conn.cursor() as c:

            c.execute("SET search_path TO petvida;")

            c.execute("""
            CREATE TABLE IF NOT EXISTS dono (
                id_dono   SERIAL PRIMARY KEY,
                nome      VARCHAR(120) NOT NULL,
                cpf       VARCHAR(20)  NOT NULL UNIQUE,
                email     VARCHAR(120),
                endereco  VARCHAR(200) NOT NULL,
                telefone  VARCHAR(30)  NOT NULL,
                observacao TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario         SERIAL PRIMARY KEY,
                username           VARCHAR(50) UNIQUE NOT NULL,
                senha_cripto       VARCHAR(255) NOT NULL,
                tipo               VARCHAR(20)  NOT NULL,
                id_dono            INT REFERENCES dono(id_dono),
                tentativas_erradas INT DEFAULT 0,
                bloqueado          BOOLEAN DEFAULT FALSE,
                criado_em          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS animal (
                id_animal SERIAL PRIMARY KEY,
                nome      VARCHAR(120) NOT NULL,
                especie   VARCHAR(60)  NOT NULL,
                raca      VARCHAR(80)  NOT NULL,
                idade     INT          NOT NULL,
                id_dono   INT          NOT NULL REFERENCES dono(id_dono) ON DELETE CASCADE,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS consulta (
                id_consulta  SERIAL PRIMARY KEY,
                data         DATE         NOT NULL,
                horario      TIME         NOT NULL,
                motivo       VARCHAR(200) NOT NULL,
                diagnostico  VARCHAR(400),
                status       VARCHAR(20)  DEFAULT 'agendada',
                prioridade   VARCHAR(20)  DEFAULT 'normal',
                id_animal    INT          NOT NULL REFERENCES animal(id_animal) ON DELETE CASCADE,
                id_vet       INT REFERENCES usuario(id_usuario),
                criado_em    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS cirurgia (
                id_cirurgia   SERIAL PRIMARY KEY,
                data          DATE         NOT NULL,
                tipo_cirurgia VARCHAR(120) NOT NULL,
                observacoes   VARCHAR(500),
                status        VARCHAR(20) DEFAULT 'agendada',
                id_animal     INT NOT NULL REFERENCES animal(id_animal) ON DELETE CASCADE,
                criado_em     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            c.execute("""
            ALTER TABLE consulta 
                ADD COLUMN IF NOT EXISTS prioridade VARCHAR(20) DEFAULT 'normal';

            ALTER TABLE dono 
                ADD COLUMN IF NOT EXISTS observacao TEXT;

            ALTER TABLE usuario 
                ADD COLUMN IF NOT EXISTS tentativas_erradas INT DEFAULT 0;

            ALTER TABLE usuario 
                ADD COLUMN IF NOT EXISTS bloqueado BOOLEAN DEFAULT FALSE;
            """)

            c.execute("""
            CREATE INDEX IF NOT EXISTS idx_dono_cpf ON dono (cpf);
            CREATE INDEX IF NOT EXISTS idx_consulta_data ON consulta (data);
            CREATE INDEX IF NOT EXISTS idx_animal_dono ON animal (id_dono);
            CREATE INDEX IF NOT EXISTS idx_usuario_username ON usuario (username);
            """)

        conn.commit()
        print("✅ Tabelas criadas/validadas com sucesso no schema petvida.")

    except Exception as e:
        conn.rollback()
        print("Erro ao criar/alterar tabelas:", e)

def limpar_tabelas(conn: PgConnection) -> None:
    sql_drop = """
    DROP TABLE IF EXISTS cirurgia CASCADE;
    DROP TABLE IF EXISTS consulta CASCADE;
    DROP TABLE IF EXISTS animal   CASCADE;
    DROP TABLE IF EXISTS usuario  CASCADE;
    DROP TABLE IF EXISTS dono     CASCADE;
    """
    conf = input(
        "ATENÇÃO: isso vai APAGAR TODAS as tabelas e dados! Confirmar? (s/n): "
    ).lower()
    if conf != "s":
        print("Operação cancelada.")
        return

    try:
        with conn.cursor() as c:
            c.execute(sql_drop)
        conn.commit()
        print("Todas as tabelas principais foram apagadas com sucesso.")
    except Exception as e:
        conn.rollback()
        print("Erro ao limpar tabelas:", e)


def garantir_admin(conn: PgConnection) -> None:
    try:
        with conn.cursor() as c:
            c.execute("SELECT 1 FROM usuario WHERE tipo='admin'")
            if c.fetchone():
                return  # já existe admin

        print("\n⚠ PRIMEIRA EXECUÇÃO ⚠")
        print("Nenhum administrador encontrado.")
        print("Crie agora a senha do ADMIN.")

        while True:
            senha = ler_senha_mascarada("Nova senha do admin: ")

            if not senha_forte(senha):
                print("Senha fraca. Use pelo menos 8 caracteres, com letras e números.")
                continue

            confirmar = ler_senha_mascarada("Confirme a senha: ")
            if senha != confirmar:
                print("As senhas não conferem. Tente novamente.")
                continue

            break

        senha_hash = gerar_hash_senha(senha)

        with conn.cursor() as c:
            c.execute(
                """
                INSERT INTO usuario (username, senha_cripto, tipo)
                VALUES (%s, %s, %s)
                """,
                ("admin", senha_hash, "admin"),
            )
        conn.commit()

        print("\n✅ ADMIN CRIADO COM SUCESSO")
        print("Usuário: admin")
        print("Senha: a que você acabou de definir")
    except Exception as e:
        conn.rollback()
        print("Erro ao criar admin:", e)

# CADASTROS
def cadastrar_usuario(conn: PgConnection) -> None:
    print("\n=== Cadastro de usuário (ADMIN) ===")

    # login
    while True:
        user = input("Login (sem espaço, letras/números/_): ").strip()
        if user and user.replace("_", "").isalnum():
            break
        print("Use apenas letras, números e underscore (_).")

    # tipo
    tipo = ""
    while tipo not in ("cliente", "veterinario", "admin"):
        tipo = input("Tipo (cliente / veterinario / admin): ").strip().lower()

    # senha forte
    while True:
        s1 = ler_senha_mascarada()
        if not senha_forte(s1):
            print("Senha fraca. Use pelo menos 8 caracteres, com letras e números.")
            continue
        s2 = ler_senha_mascarada("Confirmar senha: ")
        if s1 != s2:
            print("As senhas não conferem. Tente de novo.")
            continue
        break

    senha_hash = gerar_hash_senha(s1)

    try:
        with conn.cursor() as c:
            c.execute(
                """
                INSERT INTO usuario (username, senha_cripto, tipo)
                VALUES (%s,%s,%s) RETURNING id_usuario;
                """,
                (user, senha_hash, tipo),
            )
            id_user = c.fetchone()[0]
            id_dono = None

            if tipo == "cliente":
                print("\n--- Dados do tutor ---")
                nome = ler_letras("Nome completo: ")

                cpf = ler_numero("CPF (11 dígitos, só números): ")
                while len(cpf) != 11:
                    print("CPF precisa ter 11 dígitos.")
                    cpf = ler_numero("CPF (11 dígitos, só números): ")

                email = input("E-mail (pode deixar vazio): ").strip() or None
                end = input("Endereço: ").strip()

                tel = ler_numero("Telefone (só números): ")
                while len(tel) < 8:
                    print("Telefone muito curto, informe com DDD se possível.")
                    tel = ler_numero("Telefone (só números): ")

                c.execute(
                    """
                    INSERT INTO dono (nome, cpf, email, endereco, telefone)
                    VALUES (%s,%s,%s,%s,%s) RETURNING id_dono;
                    """,
                    (nome, cpf, email, end, tel),
                )
                id_dono = c.fetchone()[0]

                print("\n--- Dados do animal ---")
                nm = ler_letras("Nome do animal: ")
                es = ler_letras("Espécie: ")
                rc = ler_letras("Raça: ")

                idade_str = ler_numero("Idade (em anos): ")
                idade = int(idade_str)
                while idade < 0 or idade > 40:
                    print("Idade estranha... informe uma idade entre 0 e 40 anos.")
                    idade = int(ler_numero("Idade (em anos): "))

                c.execute(
                    """
                    INSERT INTO animal (nome, especie, raca, idade, id_dono)
                    VALUES (%s,%s,%s,%s,%s)
                    """,
                    (nm, es, rc, idade, id_dono),
                )

                c.execute(
                    "UPDATE usuario SET id_dono = %s WHERE id_usuario = %s",
                    (id_dono, id_user),
                )

        conn.commit()
        print("\nUsuário cadastrado com sucesso.")
        if tipo == "cliente":
            print("Tutor e animal também foram cadastrados e vinculados ao usuário.")
    except Exception as e:
        conn.rollback()
        print("Erro ao cadastrar usuário:", e)


def cadastrar_cliente_publico(conn: PgConnection) -> None:
    """Cadastro público de CLIENTE/TUTOR vindo do menu inicial."""
    print("\n=== Cadastro de CLIENTE / TUTOR ===")

    while True:
        user = input("Crie seu login (sem espaço, letras/números/_): ").strip()
        if user and user.replace("_", "").isalnum():
            break
        print("Use apenas letras, números e underscore (_).")

    while True:
        s1 = ler_senha_mascarada()
        if not senha_forte(s1):
            print("Senha fraca. Use pelo menos 8 caracteres, com letras e números.")
            continue
        s2 = ler_senha_mascarada("Confirmar senha: ")
        if s1 != s2:
            print("As senhas não conferem. Tente de novo.")
            continue
        break

    senha_hash = gerar_hash_senha(s1)
    tipo = "cliente"

    try:
        with conn.cursor() as c:
            c.execute(
                """
                INSERT INTO usuario (username, senha_cripto, tipo)
                VALUES (%s,%s,%s) RETURNING id_usuario;
                """,
                (user, senha_hash, tipo),
            )
            id_user = c.fetchone()[0]

            print("\n--- Dados do tutor (seus dados) ---")
            nome = ler_letras("Nome completo: ")

            cpf = ler_numero("CPF (11 dígitos, só números): ")
            while len(cpf) != 11:
                print("CPF precisa ter 11 dígitos.")
                cpf = ler_numero("CPF (11 dígitos, só números): ")

            email = input("E-mail (pode deixar vazio): ").strip() or None
            end = input("Endereço: ").strip()

            tel = ler_numero("Telefone (só números): ")
            while len(tel) < 8:
                print("Telefone muito curto, informe com DDD se possível.")
                tel = ler_numero("Telefone (só números): ")

            c.execute(
                """
                INSERT INTO dono (nome, cpf, email, endereco, telefone)
                VALUES (%s,%s,%s,%s,%s) RETURNING id_dono;
                """,
                (nome, cpf, email, end, tel),
            )
            id_dono = c.fetchone()[0]

            print("\n--- Dados do animal ---")
            nm = ler_letras("Nome do animal: ")
            es = ler_letras("Espécie: ")
            rc = ler_letras("Raça: ")

            idade_str = ler_numero("Idade (em anos): ")
            idade = int(idade_str)
            while idade < 0 or idade > 40:
                print("Idade estranha... informe uma idade entre 0 e 40 anos.")
                idade = int(ler_numero("Idade (em anos): "))

            c.execute(
                """
                INSERT INTO animal (nome, especie, raca, idade, id_dono)
                VALUES (%s,%s,%s,%s,%s)
                """,
                (nm, es, rc, idade, id_dono),
            )

            c.execute(
                "UPDATE usuario SET id_dono = %s WHERE id_usuario = %s",
                (id_dono, id_user),
            )

        conn.commit()
        print("\nCadastro realizado com sucesso!")
        print("Você já pode usar seu login e senha na opção 'Login como CLIENTE / TUTOR'.")
    except Exception as e:
        conn.rollback()
        print("Erro ao cadastrar cliente/tutor:", e)

# LOGIN E CONTROLE DE TENTATIVAS
def atualizar_login_sucesso(conn: PgConnection, id_usuario: int) -> None:
    with conn.cursor() as c:
        c.execute(
            "UPDATE usuario SET tentativas_erradas = 0 WHERE id_usuario = %s",
            (id_usuario,),
        )
    conn.commit()


def registrar_tentativa_falha(conn: PgConnection, id_usuario: int) -> None:
    with conn.cursor() as c:
        c.execute(
            """
            UPDATE usuario
            SET tentativas_erradas = tentativas_erradas + 1
            WHERE id_usuario = %s
            RETURNING tentativas_erradas;
            """,
            (id_usuario,),
        )
        tentativas = c.fetchone()[0]
        if tentativas >= 3:
            c.execute(
                "UPDATE usuario SET bloqueado = TRUE WHERE id_usuario = %s",
                (id_usuario,),
            )
    conn.commit()


def login(
    conn: PgConnection, tipo_esperado: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    print("\n=== Login ===")
    user = input("Usuário: ").strip()
    s = ler_senha_mascarada()

    try:
        with conn.cursor() as c:
            c.execute(
                """
                SELECT id_usuario, username, tipo, senha_cripto, bloqueado
                FROM usuario WHERE username = %s
                """,
                (user,),
            )
            r = c.fetchone()
    except Exception as e:
        print("Erro ao buscar usuário:", e)
        return None

    if not r:
        print("Usuário ou senha incorretos.")
        return None

    id_usuario, username, tipo, senha_hash, bloqueado = r

    if bloqueado:
        print("Usuário bloqueado por muitas tentativas de login. Contate o administrador.")
        return None

    if not verificar_senha(s, senha_hash):
        registrar_tentativa_falha(conn, id_usuario)
        print("Usuário ou senha incorretos.")
        return None

    if tipo_esperado and tipo != tipo_esperado:
        print(
            f"Este usuário é do tipo '{tipo}', não '{tipo_esperado}'. "
            "Entre pelo menu correto."
        )
        return None

    atualizar_login_sucesso(conn, id_usuario)
    print(f"Login realizado com sucesso ({username} - {tipo}).")
    return {"id": id_usuario, "username": username, "tipo": tipo}


def alterar_senha_admin(conn: PgConnection, usuario: Dict[str, Any]) -> None:
    print("\n=== ALTERAR SENHA DO ADMIN ===")

    senha_atual = ler_senha_mascarada("Digite sua senha atual: ")

    with conn.cursor() as c:
        c.execute(
            "SELECT senha_cripto FROM usuario WHERE id_usuario = %s",
            (usuario["id"],),
        )
        row = c.fetchone()

    if not row:
        print("Usuário não encontrado no banco.")
        return

    senha_hash_atual = row[0]

    if not verificar_senha(senha_atual, senha_hash_atual):
        print("Senha atual incorreta.")
        return

    while True:
        nova = ler_senha_mascarada("Nova senha: ")

        if not senha_forte(nova):
            print("Senha fraca. Use pelo menos 8 caracteres com letras e números.")
            continue

        confirmar = ler_senha_mascarada("Confirme a nova senha: ")
        if nova != confirmar:
            print("As senhas não conferem.")
            continue

        break

    nova_hash = gerar_hash_senha(nova)

    try:
        with conn.cursor() as c:
            c.execute(
                "UPDATE usuario SET senha_cripto = %s WHERE id_usuario = %s",
                (nova_hash, usuario["id"]),
            )
        conn.commit()
        print("✅ Senha alterada com sucesso.")
    except Exception as e:
        conn.rollback()
        print("Erro ao alterar senha:", e)

# LISTAGENS
def listar_donos(conn: PgConnection) -> None:
    print("\n=== Lista de tutores (donos) ===")
    with conn.cursor() as c:
        c.execute(
            "SELECT id_dono, nome, cpf, email, telefone FROM dono ORDER BY id_dono;"
        )
        linhas = c.fetchall()
        if not linhas:
            print("Nenhum tutor cadastrado.")
            return
        for id_dono, nome, cpf, email, tel in linhas:
            print(
                f"[{id_dono}] {nome} | CPF: {cpf} | "
                f"E-mail: {email or '-'} | Tel: {tel}"
            )


def listar_animais(conn: PgConnection) -> None:
    print("\n=== Lista de animais ===")
    with conn.cursor() as c:
        c.execute(
            """
            SELECT a.id_animal, a.nome, a.especie, a.raca, a.idade, d.nome
            FROM animal a
            JOIN dono d ON a.id_dono = d.id_dono
            ORDER BY a.id_animal;
            """
        )
        linhas = c.fetchall()
        if not linhas:
            print("Nenhum animal cadastrado.")
            return
        for id_animal, nome, especie, raca, idade, nome_dono in linhas:
            print(
                f"[{id_animal}] {nome} ({especie} - {raca}), {idade} anos | Tutor: {nome_dono}"
            )


def relatorio_qtd_animais_por_tutor(conn: PgConnection) -> None:
    print("\n=== Relatório: quantidade de animais por tutor ===")
    with conn.cursor() as c:
        c.execute(
            """
            SELECT d.id_dono,
                   d.nome,
                   COUNT(a.id_animal) AS total_animais
            FROM dono d
            LEFT JOIN animal a ON a.id_dono = d.id_dono
            GROUP BY d.id_dono, d.nome
            ORDER BY total_animais DESC, d.nome;
            """
        )
        linhas = c.fetchall()
        if not linhas:
            print("Nenhum tutor cadastrado.")
            return

        for id_dono, nome, total in linhas:
            print(f"[{id_dono}] {nome} - {total} animal(is)")


def join_consultas(
    conn: PgConnection, somente_vet_id: Optional[int] = None
) -> None:
    print("\n=== Consultas cadastradas ===")
    with conn.cursor() as c:
        if somente_vet_id:
            c.execute(
                """
                SELECT c.id_consulta, c.data, c.horario, c.status,
                       a.nome, d.nome
                FROM consulta c
                JOIN animal a ON a.id_animal = c.id_animal
                JOIN dono d   ON d.id_dono   = a.id_dono
                WHERE c.id_vet = %s
                ORDER BY c.data DESC, c.horario DESC;
                """,
                (somente_vet_id,),
            )
        else:
            c.execute(
                """
                SELECT c.id_consulta, c.data, c.horario, c.status,
                       a.nome, d.nome
                FROM consulta c
                JOIN animal a ON a.id_animal = c.id_animal
                JOIN dono d   ON d.id_dono   = a.id_dono
                ORDER BY c.data DESC, c.horario DESC;
                """
            )
        linhas = c.fetchall()
        if not linhas:
            print("Nenhuma consulta cadastrada.")
            return
        for id_consulta, data, horario, status, nome_animal, nome_dono in linhas:
            print(
                f"[{id_consulta}] {data} {horario} [{status}] "
                f"| Animal: {nome_animal} | Tutor: {nome_dono}"
            )


def listar_consultas_por_periodo(
    conn: PgConnection, somente_vet_id: Optional[int] = None
) -> None:
    print("\n=== Consultas por período ===")
    data_ini = input("Data inicial (AAAA-MM-DD): ").strip()
    data_fim = input("Data final  (AAAA-MM-DD): ").strip()

    with conn.cursor() as c:
        if somente_vet_id:
            c.execute(
                """
                SELECT c.id_consulta, c.data, c.horario, c.status,
                       a.nome, d.nome
                FROM consulta c
                JOIN animal a ON a.id_animal = c.id_animal
                JOIN dono d   ON d.id_dono   = a.id_dono
                WHERE c.data BETWEEN %s AND %s
                  AND c.id_vet = %s
                ORDER BY c.data DESC, c.horario DESC;
                """,
                (data_ini, data_fim, somente_vet_id),
            )
        else:
            c.execute(
                """
                SELECT c.id_consulta, c.data, c.horario, c.status,
                       a.nome, d.nome
                FROM consulta c
                JOIN animal a ON a.id_animal = c.id_animal
                JOIN dono d   ON d.id_dono   = a.id_dono
                WHERE c.data BETWEEN %s AND %s
                ORDER BY c.data DESC, c.horario DESC;
                """,
                (data_ini, data_fim),
            )

        linhas = c.fetchall()
        if not linhas:
            print("Nenhuma consulta encontrado nesse período.")
            return
        for id_consulta, data, horario, status, nome_animal, nome_dono in linhas:
            print(
                f"[{id_consulta}] {data} {horario} [{status}] "
                f"| Animal: {nome_animal} | Tutor: {nome_dono}"
            )

# CADASTROS (CONSULTA / CIRURGIA)
def cadastrar_consulta(
    conn: PgConnection, usuario: Optional[Dict[str, Any]] = None
) -> None:
    print("\n=== Cadastro de consulta ===")
    listar_animais(conn)

    id_animal = int(ler_numero("ID do animal: "))
    data = input("Data da consulta (AAAA-MM-DD): ").strip()
    horario = input("Horário (HH:MM): ").strip()
    motivo = input("Motivo da consulta: ").strip()
    diagnostico = input(
        "Diagnóstico (pode deixar em branco por enquanto): "
    ).strip() or None
    status = "agendada"

    id_vet: Optional[int] = None
    if usuario and usuario.get("tipo") == "veterinario":
        id_vet = usuario["id"]
    else:
        vet_resp = input("ID do veterinário responsável (ou deixe vazio): ").strip()
        if vet_resp:
            id_vet = int(vet_resp)

    try:
        with conn.cursor() as c:
            c.execute(
                """
                INSERT INTO consulta (data, horario, motivo, diagnostico,
                                      status, prioridade, id_animal, id_vet)
                VALUES (%s,%s,%s,%s,%s,'normal',%s,%s)
                """,
                (data, horario, motivo, diagnostico, status, id_animal, id_vet),
            )
        conn.commit()
        print("Consulta cadastrada com sucesso.")
    except Exception as e:
        conn.rollback()
        print("Erro ao cadastrar consulta:", e)


def cadastrar_cirurgia(conn: PgConnection) -> None:
    print("\n=== Cadastro de cirurgia ===")
    listar_animais(conn)

    id_animal = int(ler_numero("ID do animal: "))
    data = input("Data da cirurgia (AAAA-MM-DD): ").strip()
    tipo = input("Tipo de cirurgia: ").strip()
    observacoes = input("Observações (pode deixar em branco): ").strip() or None
    status = "agendada"

    try:
        with conn.cursor() as c:
            c.execute(
                """
                INSERT INTO cirurgia (data, tipo_cirurgia, observacoes,
                                      status, id_animal)
                VALUES (%s,%s,%s,%s,%s)
                """,
                (data, tipo, observacoes, status, id_animal),
            )
        conn.commit()
        print("Cirurgia cadastrada com sucesso.")
    except Exception as e:
        conn.rollback()
        print("Erro ao cadastrar cirurgia:", e)
        
def editar_dono(conn: PgConnection) -> None:
    listar_donos(conn)
    id_dono = int(ler_numero("ID do tutor para editar: "))

    print("Deixe em branco para manter o valor atual.")

    with conn.cursor() as c:
        c.execute(
            "SELECT nome, email, endereco, telefone, observacao FROM dono WHERE id_dono = %s",
            (id_dono,),
        )
        row = c.fetchone()
        if not row:
            print("Tutor não encontrado.")
            return
        nome_atual, email_atual, end_atual, tel_atual, obs_atual = row

    novo_nome = input(f"Nome [{nome_atual}]: ").strip() or nome_atual
    novo_email = input(f"E-mail [{email_atual or '-'}]: ").strip() or email_atual
    novo_end = input(f"Endereço [{end_atual}]: ").strip() or end_atual
    novo_tel = input(f"Telefone [{tel_atual}]: ").strip() or tel_atual
    nova_obs = input(f"Observação [{obs_atual or '-'}]: ").strip() or obs_atual

    try:
        with conn.cursor() as c:
            c.execute(
                """
                UPDATE dono
                SET nome = %s, email = %s, endereco = %s, telefone = %s, observacao = %s
                WHERE id_dono = %s
                """,
                (novo_nome, novo_email, novo_end, novo_tel, nova_obs, id_dono),
            )
        conn.commit()
        print("Dados do tutor atualizados.")
    except Exception as e:
        conn.rollback()
        print("Erro ao atualizar tutor:", e)


def editar_animal(conn: PgConnection) -> None:
    listar_animais(conn)
    id_animal = int(ler_numero("ID do animal para editar: "))

    with conn.cursor() as c:
        c.execute(
            "SELECT nome, especie, raca, idade FROM animal WHERE id_animal = %s",
            (id_animal,),
        )
        row = c.fetchone()
        if not row:
            print("Animal não encontrado.")
            return
        nome_atual, esp_atual, raca_atual, idade_atual = row

    print("Deixe em branco para manter o valor atual.")
    novo_nome = input(f"Nome [{nome_atual}]: ").strip() or nome_atual
    nova_esp = input(f"Espécie [{esp_atual}]: ").strip() or esp_atual
    nova_raca = input(f"Raça [{raca_atual}]: ").strip() or raca_atual
    idade_str = input(f"Idade [{idade_atual}]: ").strip()
    nova_idade = idade_atual
    if idade_str:
        try:
            nova_idade = int(idade_str)
        except ValueError:
            print("Idade inválida, mantendo valor anterior.")

    try:
        with conn.cursor() as c:
            c.execute(
                """
                UPDATE animal
                SET nome = %s, especie = %s, raca = %s, idade = %s
                WHERE id_animal = %s
                """,
                (novo_nome, nova_esp, nova_raca, nova_idade, id_animal),
            )
        conn.commit()
        print("Dados do animal atualizados.")
    except Exception as e:
        conn.rollback()
        print("Erro ao atualizar animal:", e)


def editar_diagnostico_consulta(conn: PgConnection) -> None:
    join_consultas(conn)
    id_consulta = int(ler_numero("ID da consulta para editar: "))

    with conn.cursor() as c:
        c.execute(
            "SELECT diagnostico, status, prioridade FROM consulta WHERE id_consulta = %s",
            (id_consulta,),
        )
        row = c.fetchone()
        if not row:
            print("Consulta não encontrada.")
            return
        diag_atual, status_atual, prioridade_atual = row

    print("Deixe em branco para manter o valor atual.")
    novo_diag = input(f"Diagnóstico [{diag_atual or 'vazio'}]: ").strip() or diag_atual
    novo_status = (
        input(f"Status [{status_atual} - (agendada/realizada/cancelada)]: ").strip()
        or status_atual
    )
    nova_prioridade = (
        input(f"Prioridade [{prioridade_atual} - (normal/urgente)]: ").strip()
        or prioridade_atual
    )

    try:
        with conn.cursor() as c:
            c.execute(
                """
                UPDATE consulta
                SET diagnostico = %s, status = %s, prioridade = %s
                WHERE id_consulta = %s
                """,
                (novo_diag, novo_status, nova_prioridade, id_consulta),
            )
        conn.commit()
        print("Consulta atualizada.")
    except Exception as e:
        conn.rollback()
        print("Erro ao atualizar consulta:", e)


def excluir_dono(conn: PgConnection) -> None:
    listar_donos(conn)
    id_dono = int(ler_numero("ID do tutor para excluir: "))
    conf = input("Tem certeza? Isso apagará animais e consultas. (s/n): ").lower()
    if conf != "s":
        print("Operação cancelada.")
        return

    try:
        with conn.cursor() as c:
            c.execute("DELETE FROM dono WHERE id_dono = %s", (id_dono,))
        conn.commit()
        print("Tutor excluído.")
    except Exception as e:
        conn.rollback()
        print("Erro ao excluir tutor:", e)


def excluir_animal(conn: PgConnection) -> None:
    listar_animais(conn)
    id_animal = int(ler_numero("ID do animal para excluir: "))
    conf = input(
        "Tem certeza? Consultas e cirurgias do animal serão apagadas. (s/n): "
    ).lower()
    if conf != "s":
        print("Operação cancelada.")
        return

    try:
        with conn.cursor() as c:
            c.execute("DELETE FROM animal WHERE id_animal = %s", (id_animal,))
        conn.commit()
        print("Animal excluído.")
    except Exception as e:
        conn.rollback()
        print("Erro ao excluir animal:", e)


def excluir_consulta(conn: PgConnection) -> None:
    join_consultas(conn)
    id_consulta = int(ler_numero("ID da consulta para excluir: "))
    conf = input("Confirmar exclusão da consulta? (s/n): ").lower()
    if conf != "s":
        print("Operação cancelada.")
        return

    try:
        with conn.cursor() as c:
            c.execute("DELETE FROM consulta WHERE id_consulta = %s", (id_consulta,))
        conn.commit()
        print("Consulta excluída.")
    except Exception as e:
        conn.rollback()
        print("Erro ao excluir consulta:", e)

def buscar_dono_por_cpf(conn: PgConnection) -> None:
    cpf = ler_numero("CPF (11 dígitos, só números): ")
    while len(cpf) != 11:
        print("CPF precisa ter 11 dígitos.")
        cpf = ler_numero("CPF (11 dígitos, só números): ")

    with conn.cursor() as c:
        c.execute(
            """
            SELECT id_dono, nome, email, endereco, telefone
            FROM dono
            WHERE cpf = %s;
            """,
            (cpf,),
        )
        row = c.fetchone()
        if not row:
            print("Nenhum tutor encontrado com esse CPF.")
            return

        id_dono, nome, email, end, tel = row
        print("\n=== Tutor encontrado ===")
        print(f"ID: {id_dono}")
        print(f"Nome: {nome}")
        print(f"E-mail: {email or '-'}")
        print(f"Endereço: {end}")
        print(f"Telefone: {tel}")

        c.execute(
            """
            SELECT id_animal, nome, especie, raca, idade
            FROM animal
            WHERE id_dono = %s
            ORDER BY id_animal;
            """,
            (id_dono,),
        )
        animais = c.fetchall()
        if not animais:
            print("Nenhum animal cadastrado para este tutor.")
            return

        print("\n=== Animais do tutor ===")
        for id_animal, nm, especie, raca, idade in animais:
            print(f"[{id_animal}] {nm} ({especie} - {raca}), {idade} anos")

# FUNÇÕES DO CLIENTE / TUTOR
def obter_id_dono_do_usuario(conn: PgConnection, usuario: Dict[str, Any]) -> Optional[int]:
    with conn.cursor() as c:
        c.execute(
            "SELECT id_dono FROM usuario WHERE id_usuario = %s",
            (usuario["id"],),
        )
        r = c.fetchone()
        return r[0] if r else None


def mostrar_dados_cliente(conn: PgConnection, usuario: Dict[str, Any]) -> None:
    with conn.cursor() as c:
        c.execute(
            """
            SELECT d.id_dono, d.nome, d.cpf, d.email, d.endereco, d.telefone, d.observacao
            FROM usuario u
            JOIN dono d ON d.id_dono = u.id_dono
            WHERE u.id_usuario = %s;
            """,
            (usuario["id"],),
        )
        dono = c.fetchone()
        if not dono:
            print("Nenhum tutor vinculado ao seu usuário. Fale com a recepção.")
            return

        id_dono, nome, cpf, email, end, tel, obs = dono
        print("\n=== Seus dados de tutor ===")
        print(f"ID: {id_dono}")
        print(f"Nome: {nome}")
        print(f"CPF: {cpf}")
        print(f"E-mail: {email or '-'}")
        print(f"Endereço: {end}")
        print(f"Telefone: {tel}")
        print(f"Observação: {obs or '-'}")

        c.execute(
            """
            SELECT id_animal, nome, especie, raca, idade
            FROM animal
            WHERE id_dono = %s
            ORDER BY id_animal;
            """,
            (id_dono,),
        )
        animais = c.fetchall()

        if not animais:
            print("\nNenhum animal cadastrado para este tutor.")
            return

        print("\n=== Seus animais ===")
        for id_animal, nm, especie, raca, idade in animais:
            print(f"[{id_animal}] {nm} ({especie} - {raca}), {idade} anos")


def mostrar_consultas_cliente(conn: PgConnection, usuario: Dict[str, Any]) -> None:
    id_dono = obter_id_dono_do_usuario(conn, usuario)
    if not id_dono:
        print("Nenhum tutor vinculado ao seu usuário. Fale com a recepção.")
        return

    with conn.cursor() as c:
        c.execute(
            """
            SELECT c.id_consulta, c.data, c.horario, c.status, c.prioridade, a.nome
            FROM consulta c
            JOIN animal a ON a.id_animal = c.id_animal
            WHERE a.id_dono = %s
            ORDER BY c.data DESC, c.horario DESC;
            """,
            (id_dono,),
        )
        consultas = c.fetchall()

        if not consultas:
            print("Você ainda não possui consultas cadastradas.")
            return

        print("\n=== Suas consultas ===")
        for id_consulta, data, horario, status, prioridade, nome_animal in consultas:
            print(
                f"[{id_consulta}] {data} {horario} [{status} - {prioridade}] | Animal: {nome_animal}"
            )


def cadastrar_novo_animal_cliente(conn: PgConnection, usuario: Dict[str, Any]) -> None:
    print("\n=== Cadastro de novo animal ===")

    id_dono = obter_id_dono_do_usuario(conn, usuario)
    if not id_dono:
        print("Nenhum tutor vinculado ao seu usuário. Fale com a recepção.")
        return

    nm = ler_letras("Nome do animal: ")
    es = ler_letras("Espécie: ")
    rc = ler_letras("Raça: ")

    idade_str = ler_numero("Idade (em anos): ")
    idade = int(idade_str)
    while idade < 0 or idade > 40:
        print("Idade estranha... informe uma idade entre 0 e 40 anos.")
        idade = int(ler_numero("Idade (em anos): "))

    try:
        with conn.cursor() as c:
            c.execute(
                """
                INSERT INTO animal (nome, especie, raca, idade, id_dono)
                VALUES (%s,%s,%s,%s,%s)
                """,
                (nm, es, rc, idade, id_dono),
            )
        conn.commit()
        print("Novo animal cadastrado com sucesso.")
    except Exception as e:
        conn.rollback()
        print("Erro ao cadastrar novo animal:", e)


def atualizar_dados_cliente(conn: PgConnection, usuario: Dict[str, Any]) -> None:
    print("\n=== Atualizar meus dados ===")

    id_dono = obter_id_dono_do_usuario(conn, usuario)
    if not id_dono:
        print("Nenhum tutor vinculado ao seu usuário. Fale com a recepção.")
        return

    with conn.cursor() as c:
        c.execute(
            "SELECT email, endereco, telefone, observacao FROM dono WHERE id_dono = %s",
            (id_dono,),
        )
        row = c.fetchone()
        if not row:
            print("Registro de tutor não encontrado.")
            return
        email_atual, end_atual, tel_atual, obs_atual = row

    print("Deixe em branco para manter o valor atual.")
    novo_email = input(f"E-mail [{email_atual or '-'}]: ").strip() or email_atual
    novo_end = input(f"Endereço [{end_atual}]: ").strip() or end_atual
    novo_tel = input(f"Telefone [{tel_atual}]: ").strip() or tel_atual
    nova_obs = input(f"Observação [{obs_atual or '-'}]: ").strip() or obs_atual

    try:
        with conn.cursor() as c:
            c.execute(
                """
                UPDATE dono
                SET email = %s, endereco = %s, telefone = %s, observacao = %s
                WHERE id_dono = %s
                """,
                (novo_email, novo_end, novo_tel, nova_obs, id_dono),
            )
        conn.commit()
        print("Dados atualizados com sucesso.")
    except Exception as e:
        conn.rollback()
        print("Erro ao atualizar dados:", e)


def cancelar_consulta_cliente(conn: PgConnection, usuario: Dict[str, Any]) -> None:
    print("\n=== Cancelar consulta agendada ===")

    id_dono = obter_id_dono_do_usuario(conn, usuario)
    if not id_dono:
        print("Nenhum tutor vinculado ao seu usuário. Fale com a recepção.")
        return

    with conn.cursor() as c:
        c.execute(
            """
            SELECT c.id_consulta, c.data, c.horario, c.status, c.prioridade, a.nome
            FROM consulta c
            JOIN animal a ON a.id_animal = c.id_animal
            WHERE a.id_dono = %s AND c.status = 'agendada'
            ORDER BY c.data, c.horario;
            """,
            (id_dono,),
        )
        consultas = c.fetchall()

        if not consultas:
            print("Você não possui consultas agendadas para cancelar.")
            return

        print("\nConsultas agendadas:")
        for id_consulta, data, horario, status, prioridade, nome_animal in consultas:
            print(
                f"[{id_consulta}] {data} {horario} [{status} - {prioridade}] | Animal: {nome_animal}"
            )

    id_consulta_str = ler_numero("Informe o ID da consulta a cancelar: ")
    id_consulta = int(id_consulta_str)

    try:
        with conn.cursor() as c:
            c.execute(
                """
                UPDATE consulta
                SET status = 'cancelada'
                WHERE id_consulta = %s
                  AND status = 'agendada'
                  AND id_animal IN (
                       SELECT id_animal FROM animal WHERE id_dono = %s
                  );
                """,
                (id_consulta, id_dono),
            )
            if c.rowcount == 0:
                print("Não foi possível cancelar. Verifique se o ID é seu e se está agendada.")
                conn.rollback()
                return
        conn.commit()
        print("Consulta cancelada com sucesso.")
    except Exception as e:
        conn.rollback()
        print("Erro ao cancelar consulta:", e)
