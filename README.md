# PetVida — Hospital Veterinário

Sistema de gerenciamento em Python + PostgreSQL.

[English](README.en.md) · **Português**

---

## Autores
Eduardo Souza de Barros  
Gabriel Stoffel Cirilo

---


## Visão geral

O Sistema PetVida é uma aplicação de gerenciamento veterinário desenvolvida em Python integrado ao banco PostgreSQL.  
A solução permite administrar tutores, animais, consultas, cirurgias e usuários, com controle de acesso baseado em perfis (Administrador, Tutor e Veterinário).

O sistema foi projetado para fins acadêmicos, seguindo boas práticas de modelagem, integridade referencial e divisão modular.

---

## Arquitetura do sistema

O sistema foi dividido em módulos para facilitar manutenção, leitura e organização:

```
petvida/
│  config.py        → Configuração e conexão com PostgreSQL
│  main.py          → Arquivo principal e fluxo da aplicação
│  menus.py         → Todos os menus e navegação
│  services.py      → Regras de negócio e operações SQL
│  utils.py         → Funções de validação e utilidades
```

---

## Tecnologias utilizadas

### Backend
- Python 3  
- psycopg2 (integração com PostgreSQL)  
- bcrypt (hash seguro de senha)

### Banco de Dados
- PostgreSQL  
- Schema utilizado: `petvida`

### Ferramentas adicionais
- pgAdmin  
- Git / GitHub  

---

## Instalação

Instale as dependências do projeto:

```bash
pip install psycopg2 bcrypt
```

Certifique-se de que o PostgreSQL está instalado e funcionando corretamente.

---

## Configuração

Defina a senha do PostgreSQL na variável de ambiente `PETVIDA_DB_PASSWORD`:

```bash
export PETVIDA_DB_PASSWORD="sua_senha"      # Linux / macOS
set PETVIDA_DB_PASSWORD=sua_senha           # Windows (cmd)
```

Os outros dados da conexão ficam em `config.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": os.environ.get("PETVIDA_DB_PASSWORD", ""),
    "options": "-c search_path=petvida"
}
```

Após isso, execute o script SQL `dbcode.txt` (na raiz do repositório) no PostgreSQL, por exemplo pelo pgAdmin ou com:

```bash
psql -U postgres -f dbcode.txt
```

Esse script cria:

- O schema `petvida`
- Todas as tabelas do sistema
- Constraints
- Índices
- Ajustes finais com ALTER TABLE

---

## Execução

Para iniciar o sistema:

```bash
cd petvida
python main.py
```

Na primeira execução:

- O schema será criado (caso não exista)
- As tabelas serão criadas automaticamente
- Um administrador padrão será gerado
- O menu principal será exibido

Após o login, o usuário acessa o menu correspondente ao seu perfil.

---

## Modelagem do banco

Baseada no Minimundo, MER e DER desenvolvidos no projeto acadêmico.

### Entidades Principais
- Dono
- Animal
- Consulta
- Cirurgia
- Usuário (Administrador, Tutor e Veterinário)

### Relacionamentos Essenciais
- Dono → Animal  
- Animal → Consulta  
- Animal → Cirurgia  
- Usuário (Tutor) → Dono  

Toda integridade é mantida via foreign keys e políticas ON DELETE CASCADE.

---

## Funcionalidades

### Administrador
- Criar, editar e excluir usuários  
- Gerenciar tutores  
- Gerenciar animais  
- Registrar consultas  
- Registrar cirurgias  
- Relatórios:
  - Animais por tutor  
  - Consultas por período  
  - Busca por CPF  
- Limpeza geral das tabelas para manutenção  

---

### Tutor (Cliente)
- Visualizar dados pessoais  
- Atualizar informações  
- Cadastrar animais  
- Visualizar animais cadastrados  
- Consultar consultas  
- Cancelar consultas  

---

### Veterinário
- Visualizar animais cadastrados  
- Registrar consultas  
- Registrar cirurgias  
- Ver seus próprios atendimentos  
- Filtrar consultas por período  

---

## Segurança

O sistema implementa:

- Hash seguro de senha via `bcrypt`  
- Bloqueio após múltiplas tentativas incorretas  
- Validação de entrada em todos os menus  
- Controle rígido de permissões por tipo de usuário  
- Integridade garantida via constraints no PostgreSQL  

---

## Estrutura de diretórios
```
petvida/
├── petvida/                # Pasta principal do código-fonte da aplicação
│   ├── config.py           # Configurações do banco de dados
│   ├── main.py             # Arquivo principal que inicia o sistema
│   ├── menus.py            # Menus e navegação por perfis
│   ├── services.py         # Regras de negócio e operações SQL
│   ├── utils.py            # Funções auxiliares (validações, leitura, etc.)
│
├── docs/                   # Documentação do projeto (MER, DER, Minimundo, relatório etc.)
│   └── *arquivos.docx*
│
├── dbcode.txt              # Script SQL contendo criação de schema, tabelas e constraints
│
├── README.md               # Documentação principal do repositório
│
```

---

## Licença

Projeto acadêmico desenvolvido para a disciplina de Projeto de Banco de Dados – CESMAC.  
Uso permitido para fins de estudo, desde que citados os autores:  
Eduardo Souza de Barros  
Gabriel Stoffel Cirilo
