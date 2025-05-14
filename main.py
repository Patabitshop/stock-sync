import requests, csv, io, os

SHOP_URL = os.environ.get("SHOP_URL")
SHOP_TOKEN = os.environ.get("SHOP_TOKEN")
CSV_URLS = os.environ.get("CSV_URLS")

HEADERS = {
    "X-Shopify-Access-Token": SHOP_TOKEN,
    "Content-Type": "application/json"
}

def get_location_id():
    res = requests.get(f"{SHOP_URL}/admin/api/2023-07/locations.json", headers=HEADERS)
    return res.json()["locations"][0]["id"]

def update_inventory(sku, quantity, location_id):
    item_res = requests.get(f"{SHOP_URL}/admin/api/2023-07/inventory_items.json?sku={sku}", headers=HEADERS)
    items = item_res.json().get("inventory_items", [])
    if not items:
        print(f"SKU {sku} non trovato")
        return
    inventory_item_id = items[0]["id"]
    data = {
        "location_id": location_id,
        "inventory_item_id": inventory_item_id,
        "available": quantity
    }
    requests.post(f"{SHOP_URL}/admin/api/2023-07/inventory_levels/set.json", headers=HEADERS, json=data)

def main():
    location_id = get_location_id()
    for url in CSV_URLS.split(","):
        response = requests.get(url.strip())
        reader = csv.DictReader(io.StringIO(response.text), delimiter=";")
        for row in reader:
            sku = row.get("Codice")
            qty = row.get("Disponibile")
            if sku and qty:
                try:
                    update_inventory(sku.strip(), int(float(qty)), location_id)
                except Exception as e:
                    print(f"Errore {sku}: {e}")

if __name__ == "__main__":
    main()
