# ICA-price-watcher

Fetches weekly offers from ICA stores in Skåne and shows you the best deals, sorted by how much you save.

## Requirements

```bash
pip install requests beautifulsoup4
```

## Usage

```bash
python3 ica_price_watcher.py
```

You'll get a menu to pick a single store, all stores in a city, or everything in Skåne at once. Results can be saved to a text file.

## How it works

Hits the same internal API endpoint that ICA's own website uses to load offer data. If that returns nothing for a store, it falls back to scraping the offers page directly with BeautifulSoup.

Offers are sorted by savings (original price minus current price), so the best deals come first.

## Adding more stores

Store IDs are the numeric IDs from ICA's website URLs. To find one, go to `ica.se/butiker`, navigate to your store, and grab the ID from the URL. Then add it to `SKANE_STORES` in the script:

```python
"Ystad": {
    "ICA Supermarket Ystad": "03XXX",
}
```

## Notes

- Adds a 0.5s delay between requests when scanning multiple stores — don't remove this
- ICA may change their site structure, which could break scraping — the store IDs should stay stable though
- Only use this for personal use; don't hammer their servers

## License

MIT

## Author

[@Mattan-a11y](https://github.com/Mattan-a11y) · [LinkedIn](https://www.linkedin.com/in/matin-shahid-1b426a217/)
