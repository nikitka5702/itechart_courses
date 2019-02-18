from sqlalchemy import Column, Integer, VARCHAR, Text, ForeignKey

from .base import Base


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    sphere = Column(VARCHAR(255), null=False)
    staff_amount = Column(Integer, null=False)
    shop_id = Column(Integer, ForeignKey('shops.id'))
