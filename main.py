import requests
import json

SHOPIFY_API_VERSION = "2023-07"
SHOP_NAME = "patabitshop"
ACCESS_TOKEN = "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"

SHOPIFY_LOCATION_ENDPOINT = f"https://{SHOP_NAME}.myshopify.com/admin/api/{SHOPIFY_API_VERSION}/locations.json"
HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN,
}

def get_location_id():
    res = requests.get(SHOPIFY_LOCATION_ENDPOINT, headers=HEADERS, verify=False)
    print("📡 Status code:", res.status_code)

    try:
        data = res.json()
    except json.JSONDecodeError:
        raise Exception("❌ Risposta non è JSON valida: " + res.text)

    print("📦 Risposta JSON:", json.dumps(data, indent=2))

    if "locations" not in data or not data["locations"]:
        raise Exception("❌ Nessuna location trovata o chiave 'locations' assente")

    return data["locations"][0]["id"]

def main():
    print("🚀 Avvio sync stock...")
    try:
        location_id = get_location_id()
        print(f"✅ Location ID ottenuto: {location_id}")
        # Aggiungi qui il resto della logica di sincronizzazione
    except Exception as e:
        print("💥 Errore:", e)

if __name__ == "__main__":
    main()
