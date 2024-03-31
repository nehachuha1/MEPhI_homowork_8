from bs4 import BeautifulSoup
import requests
import os

def scrapping_html_to_json(html_page: BeautifulSoup) -> list:
    page_source = html_page

    result = list()

    products_raw = page_source.findAll(name='div', class_='js-product t-store__card t-store__stretch-col t-store__stretch-col_25 t-align_center t-item')
    number = 1

    for product_raw in products_raw:
        current_product = dict()

        current_product['product_name'] = product_raw.find(name='div', class_='js-store-prod-name js-product-name t-store__card__title t-typography__title t-name t-name_xs').text.replace('/', '').replace('"', '')
        current_product['product_url'] = f'{product_raw.find(name='a').get('href')}'
        current_product['price'] = product_raw.find(name='div', class_='js-product-price js-store-prod-price-val t-store__card__price-value').text.replace(' ','')
        
        # for photo
        product_photo_url = product_raw.get('data-product-img') if product_raw.get('data-product-img') else 'https://static.tildacdn.com/stor6565-3039-4630-b830-666161666139/95222068.jpg'
        photo_page = requests.get(product_photo_url)
        photo_path = os.path.join(os.getcwd(), os.path.normpath(f'FILES/img/{current_product['product_name']}{number}.jpg'))
        with open(rf'{photo_path}', 'wb') as img:
            img.write(photo_page.content)
        current_product['product_photo_system_url'] = photo_path
        number += 1
        result.append(current_product)
    
    return result

