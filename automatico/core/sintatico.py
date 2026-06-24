import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value', 'line', 'column'])

REGEX_TOKEN = re.compile(
    r"Linha:\s*(\d+)\s*-\s*Coluna\s*(\d+)\s*-\s*Token:<([^,]+),\s*(.*)>$"
)


class ParserSintatico:

    TIPOS = {
        'TIPO_INT', 'TIPO_STR', 'TIPO_REAL', 'TIPO_BOOL',
        'TIPO_TEMPO', 'TIPO_PLACAR'
    }

    OPERADORES = {
        'SOMA', 'SUBTRACAO', 'MULT', 'DIVISAO',
        'IGUAL', 'DIFERENTE', 'MENOR', 'MAIOR',
        'MENOR_IGUAL', 'MAIOR_IGUAL',
        'LOGICO_E', 'LOGICO_OU',
    }

    VALORES = {
        'STR_VALOR', 'INT_VALOR', 'REAL_VALOR', 'TEMPO_VALOR',
        'BOOL_VERD', 'BOOL_FALSO'
    }

    SINCRONIZACAO = frozenset({
        'APITO_LANCE', 'INICIO_JOGO', 'FIM_JOGO',
        'SE_ATAQUE', 'DEFESA', 'CONTRA_ATAQUE',
        'BOLA_ROLAR', 'ESQUEMA', 'NARRAR',
        'SAI_CAMPO', 'ENTRA_CAMPO',
        'ABRE_JOGADA', 'FECHA_JOGADA',
        'EOF',
    })

    FIM_BLOCO = frozenset({'FIM_JOGO', 'EOF', 'SAI_CAMPO'})

    def __init__(self):
        self.tokens = []
        self.pos = 0
        self.erros = []
        self.regras = []

    def analisar(self, tokens_str):
        self.tokens = []
        self.pos = 0
        self.erros = []
        self.regras = []

        for s in tokens_str:
            tok = self._parse_token(s)
            if tok:
                self.tokens.append(tok)

        if not self.tokens:
            self.erros.append(
                "Linha: 01 - Coluna 01 - ERRO SINTÁTICO: "
                "Nenhum token disponível. Execute a análise léxica primeiro."
            )
            return self.erros, self.regras

        self._programa()

        if not self.erros:
            self.regras.insert(0, "PROGRAMA: estrutura sintática válida")

        return self.erros, self.regras

    def _parse_token(self, token_str):
        m = REGEX_TOKEN.match(token_str.strip())
        if m:
            return Token(
                type=m.group(3).strip(),
                value=m.group(4).strip(),
                line=int(m.group(1)),
                column=int(m.group(2))
            )
        return None

    def _peek(self, offset=0):
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return Token('EOF', '', -1, -1)

    def _consumir(self):
        t = self._peek()
        self.pos += 1
        return t

    def _esperar(self, tipo, mensagem=None):
        t = self._peek()
        if t.type == tipo:
            return self._consumir()
        msg = mensagem or f"Esperado '{tipo}', encontrado '{t.type}'"
        self._erro(msg, t)
        return None

    def _erro(self, mensagem, token=None):
        if token is None:
            token = self._peek()
        if token.line == -1:
            self.erros.append(
                f"Linha: 01 - Coluna 01 - ERRO SINTÁTICO: {mensagem}"
            )
        else:
            self.erros.append(
                f"Linha: {token.line:02d} - Coluna {token.column:02d} - "
                f"ERRO SINTÁTICO: {mensagem}"
            )

    def _panico(self):
        if self._peek().type != 'EOF':
            self._consumir()
        while self._peek().type not in self.SINCRONIZACAO:
            self._consumir()

    def _regra(self, descricao):
        self.regras.append(descricao)

    def _programa(self):
        if self._peek().type == 'INICIO_JOGO':
            tok = self._consumir()
            self._regra(f"INICIO_JOGO: {tok.value}")
            self._esperar(
                'APITO_LANCE',
                "Programa deve começar com 'apito_inicial.'"
            )
            self._lista_comandos()
            if self._peek().type == 'FIM_JOGO':
                tok = self._consumir()
                self._regra(f"FIM_JOGO: {tok.value}")
                self._esperar(
                    'APITO_LANCE',
                    "Programa deve terminar com 'apito_final.'"
                )
            elif self._peek().type != 'EOF':
                self._erro("Esperado 'apito_final' para encerrar o programa")
                self._panico()
        elif self._peek().type != 'EOF':
            self._erro("Programa deve começar com 'apito_inicial.'")
            self._panico()
            if self._peek().type == 'INICIO_JOGO':
                self._programa()

    def _lista_comandos(self):
        while self._peek().type not in self.FIM_BLOCO:
            self._comando()

    def _comando(self):
        t = self._peek()

        if t.type in self.TIPOS:
            self._declaracao()

        elif t.type == 'VAR_JOGADOR':
            if self._peek(1).type == 'PASSE':
                self._atribuicao()
            else:
                self._erro(
                    f"Esperado operador '<<' após variável '{t.value}'", t
                )
                self._consumir()
                self._panico()

        elif t.type == 'NOME_FUNCAO':
            if self._peek(1).type == 'ABRE_JOGADA':
                self._chamada_funcao()
            else:
                self._erro(
                    f"Função '{t.value}' deve ser seguida de '('", t
                )
                self._consumir()
                self._panico()

        elif t.type == 'ESQUEMA':
            self._definicao_esquema()

        elif t.type == 'BOLA_ROLAR':
            self._estrutura_repeticao()

        elif t.type == 'SE_ATAQUE':
            self._estrutura_condicional()

        elif t.type == 'NARRAR':
            self._comando_saida()

        elif t.type == 'DEFESA':
            self._consumir()
            self._erro(
                "'defesa' sem um 'se_ataque' correspondente", t
            )
            self._panico()

        elif t.type == 'CONTRA_ATAQUE':
            self._consumir()
            self._erro(
                "'contra_ataque' sem um 'se_ataque' correspondente", t
            )
            self._panico()

        elif t.type == 'APITO_LANCE':
            self._consumir()

        else:
            self._consumir()
            self._erro(f"Token inesperado '{t.type}' ('{t.value}')", t)
            self._panico()

    def _declaracao(self):
        t = self._consumir()
        self._regra(f"DECLARACAO: {t.value} @...")
        if self._peek().type == 'VAR_JOGADOR':
            self._consumir()
            self._esperar(
                'APITO_LANCE',
                "Declaração deve terminar com '.'"
            )
        else:
            tok = self._peek()
            self._erro(
                f"Esperado identificador (@) após '{t.value}', "
                f"encontrado '{tok.value}'"
            )
            self._panico()

    def _atribuicao(self):
        var = self._consumir()
        self._regra(f"ATRIBUICAO: {var.value}")
        if self._peek().type == 'PASSE':
            self._consumir()
            if self._peek().type == 'APITO_LANCE':
                self._erro(
                    "Operação incompleta: expressão esperada após '<<'"
                )
                self._panico()
                return
            self._expressao()
            self._esperar(
                'APITO_LANCE',
                "Atribuição deve terminar com '.'"
            )
        else:
            self._erro(f"Esperado '<<' após '{var.value}'")
            self._panico()

    def _expressao(self):
        self._termo()
        while self._peek().type in self.OPERADORES:
            op = self._consumir()
            if self._peek().type == 'APITO_LANCE' or \
               self._peek().type in self.SINCRONIZACAO:
                self._erro(
                    f"Expressão incompleta após operador '{op.value}'", op
                )
                return
            self._termo()

    def _termo(self):
        t = self._peek()

        if t.type in self.VALORES or t.type == 'VAR_JOGADOR':
            self._consumir()

        elif t.type == 'NOME_FUNCAO':
            nome = self._consumir()
            if self._peek().type == 'ABRE_JOGADA':
                self._consumir()
                self._lista_argumentos()
                if self._peek().type == 'FECHA_JOGADA':
                    self._consumir()
                else:
                    self._erro(
                        "Parêntese não fechado na chamada de função"
                    )
                    self._panico()
            else:
                self._erro(
                    f"Função '{nome.value}' deve ser seguida de '('"
                )
                self._panico()

        elif t.type == 'ABRE_JOGADA':
            self._consumir()
            self._expressao()
            if self._peek().type == 'FECHA_JOGADA':
                self._consumir()
            else:
                self._erro("Parêntese '(' não fechado")
                self._panico()

        else:
            self._erro(f"Expressão inválida: '{t.type}' ('{t.value}')")
            self._panico()

    def _lista_argumentos(self):
        if self._peek().type not in (
            'FECHA_JOGADA', 'APITO_LANCE', 'EOF',
            'SAI_CAMPO', 'ENTRA_CAMPO'
        ):
            self._expressao()
            while self._peek().type == 'ESCALACAO':
                self._consumir()
                self._expressao()

    def _lista_parametros(self):
        if self._peek().type in self.TIPOS:
            self._consumir()
            if self._peek().type == 'VAR_JOGADOR':
                self._consumir()
                while self._peek().type == 'ESCALACAO':
                    self._consumir()
                    if self._peek().type in self.TIPOS:
                        self._consumir()
                    else:
                        self._erro("Esperado tipo do parâmetro")
                        self._panico()
                        return
                    if self._peek().type == 'VAR_JOGADOR':
                        self._consumir()
                    else:
                        self._erro("Esperado nome do parâmetro (@)")
                        self._panico()
                        return
            else:
                self._erro("Esperado nome do parâmetro (@)")
                self._panico()

    def _chamada_funcao(self):
        nome = self._consumir()
        self._regra(f"CHAMADA_FUNCAO: {nome.value}")
        if self._peek().type == 'ABRE_JOGADA':
            self._consumir()
            self._lista_argumentos()
            if self._peek().type == 'FECHA_JOGADA':
                self._consumir()
            else:
                self._erro("Parêntese não fechado na chamada de função")
                self._panico()
                return
            self._esperar(
                'APITO_LANCE',
                "Chamada de função deve terminar com '.'"
            )
        else:
            self._erro("Função deve ser seguida de '('")
            self._panico()

    def _definicao_esquema(self):
        self._consumir()
        if self._peek().type == 'NOME_FUNCAO':
            nome = self._consumir()
            self._regra(f"ESQUEMA: {nome.value}")
        else:
            self._erro("Esperado nome da função após 'esquema'")
            self._panico()
            return
        if self._peek().type == 'ABRE_JOGADA':
            self._consumir()
            self._lista_parametros()
            if self._peek().type == 'FECHA_JOGADA':
                self._consumir()
            else:
                self._erro("Parêntese não fechado na definição da função")
                self._panico()
                return
        else:
            self._erro("Esperado '(' após nome da função")
            self._panico()
            return
        if self._peek().type == 'ENTRA_CAMPO':
            self._consumir()
            self._lista_comandos()
            if self._peek().type == 'SAI_CAMPO':
                self._consumir()
            else:
                self._erro(
                    "Bloco da função não fechado. Esperado '}'"
                )
                self._panico()
        else:
            self._erro("Esperado '{' para iniciar bloco da função")
            self._panico()

    def _estrutura_repeticao(self):
        self._consumir()
        self._regra("REPETICAO: enquanto_bola_rolar")
        if self._peek().type == 'ABRE_JOGADA':
            self._consumir()
            self._condicao()
            if self._peek().type == 'FECHA_JOGADA':
                self._consumir()
            else:
                self._erro("Parêntese não fechado na condição do loop")
                self._panico()
                return
        else:
            self._erro("Esperado '(' após 'enquanto_bola_rolar'")
            self._panico()
            return
        if self._peek().type == 'ENTRA_CAMPO':
            self._consumir()
            self._lista_comandos()
            if self._peek().type == 'SAI_CAMPO':
                self._consumir()
            else:
                self._erro("Bloco do loop não fechado. Esperado '}'")
                self._panico()
        else:
            self._erro("Esperado '{' para iniciar bloco do loop")
            self._panico()

    def _estrutura_condicional(self):
        self._consumir()
        self._regra("CONDICIONAL: se_ataque")
        if self._peek().type == 'ABRE_JOGADA':
            self._consumir()
            self._condicao()
            if self._peek().type == 'FECHA_JOGADA':
                self._consumir()
            else:
                self._erro(
                    "Parêntese não fechado na condição do 'se_ataque'"
                )
                self._panico()
                return
        else:
            self._erro("Esperado '(' após 'se_ataque'")
            self._panico()
            return
        if self._peek().type == 'ENTRA_CAMPO':
            self._consumir()
            self._lista_comandos()
            if self._peek().type == 'SAI_CAMPO':
                self._consumir()
            else:
                self._erro("Bloco 'se_ataque' não fechado. Esperado '}'")
                self._panico()
                return
        else:
            self._erro("Esperado '{' para iniciar bloco 'se_ataque'")
            self._panico()
            return
        while self._peek().type == 'CONTRA_ATAQUE':
            self._consumir()
            self._regra("CONDICIONAL: contra_ataque")
            if self._peek().type == 'ABRE_JOGADA':
                self._consumir()
                self._condicao()
                if self._peek().type == 'FECHA_JOGADA':
                    self._consumir()
                else:
                    self._erro("Parêntese não fechado no 'contra_ataque'")
                    self._panico()
                    break
            else:
                self._erro("Esperado '(' após 'contra_ataque'")
                self._panico()
                break
            if self._peek().type == 'ENTRA_CAMPO':
                self._consumir()
                self._lista_comandos()
                if self._peek().type == 'SAI_CAMPO':
                    self._consumir()
                else:
                    self._erro(
                        "Bloco 'contra_ataque' não fechado. Esperado '}'"
                    )
                    self._panico()
                    break
            else:
                self._erro(
                    "Esperado '{' para iniciar bloco 'contra_ataque'"
                )
                self._panico()
                break
        if self._peek().type == 'DEFESA':
            self._consumir()
            self._regra("CONDICIONAL: defesa")
            if self._peek().type == 'ENTRA_CAMPO':
                self._consumir()
                self._lista_comandos()
                if self._peek().type == 'SAI_CAMPO':
                    self._consumir()
                else:
                    self._erro("Bloco 'defesa' não fechado. Esperado '}'")
                    self._panico()
            else:
                self._erro("Esperado '{' para iniciar bloco 'defesa'")
                self._panico()

    def _comando_saida(self):
        self._consumir()
        self._regra("SAIDA: narrar")
        if self._peek().type == 'ABRE_JOGADA':
            self._consumir()
            self._expressao()
            if self._peek().type == 'FECHA_JOGADA':
                self._consumir()
            else:
                self._erro("Parêntese não fechado no comando 'narrar'")
                self._panico()
                return
            self._esperar(
                'APITO_LANCE',
                "Comando 'narrar' deve terminar com '.'"
            )
        else:
            self._erro("Esperado '(' após 'narrar'")
            self._panico()

    def _condicao(self):
        if self._peek().type not in (
            'FECHA_JOGADA', 'APITO_LANCE', 'EOF', 'ENTRA_CAMPO'
        ):
            self._expressao()
            while self._peek().type in (
                'LOGICO_E', 'LOGICO_OU', 'LOGICO_NAO'
            ):
                self._consumir()
                self._expressao()
