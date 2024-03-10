from dataclasses import dataclass
import memcache
import psycopg2

# @dataclass
# class CachedDatabase:
#     ip: str = '127.0.0.1'
#     port: str = '11211'
    
#     _mc = memcache.Client(servers=[f'{ip}:{port}'], debug=0)

#     def set_values(self, key_value, values) -> None:
#         self._mc.set(key_value, values)
    
#     def get_values(self, key_value) -> list:
#         return self._mc.get(key_value)
    
#     def delete_values(self, key_value) -> None:
#         self._mc.delete(key_value)

@dataclass
class Database:
    dbname: str = 'datas'
    user: str = 'postgres'
    password: str = '1234'
    host: str = 'localhost'
    port: int = '5432'

    _connection = psycopg2.connect(
        dbname= dbname,
        user=user,
        password=password,
        host=host
        )
    
    _cur = _connection.cursor()
    
    def add_new_product(self, product_name: str = None, product_url: str = None, product_photo_url: str = None, product_price: int = 0, product_id: int = 0) -> None:
        self._connection.commit()
        self._cur.execute('''
        INSERT INTO mephi8.products(
        product_name, product_url, product_photo_url, product_price, product_id)
        VALUES ('{product_name}', '{product_url}', '{product_photo_url}', {product_price}, {product_id});
    '''.format(product_name=product_name, product_url=product_url, product_photo_url=product_photo_url, product_price=product_price, product_id=product_id)
        )
        self._connection.commit()
    
    def delete_products(self) -> None:
        self._cur.execute(
            'DELETE FROM mephi8.products'
        )

    def get_product(self, product_id: int = None) -> tuple:
        self._cur.execute('''
        SELECT product_id, product_name, product_url, product_photo_url, product_price
	    FROM mephi8.products
        WHERE product_id={product_id};
        '''.format(product_id=product_id))
        
        result = self._cur.fetchone()
        return result