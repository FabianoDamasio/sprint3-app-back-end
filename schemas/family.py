from pydantic import BaseModel
from typing import List
from model.family import Family

from schemas.membro import MembroSchema

class FamilySchema(BaseModel):
    last_name: str = "Damasio"

class ListagemFamiliasSchema(BaseModel):
    """ Define como uma listagem de famílias será retornada.
    """
    family: List[FamilySchema]

class FamilyViewchema(BaseModel):
    id: int = 1
    last_name: str = "Damasio"
    membrers_ids: List[MembroSchema]

class FamilyBuscaSchema(BaseModel):
    id: int = 0
    sobrenome: str = ""

class FamilyDelSchema(BaseModel):
    mesage: str
    família: str

class FamilySchemaMember(BaseModel):
    sobrenome: str = "Damasio"
    id_do_membro: int = 1

class FamilyEditSchema(BaseModel):
    novo_sobrenome: str = ""

def show_family(family: Family):
    """ Retorna uma representação do membro seguindo o schema definido em
        membroViewSchema.
    """
    return {
        "id": family.id,
        "Sobrenome": family.last_name,
        "Membros da Família": [{"integrante": c.name} for c in family.membrers_ids]
    }

def show_familys(family: List[Family]):
    """ Retorna uma representação de famílias seguindo o schema definido em
        Family.
    """
    result = []
    for family in family:
        result.append({
            "id": family.id,
            "Sobrenome": family.last_name,
            "Membros da Família": [{"integrante": c.name, "id": c.id} for c in family.membrers_ids]
        })

    return {"famílias": result}