import os
import bcrypt  # pip install bcrypt

# Config do banco (a senha vem da variável de ambiente PETVIDA_DB_PASSWORD)
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": os.environ.get("PETVIDA_DB_PASSWORD", ""),
    "options": "-c search_path=petvida"
}

def gerar_hash_senha(senha_clara: str) -> str:
    senha_bytes = senha_clara.encode("utf-8")
    hash_bytes = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    return hash_bytes.decode("utf-8")


def verificar_senha(senha_digitada: str, senha_hash: str) -> bool:
    try:
        return bcrypt.checkpw(
            senha_digitada.encode("utf-8"),
            senha_hash.encode("utf-8")
        )
    except Exception:
        return False
