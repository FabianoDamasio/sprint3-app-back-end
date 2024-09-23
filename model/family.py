from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import mapped_column, relationship
from datetime import datetime
from typing import Union

from model import Base, membro, family

class Family(Base):
    __tablename__ = 'family'
 
    id = mapped_column('pk_family', Integer, primary_key=True)
    last_name = mapped_column(String(200), nullable=False)
    membrers_ids = relationship("Membro")
    add_date = mapped_column(DateTime, default=datetime.now())

    def __init__(self, last_name:str, add_date:Union[DateTime, None] = None):

        """Create a new family"""

        self.last_name = last_name

        if add_date:
            self.add_date = add_date


    def edita_familia(self, family: family):
        """Edit family"""

        self.last_name = family.last_name