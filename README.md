# Projeto Django: Gerenciamento de Tarefas
Este é um sistema web desenvolvido em Django para auxiliar no gerenciamento de tarefas. O objetivo principal é oferecer uma interface simples e funcional que permita ao usuário criar, editar, organizar e acompanhar suas tarefas diárias.

O projeto foi estruturado para ser escalável e flexível, servindo como uma base para futuras melhorias e novas funcionalidades, como integração com calendários, notificações e relatórios personalizados.

## ⚙️ Funcionalidades
### Gerenciamento de Tarefas:
- Adicionar novas tarefas com título e prioridade.
- Editar tarefas existentes.
- Classificar tarefas por categorias e prioridades.

### Organização das Tarefas:
- Tarefas pendentes.
- Tarefas concluídas.
- Tarefas adiadas.

### Gerenciamento de Categorias:
- Criar categorias para organizar as tarefas.
- Associar tarefas às categorias criadas.

### Templates:
- Página inicial com base em base.html.
- Páginas específicas para:
  - Criar categorias.
  - Adicionar e editar tarefas.
  - Visualizar tarefas pendentes, concluídas e adiadas.

### Banco de Dados SQLite:
- Utiliza o banco de dados SQLite para armazenar as informações sobre tarefas e categorias.


## 📝 Pré-requisitos
Antes de rodar o projeto, é necessário ter os seguintes componentes instalados:
- Python (>= 3.8)
- Anaconda
- Django (versão testada: 3.2+)

## 👨‍💻 Como Rodar o Projeto
Siga os passos abaixo para rodar o projeto localmente:
1. Baixe e Instale o Anaconda
Caso ainda não tenha o Anaconda, instale-o através do link oficial:
[Instalação do Anaconda](https://www.anaconda.com/download)

2. Crie um Ambiente no Anaconda

Abra o terminal ou prompt e execute:
```python
conda create -n meu_ambiente_django python=3.8
conda activate meu_ambiente_django
```

3. Instale as Dependências

Com o ambiente ativado, instale o Django e outras dependências necessárias:
```python
pip install django
```

4. Extraia o Projeto

Descompacte o arquivo fornecido (dia_organizado.zip) em uma pasta de sua escolha.

5. Realize as Migrações

Na pasta raiz do projeto, rode os seguintes comandos:
```python
python manage.py makemigrations
python manage.py migrate
```

6. Inicie o Servidor de Desenvolvimento

Para iniciar o servidor localmente, utilize o comando:
```python
python manage.py runserver
```

Acesse o projeto no navegador usando o seguinte link:
```python
http://127.0.0.1:8000/tarefas
```

### Observação
Lembre-se de rodar o servidor sempre no ambiente Anaconda criado (```meu_ambiente_django```) usando o comando ```conda activate meu_ambiente_django```.

## 📌 Estrutura do Projeto
A estrutura básica do projeto Django é a seguinte:
```python
DIA_ORGANIZADO/
│
├── dia_organizado/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── tarefas/
│   ├── __pycache__/
│   ├── migrations/
│   ├── templates/
│   │   └── ...  # Templates HTML
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── db.sqlite3
└── manage.py
```

## 📞 Contato
Caso tenha dúvidas ou sugestões, entre em contato pelo e-mail: gianmalfate@gmail.com
