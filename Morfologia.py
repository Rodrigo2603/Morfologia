import numpy as np
from PIL import Image
import os
import rich.console as Console

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

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
    eroded_image.save('imagem_erosao.png')

    return eroded_image

def dilate(image, kernel):
    img_array = np.array(image.convert('L'))
    
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
    dilated_image.save('imagem_dilatacao.png') 

    return dilated_image

def opening(image_path, kernel):
    image = Image.open(image_path).convert('L')
    
    # Aplicar erosão
    eroded_image = erode(image, kernel)
    
    # Aplicar dilatação na imagem erodida
    dilated_image = dilate(eroded_image, kernel)
    dilated_image.save('imagem_abertura.png')

def closing(image_path, kernel):
    image = Image.open(image_path).convert('L')
    
    # Aplicar dilatação
    dilated_image = dilate(image, kernel)
    
    # Aplicar erosão na imagem dilatada
    eroded_image = erode(dilated_image, kernel)
    eroded_image.save('imagem_fechamento.png')

def main():
    
    clear_terminal()
    
    # Cria o console
    console = Console.Console()
    
    # Listar imagens na pasta 'imagens'
    def listar_imagens(pasta):
        console.print("\nImagens disponíveis:")
        imagens = [f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]
        for i, imagem in enumerate(imagens, start=1):
            console.print(f"{i}. {imagem}", style="green")

    pasta = 'imagens'
    listar_imagens('imagens')
    
    imagem_escolhida = int(console.input(f"\nSelecione o número da imagem (1-{len(os.listdir(pasta))}): "))
    image_path = os.path.join(pasta, os.listdir(pasta)[imagem_escolhida - 1])
    
    clear_terminal()
    
    # Determinando o tamanho do kernel, só podendo ser ímpar
    while True:
        kernel_size = int(console.input(f"Digite o tamanho do kernel [bold red](apenas números ímpares)[/bold red]: "))
        if kernel_size % 2 != 0:
            break
        else:
            print("O tamanho do kernel precisa ser um número ímpar. Tente novamente.")
    
    # Criando o kernel com valores 1
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    
    clear_terminal()
    
    console.print(f"Imagem selecionada: [purple]{os.path.basename(image_path)}[/purple]\n", style="bold")
    console.print("Opções:", style="bold underline")
    console.print("'e' para [bold red]erosão[/bold red]", style="bold")
    console.print("'d' para [bold blue]dilatação[/bold blue]", style="bold")
    console.print("'a' para [bold green]abertura[/bold green]", style="bold")
    console.print("'f' para [bold yellow]fechamento[/bold yellow]", style="bold")
    
    escolha = console.input("\nEscolha uma opção: ").strip().lower()
    
    match escolha:
        case 'e':
            image = Image.open(image_path).convert('L')
            erode(image, kernel)
        case 'd':
            image = Image.open(image_path).convert('L')
            dilate(image, kernel)
        case 'a':
            opening(image_path, kernel)
        case 'f':
            closing(image_path, kernel)
        case _:
            print("Escolha inválida.")

if __name__ == "__main__":
    main()
