import requests
import json
from datetime import datetime

# Mock-lista med ICA-butiker i Skåne (baserat på verkliga data; ~150 totalt, här ett urval för demo)
# I verklig kod: Hämta från https://www.ica.se/api/stores?region=skane
SKANE_STORES = {
    "lund": {
        "1": {"name": "ICA Tuna Lund", "id": "tuna-lund"},
        "2": {"name": "ICA Kvantum Lund", "id": "lund-kvantum"},
        "3": {"name": "ICA Supermarket Mårten", "id": "lund-marten"},
        "4": {"name": "ICA Nära Nova Lund", "id": "lund-nova"},
        "5": {"name": "ICA Nära Värpinge", "id": "lund-varpinge"}
    },
    "malmo": {
        "1": {"name": "ICA Maxi Malmö", "id": "malmo-maxi"},
        "2": {"name": "ICA Kvantum City Malmö", "id": "malmo-kvantum"},
        "3": {"name": "ICA Supermarket Triangeln", "id": "malmo-triangeln"},
        "4": {"name": "ICA Nära Möllevången", "id": "malmo-mollevangen"},
        "5": {"name": "ICA Nära Limhamn", "id": "malmo-limhamn"}
    },
    # Lägg till fler orter: helsingborg, trelleborg, ystad osv. Totalt ~150 i Skåne.
    # Full lista: Hämta från ICA:s API eller https://ica.jensnylander.com/butiker/karta
}

def get_all_skanne_stores():
    """Hämtar alla butiker i Skåne (mock; ersätt med API-anrop)"""
    all_stores = {}
    for city, stores in SKANE_STORES.items():
        for num, store in stores.items():
            all_stores[f"{city}-{num}"] = store
    return all_stores  # Ca 150 i full version

def get_ica_deals(store_id):
    # Live-API (avkommentera för riktigt data):
    # url = f"https://handla.ica.se/api/weekly-offers/{store_id}"
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    # try:
    #     response = requests.get(url, headers=headers)
    #     return response.json().get("offers", [])
    # except:
    #     pass
    
    # Mock-data (realistiska deals för Skåne-butiker)
    mock_deals = [
        {"name": "Mjölk 1L Arla", "price": 12.90, "comparePrice": 18.90, "unit": ""},
        {"name": "Kycklingfilé", "price": 29.90, "comparePrice": 0, "unit": "/kg"},
        {"name": "Ägg 10-pack", "price": 22.90, "comparePrice": 0, "unit": ""},
        {"name": "Bananer", "price": 14.90, "comparePrice": 0, "unit": "/kg"},
        {"name": "Rågbröd ICA", "price": 9.90, "comparePrice": 0, "unit": ""},
        {"name": "Yoghurt 500g", "price": 15.50, "comparePrice": 20.00, "unit": ""},
        {"name": "Tomater", "price": 19.90, "comparePrice": 25.00, "unit": "/kg"}
    ]
    return mock_deals

def print_top_deals(deals, store_name):
    """Skriver ut top 5 deals"""
    deals = sorted(deals, key=lambda x: (x.get("comparePrice", 0) - x.get("price", 0)), reverse=True)[:5]
    print(f"\nTop 5 deals för {store_name}:")
    for i, deal in enumerate(deals, 1):
        name = deal.get("name", "Okänd vara")
        price = deal.get("price", 0)
        old_price = deal.get("comparePrice", 0)
        unit = deal.get("unit", "")
        was = f" (var {old_price} kr{unit})" if old_price > price else ""
        print(f"{i}. {name} - {price} kr{unit}{was}")

def save_to_file(deals, store_name, filename):
    """Sparar deals till fil"""
    with open(filename, "w", encoding="utf-8") as f:
        week = datetime.now().isocalendar()[1]
        year = datetime.now().year
        f.write(f"ICA {store_name} – Erbjudanden vecka {week} {year}\n")
        f.write("="*50 + "\n")
        deals = sorted(deals, key=lambda x: (x.get("comparePrice", 0) - x.get("price", 0)), reverse=True)[:5]
        for i, deal in enumerate(deals, 1):
            name = deal.get("name")
            price = deal.get("price")
            old_price = deal.get("comparePrice")
            unit = deal.get("unit", "")
            was = f" (var {old_price} kr{unit})" if old_price > price else ""
            f.write(f"{i}. {name} - {price} kr{unit}{was}\n")
    print(f"Sparat till: {filename}")

def main():
    print("+--------------------------------------------------+")
    print("| ICA PRICE WATCHER v2.2 – Skåne & Hela Sverige!  |")
    print("+--------------------------------------------------+\n")

    print("Välj läge:")
    print("1. En specifik butik i en ort (t.ex. Lund)")
    print("2. Alla butiker i Skåne (ca 150 st – tar tid!)")
    print("3. Alla i Sverige (ca 1300 st – långsamt, använd med försiktighet)")
    
    choice = input("\nDitt val (1/2/3): ").strip()
    
    if choice == "1":
        city = input("Välj ort i Skåne (t.ex. lund, malmo): ").strip().lower()
        if city not in SKANE_STORES:
            print("Ort inte hittad i Skåne. Lägg till fler i koden!")
            return
        print(f"\nButiker i {city.capitalize()}:")
        for num, store in SKANE_STORES[city].items():
            print(f"{num}. {store['name']}")
        subchoice = input("\nVälj nummer: ").strip()
        if subchoice in SKANE_STORES[city]:
            selected = SKANE_STORES[city][subchoice]
            print(f"\nScraping {selected['name']}... ", end="")
            deals = get_ica_deals(selected["id"])
            print("done")
            print_top_deals(deals, selected['name'])
            filename = f"ica_deals_{selected['id']}.txt"
            save_to_file(deals, selected['name'], filename)
    
    elif choice == "2":
        all_stores = get_all_skanne_stores()
        print(f"\nHittade {len(all_stores)} butiker i Skåne. Scrapar alla... (detta tar ~1-2 min)")
        summary_deals = {}  # Sammanställ top deals per butik
        for key, store in all_stores.items():
            print(f"Scraping {store['name']}... ", end="")
            deals = get_ica_deals(store["id"])
            if deals:
                best_deal = max(deals, key=lambda x: (x.get("comparePrice", 0) - x.get("price", 0)))
                summary_deals[store['name']] = best_deal
            print("done")
        # Spara sammanställning
        filename = f"ica_skanne_summary_v{datetime.now().isocalendar()[1]}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Top deals från alla ICA-butiker i Skåne – Vecka {datetime.now().isocalendar()[1]} {datetime.now().year}\n")
            f.write("="*60 + "\n")
            for name, deal in summary_deals.items():
                price = deal.get("price", 0)
                unit = deal.get("unit", "")
                f.write(f"{name}: {deal.get('name')} - {price} kr{unit}\n")
        print(f"\nSammanställning sparad till: {filename}")
        print("Exempel på top deals från Skåne:")
        for i, (name, deal) in enumerate(list(summary_deals.items())[:10], 1):  # Visa 10 exempel
            price = deal.get("price", 0)
            unit = deal.get("unit", "")
            print(f"{i}. {name}: {deal.get('name')} - {price} kr{unit}")
    
    elif choice == "3":
        print("För hela Sverige: Använd ICA:s fulla butiks-API[](https://www.ica.se/api/stores). Lägg till i koden!")
        print("Det blir ~1300 butiker – kör på en server för att undvika timeout.")
        # TODO: Implementera full Sverige-lista här
    
    else:
        print("Ogiltigt val!")
    
    input("\n> Tryck Enter för att avsluta...")

if __name__ == "__main__":
    main()