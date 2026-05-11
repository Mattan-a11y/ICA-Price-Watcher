import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
import sys

# Store IDs for ICA — these are the numeric IDs used in the ICA website URLs
# Find your store's ID by visiting ica.se/butiker and checking the URL
SKANE_STORES = {
    "Lund": {
        "ICA Maxi Lund": "01018",
        "ICA Kvantum Lund": "01452",
        "ICA Supermarket Mårten": "03451",
        "ICA Nära Nova Lund": "06202",
    },
    "Malmö": {
        "ICA Maxi Malmö": "01081",
        "ICA Kvantum City Malmö": "01208",
        "ICA Supermarket Triangeln": "03307",
        "ICA Nära Möllevången": "06389",
    },
    "Helsingborg": {
        "ICA Maxi Helsingborg": "01024",
        "ICA Supermarket Helsingborg C": "03199",
    },
    "Kristianstad": {
        "ICA Maxi Kristianstad": "01040",
        "ICA Kvantum Kristianstad": "01236",
    },
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/html",
    "Accept-Language": "sv-SE,sv;q=0.9",
}


def get_offers_for_store(store_id, store_name):
    """
    Fetch weekly offers for a specific ICA store.
    Uses ICA's internal API endpoint that the website itself calls.
    """
    url = f"https://www.ica.se/api/stores/{store_id}/weeklyoffers"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            data = response.json()
            offers = data.get("offers", [])
            return parse_offers(offers)
        elif response.status_code == 404:
            print(f"  Store ID {store_id} not found — check if the ID is correct")
            return []
        else:
            # Fallback: try scraping the offers page directly
            return scrape_offers_page(store_id, store_name)

    except requests.exceptions.Timeout:
        print(f"  Timeout fetching {store_name}")
        return []
    except requests.exceptions.ConnectionError:
        print(f"  Connection error for {store_name}")
        return []
    except (ValueError, KeyError):
        return scrape_offers_page(store_id, store_name)


def scrape_offers_page(store_id, store_name):
    """
    Fallback: scrape the ICA offers page for a store using BeautifulSoup.
    """
    url = f"https://www.ica.se/butiker/erbjudanden/?storeId={store_id}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        offers = []

        # ICA renders offer cards with these class names (may change if ICA updates their site)
        offer_cards = soup.find_all("div", class_=lambda c: c and "offer" in c.lower())

        for card in offer_cards:
            name_el = card.find(class_=lambda c: c and "name" in c.lower())
            price_el = card.find(class_=lambda c: c and "price" in c.lower())

            if name_el and price_el:
                offers.append({
                    "name": name_el.get_text(strip=True),
                    "price": price_el.get_text(strip=True),
                    "compare_price": None,
                })

        return offers

    except Exception as e:
        print(f"  Scraping failed for {store_name}: {e}")
        return []


def parse_offers(raw_offers):
    """Parse raw offer data from ICA's API into a clean list."""
    parsed = []
    for offer in raw_offers:
        try:
            parsed.append({
                "name": offer.get("productName") or offer.get("name", "Okänd vara"),
                "price": float(offer.get("price", 0)),
                "compare_price": float(offer.get("comparePrice", 0)) or None,
                "unit": offer.get("priceUnit", ""),
                "condition": offer.get("offerCondition", ""),
                "valid_until": offer.get("validUntil", ""),
            })
        except (TypeError, ValueError):
            continue
    return parsed


def calculate_savings(offer):
    """Return how much you save on an offer, for sorting."""
    price = offer.get("price", 0)
    compare = offer.get("compare_price") or 0
    if compare and compare > price:
        return compare - price
    return 0


def print_offers(offers, store_name, top_n=5):
    """Print the top N offers for a store, sorted by savings."""
    if not offers:
        print(f"  Inga erbjudanden hittades för {store_name}")
        return

    sorted_offers = sorted(offers, key=calculate_savings, reverse=True)[:top_n]

    print(f"\nTop {top_n} erbjudanden — {store_name}:")
    print("-" * 40)
    for i, offer in enumerate(sorted_offers, 1):
        name = offer.get("name", "?")
        price = offer.get("price", "?")
        compare = offer.get("compare_price")
        unit = offer.get("unit", "")
        condition = offer.get("condition", "")

        price_str = f"{price} kr{unit}"
        was_str = f" (ord. {compare} kr)" if compare and compare > price else ""
        cond_str = f" — {condition}" if condition else ""

        print(f"{i}. {name}: {price_str}{was_str}{cond_str}")


def save_to_file(all_results, filename=None):
    """Save results to a text file."""
    if not filename:
        week = datetime.now().isocalendar()[1]
        year = datetime.now().year
        filename = f"ica_erbjudanden_vecka{week}_{year}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        week = datetime.now().isocalendar()[1]
        f.write(f"ICA Erbjudanden — Vecka {week} {datetime.now().year}\n")
        f.write(f"Hämtad: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("=" * 50 + "\n\n")

        for store_name, offers in all_results.items():
            f.write(f"{store_name}\n")
            f.write("-" * len(store_name) + "\n")

            if not offers:
                f.write("Inga erbjudanden hittade.\n\n")
                continue

            sorted_offers = sorted(offers, key=calculate_savings, reverse=True)[:5]
            for i, offer in enumerate(sorted_offers, 1):
                name = offer.get("name", "?")
                price = offer.get("price", "?")
                compare = offer.get("compare_price")
                unit = offer.get("unit", "")
                was_str = f" (ord. {compare} kr)" if compare and compare > price else ""
                f.write(f"{i}. {name}: {price} kr{unit}{was_str}\n")
            f.write("\n")

    print(f"\nSparat till: {filename}")
    return filename


def select_store():
    """Interactive menu to select a store."""
    print("\nVälj stad:")
    cities = list(SKANE_STORES.keys())
    for i, city in enumerate(cities, 1):
        print(f"{i}. {city}")

    try:
        city_choice = int(input("\n> ")) - 1
        city = cities[city_choice]
    except (ValueError, IndexError):
        print("Ogiltigt val.")
        return None, None

    print(f"\nButiker i {city}:")
    stores = list(SKANE_STORES[city].items())
    for i, (name, _) in enumerate(stores, 1):
        print(f"{i}. {name}")

    try:
        store_choice = int(input("\n> ")) - 1
        store_name, store_id = stores[store_choice]
        return store_name, store_id
    except (ValueError, IndexError):
        print("Ogiltigt val.")
        return None, None


def main():
    print("+------------------------------------------+")
    print("|  ICA Price Watcher — Skåne               |")
    print("+------------------------------------------+\n")

    print("Välj läge:")
    print("1. En specifik butik")
    print("2. Alla butiker i en stad")
    print("3. Alla butiker i Skåne (tar ett tag)")

    choice = input("\n> ").strip()

    all_results = {}

    if choice == "1":
        store_name, store_id = select_store()
        if not store_name:
            return

        print(f"\nHämtar erbjudanden för {store_name}...")
        offers = get_offers_for_store(store_id, store_name)
        all_results[store_name] = offers
        print_offers(offers, store_name)

    elif choice == "2":
        print("\nVälj stad:")
        cities = list(SKANE_STORES.keys())
        for i, city in enumerate(cities, 1):
            print(f"{i}. {city}")

        try:
            city_choice = int(input("\n> ")) - 1
            city = cities[city_choice]
        except (ValueError, IndexError):
            print("Ogiltigt val.")
            return

        print(f"\nHämtar erbjudanden för alla butiker i {city}...")
        for store_name, store_id in SKANE_STORES[city].items():
            print(f"  {store_name}... ", end="", flush=True)
            offers = get_offers_for_store(store_id, store_name)
            all_results[store_name] = offers
            print(f"{len(offers)} erbjudanden")
            time.sleep(0.5)  # be nice to their servers

        for name, offers in all_results.items():
            print_offers(offers, name)

    elif choice == "3":
        print("\nHämtar erbjudanden för alla butiker i Skåne...")
        for city, stores in SKANE_STORES.items():
            print(f"\n{city}:")
            for store_name, store_id in stores.items():
                print(f"  {store_name}... ", end="", flush=True)
                offers = get_offers_for_store(store_id, store_name)
                all_results[store_name] = offers
                print(f"{len(offers)} erbjudanden")
                time.sleep(0.5)

        # Print top deal per store
        print("\n--- Bästa erbjudande per butik ---")
        for store_name, offers in all_results.items():
            if offers:
                best = max(offers, key=calculate_savings)
                savings = calculate_savings(best)
                savings_str = f" (spara {savings:.0f} kr)" if savings > 0 else ""
                print(f"{store_name}: {best['name']} — {best['price']} kr{savings_str}")
    else:
        print("Ogiltigt val.")
        return

    if all_results:
        save = input("\nSpara till fil? (j/n): ").strip().lower()
        if save == "j":
            save_to_file(all_results)

    input("\n> Tryck Enter för att avsluta...")


if __name__ == "__main__":
    main()
