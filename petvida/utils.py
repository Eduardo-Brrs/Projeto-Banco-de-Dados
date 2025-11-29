import sys
import time


def so_numeros(t: str) -> bool:
    return t.isdigit()


def so_letras(t: str) -> bool:
    return all(c.isalpha() or c.isspace() for c in t)


def ler_numero(msg: str) -> str:
    v = input(msg).strip()
    while not so_numeros(v):
        print("Digite apenas números.")
        v = input(msg).strip()
    return v


def ler_letras(msg: str) -> str:
    v = input(msg).strip()
    while not so_letras(v):
        print("Digite apenas letras (e espaços).")
        v = input(msg).strip()
    return v


def ler_senha_mascarada(txt: str = "Senha: ") -> str:
    try:
        import msvcrt  # Windows

        print(txt, end="", flush=True)
        senha = ""
        while True:
            ch = msvcrt.getch()
            if ch in (b"\r", b"\n"):
                print()
                break
            elif ch == b"\x08":  # backspace
                if senha:
                    senha = senha[:-1]
                    sys.stdout.write("\b \b")
            else:
                try:
                    senha += ch.decode("latin-1")
                    sys.stdout.write("*")
                except Exception:
                    pass
        return senha
    except Exception:
        from getpass import getpass

        return getpass(txt)


def senha_forte(s: str) -> bool:
    return len(s) >= 8 and any(c.isdigit() for c in s) and any(c.isalpha() for c in s)


def mostrar_loading(msg: str = "Carregando") -> None:
    print()
    print(msg, end="", flush=True)
    for _ in range(3):
        time.sleep(0.25)
        print(".", end="", flush=True)
    print("\n")
