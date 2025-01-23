import matplotlib.pyplot as plt
import utils
import Operacoes

def teste(imagem1, kernel, cx, cy):
    ImgOriginal = utils.LerImagem("./imagens/{}.jpg".format(imagem1))
    ImgOriginal = utils.Binarizar(ImgOriginal)

    fig, [ax1,ax2] = plt.subplots(1,2)
    ax1.imshow(ImgOriginal,cmap='gray')
    imagem = Operacoes.Erosion(ImgOriginal,kernel,cx,cy)

    ax2.imshow(imagem,cmap='gray')
    plt.show()

if __name__ == '__main__':
    kernel = [[0,1,0],[1,1,1],[0,1,0]]
    kernel1 = [[0,1,0],[1,1,1],[0,0,0]]
    kernel2 = [[1,1,1],[1,1,1],[1,1,1]]

    teste('Image_(2a)', kernel2, 1, 1)