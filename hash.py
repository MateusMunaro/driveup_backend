from passlib.context import CryptContext

# Criando contexto para hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criar um hash
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Gerando o hash corretamente
password = "12345"
hashed_password = hash_password(password)

print(f"Senha Hash: {hashed_password}")