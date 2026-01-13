from typing import Any, List
from seleniumbase import Driver
from bs4 import BeautifulSoup
from app.config import settings
from app.utils import save_product_data, clean_amazon_img, is_product_image
import time


def crawl_amazon_product(url: str, sb=None) -> dict[str, Any]:
    """
    Crawls an Amazon product page using SeleniumBase (UC mode).
    If 'sb' (driver) is provided, reuses it. Otherwise creates a new one.
    """
    should_quit = False
    if sb is None:
        sb = Driver(uc=True, headless=True) 
        should_quit = True
        
    try:
        sb.get(url)
        time.sleep(0.5) 
        
        if sb.is_text_visible("Continue shopping"):
            try:
                if sb.is_element_visible('button[alt="Continue shopping"]'):
                    sb.click('button[alt="Continue shopping"]')
                    time.sleep(1) 
            except Exception:
                pass 

        html = sb.get_page_source()
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
        # ASIN from hidden input
        asin_input = soup.select_one(settings.AMAZON.ASIN_INPUT)
        if asin_input and asin_input.get("value"):
            product_data["id"] = asin_input.get("value")
        elif "/dp/" in url:
            parts = url.split("/dp/")
            if len(parts) > 1:
                product_data["id"] = parts[1].split("/")[0].split("?")[0]
        
        # Price and Currency from hidden inputs
        price_input = soup.select_one(settings.AMAZON.PRICE_VALUE_INPUT)
        currency_input = soup.select_one(settings.AMAZON.PRICE_SYMBOL_INPUT)
        
        if price_input and price_input.get("value"):
            product_data["price"] = price_input.get("value")
        
        if currency_input and currency_input.get("value"):
            product_data["currency"] = currency_input.get("value")
        
        # Title
        title_elem = soup.select_one(settings.AMAZON.TITLE_SELECTOR)
        if title_elem:
            product_data["title"] = title_elem.get_text(strip=True)
        
        # Description
        desc_elem = soup.select_one(settings.AMAZON.DESCRIPTION_SELECTOR)
        if desc_elem:
            product_data["description"] = desc_elem.get_text(strip=True)
            
        # Availability
        avail_elem = soup.select_one(settings.AMAZON.AVAILABILITY_SELECTOR)
        if avail_elem:
            product_data["availability"] = avail_elem.get_text(strip=True)
        
        # Breadcrumbs (Category)
        breadcrumbs = soup.select(settings.AMAZON.BREADCRUMB_SELECTOR)
        if breadcrumbs:
            names = [b.get_text(strip=True) for b in breadcrumbs]
            if len(names) >= 1:
                product_data["category"] = names[0]
            if len(names) >= 2:
                product_data["sub_category"] = names[1]
        
        # Brand and Age from Details Table
        details_rows = soup.select(settings.AMAZON.DETAILS_TABLE_SELECTOR)
        for row in details_rows:
            th = row.select_one("th")
            td = row.select_one("td")
            if th and td:
                label = th.get_text(strip=True)
                value = td.get_text(strip=True)
                
                # Check for Brand
                for keyword in settings.AMAZON.BRAND_KEYWORDS:
                    if keyword.lower() in label.lower():
                        product_data["brand"] = value
                        break
                
                # Check for Age
                for keyword in settings.AMAZON.AGE_KEYWORDS:
                    if keyword.lower() in label.lower():
                        product_data["recommended_age"] = value
                        break
        
        alt_imgs = soup.select(settings.AMAZON.ALT_IMAGES_SELECTOR)
        for img in alt_imgs:
            src = img.get("src")
            if src and isinstance(src, str) and is_product_image(src):
                hi_res = clean_amazon_img(src)
                if hi_res not in product_data["images"]:
                    product_data["images"].append(hi_res)
            
        img_elem = soup.select_one(settings.AMAZON.IMAGE_SELECTOR)
        if img_elem:
            main_src = img_elem.get("src")
            if main_src and isinstance(main_src, str) and is_product_image(main_src):
                main_hi_res = clean_amazon_img(main_src)
                if main_hi_res not in product_data["images"]:
                    product_data["images"].insert(0, main_hi_res)
             
        save_product_data(product_data)
        return product_data

    finally:
        if should_quit:
            sb.quit()


def batch_crawl_amazon(urls: List[str]) -> List[dict[str, Any]]:
    """
    Crawls multiple Amazon URLs reusing the same browser instance.
    """
    results = []
    sb = Driver(uc=True, headless=True)
    try:
        for url in urls:
            try:
                data = crawl_amazon_product(url, sb=sb)
                results.append(data)
            except Exception as e:
                results.append({"error": str(e), "url": url})
    finally:
        sb.quit()
        
    return results
