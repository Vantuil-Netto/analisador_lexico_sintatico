# Gol++ Compiler - Analisador Léxico e Sintatico - Vantuil Netto, Lucio Garcia, Fabio Valeriano e Miguel Custodio

Este repositorio contem a implementacao de duas abordagens de analisadores para a linguagem Gol++, uma DSL (Domain-Specific Language) inspirada no futebol:

1. **Analisador Manual** - Construido com a biblioteca padrao `re` (apenas lexico)
2. **Analisador Automatico** - Construido com PLY (Lex) e parser descendente recursivo (lexico + sintatico)

Ambos contam com Interface Grafica (GUI) em Tkinter com tema escuro, numeracao dinamica de linhas e console de saida.

## Equipe de Desenvolvimento

- Lucio Filho
- Vantuil Netto
- Miguel Pereira
- Fabio Valeriano

## A Linguagem Gol++

A linguagem Gol++ possui elementos lexicos e sintaticos que fazem alusao ao futebol:

### Estrutura do Programa

```
apito_inicial.
    ... comandos ...
apito_final.
```

### Elementos da Linguagem

| Categoria | Comando | Descricao |
|---|---|---|
| Estrutura | `apito_inicial` / `apito_final` | Inicia / finaliza o programa |
| Tipos | `~inteiro` `~texto` `~real` `~booleano` `~tempo` `~placar` | Declaracao de variaveis |
| Variavel | `@identificador` | Variavel (ex: `@gols_time`) |
| Atribuicao (Passe) | `<<` | Operador de atribuicao |
| Funcao | `!nome()` | Chamada de funcao |
| Definicao de Funcao | `esquema !nome() {}` | Define uma funcao (ESQUEMA) |
| Condicional | `se_ataque () {}` | If |
| Condicional | `contra_ataque () {}` | Else if |
| Condicional | `defesa {}` | Else |
| Repeticao | `enquanto_bola_rolar () {}` | Loop while |
| Saida | `narrar()` | Exibe mensagem |
| Comentario | `[texto]` | Comentario (arquibancada) |
| Terminador | `.` | Ponto final (APITO_LANCE) |

### Operadores

| Tipo | Operadores |
|---|---|
| Aritmeticos | `+` `-` `*` `/` |
| Comparacao | `==` `!=` `<` `>` `<=` `>=` |
| Logicos | `E` `OU` `NAO` |

### Exemplo de Codigo

```gol
apito_inicial.
~inteiro @gols_time.
@gols_time << 0.

se_ataque (@gols_time < 10) {
    @gols_time << @gols_time + 1.
    narrar("Atacando!").
} defesa {
    narrar("Defendendo!").
}

enquanto_bola_rolar (@gols_time < 5) {
    @gols_time << @gols_time + 1.
}

!meu_gol().
apito_final.
```

## Estrutura do Projeto

```
analisador_lexico_sintatico/
├── automatico/                   # Analisador Automatico (PLY + Parser)
│   ├── core/
│   │   ├── constants.py          # Tabela de tokens e palavras reservadas
│   │   ├── lexer.py              # LexerGol (baseado em PLY)
│   │   └── sintatico.py          # ParserSintatico (analise descendente)
│   ├── gui/
│   │   └── interface.py          # GUI completa (lexico + sintatico + manual)
│   ├── examples/
│   │   ├── exemplo_basico.gol
│   │   ├── exemplo_valido.gol
│   │   ├── exemplo_erros.gol
│   │   └── exemplo_brasil_x_escocia.gol
│   └── main.py                   # Ponto de entrada
│
├── manual/                       # Analisador Manual (apenas lexico)
│   ├── core/
│   │   ├── constants.py          # Tabela de tokens e specs regex
│   │   └── lexer.py              # LexerGol (regex manual com finditer)
│   ├── gui/
│   │   └── interface.py          # GUI simplificada (apenas lexico)
│   ├── examples/
│   │   └── exemplo_basico.txt
│   └── main.py                   # Ponto de entrada
│
├── docs/
│   └── DIFERENCA_MANUAL_VS_AUTOMATICO.md
│
├── exemplo_basico.gol
├── run_manual.bat
├── run_automatico.bat
└── README.md
```

## Pre-requisitos e Instalacao

1. Python 3.8 ou superior
2. Biblioteca PLY (apenas para o analisador automatico):

   ```
   pip install ply
   ```

O analisador manual nao possui dependencias externas.

## Como Executar

### Windows (atalhos)

- Duplo clique em `run_manual.bat` para o Analisador Manual
- Duplo clique em `run_automatico.bat` para o Analisador Automatico

### Via terminal

```bash
# Analisador Manual
python manual/main.py

# Analisador Automatico
python automatico/main.py
```

## Como Operar a Interface Grafica

### Versao Manual

Interface simples com editor de codigo, numeracao de linhas e painel de saida:

- **Editor de Codigo** - Painel esquerdo com entrada de texto e numeracao dinamica
- **Carregar Arquivo** - Abre arquivos `.txt` ou `.gol`
- **Analisar Codigo** - Executa a analise lexica
- **Limpar** - Reseta todos os paineis

### Versao Automatica

Interface completa com recursos avancados:

- **Editor de Codigo** - Com numeracao de linhas sincronizada e scroll
- **Carregar Arquivo** - Abre arquivos `.gol` ou `.txt`
- **Salvar Arquivo** - Salva o codigo editado em arquivo `.gol`
- **Listar Tokens** - Executa a analise lexica e exibe os tokens encontrados
- **Executar Analise Sintatica** - Valida a estrutura gramatical do codigo
- **Limpar** - Reseta todos os paineis
- **Manual Gol++** - Abre uma janela com a referencia completa da linguagem
- **Sair do Programa** - Fecha a aplicacao

### Paineis de Saida (versao automatica)

1. **Saida de Tokens** - Lista de tokens validos no formato `"Linha: XX - Coluna: YY - Token:<TIPO, LEXEMA>"`
2. **Erros Sintaticos** - Relatorio de erros gramaticais (ou mensagem verde de sucesso)
3. **Regras Reconhecidas** - Sequencia de regras gramaticais identificadas durante a analise

## Analise Sintatica

A versao automatica inclui um **parser descendente recursivo** implementado em `automatico/core/sintatico.py` (classe `ParserSintatico`).

### Gramatica Reconhecida

```
programa     ::= INICIO_JOGO APITO_LANCE lista_comandos FIM_JOGO APITO_LANCE
lista_comandos ::= (comando)*
comando      ::= declaracao | atribuicao | chamada_funcao
               | definicao_esquema | estrutura_repeticao
               | estrutura_condicional | comando_saida
declaracao   ::= TIPO VAR_JOGADOR APITO_LANCE
atribuicao   ::= VAR_JOGADOR PASSE expressao APITO_LANCE
expressao    ::= termo (OPERADOR termo)*
termo        ::= VALOR | VAR_JOGADOR | NOME_FUNCAO ABRE_JOGADA lista_arg FECHA_JOGADA
               | ABRE_JOGADA expressao FECHA_JOGADA
```

### Recuperacao de Erros

O parser utiliza o modo **panico** para recuperacao de erros, sincronizando atraves de tokens como `APITO_LANCE`, `INICIO_JOGO`, `FIM_JOGO`, `SE_ATAQUE`, `ENTRA_CAMPO`, etc.

## Principais Diferencas entre as Versoes

| Caracteristica | Manual | Automatico |
|---|---|---|
| Analise lexica | `re.finditer` | PLY `lex` |
| Analise sintatica | - | Parser descendente recursivo |
| Dependencias | Nenhuma | PLY (`pip install ply`) |
| Complexidade | Didatica (tudo explicito) | Profissional (abstraido) |
| GUI | Simplificada | Completa (salvar, sintatico, manual interno) |
| Extensao arquivos | `.txt` | `.gol` |
| Exemplos | 1 arquivo | 4 arquivos |

Para uma analise comparativa aprofundada, leia `docs/DIFERENCA_MANUAL_VS_AUTOMATICO.md`.
