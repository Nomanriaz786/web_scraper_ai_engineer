# E-Commerce Product Crawler

A production-ready web crawler for extracting structured product data from e-commerce websites. Built with Python and FastAPI, featuring anti-bot evasion for protected sites like Amazon.

## Features

- **Multi-Site Support** - ToysRUs (HTTP) and Amazon (Browser-based)
- **Anti-Bot Evasion** - SeleniumBase UC Mode bypasses CAPTCHAs and bot detection

- **Structured Output** - Consistent JSON schema across all sources
- **Batch Processing** - Crawl multiple URLs in a single request
- **REST API** - FastAPI with automatic OpenAPI documentation

## Project Structure

```
app/
├── main.py                    # FastAPI application entry point
├── config.py                  # Site-specific selectors and settings
├── models.py                  # Pydantic data models
├── utils.py                   # Helper functions
└── crawlers/
    ├── http_crawler.py        # ToysRUs crawler (requests + BeautifulSoup)
    └── selenium_crawler.py    # Amazon crawler (SeleniumBase UC Mode)
docs/
└── AI_CRAWLER_DESIGN.md       # System design for AI-enhanced crawler
postman/
└── postman_collection.json    # Postman collection for API testing
output/                        # Extracted product data (JSON files)
```

## Quick Start

### Prerequisites

- Python 3.10+

### Installation

```bash
# Clone and navigate to project
git clone https://github.com/Nomanriaz786/web_scraper_ai_engineer.git
cd web_scraper_ai_engineer

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Run the Server

```bash
python -m app.main
```

API available at: http://localhost:8000
API Docs available at: http://localhost:8000/docs

## API Endpoints

### ToysRUs Crawler (HTTP-based)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/crawl` | Crawl a single ToysRUs product |
| `POST` | `/batch_crawl` | Crawl multiple ToysRUs products |

### Amazon Crawler (Browser-based)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/crawl/amazon` | Crawl a single Amazon product |
| `POST` | `/batch_crawl/amazon` | Crawl multiple Amazon products |

### Example Request

```bash
curl -X POST http://localhost:8000/crawl/amazon \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.amazon.com/dp/B0F8LLT3JR"}'
```

### Example Response

```json
{
  "id": "B0F8LLT3JR",
  "sku": null,
  "upc": null,
  "mfr_number": null,
  "brand": "PHIMOTA",
  "title": "Recuerdos de fiesta para niños de 8-12 y 4-8 años...",
  "description": "Paquete de 150: 3 pulseras para reventar, 4 juguetes para la ansie....",
  "category": "Juguetes y Juegos",
  "sub_category": "Artículos para Fiesta",
  "recommended_age": "3 años y más",
  "language": null,
  "price": "3356.001",
  "currency": "PKR",
  "availability": "Disponible",
  "images": [
    "https://m.media-amazon.com/images/I/815sofq0avL.jpg",
    "https://m.media-amazon.com/images/I/61nyjZt4hzL.jpg",
    "https://m.media-amazon.com/images/I/51F0a3iMM2L.jpg"
  ],
  "url": "https://www.amazon.com/-/es/Recuerdos-paquete-juguetes-rellenos-calcetines/dp/B0F8LLT3JR"
}
```

## Extracted Data Fields

| Field | Description |
|-------|-------------|
| `id` | Product identifier (ASIN for Amazon) |
| `sku` | Stock keeping unit |
| `upc` | Universal Product Code |
| `mfr_number` | Manufacturer part number |
| `brand` | Brand name |
| `title` | Product title |
| `description` | Product description |
| `category` | Main category |
| `sub_category` | Sub-category |
| `recommended_age` | Age recommendation |
| `price` | Numeric price value |
| `currency` | Currency code (USD, PKR, etc.) |
| `availability` | Stock status |
| `images` | Product image URLs (high resolution) |
| `url` | Source URL |

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Technical Approach

### ToysRUs Crawler
- Uses `requests` + `BeautifulSoup` for fast HTML parsing
- CSS selectors targeting ToysRUs-specific DOM structure

### Amazon Crawler
- **SeleniumBase UC Mode** for undetected browser automation
- **Hidden input extraction** for reliable price/currency data
- **Multi-language keyword matching** for brand and age fields
- **Interstitial handling** for "Continue shopping" popups

## Documentation

See [AI Crawler Design](docs/AI_CRAWLER_DESIGN.md) for the complete system design of an AI-enhanced crawler agent.

## Testing

Import `postman/postman_collection.json` into Postman to test all API endpoints.

## License

MIT
