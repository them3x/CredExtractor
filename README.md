# CredExtractor

**CredExtractor** é uma ferramenta em Python projetada para extrair credenciais (emails e senhas) e links de wordlists que não seguem um padrão fixo.

## 🔹 Características
✅ **Filtragem inteligente de credenciais** → Identifica e extrai combinações de email e senha mesmo em wordlists desorganizadas.  
✅ **Identifica links (URLs) automaticamente** → Capaz de detectar protocolos como HTTP, HTTPS, FTP, SMTP, IMAP, OAuth e muito mais.  
✅ **Reconhecimento de diversos delimitadores** → Suporte a `:`, `;`, `|`, ` `, entre outros.  
✅ **Correção de inconsistências** → Remove caracteres extras no final de emails, senhas e links para manter a precisão.  

## 🔹 Formatos de entrada suportados
A ferramenta é capaz de identificar credenciais e links mesmo que estejam misturados em diferentes formatos, como:

```
email@email.com P@ssw0rd123
P@ssw0rd123:email@email.com
email@email.com:email2@email2.net;P@ssw0rd123
email@email.com|P@ssw0rd123|email@email.com
P@ssw0rd123 email@email.com email@email.com
https://example.com:email@email.com;password123
```

## 🔹 Instalação
A ferramenta **não** necessita de bibliotecas externas. Para utilizá-la, basta clonar o repositório:

```bash
git clone https://github.com/them3x/CredExtractor.git
cd CredExtractor
```

## 🔹 Como usar

Crie um arquivo Python e importe o **CredExtractor**:

```python
from parsing import parsing

parser = parsing()

linha = "https://example.com email@email.com:password123"
prot, link, email1, email2, passwd = parser.parse(linha)

print("Protocolo:", prot)
print("Link:", link)
print("Email Principal:", email1)
print("Email Secundário:", email2)
print("Senha:", passwd)
```

**Saída esperada:**
```
Protocolo: https://
Link: example.com
Email Principal: email@email.com
Email Secundário: None
Senha: password123
```

## 🔹 Funcionalidades avançadas
### **1️⃣ Extração de Links**
- Identifica links completos com diversos protocolos (`http://`, `https://`, `ftp://`, `smtp://`, `imap://`, `oauth://`, etc.).
- Remove caracteres extras para garantir que o link seja extraído corretamente.

### **2️⃣ Extração de Credenciais**
- Analisa strings para identificar e extrair **emails e senhas**, mesmo em formatos incomuns.
- Suporta emails principais e secundários.
- Detecta combinações de delimitadores (`:`, `;`, `|`, ` `).

### **3️⃣ Verificação de Emails**
- Valida se o email possui formato correto.
- Verifica domínio e estrutura (`user@domain.tld`).

## 🔹 Exemplo de Uso em Wordlists
Se você tem um arquivo **wordlist.txt** e quer extrair todas as credenciais e links:

```python
import os
from parsing import parsing

parser = parsing()

with open("wordlist.txt", "r", encoding="utf-8", errors="ignore") as file:
    for line in file:
        prot, link, email1, email2, passwd = parser.parse(line)
        if email1 and passwd:
            print(f"{prot} {link} - {email1} / {passwd}")
```

## 📌 Contato e Contribuição
Caso tenha sugestões ou melhorias, sinta-se à vontade para abrir um **pull request** ou entrar em contato!



