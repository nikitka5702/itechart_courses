from contextlib import contextmanager
from operator import itemgetter

from sqlalchemy import (
    String,
    create_engine, and_, or_,
    literal, func
)
from sqlalchemy.dialects.postgresql import array
from sqlalchemy.orm import sessionmaker

from models import Base, Shop, Department, Item


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
        d = {
            1: lambda s: s.query(Item).filter(Item.description.isnot(None)),
            2: lambda s: [item.sphere for item in s.query(Department).distinct(Department.sphere).filter(Department.staff_amount > 200)],
            3: lambda s: s.query(Shop.address).filter(Shop.name.ilike('%i')),
            4: lambda s: s.query(Item.name).filter(s.query(Department).filter(and_(Item.department_id == Department.id, Department.sphere == 'Furniture')).exists()),
            5: lambda s: s.query(Shop.name).filter(s.query(Item).join(Department, Item.department_id == Department.id).join(Shop, Department.shop_id == Shop.id).filter(Item.description.isnot(None)).exists()),
            6: lambda s: [(itemgetter(0, 1, 2, 3)(item), itemgetter(4, 5, 6)(item), itemgetter(7, 8, 9)) for item in s.query(Item.name, Item.description, Item.price, Item.department_id, Department.sphere.label('department_sphere'), Department.staff_amount.label('department_staff_amount'), Department.shop_id.label('department_shop_id'), Shop.name.label('shop_name'), Shop.address.label('shop_address'), Shop.staff_amount.label('shop_staff_amount')).join(Department, Item.department_id == Department.id).join(Shop, Department.shop_id == Shop.id)],
            7: lambda s: s.query(Item).order_by(Item.name).offset(3).limit(2),
            8: lambda s: s.query(Item.name, Department.sphere).join(Department).all(),
            9: lambda s: s.query(Item.name, Department.sphere).outerjoin(Department).all(),
            10: lambda s: s.query(Department.sphere, Item.name).outerjoin(Item).all(),
            11: lambda s: s.query(Item.name, Department.sphere).outerjoin(Department, full=True).all(),
            12: lambda s: s.query(Item.name, Department.sphere).join(Department, literal(True)).all(),
            13: lambda s: s.query(func.count(Item.price).label('item_count'), func.sum(Item.price), func.max(Item.price), func.min(Item.price), func.avg(Item.price), Shop.name).join(Department, Item.department_id == Department.id).join(Shop, Department.shop_id == Shop.id).group_by(Shop.name).having(func.count() > 1),
            14: lambda s: s.query(Shop.name, array([Item.name, Item.description, Item.price.cast(String)])).join(Department, Department.shop_id == Shop.id).join(Item, Item.department_id == Department.id),
        }
        with session_scope(self.Session) as session:
            if n in range(1, 15):
                return d[n](session)
    
    def update_data(self):
        with session_scope(self.Session) as session:
            session.query(Item).filter(
                or_(Item.name.ilike('b%'), Item.name.ilike('%e'))
            ).update({'price': Item.price + 100})
    
    def delete_data(self, n):
        d = {
            1: lambda s: s.query(Item).filter(and_(Item.price >= 500, Item.description.is_(None))).delete(),
            2: lambda s: s.query(Item).filter(s.query(Item)).delete(),
            3: lambda s: s.query(Item).filter(s.query(Department).filter(and_(Department.id == Item.id, or_(Department.staff_amount < 255, Department.staff_amount > 275))).exists()).delete(),
            4: lambda s: s.query(Item, Department, Shop).delete()
        }
        if n in range(1, 5):
            d[n]()
    
    def drop_tables(self):
        Item.__table__.drop()
        Department.__table__.drop()
        Shop.__table__.drop()
