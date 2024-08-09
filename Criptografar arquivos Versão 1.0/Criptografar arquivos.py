import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def derive_key_from_content(content):
    sha256_hash = hashlib.sha256(content).digest()
    return sha256_hash[:32]

def save_key(key, key_file_path):
    with open(key_file_path, 'wb') as f:
        f.write(key)

def load_key(key_file_path):
    with open(key_file_path, 'rb') as f:
        return f.read()

def get_next_folder_name(base_path, base_name="criptografia"):
    i = 1
    while True:
        folder_name = f"{base_name} {i:02d}"
        folder_path = os.path.join(base_path, folder_name)
        if not os.path.exists(folder_path):
            return folder_path
        i += 1

def encrypt_file(file_path, progress_callback):
    with open(file_path, 'rb') as f:
        content = f.read()
    
    key = derive_key_from_content(content)
    
    nonce = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted_content = encryptor.update(content) + encryptor.finalize()
    tag = encryptor.tag

    base_path = os.path.dirname(file_path)
    folder_path = get_next_folder_name(base_path)
    os.makedirs(folder_path)

    encrypted_file_path = os.path.join(folder_path, os.path.basename(file_path) + '.enc')
    key_file_path = os.path.join(folder_path, os.path.basename(file_path) + '.key')
    
    with open(encrypted_file_path, 'wb') as f:
        f.write(nonce + tag + encrypted_content)
    
    save_key(key, key_file_path)

    os.remove(file_path)

def decrypt_file(encrypted_file_path, key_file_path, progress_callback):
    if not os.path.exists(key_file_path):
        raise FileNotFoundError("Arquivo de chave não encontrado.")

    key = load_key(key_file_path)
    
    with open(encrypted_file_path, 'rb') as f:
        nonce, tag = f.read(12), f.read(16)
        encrypted_content = f.read()

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        plaintext = decryptor.update(encrypted_content) + decryptor.finalize()
    except Exception as e:
        raise ValueError("A descriptografia falhou. Verifique a chave e o arquivo.") from e

    return plaintext

def update_progress_bar(progress, total):
    progress_var.set(progress / total * 100)
    root.update_idletasks()

def start_encryption():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        progress_bar.start()
        try:
            encrypt_file(file_path, update_progress_bar)
            progress_bar.stop()
            progress_var.set(100)

            messagebox.showinfo("Informação", "Arquivo criptografado com sucesso.\nA chave para descriptografar foi salva no mesmo diretório do arquivo.")
        except Exception as e:
            progress_bar.stop()
            messagebox.showerror("Erro", f"Erro durante a criptografia: {e}")

def browse_encrypted_file():
    file_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.txt.enc")])
    if file_path:
        encrypted_file_entry.delete(0, tk.END)
        encrypted_file_entry.insert(0, file_path)

def browse_key_file():
    key_file_path = filedialog.askopenfilename(filetypes=[("Key Files", "*.key")])
    if key_file_path:
        key_file_entry.delete(0, tk.END)
        key_file_entry.insert(0, key_file_path)

def start_decryption():
    encrypted_file_path = encrypted_file_entry.get()
    key_file_path = key_file_entry.get()

    if not encrypted_file_path or not key_file_path:
        messagebox.showwarning("Aviso", "Por favor, selecione o arquivo criptografado e o arquivo de chave.")
        return

    progress_bar.start()
    try:
        plaintext = decrypt_file(encrypted_file_path, key_file_path, update_progress_bar)
        decrypted_file_path = encrypted_file_path[:-4]
        with open(decrypted_file_path, 'wb') as f:
            f.write(plaintext)
        
        os.remove(encrypted_file_path)
        os.remove(key_file_path)
        progress_bar.stop()
        progress_var.set(100)

        messagebox.showinfo("Informação", "Arquivo descriptografado com sucesso.")
    except Exception as e:
        progress_bar.stop()
        messagebox.showerror("Erro", f"Erro durante a descriptografia: {e}")

def create_gui():
    global root, progress_bar, progress_var, encrypted_file_entry, key_file_entry

    root = tk.Tk()
    root.title("Criptografia de Arquivo Versão 1.0")

    root.geometry("500x400")

    encrypt_button = tk.Button(root, text="Selecionar Arquivo .txt para Criptografar", command=start_encryption)
    encrypt_button.pack(pady=10, padx=10)

    tk.Label(root, text="Arquivo Criptografado:").pack(pady=5)
    encrypted_file_entry = tk.Entry(root, width=50)
    encrypted_file_entry.pack(pady=5)
    encrypted_file_button = tk.Button(root, text="Selecionar Arquivo Criptografado", command=browse_encrypted_file)
    encrypted_file_button.pack(pady=5)

    tk.Label(root, text="Arquivo de Chave:").pack(pady=5)
    key_file_entry = tk.Entry(root, width=50)
    key_file_entry.pack(pady=5)
    key_file_button = tk.Button(root, text="Selecionar Arquivo de Chave", command=browse_key_file)
    key_file_button.pack(pady=5)

    decrypt_button = tk.Button(root, text="Descriptografar Arquivo", command=start_decryption, width=30, height=2)
    decrypt_button.pack(pady=20, padx=10)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, length=400, mode='determinate', variable=progress_var)
    progress_bar.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
