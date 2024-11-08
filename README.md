# Sistema de Agendamento para Web

Este projeto é um sistema de agendamento web de propósito geral que pode ser implementado por qualquer empresa. Com uma interface amigável e design responsivo, ele facilita o gerenciamento de compromissos e reservas em dispositivos móveis e desktops.

## Tecnologias Utilizadas

### Frontend
- **HTML**
- **CSS**
- **JavaScript**

### Backend
- **Python** com **Flask**

### Banco de Dados
- **PostgreSQL**

### Bibliotecas e Dependências
- Alembic 1.14.0
- Babel 2.16.0
- Bcrypt 4.2.0
- Blinker 1.8.2
- Click 8.1.7
- Colorama 0.4.6
- Customtkinter 5.2.2
- Darkdetect 0.8.0
- Flask 3.0.3
- Flask-Bcrypt 1.0.1
- Flask-Migrate 4.0.7
- Flask-SQLAlchemy 3.1.1
- Greenlet 3.1.1
- Itsdangerous 2.2.0
- Jinja2 3.1.4
- Mako 1.3.6
- MarkupSafe 3.0.2
- Packaging 24.1
- Pillow 11.0.0
- Psycopg2 2.9.10
- SQLAlchemy 2.0.36
- Tkcalendar 1.6.1
- Typing-extensions 4.12.2
- Werkzeug 3.1.1

### Ferramentas
- **Visual Studio Code** para desenvolvimento
- **PgAdmin** para administração do banco de dados

## Funcionalidades

- **Login**: Permite que os usuários acessem o sistema com suas credenciais.
- **Cadastro de Usuário**: Registra novos usuários no sistema.
- **Criação de Agendamento**: Possibilita o agendamento de compromissos.
- **Reimpressão de Agendamento**: Gera uma visualização do agendamento com os detalhes.
- **Cancelamento de Agendamento**: Permite cancelar um compromisso, mostrando uma mensagem de confirmação.

## Configuração e Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/Joaolucasos169/projeto-final-desenv.web-unifor.git

2. Instale as dependências:
   pip install -r requirements.txt

3. Configure o banco de dados PostgreSQL e insira as credenciais em config.py.
   
4. Execute as migrações para criar as tabelas:
   flask db upgrade

5. Inicie o servidor Flask:
   flask run

6. Acesse o projeto no navegador:
   http://127.0.0.1:5000

## Uso

Para um guia visual sobre como utilizar o sistema, você pode acessar o vídeo demonstrativo no [Google Drive](https://drive.google.com/drive/folders/1tPNEJbCIyMPaIMaMfwi0FJyFPNrOgOPg?usp=sharing).

## Contato

Para mais informações ou oportunidades de colaboração, sinta-se à vontade para me contatar pelo meu [LinkedIn](https://www.linkedin.com/in/jo%C3%A3o-lucas-oliveira-796504270/).
