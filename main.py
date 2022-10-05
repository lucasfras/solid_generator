from tkinter import *
import numpy as np
import math

# Participantes
# Lucas Nicola Frassetto RA:201910454


#configuração tamanho janela
window_size = [1024,720]

root = Tk()
# Configuração da janela
root.title('Projeto 2')
root.configure(background='grey')

# Informacoes do poligono criado
centro = []
poligono = []

# Matrizes padrões para as operações
# Matriz de rotação
def matrizR(teta):
    return np.array([[math.cos(teta), -math.sin(teta)],
                     [math.sin(teta), math.cos(teta)]])

# Matriz de escala
def matrizE2d(sx, sy):
    return np.array([[sx, 0], 
                    [0, sy]])



# Funcao checagem validade poligono
def poligono_invalido():
    return not myInput5.get().isdigit() or len(poligono) < int(myInput5.get())


# Redesenhará o poligono no canvas
def redesenhar_poligono(novo_poligono):
    c.delete("all")
    c.create_polygon(novo_poligono, fill='green')
    poligono.clear()
    poligono.extend(novo_poligono)

# Função que retorna o centro do polígono
def calcular_centro(vertices):
     pontos_x = [vertice[0] for vertice in vertices]
     pontos_y = [vertice[1] for vertice in vertices]
     quantidade_vertices = len(vertices)
     x_central = sum(pontos_x) / quantidade_vertices
     y_central = sum(pontos_y) / quantidade_vertices
     return [x_central, y_central]

# Funcao escalar o tamanho do poligono
def escala(sx, sy):

    matriz = matrizE2d(sx, sy)

    poligono_transladado = []
    poligono_escalado = []
    novo_poligono = []

    poligono_atual = poligono

    print(poligono_atual)
    print(centro[0])
    print(centro[1])
    
    # Translaciona o poligono para a origem
    for i in range(len(poligono_atual)):
        x2 = poligono_atual[i][0] - centro[0]
        y2 = poligono_atual[i][1] - centro[1]
        poligono_transladado.append([x2, y2])
    
    print(poligono_transladado)

    # Realiza a operação de escala
    for i in range(len(poligono_transladado)):
        [x2, y2] = np.matmul(matriz, poligono_transladado[i])
        poligono_escalado.append([x2, y2])        


    print(poligono_escalado)

    for i in range(len(poligono_escalado)):
        x2 = poligono_escalado[i][0] + centro[0]
        y2 = poligono_escalado[i][1] + centro[1]
        novo_poligono.append([x2, y2])

    print(novo_poligono)
    redesenhar_poligono(novo_poligono)


# Funcao para transalacionar o poligono
def translacao(tx, ty):
    novo_poligono = []
    poligono_atual = poligono
    for i in range(len(poligono_atual)):  
        x2 = poligono_atual[i][0] + tx
        y2 = poligono_atual[i][1] + ty
        novo_poligono.append([x2, y2])  

    redesenhar_poligono(novo_poligono)

# Funcao para rotacionar o poligono
def rotacao(teta):
    matrizR2d = matrizR(teta)
    poligono_transladado = []
    poligono_rotacionado = []
    novo_poligono = []
    poligono_atual = poligono

    # Transladar o polígono para a origem
    for i in range(len(poligono_atual)):
        x2 = poligono_atual[i][0] - centro[0]
        y2 = poligono_atual[i][1] - centro[1]
        poligono_transladado.append([x2, y2])
    

    # Rotacionar os pontos do polígono
    for i in range(len(poligono_transladado)):
        [x2, y2] = np.matmul(matrizR2d, poligono_transladado[i])
        poligono_rotacionado.append([x2, y2])
    
    
    # Transladar o polígono para o centro
    for i in range(len(poligono_rotacionado)):
        x2 = poligono_rotacionado[i][0] + centro[0]
        y2 = poligono_rotacionado[i][1] + centro[1]
        novo_poligono.append([x2, y2])

    redesenhar_poligono(novo_poligono)
    
# Funcao criar pontos no canvas
def criar_ponto(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    c.create_oval(x1, y1, x2, y2, width=4, outline='green')

# Criacao do poligono no canvas
def callback(event):
    if (poligono_invalido()):
        criar_ponto(event)
        poligono.append([event.x, event.y])

    if (len(poligono) == int(myInput5.get())):
        criar_ponto(event)
        centro.extend(calcular_centro(poligono))
        c.delete("all")
        c.create_polygon(poligono, fill='green')

def button_click(number):
    if (number != 1 and poligono_invalido()): return
    
    # Limpar
    if number == 1:
        c.delete("all")
        poligono.clear()
        centro.clear()
    # Rotacionar poligono
    elif number == 2:
        rotacao(float(myInput1.get())*math.pi/180)
    # Escalar poligono
    elif number == 3:
        escala(float(myInput2.get()), float(myInput3.get()))
    # Translação para cima
    elif number == 4:
        translacao(0, -float(myInput4.get()))
    # Translação para direita
    elif number == 5:
        translacao(float(myInput4.get()), 0)
    # Translação para esquerda
    elif number == 6:
        translacao(-float(myInput4.get()), 0)
    # Translação para baixo
    elif number == 7:
        translacao(0, float(myInput4.get()))

#criando os elementos de interface
frame = Frame(root, bg='grey', padx=5, pady=5)
buttons = Frame(root, bg='grey', padx=5, pady=5)
c = Canvas(width=window_size[0], height=window_size[1],bg="white")


#posicionando os objetos na interface
frame.grid(row=0,column=0, padx=5, pady=5)
buttons.grid(row=1,column=0, padx=5, pady=5)
c.grid(row=1,column=1,padx=5,pady=5)
c.bind("<Button-1>", callback)




#os botões serão criados dentro do frame
myButton1=Button(frame, text='Limpar', width=20, fg='#fff', bg='red', pady=3, command=lambda:button_click(1))
myButton1.pack()

#interface selecao pontos
myLabel5=Label(frame, text="Quantidade de pontos", width=24, fg='#fff', bg='grey')
myLabel5.pack()
myInput5=Entry(frame, width=24)
myInput5.insert(0,4)
myInput5.pack()



# Bloco de rotação
myLabel1=Label(buttons, text="Quantidade graus", width=24, fg='#fff', bg='grey')
myLabel1.pack()
myInput1=Entry(buttons, width=24)
myInput1.insert(0,90)
myInput1.pack()
myButton2=Button(buttons, text='Rotacionar', fg='#fff', bg='green', width=20, pady=3, command=lambda:button_click(2))
myButton2.pack()

# Bloco de escala


myLabel2=Label(buttons, text="Escala em X", width=24, fg='#fff', bg='grey')
myLabel2.pack()
myInput2=Entry(buttons, width=24)
myInput2.insert(0,2)
myInput2.pack()
myLabel3=Label(buttons, text="Escala em Y", width=24, fg='#fff', bg='grey')
myLabel3.pack()
myInput3=Entry(buttons, width=24)
myInput3.insert(0,2)
myInput3.pack()
myButton3=Button(buttons, text='Escalar', fg='#fff', bg='green', width=20, pady=3, command=lambda:button_click(3))
myButton3.pack()


# Botões de translação

myLabel4=Label(buttons, text="Quantidade de translcao", width=24, fg='#fff', bg='grey')
myLabel4.pack()
myInput4=Entry(buttons, width=24)
myInput4.insert(0,20)
myInput4.pack()
myButton4=Button(buttons, text='Cima', fg='#fff', bg='purple', width=20, pady=3, command=lambda:button_click(4))
myButton4.pack()
myButton5=Button(buttons, text='Direita', fg='#fff', bg='purple', width=20, pady=3, command=lambda:button_click(5))
myButton5.pack()
myButton6=Button(buttons, text='Esquerda', fg='#fff', bg='purple', width=20, pady=3, command=lambda:button_click(6))
myButton6.pack()
myButton7=Button(buttons, text='Baixo', fg='#fff', bg='purple', width=20, pady=3, command=lambda:button_click(7))
myButton7.pack()

root.mainloop()