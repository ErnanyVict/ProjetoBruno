from pymongo import MongoClient
from datetime import datetime, timezone
from cryptography.fernet import Fernet
import customtkinter as ctk
from tkinter import messagebox
import certifi


key = b'DwJ2YNbCIZOZMZ2Ush9WWM6foF3NVoAXqql6Q9hkPjw='
fernet = Fernet(key)

user = 'ernany'
password = '123'

uri = f"mongodb+srv://{user}:{password}@firstcluster.sz1xw3a.mongodb.net/?retryWrites=true&w=majority&appName=FirstCluster"

# ✅ Conexão segura com o certificado atualizado
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["projetobruno"]
collection = db["doces"]

try:
    client.admin.command('ping')
    print("✅ Conectado com sucesso ao MongoDB Atlas!")
except Exception as e:
    print("❌ Erro ao conectar:", e)



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.attributes('-fullscreen', True)

frame = ctk.CTkFrame(master=root)
frame.pack(fill='both', expand=True, padx=60, pady=50)

widgets_menu = []

title = ctk.CTkLabel(master=frame, text="DOCES", font=("Arial", 50))
title.pack(pady=(40, 80))
widgets_menu.append(title)


def b_adicionar():
    add_window = ctk.CTkToplevel(root)
    add_window.title("Adicionar Doce")
    add_window.geometry("600x400")

    ctk.CTkLabel(add_window, text="Nome da criança:").pack(pady=10)
    nome_entry = ctk.CTkEntry(add_window, width=300)
    nome_entry.pack()

    ctk.CTkLabel(add_window, text="Tipo do doce:").pack(pady=10)
    tipo_entry = ctk.CTkEntry(add_window, width=300)
    tipo_entry.pack()

    ctk.CTkLabel(add_window, text="Quantidade de doces:").pack(pady=10)
    qtd_entry = ctk.CTkEntry(add_window, width=300)
    qtd_entry.pack()

    def salvar_dado():
        nome = nome_entry.get()
        doce_tipo = tipo_entry.get()
        qtd_doce = qtd_entry.get()

        if not nome or not doce_tipo or not qtd_doce:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        doce_tipo_crp = fernet.encrypt(doce_tipo.encode())
        horario = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        data = {"child": nome, "candy_type": doce_tipo_crp, "qty": qtd_doce, "timestamp": horario}
        collection.insert_one(data)
        messagebox.showinfo("Sucesso", "Doce adicionado com sucesso!")
        add_window.destroy()

    ctk.CTkButton(add_window, text="Salvar", command=salvar_dado, width=150).pack(pady=20)


def b_listar():
    listar_window = ctk.CTkToplevel(root)
    listar_window.title("Lista de Doces")
    listar_window.geometry("800x600")

    todos_dados = collection.find()

    textbox = ctk.CTkTextbox(listar_window, width=750, height=550)
    textbox.pack(pady=10)

    for dado in todos_dados:
        textbox.insert("end", f"{dado}\n\n")

    textbox.configure(state="disabled")


def b_descriptografar():
    desc_window = ctk.CTkToplevel(root)
    desc_window.title("Descriptografar Doces")
    desc_window.geometry("800x600")

    textbox = ctk.CTkTextbox(desc_window, width=750, height=550)
    textbox.pack(pady=10)

    todos_dados = collection.find()
    for dado in todos_dados:
        try:
            tipo_doce_dcrp = fernet.decrypt(dado["candy_type"]).decode()
            texto = f"Criança: {dado['child']} | Doce: {tipo_doce_dcrp} | Quantidade: {dado['qty']}\n"
        except:
            texto = f"❌ Não foi possível descriptografar o doce de {dado.get('child', 'desconhecido')}\n"

        textbox.insert("end", texto)

    textbox.configure(state="disabled")

frame_botoes = ctk.CTkFrame(master=frame)
frame_botoes.pack(pady=30)

button_adicionar = ctk.CTkButton(master=frame_botoes, text="Adicionar", command=b_adicionar, width=200, height=60, font=("Arial", 26))
button_adicionar.pack(side="left", padx=30)
widgets_menu.append(button_adicionar)

button_listar = ctk.CTkButton(master=frame_botoes, text="Listar", command=b_listar, width=200, height=60, font=("Arial", 26))
button_listar.pack(side="left", padx=30)
widgets_menu.append(button_listar)

button_desc = ctk.CTkButton(master=frame_botoes, text="Descriptografar", command=b_descriptografar, width=250, height=60, font=("Arial", 26))
button_desc.pack(side="left", padx=30)
widgets_menu.append(button_desc)

root.mainloop()
