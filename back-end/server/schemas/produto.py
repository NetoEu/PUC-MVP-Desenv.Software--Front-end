from pydantic import BaseModel
from typing import Optional, List
from model.produto import Produto

from schemas import ComentarioSchema

class ProdutoSchema(BaseModel):
    """ 
        Define como um novo produto a ser inserido deve ser representado
    """
    nome: str = "Mochila Simples"
    categoria: str = "Mochilas"
    quantidade: Optional[int] = 25
    valor: float = 52.50

class ListagemCategorySchema(BaseModel):
    """ 
       Define como uma listagem de produtos da categoria será retornada.
    """
    categorias: List[ProdutoSchema]

class ProdutoBuscaSchema(BaseModel):
    """ 
        Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    nome: str = ''

class CategoriaBuscaSchema(BaseModel):
    """ 
        Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da categoria.
    """
    categoria: str = ''

class ListagemProdutosSchema(BaseModel):
    """ 
        Define como uma listagem de produtos será retornada.
    """
    produtos: List[ProdutoSchema]

class ProdutoViewSchema(BaseModel):
    """ 
        Define como um produto será retornado: produto + comentários.
    """
    id: int = 1
    nome: str = "Mochila Simples"
    categoria: str = "mochilas"
    quantidade: Optional[int] = 25
    valor: float = 52.50
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]

class ProdutoDelSchema(BaseModel):
    """ 
        Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_produto(produto: Produto):
    """ 
        Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": produto.id,
        "nome": produto.nome,
        "categoria": produto.categoria,
        "quantidade": produto.quantidade,
        "valor": produto.valor,
        "total_comentarios": len(produto.comentarios),
        "comentarios": [{"texto": c.texto} for c in produto.comentarios]
    }

def apresenta_produtos(produtos: List[Produto]):
    """ 
        Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for produto in produtos:
        result.append({
            "nome": produto.nome,
            "categoria": produto.categoria,
            "quantidade": produto.quantidade,
            "valor": produto.valor
        })

    return {"produtos": result}

# Busca na base de dados a categoria e retorna um dicionário com os produtos da categoria 
# buscada

def apresenta_categoria_produtos(categorias: List[Produto.categoria]):

    result_categorias = []
    for produto in categorias:
        result_categorias.append({
            "nome": produto.nome,
            "categoria": produto.categoria,
            "quantidade": produto.quantidade,
            "valor": produto.valor
        })

    return {"produtos": result_categorias}