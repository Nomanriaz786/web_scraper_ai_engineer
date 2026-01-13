import os
import json
from typing import Optional
from app.config import settings
import re

def save_product_data(data: dict, output_dir: str = "None") -> None:
    """
    Saves the extracted data to a JSON file in the output directory.
    
    Args:
        data: The extracted product data dictionary to save
        output_dir: Optional directory path. Defaults to TOYSRUS settings if not provided.
    """
    if output_dir == "None":
        output_dir = settings.OUTPUT_DIR
        
    os.makedirs(output_dir, exist_ok=True)
    
    filename = "output.json" 
    if data.get("id"):
        filename = f"{data['id']}.json"
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def clean_amazon_img(img_url: str) -> str:
    """
    Cleans the Amazon image URL by removing the variable part of the URL.
    """
    if not img_url:
        return img_url
    return re.sub(r'\._[A-Z0-9_]+_\.', '.', img_url)

def is_product_image(url: str) -> bool:
    """Check if URL is an actual product image, not an icon or badge."""
    return "/images/I/" in url