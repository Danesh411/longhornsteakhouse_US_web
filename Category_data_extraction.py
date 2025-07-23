import hashlib
from pymongo import MongoClient
from curl_cffi import requests

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["longhornsteakhouse_US_feasiblity"]
collection_ip = db["sitemaps_inputs_2"]

# Target API
url = "https://www.longhornsteakhouse.com/api/menu?locale=en_US&restaurantNum=5155"

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6',
    'customtimeout': '20000',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-api-id': '1871875427',
    'x-concept-code': 'LH',
    'x-request-id': 'REQ_1753173025731',
    'x-source-channel': 'WEB'
}

# Make Request
response = requests.get(url, headers=headers, impersonate="chrome120")
data = response.json()

all_urls = []

# Extract Menu URLs
categories = data.get("categories", [])
for category in categories:
    category_name = category.get("displayName", "Unknown")

    subcategories = category.get("subCategories")
    if subcategories:
        for sub in subcategories:
            products = sub.get("products", [])
            for product in products:
                product_id = product.get("id")
                product_slug = product.get("slug")
                if product_id and product_slug:
                    final_url = f"https://www.longhornsteakhouse.com/menu/{product_slug}/{product_id}"
                    all_urls.append({
                        "category_name": category_name,
                        "url": final_url
                    })
    else:
        products = category.get("products", [])
        for product in products:
            product_id = product.get("id")
            product_slug = product.get("slug")
            if product_id and product_slug:
                final_url = f"https://www.longhornsteakhouse.com/menu/{product_slug}/{product_id}"
                all_urls.append({
                    "category_name": category_name,
                    "url": final_url
                })

# Insert into MongoDB
for entry in all_urls:
    try:
        url = entry['url']
        unique_hash = hashlib.sha256(url.encode()).hexdigest()
        document = {
            "_id": unique_hash,
            "url": url,
            "category_name": entry["category_name"],
            "status": "Pending"
        }
        collection_ip.insert_one(document)
        print(f"Inserted: {url}")
    except Exception as e:
        print(f"Error inserting URL '{url}': {e}")
