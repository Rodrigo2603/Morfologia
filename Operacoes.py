import utils
import numpy as np
import matplotlib.pyplot as plt

def Erosion(imagem, SE, centrox, centroy):
    aux = np.shape(imagem)

    if np.size(aux) > 2:
        imagem = imagem[:,:,0] # seleciona apenas uma matriz de cor caso a leitura seja rgb
        aux = np.shape(imagem)

    ImgErod = [] # array vazio que será responsável pelas colunas da imagem
    ImgLinha = [] # array vazio que será responsável pelas linhas da imagem
    tam = np.shape(SE) # tamanho do elemento estruturante (SE)
    check = 0 # flag para indicar se o SE está completamente contido no objeto
    total = 0 # flag para indicar a quantidade de pixels 1 dentro do elemento estruturante

    for u in range(tam[0]):
        for v in range(tam[1]):
            if SE[u][v] != 0:
                total += 1 # contagem da quantidade de pixels maior que zero

    for x in range(aux[0]):
        for y in range(aux[1]):
            if imagem[x][y] == 1: # verifica se o pixel sobre analise é branco
                for u in range(0-centrox,tam[0]-centrox):
                    for v in range(0-centroy,tam[1]-centroy):
                        if x+u >= 0 and x+u <aux[0] and y+v >= 0 and y+v < aux[1]: 
                            # incrementa o flag se o SE está td contido no objeto
                            check += SE[u+centrox][v+centroy]*imagem[x+u][y+v] 
                if check == total: # se o SE está td contido no objeto da imagem
                    ImgLinha.append(1) # adiciona-se um pixel igual a 1
                else: # caso contrário, adiciona-se um pixel igual a 0
                    ImgLinha.append(0)
                check = 0
            else:
                ImgLinha.append(0)
        ImgErod.append(ImgLinha) # se adiciona-se uma nova coluna no array
        ImgLinha = []

    return ImgErod

def Dilation(imagem, SE, centrox, centroy):
    aux = np.shape(imagem)

    if np.size(aux) > 2:
        imagem = imagem[:,:,0] # seleciona apenas uma matriz de cor caso a leitura seja rgb
        aux = np.shape(imagem)
    
    for x in range(aux[0]): # cria-se o complemento da imagem
        for y in range(aux[1]):
            imagem[x][y] = 1 - imagem[x][y]

    ImgDilat = Erosion(imagem, SE, centrox, centroy) # erode o complemento da imagem

    for x in range(aux[0]): # tira-se o complemento da imagem erodida
        for y in range(aux[1]):
            ImgDilat[x][y] = 1 - ImgDilat[x][y]

    # corrige os valores das bordas

    ImgDilat[:][-1] = ImgDilat[:][-2] 
    ImgDilat[:][0] = ImgDilat[:][1]
    ImgDilat[0][:] = ImgDilat[1][:]
    ImgDilat[-1][:] = ImgDilat[-2][:] 

    return ImgDilat

def Opening(imagem,SE,centrox,centroy):
    ImgOpen = Dilation(Erosion(imagem,SE,centrox,centroy),SE,centrox,centroy)
    return ImgOpen

def Closing(imagem,SE,centrox,centroy):
    ImgClose = Erosion(Dilation(imagem,SE,centrox,centroy),SE,centrox,centroy)
    return ImgClose
    