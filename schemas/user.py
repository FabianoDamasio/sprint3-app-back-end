from pydantic import BaseModel
from typing import List

class UserSchema(BaseModel):
    """ Define como um novo usuário a ser inserido deve ser representado
    """
    login: str = "Fabiano"
    password: str = "senha"

class UserBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca.
    """
    login: str = ""
    password: str = ""

class UserViewchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca.
    """
    check: bool

class UserDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    login: str

class ListagemUsersSchema(BaseModel):
    """ Define como uma listagem de famílias será retornada.
    """
    family: List[UserDelSchema]

def show_users(users: List[UserSchema]):
    """ Retorna uma representação de famílias seguindo o schema definido em
        Family.
    """
    result = []
    for users in users:
        result.append({
            "login": users.login,
        })

    return {"users": result}