# manual/core/constants.py
# Constantes e configurações do Analisador Léxico Manual

PALAVRAS_RESERVADAS = {
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

TOKEN_SPECS = [
    ('COMENTARIO', r'\[.*?\]'),                # Comentários fechados [ ]
    ('ERRO_COMENTARIO', r'\[[^\]]*$'),         # Comentário não fechado
    ('STR_VALOR', r'"[^"]*"'),                 # Strings bem formadas
    ('ERRO_STRING', r'"[^"]*$'),               # String não fechada (sem aspas duplas no fim)
    ('REAL_VALOR', r'\b\d+\.\d+\b'),           # Números decimais (float)
    ('ERRO_NUMERO', r'\b\d+\.[a-zA-Z_]+'),     # Número mal formado (ex: 2.a3)
    ('TEMPO_VALOR', r'\b\d+\''),               # Representação de tempo (ex: 45')
    ('INT_VALOR', r'\b\d+\b'),                 # Números inteiros
    ('VAR_JOGADOR', r'@[a-zA-Z0-9_]+'),        # Variáveis começando com @
    ('NOME_FUNCAO', r'![a-zA-Z][a-zA-Z0-9_]*'),# Chamada de função começando com !
    ('ERRO_VAR_MAL_FORMADA', r'[a-zA-Z_][a-zA-Z0-9_]*@+[a-zA-Z0-9_]*'), # Variável mal formada (ex: j@)
    ('PALAVRA', r'~?[a-zA-Z_][a-zA-Z0-9_]*'),  # Palavras reservadas (incluindo as com ~)
    ('PASSE', r'<<'),                          # Atribuição
    ('IGUAL', r'=='),
    ('MENOR_IGUAL', r'<='),
    ('MAIOR_IGUAL', r'>='),
    ('DIFERENTE', r'!='),                      # Usando != para diferente, assumindo padrão
    ('MENOR', r'<'),
    ('MAIOR', r'>'),
    ('SOMA', r'\+'),
    ('SUBTRACAO', r'-'),
    ('MULT', r'\*'),
    ('DIVISAO', r'/'),
    ('ENTRA_CAMPO', r'\{'),                    # Abre chaves
    ('SAI_CAMPO', r'\}'),                      # Fecha chaves
    ('ABRE_JOGADA', r'\('),                    # Abre parênteses
    ('FECHA_JOGADA', r'\)'),                   # Fecha parênteses
    ('APITO_LANCE', r'\.'),                    # Ponto final
    ('ESCALACAO', r','),                       # Vírgula
    ('NEWLINE', r'\n'),                        # Nova linha
    ('SKIP', r'[ \t\r]+'),                     # Espaços e tabs
    ('ERRO_SIMBOLO', r'.'),                    # Qualquer outro símbolo inválido (ex: @ solto)
]
