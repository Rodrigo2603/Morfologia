import numpy as np
from PIL import Image
import os
import rich.console as Console

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def erode(image, kernel):
    # Converter a imagem para escala de cinza (L) usando numpy
    img_gray = np.array(image.convert('L'))
    height, width = img_gray.shape
    kernel_height, kernel_width = len(kernel), len(kernel[0])

    # Verificar se o kernel tem dimensões ímpares
    if kernel_height % 2 == 0 or kernel_width % 2 == 0:
        raise ValueError("O kernel precisa ter dimensões ímpares.")

    pad_height = kernel_height // 2
    pad_width = kernel_width // 2

    # Verificar se a imagem tem dimensões válidas
    if width <= kernel_width or height <= kernel_height:
        raise ValueError("A imagem é muito pequena para o kernel fornecido.")

    # Criar uma imagem de saída preenchida com zeros
    output = Image.new('L', (width, height), 0)
    output_pixels = output.load()

    # Aplicar a erosão
    for i in range(pad_height, height - pad_height):
        for j in range(pad_width, width - pad_width):
            region_match = True

            # Verificar cada posição do kernel
            for ki in range(kernel_height):
                for kj in range(kernel_width):
                    if kernel[ki][kj] == 1:
                        pixel_value = img_gray[i + ki - pad_height, j + kj - pad_width]
                        if pixel_value != 255:
                            region_match = False
                            break
                if not region_match:
                    break

            # Definir o pixel de saída como branco se a região coincidir
            if region_match:
                output_pixels[j, i] = 255

    # Salvar e retornar a imagem erodida
    output.save('imagem_erosao.png')
    return output

def dilate(image, kernel, condition):
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
                
    
    # Verificar se o arquivo já existe e criar um novo nome se necessário
    file_path = os.path.join('imagens', 'imagem_dilatacao.png')
    base, ext = os.path.splitext(file_path)
    counter = 1
    while os.path.exists(file_path):
        file_path = f"{base}_{counter}{ext}"
        counter += 1

    dilated_image = Image.fromarray(output)

    if condition == True:
        return dilated_image
    else:
        dilated_image.save(file_path)

def opening(image_path, kernel):
    image = Image.open(image_path).convert('L')
    
    # Aplicar erosão
    eroded_image = erode(image, kernel, True)
    
    # Aplicar dilatação na imagem erodida
    dilated_image = dilate(eroded_image, kernel, True)
    
    # Verificar se o arquivo já existe e criar um novo nome se necessário
    file_path = os.path.join('imagens', 'imagem_abertura.png')
    base, ext = os.path.splitext(file_path)
    counter = 1
    while os.path.exists(file_path):
        file_path = f"{base}_{counter}{ext}"
        counter += 1

    dilated_image.save(file_path)

def closing(image_path, kernel):
    image = Image.open(image_path).convert('L')
    
    # Aplicar dilatação
    dilated_image = dilate(image, kernel, True)
    
    # Aplicar erosão na imagem dilatada
    eroded_image = erode(dilated_image, kernel, True)
    
    # Verificar se o arquivo já existe e criar um novo nome se necessário
    file_path = os.path.join('imagens', 'imagem_fechamento.png')
    base, ext = os.path.splitext(file_path)
    counter = 1
    while os.path.exists(file_path):
        file_path = f"{base}_{counter}{ext}"
        counter += 1
        
    eroded_image.save(file_path)

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

    while True:
        
        clear_terminal()
        
        pasta = 'imagens'
        listar_imagens('imagens')
        
        while True:
            imagem_escolhida = int(console.input(f"\nSelecione o número da imagem (1-{len(os.listdir(pasta))}): "))
            if 1 <= imagem_escolhida <= len(os.listdir(pasta)):
                break
            else:
                console.print("Número inválido. Tente novamente.", style="bold red")
                
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
        console.print("'e' para [bold magenta]erosão[/bold magenta]", style="bold")
        console.print("'d' para [bold blue]dilatação[/bold blue]", style="bold")
        console.print("'a' para [bold green]abertura[/bold green]", style="bold")
        console.print("'f' para [bold yellow]fechamento[/bold yellow]", style="bold")
        console.print("'x' para [bold red]sair[/bold red]", style="bold")
        
        escolha = console.input("\nEscolha uma opção: ").strip().lower()
        
        # De acordo com a escolha do usuário, chama a função correspondente
        
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
            case 'x':
                break
            case _:
                console.print("Opção inválida. Tente novamente.", style="bold red")

if __name__ == "__main__":
    main()
