import customtkinter as ctk

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
    for widget in widgets_menu:
        widget.pack_forget()

# Criar um frame apenas para os botões lado a lado
frame_botoes = ctk.CTkFrame(master=frame)
frame_botoes.pack(pady=30)

button_adicionar = ctk.CTkButton(master=frame_botoes, text="Adicionar", command=b_adicionar, width=200, height=60, font=("Arial", 26))
button_adicionar.pack(side="left", padx=30)
widgets_menu.append(button_adicionar)

button_listar = ctk.CTkButton(master=frame_botoes, text="Listar", command=b_adicionar, width=200, height=60, font=("Arial", 26))
button_listar.pack(side="left", padx=30)
widgets_menu.append(button_listar)

button_desc = ctk.CTkButton(master=frame_botoes, text="Descriptografar", command=b_adicionar, width=250, height=60, font=("Arial", 26))
button_desc.pack(side="left", padx=30)
widgets_menu.append(button_desc)

root.mainloop()
