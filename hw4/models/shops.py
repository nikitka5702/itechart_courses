from sqlalchemy import Column, Integer, VARCHAR, Text

from .base import Base


class Shop(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255), null=False)
    address = Column(VARCHAR(255), nullable=True)
    staff_amount = Column(Integer, null=False)
