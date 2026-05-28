# manual/core/lexer.py
# Analisador Léxico Manual - Lógica de análise

import re
from manual.core.constants import PALAVRAS_RESERVADAS, TOKEN_SPECS


class LexerGol:
    """
    Analisador Léxico Manual da linguagem Gol++
    Implementação manual sem uso de bibliotecas como PLY
    """
    
    def __init__(self):
        self.palavras_reservadas = PALAVRAS_RESERVADAS
        self.token_specs = TOKEN_SPECS
        
        # Compila as expressões regulares
        self.regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.token_specs)
        self.re_compilada = re.compile(self.regex, re.DOTALL)

    def analisar(self, codigo_fonte):
        """
        Analisa o código fonte Gol++ e retorna lista de tokens e erros
        
        Args:
            codigo_fonte (str): Código a ser analisado
            
        Returns:
            tuple: (lista_tokens, lista_erros)
        """
        tokens_encontrados = []
        erros_encontrados = []
        
        linha_atual = 1
        inicio_linha = 0
        pilha_chaves = 0
        primeira_palavra_chave = None
        ultima_palavra_chave = None
        primeira_linha = 1
        ultima_linha = 1

        for match in self.re_compilada.finditer(codigo_fonte):
            tipo = match.lastgroup
            lexema = match.group()
            coluna = match.start() - inicio_linha + 1

            if tipo == 'NEWLINE':
                linha_atual += 1
                inicio_linha = match.end()
                continue
            elif tipo == 'SKIP':
                continue
            elif tipo == 'COMENTARIO':
                # Comentários são consumidos/ignorados
                linhas_no_comentario = lexema.count('\n')
                if linhas_no_comentario > 0:
                    linha_atual += linhas_no_comentario
                    inicio_linha = match.end() - len(lexema.split('\n')[-1])
                continue

            # Verificações de erros específicos
            if tipo == 'ERRO_COMENTARIO':
                erros_encontrados.append(f"Linha: {linha_atual} - Coluna {coluna} - ERRO: Fim de arquivo inesperado (comentário arquibancada não fechado).")
                continue
            elif tipo == 'ERRO_STRING':
                erros_encontrados.append(f"Linha: {linha_atual} - Coluna {coluna} - ERRO: String mal formada (abrir aspas e não fechar).")
                continue
            elif tipo == 'ERRO_NUMERO':
                erros_encontrados.append(f"Linha: {linha_atual} - Coluna {coluna} - ERRO: Número mal formado ({lexema}).")
                continue
            elif tipo == 'ERRO_SIMBOLO':
                erros_encontrados.append(f"Linha: {linha_atual} - Coluna {coluna} - ERRO: Símbolo não pertencente ao conjunto da linguagem: {lexema}")
                continue
            elif tipo == 'ERRO_VAR_MAL_FORMADA':
                erros_encontrados.append(f"Linha: {linha_atual} - Coluna {coluna} - ERRO: Identificador/variável mal formada ({lexema}).")
                continue
                
            # Regras de tamanho limite
            if tipo == 'VAR_JOGADOR' and len(lexema) > 30:
                erros_encontrados.append(f"Linha: {linha_atual} - Coluna {coluna} - ERRO: Tamanho do identificador excedido ({lexema}).")
                continue
            if tipo == 'INT_VALOR' and len(lexema) > 15:
                erros_encontrados.append(f"Linha: {linha_atual} - Coluna {coluna} - ERRO: Tamanho excessivo do número ({lexema}).")
                continue

            # Processamento de palavras reservadas vs variáveis
            if tipo == 'PALAVRA':
                if lexema in self.palavras_reservadas:
                    tipo = self.palavras_reservadas[lexema]
                    # Rastreia primeira e última palavra-chave (palavras reservadas)
                    if primeira_palavra_chave is None:
                        primeira_palavra_chave = lexema
                        primeira_linha = linha_atual
                    ultima_palavra_chave = lexema
                    ultima_linha = linha_atual
                else:
                    # Se não for palavra chave, e não começou com @ ou !, é sintaxe inválida na Gol++
                    erros_encontrados.append(f"Linha: {linha_atual} - Coluna {coluna} - ERRO: Identificador inválido ou palavra desconhecida ({lexema}). Faltou o '@'?")
                    continue

            # Controle de Chaves para erro de "Abrir e não fechar"
            if tipo == 'ENTRA_CAMPO':
                pilha_chaves += 1
            elif tipo == 'SAI_CAMPO':
                pilha_chaves -= 1

            # Saída do token formatada
            tokens_encontrados.append(f"Linha: {linha_atual:02d} - Coluna {coluna:02d} - Token:<{tipo}, {lexema}>")

        # Verifica obrigatoriedade de apito_inicial e apito_final
        if primeira_palavra_chave != 'apito_inicial':
            if primeira_palavra_chave is None:
                erros_encontrados.append("Linha: 01 - ERRO ESTRUTURAL: O código deve começar com 'apito_inicial'.")
            else:
                erros_encontrados.append(f"Linha: {primeira_linha:02d} - ERRO ESTRUTURAL: O código deve começar com 'apito_inicial', mas encontrou '{primeira_palavra_chave}'.")
        
        if ultima_palavra_chave != 'apito_final':
            if ultima_palavra_chave is None:
                erros_encontrados.append("ERRO ESTRUTURAL: O código deve terminar com 'apito_final'.")
            else:
                erros_encontrados.append(f"Linha: {ultima_linha:02d} - ERRO ESTRUTURAL: O código deve terminar com 'apito_final', mas encontrou '{ultima_palavra_chave}'.")

        # Verifica se alguma chave ficou aberta no final do arquivo
        if pilha_chaves > 0:
            erros_encontrados.append("ERRO ESTRUTURAL: Fim de arquivo inesperado. Bloco de código '{' aberto e não fechado.")
        elif pilha_chaves < 0:
            erros_encontrados.append("ERRO ESTRUTURAL: Chave de fechamento '}' encontrada sem abertura correspondente.")

        return tokens_encontrados, erros_encontrados
