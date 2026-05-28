# manual/gui/interface.py
# Interface Gráfica (GUI) em Tkinter

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from manual.core.lexer import LexerGol


class GolCompilerGUI:
    """
    Interface Gráfica para o Analisador Léxico Manual Gol++
    Implementada em Tkinter
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gol++ Compiler - Analisador Léxico (Manual)")
        self.root.geometry("1000x650")
        self.root.configure(bg="#1E1E1E")  # Tema escuro estilo VS Code

        self.lexer = LexerGol()

        # Configuração de Estilo
        self.fonte_padrao = ("Consolas", 11)
        self.cor_bg = "#252526"
        self.cor_fg = "#D4D4D4"
        self.cor_btn = "#007ACC"
        
        self.montar_interface()

    def montar_interface(self):
        """Monta a interface gráfica completa"""
        # Título
        titulo = tk.Label(self.root, text="⚽ Gol++ Analisador Léxico (Manual)", font=("Segoe UI", 16, "bold"), bg="#1E1E1E", fg="#4CAF50")
        titulo.pack(pady=10)

        # Frame Principal (dividido em Esquerda e Direita)
        main_frame = tk.Frame(self.root, bg="#1E1E1E")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # Frame Esquerdo (Código Fonte)
        left_frame = tk.Frame(main_frame, bg="#1E1E1E")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(left_frame, text="Código Fonte (Gol++):", bg="#1E1E1E", fg=self.cor_fg, font=("Segoe UI", 10)).pack(anchor="w")

        # Frame que contém a coluna de números de linha + editor de código
        code_frame = tk.Frame(left_frame, bg=self.cor_bg)
        code_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Área de números de linha (só leitura)
        self.line_numbers = tk.Text(code_frame, width=5, padx=5, takefocus=0, border=0,
                                    background=self.cor_bg, fg="#858585", font=self.fonte_padrao,
                                    state=tk.DISABLED)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Barra de rolagem vertical compartilhada
        v_scroll = tk.Scrollbar(code_frame)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Editor de código principal
        self.text_codigo = tk.Text(code_frame, wrap=tk.WORD, font=self.fonte_padrao, bg=self.cor_bg, fg=self.cor_fg, insertbackground="white",
                                   yscrollcommand=v_scroll.set)
        self.text_codigo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Configurações da scrollbar para controlar ambos widgets
        v_scroll.config(command=self._on_scrollbar)

        # Eventos para manter números de linha sincronizados
        self.text_codigo.bind('<KeyRelease>', lambda e: self._update_line_numbers())
        self.text_codigo.bind('<ButtonRelease-1>', lambda e: self._update_line_numbers())
        self.text_codigo.bind('<MouseWheel>', self._sync_scroll_event)
        # Inicializa a numeração
        self._update_line_numbers()

        # Botões
        frame_botoes = tk.Frame(left_frame, bg="#1E1E1E")
        frame_botoes.pack(fill=tk.X, pady=5)

        btn_carregar = tk.Button(frame_botoes, text="📂 Carregar Arquivo", bg="#4CAF50", fg="white", relief="flat", font=("Segoe UI", 10, "bold"), command=self.carregar_arquivo)
        btn_carregar.pack(side=tk.LEFT, padx=5)

        btn_analisar = tk.Button(frame_botoes, text="▶ Analisar Código", bg=self.cor_btn, fg="white", relief="flat", font=("Segoe UI", 10, "bold"), command=self.analisar_codigo)
        btn_analisar.pack(side=tk.LEFT, padx=5)

        btn_limpar = tk.Button(frame_botoes, text="🗑 Limpar", bg="#F44336", fg="white", relief="flat", font=("Segoe UI", 10, "bold"), command=self.limpar_textos)
        btn_limpar.pack(side=tk.RIGHT, padx=5)

        # Frame Direito (Saída: Tokens e Erros)
        right_frame = tk.Frame(main_frame, bg="#1E1E1E")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(right_frame, text="Saída (Tokens):", bg="#1E1E1E", fg=self.cor_fg, font=("Segoe UI", 10)).pack(anchor="w")
        self.text_tokens = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, font=self.fonte_padrao, bg=self.cor_bg, fg="#9CDCFE", state=tk.DISABLED)
        self.text_tokens.pack(fill=tk.BOTH, expand=True, pady=5)

        tk.Label(right_frame, text="Relatório de Erros:", bg="#1E1E1E", fg="#F44336", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.text_erros = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, font=self.fonte_padrao, bg=self.cor_bg, fg="#F44336", height=8, state=tk.DISABLED)
        self.text_erros.pack(fill=tk.X, pady=5)

    def carregar_arquivo(self):
        """Carrega um arquivo de código Gol++"""
        filepath = filedialog.askopenfilename(title="Selecione um arquivo Gol++", filetypes=(("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")))
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    conteudo = file.read()
                    self.text_codigo.delete(1.0, tk.END)
                    self.text_codigo.insert(tk.END, conteudo)
                    # Atualiza números de linha após carregar
                    self._update_line_numbers()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível ler o arquivo:\n{e}")

    def analisar_codigo(self):
        """Analisa o código e exibe tokens e erros"""
        codigo = self.text_codigo.get(1.0, tk.END)
        tokens, erros = self.lexer.analisar(codigo)

        # Atualiza a área de Tokens
        self.text_tokens.config(state=tk.NORMAL)
        self.text_tokens.delete(1.0, tk.END)
        if tokens:
            self.text_tokens.insert(tk.END, "\n".join(tokens))
        else:
            self.text_tokens.insert(tk.END, "Nenhum token válido encontrado.")
        self.text_tokens.config(state=tk.DISABLED)

        # Atualiza a área de Erros
        self.text_erros.config(state=tk.NORMAL)
        self.text_erros.delete(1.0, tk.END)
        if erros:
            self.text_erros.insert(tk.END, "\n".join(erros))
        else:
            self.text_erros.insert(tk.END, "✓ Compilação léxica concluída sem erros.")
            self.text_erros.config(fg="#4CAF50")  # Fica verde se não tiver erros
        self.text_erros.config(state=tk.DISABLED)

    def limpar_textos(self):
        """Limpa todos os campos da interface"""
        self.text_codigo.delete(1.0, tk.END)
        self._update_line_numbers()
        
        self.text_tokens.config(state=tk.NORMAL)
        self.text_tokens.delete(1.0, tk.END)
        self.text_tokens.config(state=tk.DISABLED)
        
        self.text_erros.config(state=tk.NORMAL)
        self.text_erros.delete(1.0, tk.END)
        self.text_erros.config(fg="#F44336")
        self.text_erros.config(state=tk.DISABLED)

    # ----------------------- Helpers para numeração -------------------------
    def _get_line_count(self):
        """Retorna o número total de linhas no editor"""
        return int(self.text_codigo.index('end-1c').split('.')[0])

    def _update_line_numbers(self):
        """Atualiza a coluna de números de linha"""
        total = self._get_line_count()
        lines = "\n".join(f"{i:02d}" for i in range(1, total + 1))
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        self.line_numbers.insert(tk.END, lines)
        self.line_numbers.config(state=tk.DISABLED)

    def _on_scrollbar(self, *args):
        """Sincroniza a rolagem entre editor e coluna de linhas"""
        self.text_codigo.yview(*args)
        self.line_numbers.yview(*args)

    def _sync_scroll_event(self, event):
        """Sincroniza scroll de roda do mouse"""
        if event.delta:
            move = -1 * (event.delta // 120)
            self.text_codigo.yview_scroll(move, 'units')
            self.line_numbers.yview_scroll(move, 'units')
            return 'break'
