import matplotlib.image as mpimg
import numpy as np

# leitura da imagem
def LerImagem(nome):
    imagem = mpimg.imread(nome)
    return imagem

def Binarizar(imagem):
    aux = np.shape(imagem)

    if np.size(aux) > 2: # seleciona apenas uma matriz de cor caso a leitura seja rgb
        imagem = imagem[:,:,0]
        aux = np.shape(imagem)

    # imagem binária, 0 se for menor do que 128 e 1 maior do que 128

    ImgBin = np.zeros(aux)
    
    for x in range(aux[0]):
        for y in range(aux[1]):
            if imagem[x][y] >= 128:
                ImgBin[x][y] = 1
            else:
                ImgBin[x][y] = 0

    return ImgBin