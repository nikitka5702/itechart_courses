import psycopg2


class SQLManager:

    def __init__(self):
        self.conn = psycopg2.connect('dbname=test user=postgres')
    
    def create_tables(self):
        with self.conn.cursor() as curs:
            curs.execute(
                "create table shops(id int primary key, name varchar(255) not null, address varchar(255), staff_amount int not null);"
                "create table departments(id int primary key, sphere int not null, staff_amount int not null, shop_id int references shops(id));"
                "create table items(id int primary key, description text, price int not null, department_id int references departments(id));"
            )
    
    def insert_data(self):
        with self.conn.cursor() as curs:
            curs.execute(
                "insert into shops values (1, 'Auchan', null, 250), (2, 'IKEA', 'Street Žirnių g. 56, Vilnius, Lithuania.', 500);"
                "insert into departments values (1, 'Furniture', 250, 1), (2, 'Furniture', 300, 2), (3, 'Dishes', 200, 2);"
                "insert into items values (1, 'Table', 'Cheap wooden table', 300, 1), (2, 'Table', null, 750, 2), (3, 'Bed', 'Amazing wooden bed', 1200, 2), (4, 'Cup', null, 10, 3), (5, 'Plate', 'Glass plate', 20, 3);"
            )

    def select_data(self, n):
        d = {
            1: "select from items where description is not null;",
            2: "select distinct sphere from departments where staff_amount > 200;",
            3: r"select address from shops where name ilike 'i%';",
            4: "select name from items where exists(select sphere from departments d where department_id = d.id and sphere = 'Furniture');",
            5: "select name from shops where exists(select from items i left join departments d on i.department_id = d.id left join shops s on d.shop_id = s.id where i.description is not null);",
            6: "select i.name, i.description, i.price, i.department_id, d.sphere department_sphere, d.staff_amount department_staff_amount, d.shop_id department_shop_id, s.name shop_name, s.address shop_address, s.staff_amount shop_staff_amount from items i inner join departments d on i.department_id = d.id inner join shops s on d.shop_id = s.id;",
            7: "select from items order by name offset 3 limit 2;",
            8: "select i.name, d.sphere from items i inner join departments d on i.department_id = d.id;",
            9: "select i.name, d.sphere from items i left join departments d on i.department_id = d.id;",
            10: "select i.name, d.sphere from items i right join departments d on i.department_id = d.id;",
            11: "select i.name, d.sphere from items i full outer join departments d on i.department_id = d.id;",
            12: "select i.name, d.sphere from items i, departments d;",
            13: "select count(i.price) as item_count, sum(i.price), max(i.price), min(i.price), avg(i.price), s.name from items i inner join departments d on i.department_id = d.id inner join shops s on d.shop_id = s.id group by s.name having count(*) > 1;",
            14: "select s.name, ARRAY[i.name, i.description, i.price::text] from shops s left join departments d on s.id = d.shop_id left join items i on d.id = i.department_id;"
        }
        with self.conn.cursor() as curs:
            if n in range(1, 15):
                return curs.execute(d[n])
    
    def update_data(self):
        with self.conn.cursor() as curs:
            curs.execute(
                r"update items set price = price + 100 where name ilike 'b%' or name ilike '%e';"
            )

    def delete_data(self, n):
        d = {
            1: "delete from items where price >= 500 and description isnull;",
            2: "delete from items where exists(select i.id from items i left join departments d on i.department_id = d.id left join shops s on d.shop_id = s.id where s.address isnull);",
            3: "delete from items i where exists(select from departments d where d.id = i.id and (d.staff_amount < 255 or d.staff_amount > 275));",
            4: "delete from items; delete from departments; delete from shops;"
        }
        with self.conn.cursor() as curs:
            if n in range(1, 5):
                curs.execute(
                    d[n]
                )

    def drop_tables(self):
        with self.conn.cursor() as curs:
            curs.execute(
                "drop table items;"
                "drop table departments;"
                "drop table shops;"
            )
