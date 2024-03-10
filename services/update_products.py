from services.parse import parsing_site
from database.database import Database
import os

IMG_PATH = 'FILES/img'

def reupdate_db() -> None:
    current_img_files_path = os.path.join(os.getcwd(), os.path.normpath('FILES/img'))

    for file in os.listdir(current_img_files_path):
        img_file_path = os.path.join(current_img_files_path, file)
        try:
            if os.path.isfile(img_file_path):
                os.remove(img_file_path)
        except Exception as ex:
            print(f'Exception {ex} trying remove img {img_file_path}')
    
    db = Database()
    db.delete_products()

    ids = [x for x in range(1, 251)]
    for page_num in range(1, 3):
        products = parsing_site(page_num)

        for product in products:
            db.add_new_product(
                product_name=product['product_name'],
                product_url=product['product_url'],
                product_photo_url=product['product_photo_system_url'],
                product_price=product['price'],
                product_id=ids.pop(0)
            )
        