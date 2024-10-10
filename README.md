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
Description: This function sends a request to the product URL, parses the HTML content to extract the product name, price, and manufacturer number, and returns them. If the product or price is unavailable, it returns "N/A" for those fields.
## 4. Scrape Product Details from Each Page
```
def scrape_products(soup, category, type_name, writer):
    products = soup.find_all('div', class_='product-item-info')  # Adjust based on actual HTML structure
    for product in products:
        product_link = product.find('a', class_='product-item-link')['href']  # Get the product URL
        product_name, price, manufacturer_number = check_product_details(product_link)  # Get details from the product page

        # Write product details to the CSV
        writer.writerow([product_name, category, type_name, price, manufacturer_number])

```
Description: This function iterates through the list of products on a given page, retrieves each product's details using the check_product_details function, and writes them to a CSV file.

## 5. Handle Pagination for Product Types
```
def scrape_type_pages(type_url, category, type_name, writer):
    next_page_url = type_url
    while next_page_url:
        print(f"Scraping type page: {next_page_url}")
        
        response = requests.get(next_page_url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Scrape products from the current page
        scrape_products(soup, category, type_name, writer)
        
        # Find the link to the next page
        next_page_link = soup.find('li', class_='item pages-item-next')
        if next_page_link and next_page_link.find('a', class_='action next'):
            next_page_url = next_page_link.find('a', class_='action next')['href']
        else:
            next_page_url = None

```
Description: This function handles pagination by iterating through multiple pages of products within a product type. It calls scrape_products to gather data from each page and navigates to the next page, if available.

## 6. Scrape Product Types within a Category
```def scrape_types_from_category(category_url, category_name, writer):
    response = requests.get(category_url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    # Find all types (links inside the category page)
    type_links = soup.find_all('a', class_='category-list__link')  # Adjust the class if necessary

    # Loop through each type and extract the name and URL
    for type_link in type_links:
        type_name = type_link.find('span').text.strip()
        type_url = type_link['href']
        
        # Skip "View All" links
        if "View All" in type_name:
            print(f"Skipping type: {type_name}")
            continue
        
        print(f"Scraping type: {type_name} in category: {category_name}")
        scrape_type_pages(type_url, category_name, type_name, writer)

```
Description: This function scrapes all product types (or subcategories) within a given category by iterating through the type links, passing each type to scrape_type_pages, and handling "View All" links appropriately.

## 7. Scrape All Categories from the Main Page
```
def scrape_all_categories(baseurl):
    response = requests.get(baseurl, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    
    # Open CSV file to save the data
    with open('products.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Product Name', 'Category', 'Type', 'Price', 'Manufacturer Number'])
        
        # Find all category-grid__list divs
        category_divs = soup.find_all('div', class_='category-grid__list')

        # Loop through each category div and extract the category name and URL
        for div in category_divs:
            category_name = div.find('span').text.strip()
            category_url = div.find('a')['href']  # Find the link associated with the category
            
            print(f"Scraping category: {category_name}")
            # Scrape all types and products within this category
            scrape_types_from_category(category_url, category_name, writer)
```
Description: This is the main function that handles scraping the entire website. It first opens a CSV file and writes the header, then iterates through all categories, scrapes their types and products, and writes the data to the CSV.

## 8. Start Scraping Process
```
baseurl = 'https://www.SUPPLIER WEBSITE'
scrape_all_categories(baseurl)
```
Description: The script execution begins here. The base URL is passed to scrape_all_categories, which initiates the process of scraping all categories and their respective products from the website.

