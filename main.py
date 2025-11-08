from pymongo.mongo_client import MongoClient
from datetime import datetime, timezone
from cryptography.fernet import Fernet
from pymongo import MongoClient

# Gerar uma chave de criptografia
key = b'DwJ2YNbCIZOZMZ2Ush9WWM6foF3NVoAXqql6Q9hkPjw='
fernet = Fernet(key)
print(key)
user = 'ernany'
password = '123'


uri = f"mongodb+srv://{user}:{password}@firstcluster.sz1xw3a.mongodb.net/projetobruno?retryWrites=true&w=majority&tls=true"

client = MongoClient(uri)
db = client["projetobruno"]
collection = db["doces"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Erro ao conectar: ", e)

op = int(input("Você deseja (1) Adicionar, (2) Listar, (3) Descriptografar: "))

if op == 1:
    nome = input("nome da criança: ")
    doce_tipo = input("Tipo do doce: ")
    qtd_doce = input("Quantidade de doces: ")
    doce_tipo_crp = fernet.encrypt(str(doce_tipo).encode())

    agora_utc = datetime.now(timezone.utc)

    # Formata no estilo ISO 8601
    horario = agora_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

    data = {"child": nome, "candy_type": doce_tipo_crp, "qty": qtd_doce, "timestamp": horario}
    collection.insert_one(data)

    print('valores inseridos')

elif op == 2:
    todos_dados = collection.find()
    for dado in todos_dados:
        print(dado)

elif op == 3:
    todos_dados = collection.find()
    for dado in todos_dados:
        try:
            tipo_doce_dcrp = fernet.decrypt(dado["candy_type"]).decode()
            print(tipo_doce_dcrp)
        except:
            print('Não foi possivel descriptografar')