import requests
import json
from config import settings
from requests_html import HTMLSession


def fetch_productReviews(asin):
    """
    This function is used to fetch the customer reveiws of a product
    """
    payload = {
        "api_key": settings.scraper_api_token,
        "asin": asin,
        "country": "ca",
        "tld": "ca",
    }
    r = requests.get(
        "https://api.scraperapi.com/structured/amazon/review", params=payload
    )
    productReviews = r.text

    return productReviews


def fetch_productDetails(asin):
    """
    This function is used to fetch the product details from amazon
    """
    payload = {
        "api_key": settings.scraper_api_token,
        "asin": asin,
        "country": "ca",
        "tld": "ca",
        "output_fomat": "json",
    }
    r = requests.get(
        "https://api.scraperapi.com/structured/amazon/product", params=payload
    )
    productDetails = json.loads(r.text)

    return productDetails


def fetch_asin(search_query):
    """
    This function is used to fetch product codes listed on an amazon page
    """
    session = HTMLSession()
    r = session.get(
        f"http://api.scraperapi.com?api_key={settings.scraper_api_token}=https://www.amazon.ca/s?k={search_query}"
    )

    products = r.html.find("div[data-asin]")

    asins = []

    for product in products:
        if product.attrs["data-asin"] != "":
            asins.append(product.attrs["data-asin"])

    return asins


if __name__ == "__main__":
    """
    Use this script to fetch the product details based on a search query
    """
    asins = fetch_asin("<searchq_uery>")
    counter = 0
    all_product_dict = dict()
    for asin in asins:
        print(counter)
        productDetail = fetch_productDetails(asin)
        all_product_dict[str(counter)] = productDetail
        counter += 1
    with open("productDetails.json", "w") as fp:
        json.dump(all_product_dict, fp)
