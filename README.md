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
```
Description: This function retrieves product information (name, price, and manufacturer number) from a single product page using BeautifulSoup.
