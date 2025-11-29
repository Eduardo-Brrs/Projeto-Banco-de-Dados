# HOSPITAL VETERINÁRIO PETVIDA  
### Sistema de Gerenciamento em Python + PostgreSQL

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

```text
/
├── src/
│   ├── main.py
│   ├── menus.py
│   ├── services.py
│   ├── utils.py
│   └── config.py
│
├── database/
│   └── dbcode.sql
│
├── docs/
│   └── Documentação (MER, DER, Minimundo)
│
└── README.md
```

---

## LICENÇA

Projeto acadêmico desenvolvido para a disciplina de Projeto de Banco de Dados – CESMAC.  
Uso permitido para fins de estudo, desde que citados os autores:  
**Eduardo Souza de Barros**  
**Gabriel Stoffel Cirilo**
