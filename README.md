# ICA Price Watcher 🛒

A smart Python tool for tracking and comparing grocery deals across ICA stores in Skåne (and potentially all of Sweden). Find the best prices without manually checking every store's website!

## 🎯 Features

- **Store-specific deals**: Check offers from individual ICA stores
- **Regional scanning**: Scan all ~150 stores in Skåne at once
- **Nationwide capability**: Framework to scan all ~1,300 ICA stores in Sweden
- **Top deals ranking**: Automatically finds and ranks the best offers
- **Export functionality**: Save deals to text files for easy sharing
- **Real-time data**: Fetches current weekly offers (when connected to live API)
- **Compare prices**: Shows original prices to highlight savings

## 📋 Requirements

- Python 3.6 or higher
- `requests` library

## 🚀 Installation

```bash
# Clone or download the repository
git clone https://github.com/yourusername/ica-price-watcher.git
cd ica-price-watcher

# Install required package
pip install requests

# Run the script
python ICA_PRICE_WATCHER.py
```

## 💻 Usage

### Quick Start

Simply run the script and follow the interactive prompts:

```bash
python ICA_PRICE_WATCHER.py
```

### Usage Modes

**Mode 1: Single Store**
```
1. Select mode 1
2. Choose a city (lund, malmo, etc.)
3. Pick a specific store from the list
4. Get top 5 deals + exported file
```

**Mode 2: All Stores in Skåne**
```
1. Select mode 2
2. Wait for ~1-2 minutes while scanning ~150 stores
3. Get summary of best deals from each store
4. Results exported to timestamped file
```

**Mode 3: Nationwide (Future)**
```
Currently shows instructions for implementation
Will scan all ~1,300 ICA stores in Sweden
```

## 📊 Example Output

```
+--------------------------------------------------+
| ICA PRICE WATCHER v2.2 – Skåne & Hela Sverige!  |
+--------------------------------------------------+

Välj läge:
1. En specifik butik i en ort (t.ex. Lund)
2. Alla butiker i Skåne (ca 150 st – tar tid!)
3. Alla i Sverige (ca 1300 st – långsamt, använd med försiktighet)

Ditt val (1/2/3): 1
Välj ort i Skåne (t.ex. lund, malmo): lund

Butiker i Lund:
1. ICA Tuna Lund
2. ICA Kvantum Lund
3. ICA Supermarket Mårten
4. ICA Nära Nova Lund
5. ICA Nära Värpinge

Välj nummer: 2

Scraping ICA Kvantum Lund... done

Top 5 deals för ICA Kvantum Lund:
1. Mjölk 1L Arla - 12.90 kr (var 18.90 kr)
2. Yoghurt 500g - 15.50 kr (var 20.00 kr)
3. Tomater - 19.90 kr/kg (var 25.00 kr/kg)
4. Kycklingfilé - 29.90 kr/kg
5. Ägg 10-pack - 22.90 kr

Sparat till: ica_deals_lund-kvantum.txt
```

## 📁 Output Files

### Single Store Mode
```
ica_deals_[store-id].txt

Example:
ICA ICA Kvantum Lund – Erbjudanden vecka 7 2024
==================================================
1. Mjölk 1L Arla - 12.90 kr (var 18.90 kr)
2. Yoghurt 500g - 15.50 kr (var 20.00 kr)
...
```

### Regional Scan Mode
```
ica_skanne_summary_v[week].txt

Example:
Top deals från alla ICA-butiker i Skåne – Vecka 7 2024
============================================================
ICA Tuna Lund: Mjölk 1L Arla - 12.90 kr
ICA Kvantum Lund: Yoghurt 500g - 15.50 kr
ICA Maxi Malmö: Kycklingfilé - 29.90 kr/kg
...
```

## 🔧 Configuration

### Adding More Cities

Edit the `SKANE_STORES` dictionary to add more locations:

```python
SKANE_STORES = {
    "helsingborg": {
        "1": {"name": "ICA Maxi Helsingborg", "id": "helsingborg-maxi"},
        "2": {"name": "ICA Kvantum Drottninggatan", "id": "helsingborg-drottning"},
        # Add more stores...
    },
    # Add more cities...
}
```

### Connecting to Live API

The script currently uses mock data for demonstration. To connect to ICA's actual API:

1. Uncomment the live API code in `get_ica_deals()`:
```python
def get_ica_deals(store_id):
    url = f"https://handla.ica.se/api/weekly-offers/{store_id}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers)
        return response.json().get("offers", [])
    except:
        return []
```

2. Get actual store IDs from: https://ica.jensnylander.com/butiker/karta

## 🎓 Use Cases

### Personal Shopping
- Find the best weekly deals before your grocery trip
- Compare prices across multiple nearby stores
- Track price changes over time

### Budget Management
- Plan meals around the best deals
- Optimize shopping routes based on offers
- Save receipts (output files) for expense tracking

### Price Analysis
- Identify seasonal price patterns
- Track which stores consistently have better deals
- Compare regional pricing differences

### Family & Friends
- Share deal files with roommates/family
- Create shopping lists based on offers
- Coordinate bulk buying for better savings

## 🚨 Important Notes

- **API Limitations**: Frequent requests may be rate-limited by ICA's servers
- **Mock Data**: Current version uses example data; connect to live API for real deals
- **Respect Terms**: Always check ICA's terms of service before scraping
- **Ethical Usage**: Don't overload servers; add delays between requests in bulk scans
- **Store IDs**: Actual store IDs must be obtained from ICA's official API

## 🛠️ Troubleshooting

### "requests module not found"
```bash
pip install requests
```

### No deals returned
- Check if store ID is correct
- Verify API endpoint is accessible
- Check if weekly offers are currently available

### Slow scanning
- Reduce number of stores
- Add delays between requests: `time.sleep(0.5)`
- Run during off-peak hours

## 🔮 Future Enhancements

- [ ] Live API integration with proper error handling
- [ ] Price history tracking and graphs
- [ ] Email notifications for specific product deals
- [ ] Web interface with real-time updates
- [ ] Mobile app integration
- [ ] Support for other Swedish grocery chains (Coop, Willys, etc.)
- [ ] Machine learning for price prediction
- [ ] Telegram/Discord bot integration

## 📊 Technical Details

### Architecture
- **Modular design**: Separate functions for API calls, data processing, output
- **Error handling**: Graceful failures with fallback to mock data
- **Scalable**: Easy to extend to nationwide coverage
- **Export-friendly**: Simple text format for easy sharing

### Performance
- Single store: ~1-2 seconds
- Regional scan (150 stores): ~1-2 minutes
- Nationwide (1300 stores): ~10-15 minutes (estimated)

## ⚖️ Legal & Ethical Considerations

- This tool is for **personal use and educational purposes**
- Always respect ICA's robots.txt and terms of service
- Don't use for commercial purposes without permission
- Add reasonable delays between requests (rate limiting)
- Don't distribute or sell scraped data

## 💡 Pro Tips

1. **Schedule Regular Scans**: Use cron jobs to check for new deals weekly
2. **Create Store Profiles**: Save your favorite stores for quick access
3. **Compare Timestamps**: Keep old files to track price changes
4. **Share with Friends**: Split bulk purchases based on deals
5. **Track Savings**: Calculate how much you save each month

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions welcome! Some ideas:
- Add more Swedish cities and stores
- Implement live API connections
- Create data visualization features
- Add support for other grocery chains
- Improve error handling and logging

## 👤 Author

Your Name
- GitHub: [@Mattan-a11y](https://github.com/Mattan-a11y)
- LinkedIn: [Matin Shahid](https://www.linkedin.com/in/matin-shahid-1b426a217/)

## 🙏 Acknowledgments

- ICA Sverige for making data accessible
- Swedish grocery shopping community
- Open-source Python community

## 📧 Support

If you find this tool useful, please:
- ⭐ Star the repository
- 🐛 Report bugs via Issues
- 💡 Suggest features
- 🔀 Submit pull requests

---

**Happy Deal Hunting! 🎉**
