from pydantic import BaseModel
from typing import Optional, List
from model.membro import Membro

class MembroSchema(BaseModel):
    """ Define como um novo membro a ser inserido deve ser representado
    """
    name: str = "Fabiano"
    cpf: int = 00000000000
    age: int = 33
    civil_status: str = "Casado"
    street: str = "Rua Aureliano Pires"
    number: int = 22
    complement: str = "Apartamento 303"
    district: str = "Serraria"
    city: str = "São José"
    cep: int = 00000000

class MembroBuscaUnicaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome ou no cpf do membro.
    """
    cpf: int = 0

class MembroBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome ou no cpf do membro.
    """
    name: str = ""
    cpf: int = 0
    id: int = 0


class ListagemMembrosSchema(BaseModel):
    """ Define como uma listagem de membro será retornada.
    """
    membros:List[MembroSchema]


def apresenta_membros(membros: List[Membro]):
    """ Retorna uma representação do membro seguindo o schema definido em
        MembroViewSchema.
    """
    result = []
    for membro in membros:
        result.append({
            "id": membro.id,
            "nome": membro.name,
            "cpf": membro.cpf,
            "idade": membro.age,
            "estadoCivil": membro.civil_status,
            "endereço": membro.street,
            "numero": membro.number,
            "complemento": membro.complement,
            "bairro": membro.district,
            "cidade": membro.city,
            "cep": membro.cep,
            "família": membro.family
        })

    return {"membros": result}


class MembroViewSchema(BaseModel):
    """ Define como um membro será retornado: membro + família.
    """
    name: str = "Fabiano Damasio"
    cpf: int = 00000000000
    age: int = 33
    civil_status: str = "Casado"
    street: str = "Rua Aureliano Pires"
    number: int = 22
    complement: str = "Apartamento 303"
    district: str = "Serraria"
    city: str = "São José"
    cep: int = 00000000
    family: str = "Damasio"


class MembroDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    name: str

def apresenta_membro(membro: Membro):
    """ Retorna uma representação do membro seguindo o schema definido em
        Membro.
    """
    return {
        "id": membro.id,
        "nome": membro.name,
        "cpf": membro.cpf,
        "idade": membro.age,
        "estado civil": membro.civil_status,
        "endereço": membro.street,
        "numero": membro.number,
        "complemento": membro.complement,
        "bairro": membro.district,
        "cidade": membro.city,
        "cep": membro.cep,
        "família": membro.family
    }