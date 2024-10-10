# Web-scraping Project

## 1. Import Required Libraries
```import requests
from bs4 import BeautifulSoup
import csv
import re
```
Description: This step imports the necessary libraries for sending HTTP requests, parsing HTML content, working with CSV files, and using regular expressions.
## 2. Define HTTP Request Headers
```headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
```
Description: The headers are defined to mimic a browser request, helping avoid detection and blocking by the target website during scraping.
## 3. Check Product Details from a Product Page
```
def check_product_details(product_url):
    response = requests.get(product_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Try to find product name
        product_name = soup.find('h1', class_='page-title').text.strip() if soup.find('h1', class_='page-title') else "N/A"
        
        # Try to find price
        price_element = soup.find('span', class_='price')
        if price_element:
            price_text = price_element.text.strip()
            price_match = re.search(r'[\d,.]+', price_text)
            price = price_match.group(0) if price_match else "N/A"
            price = price.replace(',', '')
            price = f"${price}"
        else:
            price = "N/A"
        
        # Try to find manufacturer number
        manufacturer_number = soup.find('div', class_='value', itemprop='sku').text.strip() if soup.find('div', class_='value', itemprop='sku') else "N/A"
        
        return product_name, price, manufacturer_number
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return "N/A", "N/A", "N/A"

```
Description: This function retrieves product information (name, price, and manufacturer number) from a single product page using BeautifulSoup.

## 4. Extract Product Name, Price, and Manufacturer Number
```
soup.find('h1', class_='page-title')
soup.find('span', class_='price')
soup.find('div', class_='value', itemprop='sku')
```
Description: These lines attempt to extract specific details like the product name, price, and manufacturer number from the HTML structure. If unavailable, it returns "N/A".
## 5. Scrape Product Details from Each Page
```
def scrape_products(soup, category, type_name, writer):
```
Description: This function iterates through each product on a page, collects its details using the check_product_details function, and writes them to a CSV file.
## 6. Handle Pagination for Product Types
```
def scrape_type_pages(type_url, category, type_name, writer):
```
Description: This function handles pagination by scraping multiple pages of products within a single type and continuing until no more pages are available.
## 7. Scrape Types within a Category
```
def scrape_types_from_category(category_url, category_name, writer):
```
Description: This function extracts all types (subcategories) within a category and scrapes each type by passing it to the scrape_type_pages function.
## 8. Scrape All Categories from the Main Page
```
def scrape_all_categories(baseurl):
```
Description: This is the main function that scrapes the entire website by first fetching all product categories, then extracting and storing product details for each category and type in a CSV file.
## 9. Open CSV and Write Data
```
with open('products.csv', 'w', newline='', encoding='utf-8') as file:
```
Description: Opens a CSV file and writes the header row followed by product data gathered during the scraping process.
## 10. Execute Scraping Process
```
baseurl = 'https://www.SUPPLIER WEBSITE'
scrape_all_categories(baseurl)
```
Description: Starts the scraping process by calling the scrape_all_categories function using the base URL of the website.
