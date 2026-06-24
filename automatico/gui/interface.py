import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
from automatico.core.lexer import LexerGol
from automatico.core.sintatico import ParserSintatico


class GolCompilerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Gol++ Compiler - Analisador Léxico e Sintático (PLY)")
        self.root.geometry("1100x700")
        self.root.configure(bg="#1E1E1E")

        self.lexer = LexerGol()
        self.parser = ParserSintatico()
        self.ultimos_tokens = []
        self.ultimo_codigo = ""

        self.fonte = ("Consolas", 10)
        self.cor_bg = "#252526"
        self.cor_fg = "#D4D4D4"

        self.montar_interface()

    def montar_interface(self):
        titulo = tk.Label(
            self.root,
            text="Gol++ Compiler - Analisador Léxico e Sintático (PLY)",
            font=("Segoe UI", 15, "bold"),
            bg="#1E1E1E", fg="#4CAF50"
        )
        titulo.pack(pady=8)

        frame_botoes = tk.Frame(self.root, bg="#1E1E1E")
        frame_botoes.pack(fill=tk.X, padx=15, pady=3)

        btn_conf = [
            ("Abrir arquivo", "#4CAF50", self.carregar_arquivo),
            ("Salvar arquivo", "#2196F3", self.salvar_arquivo),
            ("Listar tokens", "#FF9800", self.listar_tokens),
            ("Executar análise sintática", "#9C27B0", self.executar_sintatico),
            ("Limpar", "#F44336", self.limpar_textos),
            ("Manual Gol++", "#E91E63", self.abrir_manual),
            ("Sair do programa", "#607D8B", self.sair_programa),
        ]
        for texto, cor, cmd in btn_conf:
            btn = tk.Button(
                frame_botoes, text=texto, bg=cor, fg="white",
                relief="flat", font=("Segoe UI", 9, "bold"),
                command=cmd, padx=12, pady=4
            )
            btn.pack(side=tk.LEFT, padx=3)

        main_frame = tk.Frame(self.root, bg="#1E1E1E")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        left_frame = tk.Frame(main_frame, bg="#1E1E1E")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)

        tk.Label(
            left_frame, text="Código Fonte (Gol++):",
            bg="#1E1E1E", fg=self.cor_fg, font=("Segoe UI", 10)
        ).pack(anchor="w")

        code_frame = tk.Frame(left_frame, bg=self.cor_bg)
        code_frame.pack(fill=tk.BOTH, expand=True, pady=3)

        self.line_numbers = tk.Text(
            code_frame, width=4, padx=4, takefocus=0, border=0,
            background=self.cor_bg, fg="#858585", font=self.fonte,
            state=tk.DISABLED
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        v_scroll = tk.Scrollbar(code_frame)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_codigo = tk.Text(
            code_frame, wrap=tk.WORD, font=self.fonte,
            bg=self.cor_bg, fg=self.cor_fg, insertbackground="white",
            yscrollcommand=v_scroll.set
        )
        self.text_codigo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        v_scroll.config(command=self._on_scrollbar)

        self.text_codigo.bind('<KeyRelease>',
                              lambda e: self._update_line_numbers())
        self.text_codigo.bind('<ButtonRelease-1>',
                              lambda e: self._update_line_numbers())
        self.text_codigo.bind('<MouseWheel>', self._sync_scroll_event)
        self._update_line_numbers()

        right_frame = tk.Frame(main_frame, bg="#1E1E1E")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=3)

        tk.Label(
            right_frame, text="Saída de Tokens:",
            bg="#1E1E1E", fg=self.cor_fg, font=("Segoe UI", 10)
        ).pack(anchor="w")
        self.text_tokens = scrolledtext.ScrolledText(
            right_frame, wrap=tk.WORD, font=self.fonte,
            bg=self.cor_bg, fg="#9CDCFE", state=tk.DISABLED
        )
        self.text_tokens.pack(fill=tk.BOTH, expand=True, pady=2)

        tk.Label(
            right_frame, text="Erros Sintáticos:",
            bg="#1E1E1E", fg="#FF9800", font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")
        self.text_erros_sintatico = scrolledtext.ScrolledText(
            right_frame, wrap=tk.WORD, font=self.fonte,
            bg=self.cor_bg, fg="#FF9800", height=6, state=tk.DISABLED
        )
        self.text_erros_sintatico.pack(fill=tk.X, pady=2)

        tk.Label(
            right_frame, text="Regras Reconhecidas:",
            bg="#1E1E1E", fg="#4FC3F7", font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")
        self.text_regras = scrolledtext.ScrolledText(
            right_frame, wrap=tk.WORD, font=self.fonte,
            bg=self.cor_bg, fg="#4FC3F7", height=4, state=tk.DISABLED
        )
        self.text_regras.pack(fill=tk.X, pady=2)

    def carregar_arquivo(self):
        path = filedialog.askopenfilename(
            title="Selecione um arquivo Gol++",
            filetypes=(("Arquivos Gol++", "*.gol"),
                       ("Arquivos de Texto", "*.txt"),
                       ("Todos os Arquivos", "*.*"))
        )
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.text_codigo.delete(1.0, tk.END)
                    self.text_codigo.insert(tk.END, f.read())
                    self._update_line_numbers()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível ler o arquivo:\n{e}")

    def salvar_arquivo(self):
        path = filedialog.asksaveasfilename(
            title="Salvar arquivo Gol++",
            defaultextension=".gol",
            filetypes=(("Arquivos Gol++", "*.gol"),
                       ("Arquivos de Texto", "*.txt"),
                       ("Todos os Arquivos", "*.*"))
        )
        if path:
            try:
                conteudo = self.text_codigo.get(1.0, tk.END)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(conteudo)
                messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o arquivo:\n{e}")

    def listar_tokens(self):
        self.ultimo_codigo = self.text_codigo.get(1.0, tk.END)
        tokens, erros = self.lexer.analisar(self.ultimo_codigo)
        self.ultimos_tokens = tokens

        self.text_tokens.config(state=tk.NORMAL)
        self.text_tokens.delete(1.0, tk.END)
        if tokens:
            self.text_tokens.insert(tk.END, "\n".join(tokens))
        else:
            self.text_tokens.insert(tk.END, "Nenhum token válido encontrado.")
        if erros:
            self.text_tokens.insert(tk.END, "\n\n")
            self.text_tools_inserir_separador(self.text_tokens)
            self.text_tokens.insert(
                tk.END, "\n--- TOKENS COM ERRO IGNORADOS ---\n"
            )
            self.text_tokens.insert(tk.END, "\n".join(erros))
        self.text_tokens.config(state=tk.DISABLED)

        self.text_erros_sintatico.config(state=tk.NORMAL)
        self.text_erros_sintatico.delete(1.0, tk.END)
        if erros:
            self.text_erros_sintatico.config(fg="#F44336")
            self.text_erros_sintatico.insert(
                tk.END,
                "Erros léxicos detectados! Corrija-os e clique em "
                "'Executar análise sintática'."
            )
        else:
            self.text_erros_sintatico.insert(
                tk.END,
                "Clique em 'Executar análise sintática' para validar "
                "a estrutura."
            )
            self.text_erros_sintatico.config(fg="#858585")
        self.text_erros_sintatico.config(state=tk.DISABLED)

        self.text_regras.config(state=tk.NORMAL)
        self.text_regras.delete(1.0, tk.END)
        self.text_regras.config(state=tk.DISABLED)

    def text_tools_inserir_separador(self, widget):
        cfg = widget.tag_config("sep", foreground="#555555", font=("Consolas", 10))
        widget.insert(tk.END, "─" * 50 + "\n", "sep")

    def executar_sintatico(self):
        self.ultimo_codigo = self.text_codigo.get(1.0, tk.END)
        tokens, erros_lex = self.lexer.analisar(self.ultimo_codigo)
        self.ultimos_tokens = tokens

        if erros_lex:
            self.text_erros_sintatico.config(state=tk.NORMAL, fg="#F44336")
            self.text_erros_sintatico.delete(1.0, tk.END)
            cabecalho = "=" * 10 + " ERROS LÉXICOS " + "=" * 10 + "\n"
            cabecalho += "Corrija os erros abaixo antes de analisar a sintaxe.\n\n"
            self.text_erros_sintatico.insert(tk.END, cabecalho)
            self.text_erros_sintatico.insert(tk.END, "\n".join(erros_lex))
            self.text_erros_sintatico.config(state=tk.DISABLED)

            self.text_regras.config(state=tk.NORMAL)
            self.text_regras.delete(1.0, tk.END)
            self.text_regras.insert(
                tk.END, "Análise sintática bloqueada devido a erros léxicos."
            )
            self.text_regras.config(state=tk.DISABLED)
            return

        if not tokens:
            self.text_erros_sintatico.config(state=tk.NORMAL, fg="#F44336")
            self.text_erros_sintatico.delete(1.0, tk.END)
            self.text_erros_sintatico.insert(
                tk.END,
                "Nenhum token gerado. O código pode estar vazio ou conter "
                "apenas caracteres inválidos."
            )
            self.text_erros_sintatico.config(state=tk.DISABLED)
            return

        erros_sin, regras = self.parser.analisar(tokens)

        self.text_erros_sintatico.config(state=tk.NORMAL)
        self.text_erros_sintatico.delete(1.0, tk.END)
        if erros_sin:
            cabecalho = "=" * 10 + " ERROS SINTÁTICOS " + "=" * 10 + "\n"
            self.text_erros_sintatico.config(fg="#FF9800")
            self.text_erros_sintatico.insert(tk.END, cabecalho)
            self.text_erros_sintatico.insert(tk.END, "\n".join(erros_sin))
        else:
            self.text_erros_sintatico.config(fg="#4CAF50")
            self.text_erros_sintatico.insert(
                tk.END, "Estrutura sintática válida! Nenhum erro encontrado."
            )
        self.text_erros_sintatico.config(state=tk.DISABLED)

        self.text_regras.config(state=tk.NORMAL)
        self.text_regras.delete(1.0, tk.END)
        if regras:
            self.text_regras.insert(tk.END, "\n".join(regras))
        else:
            self.text_regras.insert(tk.END, "Nenhuma regra reconhecida.")
        self.text_regras.config(state=tk.DISABLED)

    def limpar_textos(self):
        self.text_codigo.delete(1.0, tk.END)
        self._update_line_numbers()
        self.ultimos_tokens = []
        self.ultimo_codigo = ""

        for widget in (self.text_tokens, self.text_erros_sintatico,
                       self.text_regras):
            widget.config(state=tk.NORMAL)
            widget.delete(1.0, tk.END)
            widget.config(state=tk.DISABLED)

        self.text_erros_sintatico.config(fg="#FF9800")

    def sair_programa(self):
        self.root.destroy()

    def abrir_manual(self):
        manual = tk.Toplevel(self.root)
        manual.title("Manual Gol++ - Referência Rápida da Sintaxe")
        manual.geometry("720x520")
        manual.configure(bg="#1E1E1E")
        manual.transient(self.root)

        tk.Label(
            manual, text="Manual de Referência Gol++",
            font=("Segoe UI", 14, "bold"), bg="#1E1E1E", fg="#4CAF50"
        ).pack(pady=10)

        frame = tk.Frame(manual, bg="#1E1E1E")
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        cols = ("Categoria", "Comando", "Descrição")
        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            height=18)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=220 if col == "Descrição" else
                        140 if col == "Categoria" else 130)

        v_scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=v_scroll.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#252526", foreground="#D4D4D4",
                        fieldbackground="#252526", rowheight=24,
                        font=("Consolas", 9))
        style.configure("Treeview.Heading", background="#007ACC",
                        foreground="white", font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", "#007ACC")])

        dados = [
            ("Estrutura", "apito_inicial", "Inicia o programa"),
            ("Estrutura", "apito_final", "Finaliza o programa"),
            ("Estrutura", ".", "Terminador de instrução (APITO_LANCE)"),
            ("Tipo", "~inteiro", "Declara variável inteira"),
            ("Tipo", "~texto", "Declara variável de texto"),
            ("Tipo", "~real", "Declara variável real"),
            ("Tipo", "~booleano", "Declara variável booleana"),
            ("Tipo", "~tempo", "Declara variável de tempo (minutos)"),
            ("Tipo", "~placar", "Declara variável de placar"),
            ("Variável", "@identificador", "Variável (ex: @gols_time)"),
            ("Atribuição", "<<", "Operador PASSE (atribuição)"),
            ("Função", "!nome()", "Chamada de função (ex: !meu_gol)"),
            ("Def. Função", "esquema !nome() {}", "Define uma função (ESQUEMA)"),
            ("Condicional", "se_ataque () {}", "Estrutura condicional (if)"),
            ("Condicional", "contra_ataque () {}", "Condicional adicional (else if)"),
            ("Condicional", "defesa {}", "Bloco padrão (else)"),
            ("Repetição", "enquanto_bola_rolar () {}", "Loop enquanto condição"),
            ("Saída", "narrar()", "Exibe mensagem no console"),
            ("Operador", "+", "Soma"),
            ("Operador", "-", "Subtração"),
            ("Operador", "*", "Multiplicação"),
            ("Operador", "/", "Divisão"),
            ("Comparação", "==", "Igualdade"),
            ("Comparação", "!=", "Diferente"),
            ("Comparação", "<", "Menor que"),
            ("Comparação", ">", "Maior que"),
            ("Comparação", "<=", "Menor ou igual"),
            ("Comparação", ">=", "Maior ou igual"),
            ("Lógico", "E", "AND lógico"),
            ("Lógico", "OU", "OR lógico"),
            ("Lógico", "NAO", "NOT lógico"),
            ("Delimitador", "()", "Parênteses (abrir/fechar jogada)"),
            ("Delimitador", "{}", "Chaves (entrar/sair campo)"),
            ("Comentário", "[texto]", "Comentário (arquibancada)"),
            ("Valor", "Verdadeiro", "Booleano verdadeiro"),
            ("Valor", "Falso", "Booleano falso"),
        ]

        for item in dados:
            tree.insert("", tk.END, values=item)

        btn_fechar = tk.Button(
            manual, text="Fechar", bg="#F44336", fg="white",
            relief="flat", font=("Segoe UI", 10, "bold"),
            command=manual.destroy, padx=20, pady=4
        )
        btn_fechar.pack(pady=10)

    def _get_line_count(self):
        return int(self.text_codigo.index('end-1c').split('.')[0])

    def _update_line_numbers(self):
        total = self._get_line_count()
        lines = "\n".join(f"{i:02d}" for i in range(1, total + 1))
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        self.line_numbers.insert(tk.END, lines)
        self.line_numbers.config(state=tk.DISABLED)

    def _on_scrollbar(self, *args):
        self.text_codigo.yview(*args)
        self.line_numbers.yview(*args)

    def _sync_scroll_event(self, event):
        if event.delta:
            move = -1 * (event.delta // 120)
            self.text_codigo.yview_scroll(move, 'units')
            self.line_numbers.yview_scroll(move, 'units')
            return 'break'
