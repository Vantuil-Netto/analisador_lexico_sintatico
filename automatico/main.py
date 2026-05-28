# automatico/main.py
# Ponto de entrada para o Analisador Léxico Automático (PLY)

import sys
import os

# Adiciona a pasta raiz do projeto ao sys.path para permitir execução direta (ex: python automatico/main.py)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from automatico.gui.interface import GolCompilerGUI


def main():
    """Função principal que inicia a aplicação"""
    root = tk.Tk()
    app = GolCompilerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
