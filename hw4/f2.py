from contextlib import contextmanager

import sqlalchemy
from sqlalchemy import (
    create_engine, select, update,
    and_, or_
)
from sqlalchemy.orm import sessionmaker

from .models import Base, Shop, Department, Item


@contextmanager
def session_scope(s):
    session = s()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class SQLManager:
    
    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://postgres@localhost/test')
        self.Session = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def insert_data(self):
        with session_scope(self.Session) as session:
            session.add_all([
                Shop(id=1, name='Auchan', staff_amount=250),
                Shop(id=2, name='IKEA', address='Street Žirnių g. 56, Vilnius, Lithuania.', staff_amount=500),
                Department(id=1, sphere='Furniture', staff_amount=250, shop_id=1),
                Department(id=2, sphere='Furniture', staff_amount=300, shop_id=2),
                Department(id=2, sphere='Dishes', staff_amount=200, shop_id=2),
                Item(id=1, name='Table', description='Cheap wooden table', price=300, department_id=1),
                Item(id=2, name='Table', price=750, department_id=2),
                Item(id=3, name='Bed', description='Amazing wooden bed', price=1200, department_id=2),
                Item(id=4, name='Cup', price=10, department_id=3),
                Item(id=5, name='Plate', description='Glass plate', price=20, department_id=3),
            ])
    
    def select_data(self, n):
        pass
    
    def update_data(self):
        update(Item).values(
            price=(Item.price + 100)
        ).where(
            or_(Item.name.ilike('b%'), Item.name.ilike('%e'))
        )
    
    def delete_data(self, n):
        d = {
            1: lambda: None,
            2: lambda: None,
            3: lambda: None,
            4: lambda: None
        }
        if n in range(1, 5):
            d[n]()
    
    def drop_tables(self):
        Item.__table__.drop()
        Department.__table__.drop()
        Shop.__table__.drop()
