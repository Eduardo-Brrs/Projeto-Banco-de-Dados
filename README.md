 Hospital Veterinário PetVida – Sistema Python + PostgreSQL

Este repositório contém a implementação completa do sistema do Hospital Veterinário PetVida, desenvolvido para fins acadêmicos na disciplina de Projeto de Banco de Dados do curso de Sistemas de Informação – CESMAC.

O projeto integra:

 Modelagem conceitual e lógica
 Banco de dados em PostgreSQL
 Sistema em Python
 Autenticação com senha criptografada
 Relacionamentos entre Dono, Animal, Consulta, Cirurgia e Usuário
 CRUD completo para todos os tipos de usuários

 Autores

Eduardo Souza de Barros
Gabriel Stoffel Cirilo

 Sobre o Projeto

O objetivo do sistema é permitir o gerenciamento completo do Hospital Veterinário PetVida, oferecendo funcionalidades diferentes para:

Administrador

Tutor (Dono do Animal)

Veterinário

Toda a aplicação foi construída em Python, utilizando psycopg2 para conexão com o banco de dados PostgreSQL, além de rotinas para autenticação via bcrypt e menus em terminal.

 Tecnologias Utilizadas
Backend

Python 3

psycopg2 (PostgreSQL driver)

bcrypt (hash de senha)

Banco de Dados

PostgreSQL 15+

Schema: petvida

Estrutura do Projeto
/src
   config.py
   main.py
   menus.py
   services.py
   utils.py

/database
   dbcode.sql  

 Modelagem do Banco

A modelagem inclui:

Minimundo

MER

DER

Regras de integridade e relacionamentos

Índices e constraints

Entidades principais:

Dono

Animal

Consulta

Cirurgia

Usuário (Administrador, Tutor, Veterinário)

 Como Executar o Sistema
1️⃣ Instalar dependências
pip install psycopg2 bcrypt

2️⃣ Criar banco de dados no PostgreSQL

Abra o pgAdmin

Crie um banco chamado, por exemplo: postgres ou petvida

Execute o script SQL encontrado em /database/dbcode

O script cria automaticamente:

Schema petvida

Todas as tabelas

Índices

Constraints

Atualizações (ALTER TABLE)

3️⃣ Configurar credenciais no arquivo

Abra o arquivo:

config.py


E ajuste:

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "SUA_SENHA",
    "options": "-c search_path=petvida"
}

4️⃣ Executar o sistema
python main.py


Na primeira execução, o sistema:

Cria o esquema e tabelas automaticamente

Garante que um administrador padrão exista

Exibe o menu principal de acesso

🧩 Funcionalidades
👑 Administrador

Cadastro e gerenciamento de usuários

Registro e edição de donos

Cadastro de animais

Agendamento e edição de consultas

Registro de cirurgias

Relatórios: animais por dono, consultas por período, etc.

Limpeza completa das tabelas

🧍‍♂️ Tutor (Cliente)

Ver seus dados e animais

Cadastrar novos animais

Ver consultas e cirurgias

Cancelar consultas

Atualizar informações do perfil

🩺 Veterinário

Ver lista de todos os animais

Registrar consultas

Registrar cirurgias

Acessar seus atendimentos específicos


 Segurança

O sistema utiliza:

Hash seguro de senha via bcrypt

Bloqueio de conta após tentativas incorretas

Controle de sessão por tipo de usuário

ON DELETE CASCADE para preservar integridade

 Licença

Este projeto foi desenvolvido para fins acadêmicos e pode ser reutilizado para estudo e aprendizado, desde que citados os autores.

✉️ Contato

📌 Eduardo Souza de Barros
📌 Gabriel Stoffel Cirilo
