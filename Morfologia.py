import numpy as np
from PIL import Image

def erode(image, kernel):
    img_array = np.array(image.convert('L'))  # Garantir que a imagem seja convertida para escala de cinza (L)
    
    # Verificar se a imagem tem apenas 2 dimensões (escala de cinza)
    if img_array.ndim != 2:
        raise ValueError("A imagem precisa ser em escala de cinza (2D).")
    
    output = np.zeros_like(img_array)
    
    # Garantir que o kernel tenha tamanho ímpar
    if kernel.shape[0] % 2 == 0 or kernel.shape[1] % 2 == 0:
        raise ValueError("O kernel precisa ter dimensões ímpares.")
    
    pad_height = kernel.shape[0] // 2
    pad_width = kernel.shape[1] // 2
    
    # Verificar se a imagem tem dimensões válidas
    if img_array.shape[0] <= kernel.shape[0] or img_array.shape[1] <= kernel.shape[1]:
        raise ValueError("A imagem é muito pequena para o kernel fornecido.")
    
    padded_image = np.pad(img_array, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant', constant_values=0)
    
    for i in range(pad_height, padded_image.shape[0] - pad_height):
        for j in range(pad_width, padded_image.shape[1] - pad_width):
            region = padded_image[i - pad_height:i + pad_height + 1, j - pad_width:j + pad_width + 1]
            if np.all(region[kernel == 1] == 255):
                output[i - pad_height, j - pad_width] = 255
                
    eroded_image = Image.fromarray(output)
    eroded_image.save('imagem_erosao.png')  # Salvar a imagem de erosão

    return eroded_image

def dilate(image, kernel):
    img_array = np.array(image.convert('L'))  # Garantir que a imagem seja convertida para escala de cinza (L)
    
    # Verificar se a imagem tem apenas 2 dimensões (escala de cinza)
    if img_array.ndim != 2:
        raise ValueError("A imagem precisa ser em escala de cinza (2D).")
    
    output = np.zeros_like(img_array)
    
    # Garantir que o kernel tenha tamanho ímpar
    if kernel.shape[0] % 2 == 0 or kernel.shape[1] % 2 == 0:
        raise ValueError("O kernel precisa ter dimensões ímpares.")
    
    pad_height = kernel.shape[0] // 2
    pad_width = kernel.shape[1] // 2
    
    padded_image = np.pad(img_array, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant', constant_values=0)
    
    for i in range(pad_height, padded_image.shape[0] - pad_height):
        for j in range(pad_width, padded_image.shape[1] - pad_width):
            region = padded_image[i - pad_height:i + pad_height + 1, j - pad_width:j + pad_width + 1]
            if np.any(region[kernel == 1] == 255):
                output[i - pad_height, j - pad_width] = 255
                
    dilated_image = Image.fromarray(output)
    dilated_image.save('imagem_dilatacao.png')  # Salvar a imagem de dilatação

    return dilated_image

def opening(image_path, kernel):
    image = Image.open(image_path).convert('L')  # Abrir a imagem e converter para escala de cinza (L)
    
    # Aplicar erosão
    eroded_image = erode(image, kernel)
    
    # Aplicar dilatação na imagem erodida
    dilated_image = dilate(eroded_image, kernel)
    dilated_image.save('imagem_abertura.png')  # Salvar a imagem de abertura

def closing(image_path, kernel):
    image = Image.open(image_path).convert('L')  # Abrir a imagem e converter para escala de cinza (L)
    
    # Aplicar dilatação
    dilated_image = dilate(image, kernel)
    
    # Aplicar erosão na imagem dilatada
    eroded_image = erode(dilated_image, kernel)
    eroded_image.save('imagem_fechamento.png')  # Salvar a imagem de fechamento

def main():
    image_path = 'teste3.png'  # Substitua com o caminho da sua imagem
    kernel = np.ones((51, 51), np.uint8)  # Kernel 3x3
    
    escolha = input("Opções:\n'e' para erosão\n'd' para dilatação\n'a' para abertura\n'f' para fechamento\n").strip().lower()
    
    if escolha == 'e':
        image = Image.open(image_path).convert('L')  # Abrir a imagem e converter para escala de cinza (L)
        erode(image, kernel)
    elif escolha == 'd':
        image = Image.open(image_path).convert('L')  # Abrir a imagem e converter para escala de cinza (L)
        dilate(image, kernel)
    elif escolha == 'a':
        opening(image_path, kernel)      
    elif escolha == 'f':
        closing(image_path, kernel)
    else:
        print("Escolha inválida.")

if __name__ == "__main__":
    main()