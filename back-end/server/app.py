from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from unidecode import unidecode
from sqlalchemy.exc import IntegrityError
from model import Session, Produto, Comentario
from schemas import *
from flask_cors import CORS


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# DOCUMENTAÇÃO DO SWAGGER
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um produto cadastro na base")

# ROTA PRINCIPAL
@app.get("/", tags=[home_tag]) # O método GET já é imposto  por padrão
def home():
    return redirect('/openapi'), 200

# BUSCA TODOS OS PRODUTOS DA BASE E RETORNA PARA A
# FUNÇÃO "getList" DO SCRIPT.JS
@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})

def get_produtos():
    """
        Faz a busca por todos os Produto cadastrados
        Retorna uma representação da listagem de produtos.
    """

    session = Session() # criando conexão com a base

    produtos = session.query(Produto).all() # fazendo a busca

    # se não há produtos cadastrados
    if not produtos:
        return {"produtos": []}, 200
    # retorna a representação de produto
    else:
        return apresenta_produtos(produtos), 200

# ROTA PARA ADICIONAR UM NOVO PRODUTO NA BASE
@app.post('/adicionar_produto', tags=[produto_tag],
        responses= { "200": ProdutoViewSchema, "409": ErrorSchema, "400" : ErrorSchema } )
def add_produto(form: ProdutoSchema):
    '''
        Adiciona um novo produto na base
    '''

    produto = Produto(
        nome=unidecode(form.nome.lower()),
        categoria=unidecode(form.categoria.lower()),
        quantidade=form.quantidade,
        valor=form.valor
    )
    
    try:
        session = Session() # criando conexão com a base

        session.add(produto) # adicionando produto

        session.commit() # salvando o dado na base

        return apresenta_produto(produto), 200
    
    # como a duplicidade do nome é a provável razão do Integrity Error
    except IntegrityError as e:
        error_msg = "Produto de mesmo nome já salvo na base"
        return {"mesage": error_msg}, 409
    
    # caso haja um erro fora do previsto
    except Exception as e:
        error_msg = "Não foi possível salvar novo item."
        return {"mesage": error_msg}, 400

# BUSCA PRODUTOS POR NOME
@app.get('/buscar_produto_nome', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})

def get_produto(query: ProdutoBuscaSchema):
    """
        Faz a busca por um Produto a partir do nome do produto
    """

    produto_nome = query.nome # faz uma busca por nome

    session = Session() # criando conexão com a base

    produto = session.query(Produto).filter(Produto.nome == produto_nome).first() # fazendo a busca

    # se o produto não foi encontrado
    if not produto:
        error_msg = "Produto não encontrado na base." 
        return {"mesage": error_msg}, 404
    # retorna a representação de produto
    else:
        return apresenta_produto(produto), 200
    
# BUSCA PRODUTOS POR CATEGORIA
@app.get('/buscar_produto_categoria', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})

def get_produto_categoria(query: CategoriaBuscaSchema):
    """
        Faz uma busca por uma Categoria de produtos
    """
    produto_categoria = query.categoria # faz uma busca por categoria

    session = Session() # criando conexão com a base

    produto = session.query(Produto).filter(Produto.categoria == produto_categoria) # fazendo a busca

    # se a categoria não foi encontrado
    if not produto:
        error_msg = "Categoria não encontrada na base."
        return {"mesage": error_msg}, 404
    # retorna a representação de produtos da categoria
    else:
        return apresenta_categoria_produtos(produto), 200
    
@app.delete('/deletar_produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})

# DELETA UM PRODUTO CADASTRADO A PARTIR DO NOME
def del_produto(query: ProdutoBuscaSchema):
    """
        Deleta um Produto a partir do nome de produto informado
    """
    produto_nome = unquote(unquote(query.nome)) # Decodificador de strings em URLs

    session = Session() # criando conexão com a base

    count = session.query(Produto).filter(Produto.nome == produto_nome).delete() # fazendo a remoção

    session.commit() # salvando a base

    # retorna a representação da mensagem de confirmação
    if count:
        return {"mesage": "Produto removido", "id": produto_nome}
    # se o produto não foi encontrado
    else:
        error_msg = "Produto não encontrado na base." 
        return {"mesage": error_msg}, 404
    
# ADICIONA UM COMENTARIO NO PRODUTO
@app.post('/adicionar_comentario', tags=[comentario_tag],
          responses={"200": ProdutoViewSchema, "404": ErrorSchema})

def add_comentario(form: ComentarioSchema):
    """
        Adiciona de um novo comentário à um produtos cadastrado na base identificado pelo id
    """
    produto_id = form.produto_id

    session = Session() # criando conexão com o banco

    produto = session.query(Produto).filter(Produto.id == produto_id).first() # fazendo a busca pelo produto

    # se produto não for encontrado
    if not produto:
        error_msg = "Produto não encontrado na base."
    
    # criando comentario
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao produto
    produto.adiciona_comentario(comentario)
    session.commit()

    return apresenta_produto(produto), 200     # retorna a representação de produto