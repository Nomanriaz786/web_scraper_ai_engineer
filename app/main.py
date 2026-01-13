from typing import List, Union

from fastapi import FastAPI, HTTPException
from app.config import settings

from app.models import (
    CrawlRequest, 
    BatchCrawlRequest, 
    ProductData, 
    ErrorResponse
)
from app.crawlers.http_crawler import crawl_product_logic
from app.crawlers.selenium_crawler import crawl_amazon_product, batch_crawl_amazon


app = FastAPI(
    title=settings.APP_NAME,
    description="API to crawl and extract structured product data from e-commerce pages",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    return {"status": "ok", "message": f"{settings.APP_NAME} is running"}


@app.post(
    "/crawl",
    response_model=ProductData,
    responses={
        200: {"description": "Successfully extracted product data"},
        400: {"model": ErrorResponse, "description": "Invalid URL provided"},
        500: {"model": ErrorResponse, "description": "Server error during crawling"},
    },
    tags=["Crawler"],
)
async def crawl_endpoint(request: CrawlRequest) -> ProductData:
    product_data = crawl_product_logic(request.url)
    return ProductData(**product_data)


@app.post(
    "/batch_crawl",
    response_model=List[Union[ProductData, ErrorResponse]],
    tags=["Crawler"],
)
async def batch_crawl_endpoint(request: BatchCrawlRequest) -> List[Union[ProductData, ErrorResponse]]:
    results = []
    
    for url in request.urls:
        try:
            product_data = crawl_product_logic(url)
            results.append(ProductData(**product_data))
        except Exception as e:
            results.append(ErrorResponse(error="Crawl Failed", detail=str(e)))
            
    return results

@app.post(
    "/crawl/amazon",
    response_model=ProductData,
    tags=["Amazon"],
    description="Crawl an Amazon product using SeleniumBase (UC Mode)"
)
async def crawl_amazon_endpoint(request: CrawlRequest) -> ProductData:
    try:
        product_data = crawl_amazon_product(request.url)
        return ProductData(**product_data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Amazon crawl failed: {str(e)}"
        )


@app.post(
    "/batch_crawl/amazon",
    response_model=List[Union[ProductData, ErrorResponse]],
    tags=["Amazon"],
    description="Batch crawl Amazon products reusing browser session"
)
async def batch_crawl_amazon_endpoint(request: BatchCrawlRequest) -> List[Union[ProductData, ErrorResponse]]:
    raw_results = batch_crawl_amazon(request.urls)
    
    results = []
    for item in raw_results:
        if "error" in item:
             results.append(ErrorResponse(error="Crawl Failed", detail=item["error"]))
        else:
             results.append(ProductData(**item))
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
