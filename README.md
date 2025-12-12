# Projeto-Web

## Integrantes do Grupo

Luis Antônio Lustosa de Araújo Costa — RA: 22401677

Davi de Albuquerque Chavante — RA: XXXX

Davi Carvalho Aguiar Morais — RA: 22350152

## Descrição Geral do Projeto

Este projeto é um Sistema de Gerenciamento de Eventos Acadêmicos desenvolvido em Django e Django REST Framework.
O sistema permite que usuários cadastrem, visualizem, editem e excluam eventos relacionados ao ambiente acadêmico, tais como:

Palestras

Workshops

Seminários

Congressos

Minicursos

O objetivo do sistema é facilitar a organização e controle de eventos dentro de instituições educacionais, permitindo um fluxo simples e eficiente tanto para administradores quanto para participantes.

## Principais Funcionalidades
- Cadastro de eventos

Com informações como:

título

descrição

data e horário

local

professor/responsável

número de vagas

-Listagem de eventos

Interface amigável para visualizar todos os eventos cadastrados.

- Detalhamento do evento

Exibe informações completas do evento selecionado.

- Edição e exclusão

Administradores podem editar ou remover eventos facilmente.

- API REST completa

Todas as operações também podem ser realizadas via endpoints JSON.


 ## O sistema segue a estrutura tradicional de um projeto Django:

Models

Representam os eventos no banco de dados.
Cada evento é mapeado como uma tabela no SQLite.

Views

Controlam:

Páginas web (HTML)

Operações da API (JSON)

Serializers

Transformam modelos em JSON para a API e validam dados recebidos.

Forms

Criam automaticamente formulários para cadastro/edição de eventos.

Templates

Páginas HTML usadas para exibir listas, formulários, detalhes, etc.

URLs

Cada funcionalidade (web e API) possui uma rota própria.



## Como inicializar?

Clonar o repositório


git clone https://github.com/luislustosa/Projeto-Web

cd Projeto-Web

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

(TODOS ESSES COMANDOS NO TERMINAL)

ACESSAR : http://localhost:8000


## COMO POPULAR O BANCO DE DADOS? 

acessar a conta de admin -- nome: Organizador ; senha: Admin@123 

#### OU usando o script python

Por exemplo:
import requests

evento = {
    "titulo": "Seminário de IA",
    "descricao": "Discussão sobre IA Generativa",
    "local": "Sala 12",
    "data": "2025-04-10",
    "horario": "09:30",
    "vagas": 50
}

requests.post("http://localhost:8000/api/eventos/", json=evento)

#### OU por meio da api - Postman

POST /api/eventos/

{
  "titulo": "Semana da Computação",
  "descricao": "Evento com palestras e workshops",
  "local": "Auditório Central",
  "data": "2025-03-20",
  "horario": "14:00",
  "vagas": 120
}


Conclusao:
Este Sistema de Gerenciamento de Eventos Acadêmicos demonstra um projeto completo Django:
CRUD, API REST, templates, formulários e banco de dados.
