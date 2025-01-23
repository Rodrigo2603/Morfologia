import matplotlib.pyplot as plt
import utils
import Operacoes
import os
from rich.console import Console
from rich.prompt import Prompt

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def executa_morfologia(imagem1, kernel, cx, cy):
    
    for ext in ['jpg', 'jpeg', 'png']:
        try:
            ImgOriginal = utils.LerImagem(f"./imagens/{imagem1}.{ext}")
            ImgOriginal = utils.Binarizar(ImgOriginal)
            break
        except FileNotFoundError:
            continue
    else:
        raise FileNotFoundError(f"Imagem {imagem1} não encontrada nos formatos jpg, jpeg ou png.")

    fig, [ax1,ax2] = plt.subplots(1,2)
    ax1.imshow(ImgOriginal,cmap='gray')
    
    clear_terminal()    
    
    # Executa a escolha para Erosão, Dilatação, Abertura e Fechamento
    console.print("\n[bold blue]Escolha a operação desejada:[/bold blue]\n")
    console.print("[bold yellow]1[/bold yellow]: [bold magenta]Erosão[/bold magenta]")
    console.print("[bold yellow]2[/bold yellow]: [bold magenta]Dilatação[/bold magenta]")
    console.print("[bold yellow]3[/bold yellow]: [bold magenta]Abertura[/bold magenta]")
    console.print("[bold yellow]4[/bold yellow]: [bold magenta]Fechamento[/bold magenta]")
    
    operacao = Prompt.ask("\n[blue]Escolha o número da operação que deseja realizar [blue]", console=console)
    
    match operacao:
        case "1":
            imagem = Operacoes.Erosion(ImgOriginal,kernel,cx,cy)
        case "2":
            imagem = Operacoes.Dilation(ImgOriginal,kernel,cx,cy)
        case "3":
            imagem = Operacoes.Opening(ImgOriginal,kernel,cx,cy)
        case "4":
            imagem = Operacoes.Closing(ImgOriginal,kernel,cx,cy)
        case _:
            console.print("\n[bold red]Escolha uma operação válida![/bold red]")
            return

    ax2.imshow(imagem,cmap='gray')
    plt.show()

if __name__ == '__main__':
        
    clear_terminal()    
    
    console = Console()

    console.print("\n[bold italic red]Morfologia - T01 (PID)[/bold italic red]\n")
    
    def listar_imagens(diretorio):
        
        console = Console()
        
        imagens = [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]
        console.print("\n[bold blue]Imagens disponíveis:[/bold blue]\n")
        for i, imagem in enumerate(imagens):
            console.print(f"[bold yellow]{i}[/bold yellow]: [bold magenta]{imagem}[/bold magenta]")
        return imagens
    

    kernel = [[0,1,0],[1,1,1],[0,1,0]]
    kernel1 = [[0,1,0],[1,1,1],[0,0,0]]
    kernel2 = [[1,1,1],[1,1,1],[1,1,1]]

    diretorio_imagens = "./imagens"
    imagens_disponiveis = listar_imagens(diretorio_imagens)

    
    while True:
            
        escolha = int(Prompt.ask("\n[blue]Escolha o número da imagem que deseja usar [blue]", console=console))
        if escolha >= 0 and escolha < len(imagens_disponiveis):
            break
        else:  
            console.print("\n[bold red]Escolha um número válido![/bold red]")
            
    
    imagem_escolhida = imagens_disponiveis[escolha].split('.')[0]
    
    executa_morfologia(imagem_escolhida, kernel2, 1, 1)