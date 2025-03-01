# CredExtractor

## Descrição

A classe `parsing` foi desenvolvida para filtrar e extrair combinações de **email/senha** a partir de wordlists que não possuem um padrão fixo e definido. Diferente de filtros simples, essa classe permite identificar padrões mistos e inconsistentes, facilitando a extração de credenciais válidas em grandes volumes de dados.

O algoritmo é capaz de identificar e extrair credenciais em diversos formatos, como:
- `email<limiteador>senha`
- `senha<limiteador>email`
- `email<limiteador>email<limiteador2>senha`
- `email<limiteador>senha<limiteador2>email`
- `senha<limiteador>email<limiteador2>email`

## Funcionalidades

- **Filtragem inteligente de credenciais**: Identifica e extrai combinações de email e senha mesmo quando não há um padrão fixo na wordlist.
- **Identifica endereços de email válidos**: Verifica se o email segue padrões válidos antes da extração.
- **Suporte a diversos delimitadores**: Reconhece delimitadores como `:`, `;`, `|` e ` ` para separação de credenciais.
- **Correção de inconsistências**: Remove delimitadores extras no final de emails e senhas.

## Instalação

Não são necessárias bibliotecas externas. Basta clonar ou baixar o arquivo `parsing.py` e importá-lo em seu projeto.

```bash
# Clonar o repositório
$ git clone https://github.com/seu-repositorio.git
```

## Uso

1. Com a classe no mesmo diretorio **Importe a classe `parsing` em seu projeto:**

```python
from parsing import parsing
```

2. **Crie uma instância da classe:**

```python
parser = parsing()
```

3. **Chame o método `parse()` para processar uma linha de wordlist:**

```python
email1, email2, senha = parser.parse("exemplo@email.com:senha123")
print(email1, email2, senha)
```

🔹 **Saída:**
```
exemplo@email.com None senha123
```

4. **Testando diferentes padrões de entrada:**

```python
print(parser.parse("senha123:usuario@email.com"))  # Inverte os valores
print(parser.parse("primeiro@email.com;senha321")) # Identifica email e senha
print(parser.parse("conta@email.com:backup@email.com;passw0rd")) # Dois emails e senha
```

🔹 **Saída esperada:**
```
('usuario@email.com', None, 'senha123')
('primeiro@email.com', None, 'senha321')
('conta@email.com', 'backup@email.com', 'passw0rd')
(None, None, None)

```



