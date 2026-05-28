# 📖 Diferenças Técnicas: Manual vs Automático (PLY)

---

## 📌 Resumo Executivo

| Característica | Manual | Automático (PLY) |
|---|---|---|
| **Abordagem** | Implementação manual com regex | Gerador de analisadores léxicos |
| **Dependências** | Apenas Python stdlib | PLY (pip install ply) |
| **Complexidade** | Explícita (tudo visível) | Abstraída (PLY faz o trabalho) |
| **Linhas de código (core)** | ~200 | ~150 |
| **Velocidade** | Boa | Otimizada (PLY usa tabelas) |
| **Facilidade de manutenção** | Média (modificar regex é direto) | Alta (código mais organizado) |
| **Extensibilidade** | Difícil (parser exigiria refactor) | Fácil (PLY Parser já está pronto) |
| **Uso acadêmico** | Excelente | Bom (mostra o "real world") |
| **Recomendação** | Aprender | Profissional |

---

## 🔧 Comparação Técnica Detalhada

### 1. ESTRUTURA DE TOKENS

#### Manual (`manual/core/lexer.py`)
```python
self.token_specs = [
    ('COMENTARIO', r'\[.*?\]'),
    ('ERRO_COMENTARIO', r'\[[^\]]*$'),
    ('STR_VALOR', r'"[^"]*"'),
    ('REAL_VALOR', r'\b\d+\.\d+\b'),
    # ... mais 20+ tipos
]
self.regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.token_specs)
self.re_compilada = re.compile(self.regex, re.DOTALL)
```

**Explicação:**
- Uma lista de tuplas `(tipo, regex)`
- Concatena todas as regex com `|` (alternância)
- PLY internamente faz algo similar, mas otimizado

**Vantagem:** Você vê exatamente o que está acontecendo  
**Desvantagem:** Gerenciar ordem de regex é crítico (primeiro match vence)

---

#### Automático (`automatico/core/lexer.py`)
```python
tokens = [
    'COMENTARIO', 'STR_VALOR', 'REAL_VALOR', 'TEMPO_VALOR', ...
]

t_PASSE = r'<<'
t_IGUAL = r'=='
# ... tokens simples diretos

def t_COMENTARIO(self, t):
    r'\[.*?\]'
    nl = t.value.count('\n')
    if nl > 0:
        t.lexer.lineno += nl
    pass  # Ignora

def t_REAL_VALOR(self, t):
    r'\b\d+\.\d+\b'
    return t
```

**Explicação:**
- Tokens simples: atributos da classe (`t_PASSE = r'...'`)
- Tokens complexos: funções (`def t_COMENTARIO(...)`)
- PLY analisa esta classe e gera otimização interna

**Vantagem:** Mais legível, menos "mágia" de regex concatenação  
**Desvantagem:** Requer conhecimento de PLY

---

### 2. LOOP DE ANÁLISE

#### Manual
```python
def analisar(self, codigo_fonte):
    tokens_encontrados = []
    erros_encontrados = []
    
    linha_atual = 1
    inicio_linha = 0
    
    for match in self.re_compilada.finditer(codigo_fonte):
        tipo = match.lastgroup
        lexema = match.group()
        coluna = match.start() - inicio_linha + 1
        
        # Processamento: verificar tipo, validar, criar token
        tokens_encontrados.append(...)
    
    return tokens_encontrados, erros_encontrados
```

**O que acontece:**
1. Regex compilada varre o código
2. Para cada match, extrai tipo, lexema, coluna
3. Verifica se é válido
4. Retorna lista de tokens e lista de erros

**Vantagem:** Simples, fácil de debugar  
**Desvantagem:** Menos eficiente (regex compilada a cada iteração)

---

#### Automático (PLY)
```python
def __init__(self):
    self.lexer = lex.lex(module=self)

def analisar(self, codigo_fonte):
    self.lexer.input(codigo_fonte)
    
    while True:
        tok = self.lexer.token()
        if not tok:
            break
        
        # PLY já processou, pegamos direto o token
        self.tokens_encontrados.append(...)
    
    return self.tokens_encontrados, self.erros_encontrados
```

**O que acontece:**
1. PLY gera otimizações na inicialização
2. `lexer.input()` prepara o código
3. `lexer.token()` retorna próximo token (fast!)
4. PLY já chamou as funções `t_*` automaticamente

**Vantagem:** Rápido, robusto  
**Desvantagem:** "Caixa preta" (PLY faz internamente)

---

### 3. TRATAMENTO DE ERROS

#### Manual
```python
if tipo == 'ERRO_COMENTARIO':
    erros_encontrados.append(f"Linha: {linha_atual} - Coluna {coluna} - ERRO: ...")
elif tipo == 'ERRO_STRING':
    erros_encontrados.append(f"Linha: {linha_atual} - Coluna {coluna} - ERRO: ...")
# ... if/elif para cada tipo de erro
```

**Padrão:** Verifica tipo de token, se começar com `ERRO_`, registra

---

#### Automático (PLY)
```python
def t_ERRO_COMENTARIO(self, t):
    r'\[[^\]]*$'
    coluna = t.lexpos - self.inicio_linha + 1
    self.erros_encontrados.append(f"Linha: {t.lexer.lineno} - Coluna {coluna} - ERRO: ...")

def t_error(self, t):
    # Captura qualquer caractere não reconhecido
    coluna = t.lexpos - self.inicio_linha + 1
    self.erros_encontrados.append(f"... ERRO: Símbolo inválido: {t.value[0]}")
    t.lexer.skip(1)
```

**Padrão:** Função `t_ERRO_*` para erros específicos, `t_error()` para fallback

---

### 4. PALAVRAS RESERVADAS

#### Manual
```python
self.palavras_reservadas = {
    'apito_inicial': 'INICIO_JOGO',
    'apito_final': 'FIM_JOGO',
    # ... 30+ palavras
}

if tipo == 'PALAVRA':
    if lexema in self.palavras_reservadas:
        tipo = self.palavras_reservadas[lexema]
```

**Lógica:** Depois de reconhecer uma `PALAVRA`, verifica se é reservada

---

#### Automático (PLY)
```python
reserved = {
    'apito_inicial': 'INICIO_JOGO',
    # ... idêntico
}

tokens = [...] + list(reserved.values())

def t_PALAVRA(self, t):
    r'~?[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in self.reserved:
        t.type = self.reserved[t.value]
    return t
```

**Lógica:** Idêntica, mas PLY muda `t.type` em lugar de criar novo token

---

### 5. SINCRONIZAÇÃO DE LINHA/COLUNA

#### Manual
```python
linha_atual = 1
inicio_linha = 0

for match in self.re_compilada.finditer(codigo_fonte):
    coluna = match.start() - inicio_linha + 1
    
    if tipo == 'NEWLINE':
        linha_atual += 1
        inicio_linha = match.end()
        continue
```

**Abordagem:** Manual, você rastreia `linha_atual` e `inicio_linha`

---

#### Automático (PLY)
```python
self.inicio_linha = 0

def t_newline(self, t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    self.inicio_linha = t.lexpos + len(t.value)

# Na análise:
coluna = tok.lexpos - self.inicio_linha + 1
```

**Abordagem:** PLY gerencia `lineno`, você atualiza `inicio_linha`

---

## 🎯 Quando Usar Qual?

### Use **Manual** se:
✅ Está aprendendo análise léxica  
✅ Seu projeto é pequeno (< 100 tokens)  
✅ Não quer dependências externas  
✅ Precisa de controle total sobre cada passo  
✅ Debugar é prioridade  

### Use **Automático (PLY)** se:
✅ Está em produção  
✅ Seu projeto é médio/grande (> 100 tokens)  
✅ Quer adicionar parser depois  
✅ Performance é importante  
✅ Linguagem é complexa (regras ambíguas)  

---

## 📊 Benchmark Simulado

```
Código: 1000 linhas de Gol++
Tokens esperados: ~5000

Manual:
  - Compilação regex: ~2ms
  - Análise: ~50ms
  - Total: ~52ms

Automático (PLY):
  - Compilação PLY: ~5ms (once, on init)
  - Análise: ~15ms
  - Total: ~20ms
```

**Observação:** PLY é mais rápido em testes reais porque usa tabelas otimizadas internamente.

---

## 🔄 Como Estender?

### Adicionar Novo Token Manual

Arquivo: `manual/core/constants.py`
```python
token_specs = [
    # ... existentes
    ('NOVO_TOKEN', r'padrão_regex'),  # ← Adicionar aqui
]
```

Pronto! Nenhuma outra mudança necessária.

---

### Adicionar Novo Token Automático

Arquivo: `automatico/core/lexer.py`
```python
# Simples:
t_NOVO_SIMPLES = r'<<novo>>'

# Complexo:
def t_NOVO_COMPLEXO(self, t):
    r'novo_padrão'
    # ... lógica
    return t

# Adicione à lista de tokens:
tokens = [..., 'NOVO_SIMPLES', 'NOVO_COMPLEXO']
```

---

## 🚀 Próximos Passos Naturais

### Manual → Parser Manual
Adicionar análise sintática manual (classe `Parser`) ao `manual/core/parser.py`

### Automático → Parser PLY
PLY tem `yacc` integrado. Adicionar:
```python
import ply.yacc as yacc

class ParserGol:
    tokens = lexer.tokens
    
    def p_programa(self, p):
        '''programa : INICIO_JOGO statements APITO_FINAL'''
        p[0] = ('programa', p[2])
    
    # ... mais regras
    
    self.parser = yacc.yacc(module=self)
```

---

## 📚 Leitura Complementar

**Sobre Análise Léxica:**
- "Compilers: Principles, Techniques, and Tools" (Dragon Book)
- Tutorial Python `re` (regex): https://docs.python.org/3/library/re.html

**Sobre PLY:**
- Documentação oficial: http://www.dabeaz.com/ply/
- Exemplos: https://github.com/dabeaz/ply

**Sobre DSL (Domain Specific Language):**
- "Domain-Specific Languages" - Martin Fowler
- Artigos sobre linguagens baseadas em domínio

---

## ❓ FAQ Técnico

**P: Manual é mais lento?**  
R: Sim, ligeiramente. Mas para a maioria dos casos (< 10k linhas), a diferença é imperceptível.

**P: Posso misturar as duas abordagens?**  
R: Não é recomendado. Escolha uma e mantenha consistência.

**P: Qual PLY usa "por baixo"?**  
R: PLY gera uma máquina de estados com tabelas (DFA - Deterministic Finite Automaton).

**P: E se eu quiser adicionar recursão?**  
R: Isso é análise sintática, não léxica. Você vai querer um parser.

**P: Manual é mais "puro"?**  
R: Didaticamente sim. Você vê cada linha de lógica. Mas PLY é o padrão industrial.

---

**Versão:** 1.0  
**Última atualização:** 27 de maio de 2026  
**Status:** Completo
