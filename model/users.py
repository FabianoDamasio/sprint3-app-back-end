from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import mapped_column
from datetime import datetime
from typing import Union

from model import Base

class Users(Base):
    __tablename__ = 'users'

    id = mapped_column("pk_user", Integer, primary_key=True)
    login = mapped_column(String(140), unique=True, nullable=False)
    password = mapped_column(String(140), nullable=False)
    add_date = mapped_column(DateTime, default=datetime.now())

    def __init__(self, login:str, password:str, add_date:Union[DateTime, None] = None):

        """Add new usuário"""

        self.login = login
        self.password = password

        if add_date:
            self.add_date = add_date


