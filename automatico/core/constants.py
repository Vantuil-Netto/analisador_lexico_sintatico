# automatico/core/constants.py
# Constantes e configurações do Analisador Léxico Automático (PLY)

RESERVED = {
    'apito_inicial': 'INICIO_JOGO',
    'apito_final': 'FIM_JOGO',
    '~inteiro': 'TIPO_INT',
    '~texto': 'TIPO_STR',
    '~real': 'TIPO_REAL',
    '~booleano': 'TIPO_BOOL',
    '~tempo': 'TIPO_TEMPO',
    '~placar': 'TIPO_PLACAR',
    'TEMPO_JOGO': 'ESTADO_TEMPO',
    'POSSE_BOLA': 'ESTADO_POSSE',
    'FALTAS': 'ESTADO_FALTA',
    'ESCANTEIOS': 'ESTADO_ESC',
    'CARTOES': 'ESTADO_CARD',
    'E': 'LOGICO_E',
    'OU': 'LOGICO_OU',
    'NAO': 'LOGICO_NAO',
    'se_ataque': 'SE_ATAQUE',
    'defesa': 'DEFESA',
    'contra_ataque': 'CONTRA_ATAQUE',
    'enquanto_bola_rolar': 'BOLA_ROLAR',
    'cada_lance': 'CADA_LANCE',
    'revisao_var': 'REVISAO_VAR',
    'expulsao': 'EXPULSAO',
    'esquema': 'ESQUEMA',
    'entrega_taca': 'RETORNO',
    'narrar': 'NARRAR',
    'gol': 'EVENTO_GOL',
    'falta': 'EVENTO_FALTA',
    'escanteio': 'EVENTO_ESC',
    'Verdadeiro': 'BOOL_VERD',
    'Falso': 'BOOL_FALSO'
}

TOKENS = [
    'COMENTARIO', 'STR_VALOR', 'REAL_VALOR', 'TEMPO_VALOR', 'INT_VALOR',
    'VAR_JOGADOR', 'NOME_FUNCAO', 'PALAVRA', 'PASSE', 'IGUAL',
    'MENOR_IGUAL', 'MAIOR_IGUAL', 'DIFERENTE', 'MENOR', 'MAIOR',
    'SOMA', 'SUBTRACAO', 'MULT', 'DIVISAO', 'ENTRA_CAMPO', 'SAI_CAMPO',
    'ABRE_JOGADA', 'FECHA_JOGADA', 'APITO_LANCE', 'ESCALACAO'
] + list(RESERVED.values())
