import tkinter as tk
import asyncio
import edge_tts
import pygame
import os

class AppTTS:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistente TTS - 1.0")
        self.root.geometry("480x250")

        # Interface gráfica
        self.label = tk.Label(root, text="Digite o que você quer dizer:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.entrada = tk.Entry(root, width=55, font=("Arial", 12))
        self.entrada.pack(pady=5)

        self.checkbox_var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(root, text="Ouvir também (reproduzir no seu fone)", variable=self.checkbox_var, font=("Arial", 10))
        self.checkbox.pack(pady=5)

        self.botao_feminino = tk.Button(root, text="Falar com voz feminina", command=self.falar_feminino, bg="#d1e7dd", font=("Arial", 11))
        self.botao_feminino.pack(pady=5)

        self.botao_masculino = tk.Button(root, text="Falar com voz masculina", command=self.falar_masculino, bg="#dbe7f1", font=("Arial", 11))
        self.botao_masculino.pack(pady=5)

    def falar_feminino(self):
        texto = self.entrada.get()
        if texto.strip():
            asyncio.run(self.falar_com_edge(texto, "pt-BR-FranciscaNeural"))

    def falar_masculino(self):
        texto = self.entrada.get()
        if texto.strip():
            asyncio.run(self.falar_com_edge(texto, "pt-BR-AntonioNeural"))

    async def falar_com_edge(self, texto, voz):
        communicate = edge_tts.Communicate(texto, voice=voz)
        output_file = "fala_temp.mp3"
        await communicate.save(output_file)

        # Se "ouvir também" estiver marcado, toca no seu fone + Discord
        if self.checkbox_var.get():
            # Reproduz com o dispositivo padrão (fone)
            pygame.mixer.init()
        else:
            # Apenas para o Discord via VB-Cable
            pygame.mixer.init(devicename="CABLE Input (VB-Audio Virtual Cable)")

        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()
        os.remove(output_file)

# Executar a interface
if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("icon.ico")
    root.geometry("300x200")
    app = AppTTS(root)
    root.mainloop()
