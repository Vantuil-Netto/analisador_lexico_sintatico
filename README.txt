========================================================================
           ⚽ COMPILADOR GOL++ - ANALISADORES LÉXICOS ⚽
========================================================================

Este repositório contém a especificação e a implementação de dois
Analisadores Léxicos para a linguagem Gol++, uma linguagem de domínio
específico (DSL) inspirada no futebol.

O projeto dispõe de duas abordagens de implementação:
1. Analisador Léxico Manual: Construído usando a biblioteca padrão 're'.
2. Analisador Léxico Automático: Construído usando a biblioteca PLY (Lex).

Ambos contam com uma Interface Gráfica (GUI) moderna desenvolvida em
Tkinter com numeração dinâmica de linhas, destaque de erros e console.

------------------------------------------------------------------------
1. INFORMAÇÕES GERAIS DO PROJETO
------------------------------------------------------------------------
* Linguagem de Domínio Específico (DSL): Gol++ (Tema: Futebol)
* Linguagem de Desenvolvimento: Python 3.8+
* Biblioteca de Automação (versão automática): PLY (Python Lex-Yacc)
* Interface Gráfica: Tkinter (Padrão do Python)
* IDE Recomendada: VS Code ou qualquer editor de texto de sua preferência.

Equipe de Desenvolvimento:
- Lúcio Filho
- Vantuil Netto
- Miguel Pereira
- Fábio Valeriano

------------------------------------------------------------------------
2. A LINGUAGEM GOL++ (ELEMENTOS TEMÁTICOS)
------------------------------------------------------------------------
A linguagem Gol++ possui elementos léxicos e sintáticos que fazem alusão 
ao futebol:
- Inicialização/Finalização: 'apito_inicial' e 'apito_final'.
- Condicionais: 'se_ataque' (if) e 'defesa' (else).
- Atribuição (Passe): '<<' (ex: @jogador1 << 10).
- Identificadores (Jogadores): Iniciam com '@' (ex: @jogador1).
- Funções: Iniciam com '!' (ex: !chutar).
- Exibição de Mensagens (Narrador): 'narrar' (ex: narrar "Goooool!").
- Comentários (Arquibancada): Delimitados por colchetes '[ comentário ]'.
- Unidades de Tempo: Números seguidos de aspa simples (ex: 90').

------------------------------------------------------------------------
3. ESTRUTURA DO PROJETO
------------------------------------------------------------------------
O projeto está organizado de forma modular e limpa:

analisador_lexico/
├── manual/                    # Analisador Manual (sem dependências)
│   ├── core/
│   │   ├── lexer.py           # Classe LexerGol (lógica manual)
│   │   └── constants.py       # Tabela de tokens e palavras reservadas
│   ├── gui/
│   │   └── interface.py       # Interface Tkinter adaptada ao manual
│   └── main.py                # Ponto de entrada do Analisador Manual
│
├── automatico/                # Analisador Automático (com PLY)
│   ├── core/
│   │   ├── lexer.py           # Classe LexerGol (lógica baseada no PLY)
│   │   └── constants.py       # Configurações de tokens compartilhadas
│   ├── gui/
│   │   └── interface.py       # Interface Tkinter adaptada ao automático
│   └── main.py                # Ponto de entrada do Analisador Automático
│
├── docs/                      # Documentações Técnicas e Roteiros
│   ├── DIFERENCA_MANUAL_VS_AUTOMATICO.md  # Comparativo técnico detalhado
│
├── exemplo_basico.txt         # Arquivo com código simples em Gol++ para teste
├── run_manual.bat             # Atalho Windows para rodar a versão manual
├── run_automatico.bat         # Atalho Windows para rodar a versão automática
└── README.txt                 # Este arquivo de instruções

------------------------------------------------------------------------
4. PRÉ-REQUISITOS E INSTALAÇÃO
------------------------------------------------------------------------
1. Python 3.8 ou superior instalado no seu sistema.
2. Biblioteca PLY (necessária apenas para executar o analisador automático):
   Abra o terminal e execute:
   
   pip install ply

*Nota: O analisador manual não possui dependências externas adicionais e 
roda puramente com a biblioteca padrão do Python.*

------------------------------------------------------------------------
5. COMO EXECUTAR
------------------------------------------------------------------------
Você pode executar o analisador de duas maneiras no Windows:

Opção A: Usando os scripts de lote (.bat)
- Dê um duplo clique em `run_manual.bat` para abrir o Analisador Manual.
- Dê um duplo clique em `run_automatico.bat` para abrir o Analisador Automático.

Opção B: Via Terminal de Comando
Certifique-se de estar na pasta raiz do projeto (`analisador_lexico`).
- Para executar o Analisador Manual:
  python manual/main.py

- Para executar o Analisador Automático:
  python automatico/main.py

------------------------------------------------------------------------
6. COMO OPERAR A INTERFACE GRÁFICA (GUI)
------------------------------------------------------------------------
Ambas as versões iniciam uma janela gráfica de layout unificado:

1. Editor de Código (Painel Esquerdo):
   - Permite digitar o código em tempo real.
   - Apresenta numeração dinâmica de linhas sincronizada.
   
2. Botão "📂 Carregar Arquivo":
   - Abre o explorador de arquivos para carregar arquivos de texto (.txt) 
     diretamente no editor de código (como o `exemplo_basico.txt`).
     
3. Botão "▶ Analisar Código":
   - Processa o código contido no editor.
   
4. Saída de Tokens (Painel Superior Direito):
   - Exibe a lista de tokens válidos encontrados no formato:
     "Linha: XX - Coluna: YY - Token:<TIPO, LEXEMA>"
     
5. Relatório de Erros (Painel Inferior Direito):
   - Se o código não possuir erros: exibe uma mensagem verde indicando
     sucesso ("✓ Compilação léxica concluída sem erros.").
   - Se houver erros (como strings não fechadas, comentários de arquibancada
     sem fechar, ou símbolos inválidos): exibe o relatório detalhado
     em vermelho com a linha e coluna exata de cada ocorrência.
     
6. Botão "🗑 Limpar":
   - Limpa todos os painéis e reseta os contadores.

------------------------------------------------------------------------
7. PRINCIPAIS DIFERENÇAS ENTRE AS VERSÕES
------------------------------------------------------------------------
- MANUAL:
  - Desenvolvido do zero utilizando o mecanismo de expressões regulares (`re`) 
    do Python.
  - Concatena as expressões regulares em um único padrão e varre usando 
    `finditer`.
  - Excelente para fins didáticos (mostra a lógica pura de como a varredura é 
    feita e como o contador de colunas é controlado manualmente).
    
- AUTOMÁTICO (PLY):
  - Utiliza o PLY (Python Lex-Yacc), que cria um analisador de alto desempenho 
    gerando tabelas internas otimizadas e autômatos eficientes.
  - Mapeia regras léxicas diretamente para variáveis e funções da classe.
  - Mais adequado para ambientes de produção e para posterior integração
    com geradores de árvore sintática (Yacc/Parser).

Para uma análise comparativa aprofundada, leia o documento em:
`docs/DIFERENCA_MANUAL_VS_AUTOMATICO.md`
========================================================================
