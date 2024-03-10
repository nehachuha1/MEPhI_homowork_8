from bs4 import BeautifulSoup
import requests
import os

def scrapping_html_to_json(html_page: BeautifulSoup) -> list:
    page_source = html_page

    result = list()

    products_raw = page_source.findAll(name='article', class_='product-card product-card--hoverable j-card-item')

    for product_raw in products_raw:
        current_product = dict()

        current_product['product_name'] = product_raw.find(name='a', class_='product-card__link j-card-link j-open-full-product-card').get('aria-label').replace('"','').replace("'","")
        current_product['product_url'] = f'{product_raw.find(name='a', class_='product-card__link j-card-link j-open-full-product-card').get('href')}'
        current_product['price'] = ''.join(product_raw.find(name='ins', class_='price__lower-price wallet-price').text.strip()[:-1].split())
        
        # for photo
        product_photo_url = product_raw.find(name='img', class_='j-thumbnail').get('src')
        photo_page = requests.get(product_photo_url)
        photo_path = os.path.join(os.getcwd(), os.path.normpath(f'FILES/img/{current_product['product_name']}.webp'))
        with open(photo_path, 'wb') as img:
            img.write(photo_page.content)
        current_product['product_photo_system_url'] = photo_path
        result.append(current_product)
    
    return result

