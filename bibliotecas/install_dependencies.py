import os

def install_dependencies():
    os.system('pip install -r requirements.txt')

if __name__ == "__main__":
    install_dependencies()