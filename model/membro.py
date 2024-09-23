from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column
from datetime import datetime
from typing import Union

from model import Base, family

class Membro(Base):
    __tablename__ = 'membrezia'

    id = mapped_column("pk_membro", Integer, primary_key=True)
    name = mapped_column(String(140), unique=True, nullable=False)
    cpf = mapped_column(Integer, nullable=False)
    age = mapped_column(Integer)
    civil_status = mapped_column(String(50))
    street = mapped_column(String(200))
    number = mapped_column(Integer)
    complement = mapped_column(String(200))
    district = mapped_column(String(50))
    city = mapped_column(String(50))
    cep = mapped_column(Integer)
    family = mapped_column(Integer, ForeignKey("family.pk_family"))
    add_date = mapped_column(DateTime, default=datetime.now())

    def __init__(self, name:str, cpf:int, age:int, civil_status:str, street:str, number:int, complement:str, district:str, city:str, cep:int,
                 add_date:Union[DateTime, None] = None):

        """Add new membro"""

        self.name = name
        self.cpf = cpf
        self.age = age
        self.civil_status = civil_status
        self.street = street
        self.number = number
        self.complement = complement
        self.district = district
        self.city = city
        self.cep = cep

        # se não for informada, será o data exata da inserção no banco
        if add_date:
            self.add_date = add_date

    def adiciona_familia(self, family: family):
        """Add member in family"""

        self.family = family.id

