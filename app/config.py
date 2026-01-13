from pydantic import BaseModel

class ToysRusSettings(BaseModel):
    # CSS Selectors
    TITLE_SELECTOR: str = 'h1.b-product_details-name[data-attribute="productName"]'
    BRAND_SELECTOR: str = 'span[data-attribute="brand"]'
    DESCRIPTION_SELECTOR: str = '.b-product_description'
    PRICE_SELECTOR: str = '.b-price-value.js-sales-price-value'
    SKU_SELECTOR: str = '.b-product_details-sku strong[data-attribute="SKN"]'
    ADDITIONAL_INFO_SELECTOR: str = '.additional-info-list li'
    BREADCRUMB_SELECTOR: str = '.b-breadcrumbs-item span[itemprop="name"]'
    OG_IMAGE_SELECTOR: str = 'meta[property="og:image"]'
    GALLERY_SELECTOR: str = '.b-product_gallery img, .b-product_carousel img'
    
    # Crawler settings
    TIMEOUT_SECONDS: int = 30
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

class AmazonSettings(BaseModel):
    TITLE_SELECTOR: str = "#productTitle"
    DESCRIPTION_SELECTOR: str = "#feature-bullets"
    IMAGE_SELECTOR: str = "#landingImage"
    ALT_IMAGES_SELECTOR: str = "#altImages ul li img"
    AVAILABILITY_SELECTOR: str = "#availability"
    BREADCRUMB_SELECTOR: str = "#wayfinding-breadcrumbs_feature_div ul li:not(.a-breadcrumb-divider) a"
    
    # Hidden Input Selectors (most reliable source)
    PRICE_VALUE_INPUT: str = "input#priceValue"
    PRICE_SYMBOL_INPUT: str = "input#priceSymbol"
    ASIN_INPUT: str = "input#asin"
    
    # Product Details Table (for brand, age, etc.)
    DETAILS_TABLE_SELECTOR: str = "#productDetails_detailBullets_sections1 tr"
    
    # Brand keywords to search in details table (multi-language)
    BRAND_KEYWORDS: list = ["Fabricante", "Manufacturer", "Brand", "Marca"]
    AGE_KEYWORDS: list = ["Edad recomendada por el fabricante", "Manufacturer recommended age", "Recommended Age"]
    
    # Configuration
    TIMEOUT_SECONDS: int = 60


class Settings(BaseModel):
    APP_NAME: str = "E-Commerce Product Crawler API"
    VERSION: str = "1.0.0"
    API_PORT: int = 8000
    API_HOST: str = "0.0.0.0"
    OUTPUT_DIR: str = "output"
    
    TOYSRUS: ToysRusSettings = ToysRusSettings()
    AMAZON: AmazonSettings = AmazonSettings()

settings = Settings()
