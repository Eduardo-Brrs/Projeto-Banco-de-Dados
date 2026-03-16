# PETVIDA VETERINARY HOSPITAL
### Management System in Python + PostgreSQL
EN-US
---

## AUTHORS
Eduardo Souza de Barros  
Gabriel Stoffel Cirilo

---

## TABLE OF CONTENTS
- Overview
- System Architecture
- Technologies Used
- Installation
- Configuration
- Execution
- Database Modeling
- Features
- Security
- Directory Structure

---

## OVERVIEW

PetVida is a veterinary management system developed in Python integrated with PostgreSQL.

The application allows management of pet owners, animals, consultations, surgeries, and system users, with role-based access control (Administrator, Owner, and Veterinarian).

This project was developed for academic purposes, following good practices of database modeling, referential integrity, and modular code structure.

---

## SYSTEM ARCHITECTURE

The system is divided into modules to improve maintainability, readability, and organization.

src/
config.py → PostgreSQL configuration and connection  
main.py → Main application entry point  
menus.py → System menus and navigation  
services.py → Business logic and SQL operations  
utils.py → Validation functions and utilities  

---

## TECHNOLOGIES USED

Backend
- Python 3
- psycopg2 (PostgreSQL integration)
- bcrypt (secure password hashing)

Database
- PostgreSQL
- Schema used: petvida

Tools
- pgAdmin
- Git
- GitHub

---

## INSTALLATION

Install dependencies:

pip install psycopg2 bcrypt

Make sure PostgreSQL is installed and running.

---

## CONFIGURATION

Update the config.py file with your database connection settings.

DB_CONFIG = {
"host": "localhost",
"port": 5432,
"dbname": "postgres",
"user": "postgres",
"password": "YOUR_PASSWORD",
"options": "-c search_path=petvida"
}

After that run the SQL script:

database/dbcode.sql

This script creates:

- petvida schema
- all system tables
- constraints
- indexes

---

## EXECUTION

Run the system with:

python main.py

During the first execution:

- The schema will be created if it does not exist
- Tables will be automatically generated
- A default administrator user will be created
- The main menu will be displayed

---

## DATABASE MODELING

Based on the Minimundo, ER Model (MER), and ER Diagram (DER) created for the academic project.

Main Entities

- Owner
- Animal
- Consultation
- Surgery
- User (Administrator, Owner, Veterinarian)

Relationships

Owner → Animal  
Animal → Consultation  
Animal → Surgery  
User (Owner) → Owner  

Integrity is enforced using foreign keys and ON DELETE CASCADE.

---

## FEATURES

Administrator
- Manage users
- Manage owners
- Manage animals
- Register consultations
- Register surgeries
- Generate reports

Owner
- View personal data
- Update personal information
- Register animals
- View registered animals
- Check consultations
- Cancel consultations

Veterinarian
- View animals
- Register consultations
- Register surgeries
- View their own appointments
- Filter consultations by period

---

## SECURITY

The system implements:

- Password hashing with bcrypt
- Login blocking after multiple failed attempts
- Input validation
- Role-based access control
- PostgreSQL constraints

---

## DIRECTORY STRUCTURE

petvida/
petvida/ → source code  
config.py → database configuration  
main.py → system entry point  
menus.py → menu navigation  
services.py → business logic  
utils.py → validation functions  

docs/ → project documentation  
dbcode.sql → database creation script  
README.md → repository documentation  

---
## LICENSE

This project was developed for academic purposes as part of the **Database Project course at CESMAC**.

Use for study and educational purposes is permitted, provided that the authors are properly credited.

Authors:  
**Eduardo Souza de Barros**  
**Gabriel Stoffel Cirilo**

---

# HOSPITAL VETERINÁRIO PETVIDA  
### Sistema de Gerenciamento em Python + PostgreSQL
PT-BR
---

## AUTORES  
**Eduardo Souza de Barros**  
**Gabriel Stoffel Cirilo**

---

## SUMÁRIO
- Visão Geral  
- Arquitetura do Sistema  
- Tecnologias Utilizadas  
- Instalação  
- Configuração  
- Execução  
- Modelagem do Banco  
- Funcionalidades  
- Segurança  
- Estrutura de Diretórios  
- Licença  

---

## VISÃO GERAL

O Sistema PetVida é uma aplicação de gerenciamento veterinário desenvolvida em Python integrado ao banco PostgreSQL.  
A solução permite administrar tutores, animais, consultas, cirurgias e usuários, com controle de acesso baseado em perfis (Administrador, Tutor e Veterinário).

O sistema foi projetado para fins acadêmicos, seguindo boas práticas de modelagem, integridade referencial e divisão modular.

---

## ARQUITETURA DO SISTEMA

O sistema foi dividido em módulos para facilitar manutenção, leitura e organização:

```
src/
│  config.py        → Configuração e conexão com PostgreSQL
│  main.py          → Arquivo principal e fluxo da aplicação
│  menus.py         → Todos os menus e navegação
│  services.py      → Regras de negócio e operações SQL
│  utils.py         → Funções de validação e utilidades
```

---

## TECNOLOGIAS UTILIZADAS

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

## INSTALAÇÃO

Instale as dependências do projeto:

```bash
pip install psycopg2 bcrypt
```

Certifique-se de que o PostgreSQL está instalado e funcionando corretamente.

---

## CONFIGURAÇÃO

Ajuste o arquivo `config.py` com os dados da sua conexão:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "SUA_SENHA",
    "options": "-c search_path=petvida"
}
```

Após isso, execute o script SQL:

```
/database/dbcode.sql
```

Esse script cria:

- O schema `petvida`
- Todas as tabelas do sistema
- Constraints
- Índices
- Ajustes finais com ALTER TABLE

---

## EXECUÇÃO

Para iniciar o sistema:

```bash
python main.py
```

Na primeira execução:

- O schema será criado (caso não exista)
- As tabelas serão criadas automaticamente
- Um administrador padrão será gerado
- O menu principal será exibido

Após o login, o usuário acessa o menu correspondente ao seu perfil.

---

## MODELAGEM DO BANCO

Baseada no Minimundo, MER e DER desenvolvidos no projeto acadêmico.

### Entidades Principais
- **Dono**
- **Animal**
- **Consulta**
- **Cirurgia**
- **Usuário** (Administrador, Tutor e Veterinário)

### Relacionamentos Essenciais
- Dono → Animal  
- Animal → Consulta  
- Animal → Cirurgia  
- Usuário (Tutor) → Dono  

Toda integridade é mantida via foreign keys e políticas ON DELETE CASCADE.

---

## FUNCIONALIDADES

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

## SEGURANÇA

O sistema implementa:

- Hash seguro de senha via `bcrypt`  
- Bloqueio após múltiplas tentativas incorretas  
- Validação de entrada em todos os menus  
- Controle rígido de permissões por tipo de usuário  
- Integridade garantida via constraints no PostgreSQL  

---

## ESTRUTURA DE DIRETÓRIOS
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
├── dbcode.sql              # Script SQL contendo criação de schema, tabelas e constraints
│
├── README.md               # Documentação principal do repositório
│
```

---

## LICENÇA

Projeto acadêmico desenvolvido para a disciplina de Projeto de Banco de Dados – CESMAC.  
Uso permitido para fins de estudo, desde que citados os autores:  
**Eduardo Souza de Barros**  
**Gabriel Stoffel Cirilo**
