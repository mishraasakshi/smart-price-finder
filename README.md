# 🛒 Smart Price Finder

> Compare prices across Amazon & Flipkart instantly — no paid APIs, no credit card required.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.3-black?style=flat-square&logo=flask)
![Netlify](https://img.shields.io/badge/Deployed-Netlify-00C7B7?style=flat-square&logo=netlify)
![Render](https://img.shields.io/badge/Backend-Render-46E3B7?style=flat-square&logo=render)

---

## 🌐 Live Demo

| | URL |
|---|---|
| **Frontend** | https://rainbow-griffin-95a590.netlify.app |
| **Backend API** | https://smart-price-finder-2w16.onrender.com |

---

## 📌 What It Does

- Search any product by name
- Fetches live prices from **Amazon India** and **Flipkart** simultaneously
- Displays product name, price, rating, image, and direct buy link
- Automatically highlights the **best deal** (lowest price)
- Clean, responsive dark-mode UI

---

## 🏗️ Architecture

```
User (Browser)
      ↓
Frontend — HTML + CSS + JS (Netlify)
      ↓
Backend API — Flask / Python (Render)
      ↓
Scraper Modules
  ├── Amazon Scraper (BeautifulSoup)
  └── Flipkart Scraper (BeautifulSoup)
      ↓
Comparison Engine (sort by price, tag best deal)
      ↓
JSON Response → UI Cards
```

---

## 📁 Project Structure

```
smart-price-finder/
├── backend/
│   ├── app.py                  # Flask API server
│   ├── requirements.txt        # Python dependencies
│   ├── Procfile                # Render start command
│   └── scrapers/
│       ├── __init__.py
│       ├── amazon_scraper.py   # Amazon India scraper
│       └── flipkart_scraper.py # Flipkart scraper
├── frontend/
│   ├── index.html              # Main UI
│   ├── style.css               # Dark mode styles
│   └── script.js               # Search logic + API calls
├── runtime.txt                 # Python version for Render
├── netlify.toml                # Netlify build config
├── .gitignore
└── README.md
```

---

## 🚀 Run Locally

### Prerequisites
- Python 3.11+
- pip

### 1. Clone the repo
```bash
git clone https://github.com/mishraasakshi/smart-price-finder.git
cd smart-price-finder
```

### 2. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Start the backend
```bash
python app.py
```
Backend runs at `http://127.0.0.1:5000`

### 4. Open the frontend
```bash
open ../frontend/index.html
```

---

## 🔌 API Reference

### `GET /health`
Check if the server is running.

**Response:**
```json
{ "status": "ok" }
```

---

### `GET /search?q={query}`
Search for a product across Amazon and Flipkart.

**Example:**
```
GET /search?q=samsung+galaxy
```

**Response:**
```json
{
  "query": "samsung galaxy",
  "total": 6,
  "results": [
    {
      "source": "Amazon",
      "title": "Samsung Galaxy M56 5G",
      "price": "₹23,499",
      "price_raw": 23499.0,
      "rating": "4.3",
      "reviews": "1,234",
      "link": "https://www.amazon.in/...",
      "image": "https://...",
      "best_deal": true
    }
  ],
  "errors": []
}
```

---

## 🛠️ Tech Stack

| Layer | Technology | Cost |
|---|---|---|
| Frontend | HTML, CSS, JavaScript | Free |
| Backend | Python, Flask | Free |
| Scraping | BeautifulSoup4, Requests | Free |
| Anti-block | fake-useragent | Free |
| Frontend Hosting | Netlify | Free |
| Backend Hosting | Render | Free |
| API Keys | None required | ₹0 |

---

## ⚠️ Known Limitations

- **Render free tier** sleeps after 15 mins of inactivity — first request may take ~30 seconds to wake up
- Amazon/Flipkart occasionally block scrapers — results may vary by network and time of day
- Flipkart results depend on their current HTML structure which changes periodically
- Not for commercial use — scraping is for personal/educational purposes only

---

## 🔮 Future Features

- [ ] Price history tracking
- [ ] Price drop email alerts
- [ ] Filter by rating / price range
- [ ] More platforms (Croma, Reliance Digital)
- [ ] Browser extension

---

## 👩‍💻 Author

**Sakshi Mishra**
- GitHub: [@mishraasakshi](https://github.com/mishraasakshi)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> Built with ❤️ for budget shoppers everywhere 🛍️
