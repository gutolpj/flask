# flask
Documentação do Código Flask
Resumo
Este é um aplicativo Flask para gerenciamento de jogos e usuários. Ele inclui funcionalidades como criação, edição e exclusão de jogos, login e autenticação de usuários, e gerenciamento de usuários.

Configuração do Ambiente
Antes de executar o aplicativo, é necessário ter Python, Flask e SQLAlchemy instalados. O aplicativo também requer um banco de dados MySQL.

Estrutura do Código
Imports:

Flask, render_template, request, redirect, session, flash, url_for: Para criar e gerenciar rotas e renderizar templates HTML.
SQLAlchemy: Para interagir com o banco de dados.
datetime: Para trabalhar com datas e horários.
Configuração do Flask:

app: Cria uma instância do Flask.
app.secret_key: Define a chave de segurança para a sessão.
app.config['SQLALCHEMY_DATABASE_URI']: Define a URI do banco de dados.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']: Configura o rastreamento de modificações no SQLAlchemy.
Modelos de Dados:

Jogo: Define o modelo para a tabela de jogos no banco de dados.
Usuario: Define o modelo para a tabela de usuários no banco de dados.
Função de Criação de Usuário Admin:

create_admin_user(): Verifica se o usuário admin já existe no banco de dados e o cria se não existir.
Rotas:

/: Página inicial do aplicativo, lista todos os jogos.
/novo: Página para adicionar um novo jogo.
/criar: Rota para criar um novo jogo.
/login: Página de login.
/logout: Rota para fazer logout.
/autenticar: Rota para autenticar o usuário.
/usuarios: Lista todos os usuários (apenas para admin).
/novo_usuario: Página para adicionar um novo usuário (apenas para admin).
/criar_usuario: Rota para criar um novo usuário (apenas para admin).
/editar_usuario/<int:id>: Página para editar um usuário específico (apenas para admin).
/atualizar_usuario/<int:id>: Rota para atualizar os dados de um usuário (apenas para admin).
/deletar_usuario/<int:id>: Rota para excluir um usuário (apenas para admin).
/ola: Rota de teste para retornar uma mensagem "Olá mundo".
Criação do Banco de Dados e Tabelas:

O código verifica se o banco de dados e as tabelas estão criadas e cria-as, se necessário, ao iniciar o aplicativo.
Execução do Aplicativo
Para executar o aplicativo, basta rodar o script Python. Certifique-se de que o banco de dados MySQL está em execução e acessível. Após a execução, o aplicativo estará disponível em http://localhost:5000/.

Observações
Certifique-se de configurar corretamente a URI do banco de dados no código antes de executar o aplicativo.
A função create_admin_user() garante que sempre haverá um usuário admin no banco de dados.
Algumas rotas só estão acessíveis para o usuário admin, como a listagem e o gerenciamento de usuários.