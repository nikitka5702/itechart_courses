from sqlalchemy import Column, Integer, VARCHAR, Text, ForeignKey

from .base import Base


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255), null=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, null=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
