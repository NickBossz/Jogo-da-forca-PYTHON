import pandas as pd
import tkinter
import string
from random import randint
from time import sleep
import os
import sys
import atexit

alfabeto = list(string.ascii_lowercase)
BotaoAntigo = "Vazio"
TracoAntigo = "Vazio"
Acertos = 0
VidasDoPlayer = 6

def funcao_saida():
    os.remove("palavras_NAO_APAGUE.txt")

atexit.register(funcao_saida)

def ColocarCoordenadas(janelaDesejada):
    def atualizar_coordenadas(event):
        coordenadas = f"X: {event.x}, Y: {event.y}"
        label_coordenadas.config(text=coordenadas)
        
    label_coordenadas = tkinter.Label(janelaDesejada, text="X: 0, Y: 0")
    label_coordenadas.pack()

    janelaDesejada.bind("<Motion>", atualizar_coordenadas)



def IniciarJogo():
    JanelaInicial.destroy()
    Janela = tkinter.Tk()
    Janela.geometry("933x600")
    Janela.title("Jogo da forca")


    ColocarCoordenadas(Janela)
    Desenho = tkinter.Canvas(Janela, width=933, height=600)
    Desenho.pack()
    
    Desenho.create_line(20, 50, 20, 250)
    Desenho.create_line(20, 50, 133, 50)
    Desenho.create_line(133, 50, 133, 100)


    Botoes = {}
    def AoApertarBotao(indice2):
        global VidasDoPlayer
        global BotaoAntigo
        global TracoAntigo
        global Acertos


        botaoApertado = Botoes[indice2]
        letra = botaoApertado['text']
        if letra.lower() in PalavraEscolhida.lower():
            botaoApertado.config(bg="green")
     

        else:
            botaoApertado.config(bg="red")
            if VidasDoPlayer == 6:
                Desenho.create_oval(110,80,150,120, fill="blue")
                VidasDoPlayer -= 1
            elif VidasDoPlayer == 5:
                Desenho.create_line(129,121,129,162, fill="blue")
                VidasDoPlayer -= 1
            elif VidasDoPlayer == 4:
                Desenho.create_line(129,130, 115, 136, fill="blue")
                VidasDoPlayer -= 1
            elif VidasDoPlayer == 3:
                Desenho.create_line(129,130, 143, 136, fill="blue")
                VidasDoPlayer -= 1
            elif VidasDoPlayer == 2:
                Desenho.create_line(129,162, 115, 172, fill="blue")
                VidasDoPlayer -= 1
            elif VidasDoPlayer == 1:
                Desenho.create_line(129,162,143, 172, fill="blue")
                VidasDoPlayer -= 1
                Janela.destroy()

                def AssimQueFechar():
                    JanelaVocePerdeu.destroy()
                    quit()

                JanelaVocePerdeu = tkinter.Tk()
                JanelaVocePerdeu.geometry("400x200")
                JanelaVocePerdeu.title("Voce perdeu")
                LabelPalavra = tkinter.Label(JanelaVocePerdeu, text="A palavra era: " + PalavraEscolhida, font=("Arial", 20, "bold"))
                LabelVocePerdeu = tkinter.Label(JanelaVocePerdeu, text="Você perdeu!", font=("Arial", 20, "bold"), fg="red")
                LabelVocePerdeu.pack()
                LabelPalavra.place(x=25, y=100)
                JanelaVocePerdeu.mainloop()

        for i in range(len(PalavraEscolhida)):
            caractere = PalavraEscolhida[i]
            if caractere.lower() == letra.lower():
                Labels[i].config(text=letra)
                Acertos += 1
                if Acertos == len(PalavraEscolhida):
                    Janela.destroy()
                    def alterar_cores(contador=0):
                        if contador < 1000:
                            if contador % 2 == 0:
                                label_voce_ganhou.config(fg="blue")
                            else:
                                label_voce_ganhou.config(fg="yellow")

                            janela_voce_ganhou.after(500, alterar_cores, contador + 1)
                        else:
                            label_voce_ganhou.config(fg="green")

                    janela_voce_ganhou = tkinter.Tk()
                    janela_voce_ganhou.geometry("400x100")
                    janela_voce_ganhou.title("Você ganhou")

                    label_voce_ganhou = tkinter.Label(janela_voce_ganhou, text="Você ganhou!", font=("Arial", 20, "bold"), fg="green")
                    label_voce_ganhou.pack()

                    janela_voce_ganhou.after(5, alterar_cores)
                    janela_voce_ganhou.mainloop()
                    


            
    

    global BotaoAntigo
    for indice in range(len(alfabeto)):
        letra = alfabeto[indice]
        Botoes[indice] = tkinter.Button(Janela, text=letra.upper(), padx=20, pady=20, font=("Arial", 9, "bold"), command=lambda indice2=indice: AoApertarBotao(indice2))
        if BotaoAntigo != "Vazio":
            if BotaoAntigo.winfo_x() > 800:
                Botoes[indice].place(x=(20), y=BotaoAntigo.winfo_y() + 100)
            else:
                Botoes[indice].place(x=(20 + BotaoAntigo.winfo_x() + 40), y=BotaoAntigo.winfo_y())
            
            Botoes[indice].update_idletasks()
            print(Botoes[indice].winfo_rootx())
        else:
            Botoes[indice].place(x=20, y=300)
            Botoes[indice].update_idletasks()
            print(Botoes[indice].winfo_rootx())
        BotaoAntigo = Botoes[indice]

    PalavrasEscritas = pd.read_csv("palavras.txt")

    regex = r'^[a-zA-Z\s]+$'

    df_filtrado = PalavrasEscritas[PalavrasEscritas.iloc[:, 0].str.match(regex)]
    df_filtrado.to_csv("palavras_NAO_APAGUE.txt", index=False, header=False)
    
    Palavras = pd.read_csv("palavras_NAO_APAGUE.txt")

    NumeroAleatorio = randint(0, Palavras.shape[0] - 1)
    PalavraEscolhida = Palavras.values[NumeroAleatorio][0]


    Labels = {}
    x1 = None 
    x2 = None

    yPlace = 190
    for i in range(len(PalavraEscolhida)):
        caractere = PalavraEscolhida[i]
        if caractere != " ":
            print(PalavraEscolhida)
            if x1 == None and x2 == None:
                Desenho.create_line(187, 195, 210, 195)
                x1 = 187
                x2 = 210

                Labels[i] = tkinter.Label(Janela, text=" ")
                Labels[i].place(x=(x1+5), y=yPlace)
            else:
                Desenho.create_line(x1 + 30, 195, x2 + 30, 195)
                x1 = x1 + 30
                x2 = x2 + 30

                Labels[i] = tkinter.Label(Janela, text=" ")
                Labels[i].place(x=(x1+5), y=yPlace)
        else:
            Desenho.create_line(x1 + 30, 190, x2 + 30, 190, fill="red")
            x1 = x1 + 30
            x2 = x2 + 30


    Janela.mainloop()

def FecharJanela(JalenaEscolhida):
    JalenaEscolhida.destroy()


JanelaInicial = tkinter.Tk()
JanelaInicial.geometry("400x100")

# Criação do botão iniciar

Botao = tkinter.Button(JanelaInicial, text="Iniciar", padx=50, pady=20, font=("Arial", 15, "bold"), command=IniciarJogo, bg="green")
Botao.place(x=35,y=10)

# Criação do botão fechar
Botao2 = tkinter.Button(JanelaInicial, text="Fechar", padx=50, pady=20, font=("Arial", 15, "bold"), command=lambda JanelaEscolhida=JanelaInicial: FecharJanela(JanelaEscolhida), bg="red")
Botao2.place(x=205, y=10)

JanelaInicial.mainloop()