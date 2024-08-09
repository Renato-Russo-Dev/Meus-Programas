import tkinter as tk
from tkinter import ttk
import time

def atualizar_frases_e_barra_progresso(loading_window, progress_bar, frase_label, frases):
    for frase in frases:
        frase_label.config(text=frase)
        loading_window.update()
        time.sleep(2) 
        progress_bar.step(33.3)  

def iniciar_leitor_de_mente():
   
    loading_window = tk.Toplevel(root)
    loading_window.title("Carregando...")
    loading_window.geometry("300x100")

    frase_label = ttk.Label(loading_window, text="", font=("Arial", 12))
    frase_label.pack(pady=(10, 0))

    progress_bar = ttk.Progressbar(loading_window, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack(pady=10)

    frases = ["checando atividade cerebral", "acessando memórias", "realizando tomografia do córtex cerebral"]

    
    atualizar_frases_e_barra_progresso(loading_window, progress_bar, frase_label, frases)

   
    desenvolvido_label = ttk.Label(loading_window, text="Desenvolvido por Renato Russo", font=("Arial", 8))
    desenvolvido_label.pack(side="bottom", anchor="se", padx=10, pady=5)

    
    resposta_window = tk.Toplevel(root)
    resposta_window.title("Resposta")
    resposta_window.geometry("400x100")  

    resposta_label = ttk.Label(resposta_window, text=f"O número você pensou é: {entrada.get()}", font=("Arial", 16))  # Ajustar a fonte para torná-la mais legível
    resposta_label.pack(pady=20)

    
    desenvolvido_label = ttk.Label(resposta_window, text="Desenvolvido por Renato Russo", font=("Arial", 8))
    desenvolvido_label.pack(side="bottom", anchor="se", padx=10, pady=5)


root = tk.Tk()
root.title("Leitor de Mente")
# coloquei um espaço pq a janela tava bugando kkkkkkkk
#LEMBRAR DE COLOCAR PRA NÃO BUGAR COM LETRA
titulo_label = ttk.Label(root, text="                   Pense em um número                 ", font=("Arial", 12))
titulo_label.pack(pady=10)

entrada = ttk.Entry(root, font=("Arial", 12))
entrada.pack(pady=10)

botao_iniciar = ttk.Button(root, text="Iniciar", command=iniciar_leitor_de_mente)
botao_iniciar.pack(pady=10)

root.mainloop()
