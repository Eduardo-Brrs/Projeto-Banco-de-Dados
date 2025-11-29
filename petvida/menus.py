from typing import Dict, Any

from psycopg2.extensions import connection as PgConnection

from utils import mostrar_loading
from services import (
    # infra
    criar_conexao,
    criar_tabelas,
    garantir_admin,
    login,
    cadastrar_cliente_publico,

    # admin
    cadastrar_usuario,
    listar_donos,
    listar_animais,
    editar_dono,
    editar_animal,
    excluir_dono,
    excluir_animal,
    buscar_dono_por_cpf,
    join_consultas,
    cadastrar_consulta,
    editar_diagnostico_consulta,
    excluir_consulta,
    listar_consultas_por_periodo,
    cadastrar_cirurgia,
    relatorio_qtd_animais_por_tutor,
    limpar_tabelas,
    alterar_senha_admin,

    # cliente
    mostrar_dados_cliente,
    mostrar_consultas_cliente,
    cadastrar_novo_animal_cliente,
    atualizar_dados_cliente,
    cancelar_consulta_cliente,
)

def submenu_usuarios_admin(conn: PgConnection) -> None:
    while True:
        print(
            """
--- ADMIN > USUÁRIOS ---
1) Cadastrar usuário
0) Voltar
"""
        )
        op = input("> ").strip()
        if op == "1":
            cadastrar_usuario(conn)
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def submenu_donos_animais_admin(conn: PgConnection) -> None:
    while True:
        print(
            """
--- ADMIN > DONOS / ANIMAIS ---
1) Listar donos
2) Listar animais
3) Editar tutor
4) Editar animal
5) Excluir tutor
6) Excluir animal
0) Voltar
"""
        )
        op = input("> ").strip()
        if op == "1":
            listar_donos(conn)
        elif op == "2":
            listar_animais(conn)
        elif op == "3":
            editar_dono(conn)
        elif op == "4":
            editar_animal(conn)
        elif op == "5":
            excluir_dono(conn)
        elif op == "6":
            excluir_animal(conn)
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def submenu_consultas_admin(conn: PgConnection) -> None:
    while True:
        print(
            """
--- ADMIN > CONSULTAS ---
1) Listar todas
2) Cadastrar consulta
3) Editar diagnóstico / status / prioridade
4) Excluir consulta
5) Listar por período
0) Voltar
"""
        )
        op = input("> ").strip()
        if op == "1":
            join_consultas(conn)
        elif op == "2":
            cadastrar_consulta(conn)
        elif op == "3":
            editar_diagnostico_consulta(conn)
        elif op == "4":
            excluir_consulta(conn)
        elif op == "5":
            listar_consultas_por_periodo(conn)
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def submenu_cirurgias_admin(conn: PgConnection) -> None:
    while True:
        print(
            """
--- ADMIN > CIRURGIAS ---
1) Cadastrar cirurgia
0) Voltar
"""
        )
        op = input("> ").strip()
        if op == "1":
            cadastrar_cirurgia(conn)
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def submenu_relatorios_admin(conn: PgConnection) -> None:
    while True:
        print(
            """
--- ADMIN > RELATÓRIOS / MANUTENÇÃO ---
1) Quantidade de animais por tutor
2) Buscar tutor por CPF
3) LIMPAR TODAS AS TABELAS (DROP) [CUIDADO]
0) Voltar
"""
        )
        op = input("> ").strip()
        if op == "1":
            relatorio_qtd_animais_por_tutor(conn)
        elif op == "2":
            buscar_dono_por_cpf(conn)
        elif op == "3":
            limpar_tabelas(conn)
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def menu_admin(conn: PgConnection, usuario: Dict[str, Any]) -> None:
    """Menu administrativo principal, com submenus."""
    mostrar_loading("Carregando menu do administrador")

    while True:
        print(
            """
--- MENU ADMIN ---
1) Usuários
2) Donos / Animais
3) Consultas
4) Cirurgias
5) Relatórios / Manutenção
6) Alterar minha senha
0) Voltar ao menu principal
"""
        )
        op = input("> ").strip()

        if op == "1":
            submenu_usuarios_admin(conn)
        elif op == "2":
            submenu_donos_animais_admin(conn)
        elif op == "3":
            submenu_consultas_admin(conn)
        elif op == "4":
            submenu_cirurgias_admin(conn)
        elif op == "5":
            submenu_relatorios_admin(conn)
        elif op == "6":
            alterar_senha_admin(conn, usuario)
        elif op == "0":
            break
        else:
            print("Opção inválida.")

def menu_cliente(conn: PgConnection, usuario: Dict[str, Any]) -> None:
    mostrar_loading("Carregando menu do cliente")

    while True:
        print(
            f"""
--- MENU CLIENTE / TUTOR ({usuario['username']}) ---
1) Ver meus dados de tutor e animais
2) Ver minhas consultas
3) Cadastrar novo animal
4) Atualizar meus dados (e-mail, endereço, telefone, observação)
5) Cancelar consulta agendada
0) Voltar ao menu principal
"""
        )
        op = input("> ").strip()

        if op == "1":
            mostrar_dados_cliente(conn, usuario)
        elif op == "2":
            mostrar_consultas_cliente(conn, usuario)
        elif op == "3":
            cadastrar_novo_animal_cliente(conn, usuario)
        elif op == "4":
            atualizar_dados_cliente(conn, usuario)
        elif op == "5":
            cancelar_consulta_cliente(conn, usuario)
        elif op == "0":
            break
        else:
            print("Opção inválida.")

def menu_veterinario(conn: PgConnection, usuario: Dict[str, Any]) -> None:
    mostrar_loading("Carregando menu do veterinário")

    while True:
        print(
            f"""
--- MENU VETERINÁRIO ({usuario['username']}) ---
1) Listar animais
2) Cadastrar consulta (como vet)
3) Cadastrar cirurgia
4) Ver MINHAS consultas
5) Ver MINHAS consultas por período
0) Voltar ao menu principal
"""
        )
        op = input("> ").strip()

        if op == "1":
            listar_animais(conn)
        elif op == "2":
            cadastrar_consulta(conn, usuario)
        elif op == "3":
            cadastrar_cirurgia(conn)
        elif op == "4":
            join_consultas(conn, somente_vet_id=usuario["id"])
        elif op == "5":
            listar_consultas_por_periodo(conn, somente_vet_id=usuario["id"])
        elif op == "0":
            break
        else:
            print("Opção inválida.")

def menu_principal() -> None:
    conn = criar_conexao()
    if not conn:
        return

    criar_tabelas(conn)
    garantir_admin(conn)

    while True:
        print(
            """
=== PETVIDA - SISTEMA TERMINAL ===
1) Login como ADMINISTRADOR
2) Login como CLIENTE / TUTOR
3) Login como VETERINÁRIO
4) Cadastrar CLIENTE / TUTOR
0) Sair
"""
        )
        op = input("> ").strip()

        if op == "1":
            u = login(conn, tipo_esperado="admin")
            if u:
                menu_admin(conn, u)

        elif op == "2":
            u = login(conn, tipo_esperado="cliente")
            if u:
                menu_cliente(conn, u)

        elif op == "3":
            u = login(conn, tipo_esperado="veterinario")
            if u:
                menu_veterinario(conn, u)

        elif op == "4":
            cadastrar_cliente_publico(conn)

        elif op == "0":
            print("Saindo... até mais!")
            break

        else:
            print("Opção inválida.")

    conn.close()
