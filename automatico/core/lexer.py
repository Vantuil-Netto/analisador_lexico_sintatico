# automatico/core/lexer.py
# Analisador Léxico Automático com PLY (Python Lex-Yacc)

import ply.lex as lex
from automatico.core.constants import RESERVED, TOKENS


class LexerGol:
    """
    Analisador Léxico Automático da linguagem Gol++
    Implementado usando PLY (Python Lex-Yacc)
    """
    
    # Palavras reservadas
    reserved = RESERVED
    
    # Lista de tokens exigida pela biblioteca PLY
    tokens = TOKENS

    # Definição automática de tokens simples por String
    t_PASSE = r'<<'
    t_IGUAL = r'=='
    t_MENOR_IGUAL = r'<='
    t_MAIOR_IGUAL = r'>='
    t_DIFERENTE = r'!='
    t_MENOR = r'<'
    t_MAIOR = r'>'
    t_SOMA = r'\+'
    t_SUBTRACAO = r'-'
    t_MULT = r'\*'
    t_DIVISAO = r'/'
    t_ENTRA_CAMPO = r'\{'
    t_SAI_CAMPO = r'\}'
    t_ABRE_JOGADA = r'\('
    t_FECHA_JOGADA = r'\)'
    t_APITO_LANCE = r'\.'
    t_ESCALACAO = r','

    # Caracteres que a biblioteca deve ignorar automaticamente
    t_ignore = ' \t\r'

    def __init__(self):
        """Inicializa o analisador PLY"""
        self.lexer = lex.lex(module=self)
        self.erros_encontrados = []
        self.tokens_encontrados = []
        self.inicio_linha = 0
        self.pilha_chaves = 0

    # ==================== Regras Complexas ====================
    
    def t_COMENTARIO(self, t):
        r'\[.*?\]'
        nl = t.value.count('\n')
        if nl > 0:
            t.lexer.lineno += nl
            self.inicio_linha = t.lexpos + t.value.rfind('\n') + 1
        pass  # Ignora comentário

    def t_ERRO_COMENTARIO(self, t):
        r'\[[^\]]*$'
        coluna = t.lexpos - self.inicio_linha + 1
        self.erros_encontrados.append(f"Linha: {t.lexer.lineno} - Coluna {coluna} - ERRO: Fim de arquivo inesperado (comentário arquibancada não fechado).")
        t.lexer.lineno += t.value.count('\n')

    def t_STR_VALOR(self, t):
        r'"[^"]*"'
        return t

    def t_ERRO_STRING(self, t):
        r'"[^"]*$'
        coluna = t.lexpos - self.inicio_linha + 1
        self.erros_encontrados.append(f"Linha: {t.lexer.lineno} - Coluna {coluna} - ERRO: String mal formada (abrir aspas e não fechar).")

    def t_ERRO_NUMERO(self, t):
        r'\d+\.[a-zA-Z_]+'
        coluna = t.lexpos - self.inicio_linha + 1
        self.erros_encontrados.append(f"Linha: {t.lexer.lineno} - Coluna {coluna} - ERRO: Número mal formado ({t.value}).")

    def t_REAL_VALOR(self, t):
        r'\b\d+\.\d+\b'
        return t

    def t_TEMPO_VALOR(self, t):
        r'\b\d+\''
        return t

    def t_INT_VALOR(self, t):
        r'\b\d+\b'
        coluna = t.lexpos - self.inicio_linha + 1
        if len(t.value) > 15:
            self.erros_encontrados.append(f"Linha: {t.lexer.lineno} - Coluna {coluna} - ERRO: Tamanho excessivo do número ({t.value}).")
        else:
            return t

    def t_VAR_JOGADOR(self, t):
        r'@[a-zA-Z0-9_]+'
        coluna = t.lexpos - self.inicio_linha + 1
        if len(t.value) > 30:
            self.erros_encontrados.append(f"Linha: {t.lexer.lineno} - Coluna {coluna} - ERRO: Tamanho do identificador excedido ({t.value}).")
        else:
            return t

    def t_NOME_FUNCAO(self, t):
        r'![a-zA-Z][a-zA-Z0-9_]*'
        return t

    def t_ERRO_VAR_MAL_FORMADA(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*@+[a-zA-Z0-9_]*'
        coluna = t.lexpos - self.inicio_linha + 1
        self.erros_encontrados.append(f"Linha: {t.lexer.lineno} - Coluna {coluna} - ERRO: Identificador/variável mal formada ({t.value}).")

    def t_PALAVRA(self, t):
        r'~?[a-zA-Z_][a-zA-Z0-9_]*'
        coluna = t.lexpos - self.inicio_linha + 1
        if t.value in self.reserved:
            t.type = self.reserved[t.value]
            return t
        else:
            self.erros_encontrados.append(f"Linha: {t.lexer.lineno} - Coluna {coluna} - ERRO: Identificador inválido ou palavra desconhecida ({t.value}). Faltou o '@'?")

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        self.inicio_linha = t.lexpos + len(t.value)

    # Tratamento automático de qualquer caractere inválido geral
    def t_error(self, t):
        coluna = t.lexpos - self.inicio_linha + 1
        self.erros_encontrados.append(f"Linha: {t.lexer.lineno} - Coluna {coluna} - ERRO: Símbolo não pertencente ao conjunto da linguagem: {t.value[0]}")
        t.lexer.skip(1)

    # Método principal chamado pela Interface
    def analisar(self, codigo_fonte):
        """
        Analisa o código fonte Gol++ e retorna lista de tokens e erros
        
        Args:
            codigo_fonte (str): Código a ser analisado
            
        Returns:
            tuple: (lista_tokens, lista_erros)
        """
        self.erros_encontrados = []
        self.tokens_encontrados = []
        self.inicio_linha = 0
        self.pilha_chaves = 0
        self.lexer.lineno = 1
        
        primeira_palavra_chave = None
        ultima_palavra_chave = None
        primeira_linha = 1
        ultima_linha = 1
        
        # Alimenta a biblioteca com o código fonte
        self.lexer.input(codigo_fonte)
        
        # Coleta os tokens gerados automaticamente pelo PLY
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            
            coluna = tok.lexpos - self.inicio_linha + 1
            
            # Rastreia primeira e última palavra-chave (INICIO_JOGO e FIM_JOGO)
            if tok.type == 'INICIO_JOGO':
                if primeira_palavra_chave is None:
                    primeira_palavra_chave = tok.value
                    primeira_linha = tok.lineno
                ultima_palavra_chave = tok.value
                ultima_linha = tok.lineno
            elif tok.type == 'FIM_JOGO':
                if primeira_palavra_chave is None:
                    primeira_palavra_chave = tok.value
                    primeira_linha = tok.lineno
                ultima_palavra_chave = tok.value
                ultima_linha = tok.lineno
            
            if tok.type == 'ENTRA_CAMPO':
                self.pilha_chaves += 1
            elif tok.type == 'SAI_CAMPO':
                self.pilha_chaves -= 1
                
            self.tokens_encontrados.append(f"Linha: {tok.lineno:02d} - Coluna {coluna:02d} - Token:<{tok.type}, {tok.value}>")
            
        # Verifica obrigatoriedade de apito_inicial e apito_final
        if primeira_palavra_chave != 'apito_inicial':
            if primeira_palavra_chave is None:
                self.erros_encontrados.append("Linha: 01 - ERRO ESTRUTURAL: O código deve começar com 'apito_inicial'.")
            else:
                self.erros_encontrados.append(f"Linha: {primeira_linha:02d} - ERRO ESTRUTURAL: O código deve começar com 'apito_inicial', mas encontrou '{primeira_palavra_chave}'.")
        
        if ultima_palavra_chave != 'apito_final':
            if ultima_palavra_chave is None:
                self.erros_encontrados.append("ERRO ESTRUTURAL: O código deve terminar com 'apito_final'.")
            else:
                self.erros_encontrados.append(f"Linha: {ultima_linha:02d} - ERRO ESTRUTURAL: O código deve terminar com 'apito_final', mas encontrou '{ultima_palavra_chave}'.")
            
        # Verificações estruturais de fim de arquivo
        if self.pilha_chaves > 0:
            self.erros_encontrados.append("ERRO ESTRUTURAL: Fim de arquivo inesperado. Bloco de código '{' aberto e não fechado.")
        elif self.pilha_chaves < 0:
            self.erros_encontrados.append("ERRO ESTRUTURAL: Chave de fechamento '}' encontrada sem abertura correspondente.")
            
        return self.tokens_encontrados, self.erros_encontrados
