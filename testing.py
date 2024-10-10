import requests
from bs4 import BeautifulSoup
import csv
import re

# Define headers for requests
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Function to check price and manufacturer number from a single product page
def check_product_details(product_url):
    response = requests.get(product_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Try to find product name
        product_name = soup.find('h1', class_='page-title').text.strip() if soup.find('h1', class_='page-title') else "N/A"
        
        # Try to find price
        price_element = soup.find('span', class_='price')
        if price_element:
            # Extract text and clean it up
            price_text = price_element.text.strip()
            # Use regex to find all digits and decimal points
            price_match = re.search(r'[\d,.]+', price_text)
            price = price_match.group(0) if price_match else "N/A"  # Get the matched price
            price = price.replace(',', '')  # Remove commas if present
            price = f"${price}"  # Add dollar sign
        else:
            price = "N/A"

        # Try to find manufacturer number
        manufacturer_number = soup.find('div', class_='value', itemprop='sku').text.strip() if soup.find('div', class_='value', itemprop='sku') else "N/A"
        
        return product_name, price, manufacturer_number
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return "N/A", "N/A", "N/A"

# Function to scrape product details from a page
def scrape_products(soup, category, type_name, writer):
    products = soup.find_all('div', class_='product-item-info')  # Adjust based on actual HTML structure
    for product in products:
        product_link = product.find('a', class_='product-item-link')['href']  # Get the product URL
        product_name, price, manufacturer_number = check_product_details(product_link)  # Get details from the product page

        # Write product details to the CSV
        writer.writerow([product_name, category, type_name, price, manufacturer_number])

# Loop through multiple pages for a single type
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

# Function to scrape types within a category
def scrape_types_from_category(category_url, category_name, writer):
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

# Function to scrape all categories from the main page
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

# Start scraping
baseurl = 'https://www.penn-elcom.com/nl/flight-case-hardware'
scrape_all_categories(baseurl)
