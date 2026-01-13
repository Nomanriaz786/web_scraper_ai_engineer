import os
import json
from typing import Any
import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException, status
from app.config import settings
from app.utils import save_product_data

def fetch_html(url: str) -> str:
    """
    Fetches the HTML content of a given URL.
    
    Args:
        url: The URL to fetch
        
    Returns:
        The HTML content as a string
        
    Raises:
        requests.RequestException: If the request fails
    """
    headers = {
        "User-Agent": settings.TOYSRUS.USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    
    response = requests.get(url, headers=headers, timeout=settings.TOYSRUS.TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.text


def extract_product_data(html: str, url: str) -> dict[str, Any]:
    """
    Parses HTML and extracts structured product data using precise CSS selectors.
    
    Args:
        html: The HTML content to parse
        url: The source URL (for reference)
        
    Returns:
        Dictionary containing extracted product data
    """
    soup = BeautifulSoup(html, 'lxml')
    
    product_data = {
        "id": None,
        "sku": None,
        "upc": None,
        "mfr_number": None,
        "brand": None,
        "title": None,
        "description": None,
        "category": None,
        "sub_category": None,
        "recommended_age": None,
        "language": None,
        "price": None,
        "currency": None,
        "availability": None,
        "images": [],
        "url": url,
    }
    
    title_elem = soup.select_one(settings.TOYSRUS.TITLE_SELECTOR)
    if title_elem:
        product_data["title"] = title_elem.get_text(strip=True)
    
    brand_elem = soup.select_one(settings.TOYSRUS.BRAND_SELECTOR)
    if brand_elem:
        product_data["brand"] = brand_elem.get_text(strip=True)
    
    sku_elem = soup.select_one(settings.TOYSRUS.SKU_SELECTOR)
    if sku_elem:
        product_data["sku"] = sku_elem.get_text(strip=True)
        
    additional_info_items = soup.select(settings.TOYSRUS.ADDITIONAL_INFO_SELECTOR)
    for item in additional_info_items:
        text = item.get_text(strip=True)
        strong_elem = item.select_one('strong')
        value = strong_elem.get_text(strip=True) if strong_elem else None
        
        if text.startswith('ID:') and value:
            product_data["id"] = value
        elif text.startswith('UPC:') and value:
            product_data["upc"] = value
        elif text.startswith('MFR Number:') and value:
            product_data["mfr_number"] = value
        elif text.startswith('Toysrus Recommended Age:') and value:
            product_data["recommended_age"] = value
        elif text.startswith('Language:') and value:
            product_data["language"] = value
        elif text.startswith('Ship to Quebec:') and value:
            if value.lower() == 'yes':
                product_data["availability"] = "In Stock"
        elif text.startswith('In Store Only:') and value:
            if value.lower() == 'yes' and not product_data["availability"]:
                product_data["availability"] = "In Stock"
    
    desc_elem = soup.select_one(settings.TOYSRUS.DESCRIPTION_SELECTOR)
    if desc_elem:
        product_data["description"] = desc_elem.get_text(strip=True)
        
    breadcrumb_items = soup.select(settings.TOYSRUS.BREADCRUMB_SELECTOR)
    categories = []
    for item in breadcrumb_items:
        text = item.get_text(strip=True)
        if text.lower() not in ['home', 'category']:
            categories.append(text)
    
    if categories and product_data["title"]:
        if categories[-1] == product_data["title"]:
            categories = categories[:-1]
    
    if len(categories) >= 1:
        product_data["category"] = categories[0]
    if len(categories) >= 2:
        product_data["sub_category"] = categories[1]

    price_elem = soup.select_one(settings.TOYSRUS.PRICE_SELECTOR)
    if price_elem:
        product_data["price"] = price_elem.get('content')
        price_text = price_elem.get_text(strip=True)
        if price_text.startswith('$'):
            product_data["currency"] = "$"
        elif price_text.startswith('€'):
            product_data["currency"] = "€"
        elif price_text.startswith('£'):
            product_data["currency"] = "£"
    
    og_image = soup.select_one(settings.TOYSRUS.OG_IMAGE_SELECTOR)
    if og_image and og_image.get('content'):
        product_data["images"].append(og_image['content'])
    
    for img in soup.select(settings.TOYSRUS.GALLERY_SELECTOR):
        src = img.get('src') or img.get('data-src')
        if src and src not in product_data["images"]:
            product_data["images"].append(src)
    
    return product_data

def crawl_product_logic(url: str) -> dict[str, Any]:
    """
    Orchestrates the crawling process: fetching, extracting, and saving data.
    
    Args:
        url: The product page URL to crawl
        
    Returns:
        Extracted product data dictionary
        
    Raises:
        HTTPException: Maps request errors to FastAPI HTTP exceptions
    """
    try:
        html = fetch_html(url)
        product_data = extract_product_data(html, url)
        save_product_data(product_data)
        return product_data
        
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Request timed out while fetching the URL"
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not connect to the provided URL"
        )
    except requests.exceptions.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"HTTP error from target site: {e.response.status_code}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
