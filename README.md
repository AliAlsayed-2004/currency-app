# 💱 Currency Converter

A sleek and interactive Python command-line application for real-time currency exchange using **ExchangeRate-API**. This app includes features like live exchange rate display, currency conversion, favorite currency management, and conversion history—all with a user-friendly and beautifully formatted interface! 🚀

---

## ✨ Features

* 🌐 **Real-Time Rates**: Fetch live exchange rates for your selected currencies.
* 💸 **Currency Conversion**: Instantly convert amounts between any two currencies.
* ⚙️ **Custom Settings**: Add, remove, or change the base currency easily.
* 📜 **Conversion History**: Save and view your past conversions in a tidy table.
* 🎨 **Rich CLI Interface**: Beautifully formatted tables and messages using the `rich` library.
* 💾 **Persistent Storage**: Settings and currency lists are stored in JSON files.
* 🌍 **Wide Currency Support**: Choose from a comprehensive list of currencies.

---

## 🛠️ Requirements

To get started, make sure you have:

* 🐍 Python 3.7 or higher
* 🔑 An API key from [ExchangeRate-API](https://www.exchangerate-api.com/)
* 📦 Required packages: `requests`, `rich`

---

## 🚀 Setup

1. **Clone the Repository (if using Git):**

   ```bash
   git clone <repository-url>
   cd currency-converter
   ```

2. **Install Dependencies:**

   ```bash
   pip install requests rich
   ```

3. **Add Your API Key:**

   * Sign up at ExchangeRate-API to get a free API key.
   * Create a file named `api.txt` in the project root and paste your key inside.

4. **Configure Settings Files:**

   * Create a folder named `config/`.

   * Add the following file: `config/settings.json` (auto-generated if missing):

     ```json
     {
       "base_currency": "USD",
       "target_currencies": ["USD", "JOD", "ILS", "USDT"]
     }
     ```

   * Add `config/currencies.json` with supported currencies:

     ```json
     {
       "currencies": {
         "United States Dollar": "USD",
         "Euro": "EUR",
         "Jordanian Dinar": "JOD",
         "Israeli New Shekel": "ILS",
         "Tether": "USDT"
       }
     }
     ```

5. **Prepare History Folder:**

   * Create a folder named `history/`. `conversion_history.csv` will be auto-created on the first conversion.

---

## 🎮 Usage

To run the app:

```bash
python currency_app.py
```

Explore the interactive menu with these options:

* 📊 **Show Exchange Rates**
* ➕ **Add Currency**
* ➖ **Remove Currency**
* 🔄 **Change Base Currency**
* 💱 **Convert Currency**
* 📜 **Show Conversion History**
* 🌍 **Show All Available Currencies**
* 🚪 **Quit**

### Example:

Choose option `5` to convert currency.

Enter `USD` (from), `EUR` (to), and `100` (amount).

The result will be displayed and logged in `history/conversion_history.csv`.

---

## 📂 Project Structure

```
currency-converter/
├── api.txt                   # Your API key
├── currency_app.py           # Main script
├── config/
│   ├── currencies.json       # Supported currencies
│   └── settings.json         # User settings (base/target currencies)
├── history/
│   └── conversion_history.csv # Conversion logs
└── README.md                 # This file
```

---

## 📦 Dependencies

* `requests`: For API requests.
* `rich`: For rich, styled console output.
* Standard Python libraries: `json`, `csv`, `datetime`

```bash
pip install requests rich
```

---

## 📝 Notes

* 🔒 **API Key Security**: Keep `api.txt` private and add it to `.gitignore`.
* 🛡️ **Error Handling**: Handles API errors, invalid inputs, and missing files gracefully.
* ✅ **Currency Validation**: Codes are verified against `currencies.json`.
* ⏳ **Rate Limits**: Check your ExchangeRate-API plan for rate limits.
* 🔧 **Extensibility**: Easily extend the app with support for more APIs or features like charts or historical data.

---

## 📜 License

This project is licensed under the Apache License 2.0 License. See the `LICENSE` file for details.

---

## 📬 Contact

Have a question or suggestion? Open an issue on the repository or reach out to the maintainer. Let’s make this app even better! 🌟
