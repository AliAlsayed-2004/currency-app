import requests
import json
import csv
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt

SETTINGS_FILE = 'config/settings.json'
HISTORY_FILE = 'history/conversion_history.csv'
CURRENCIES_FILE = 'config/currencies.json'

console = Console()

class SettingsManager:
    def __init__(self):
        self.settings = {
            "base_currency": "USD",
            "target_currencies": ["USD", "JOD", "ILS", "USDT"]
        }
        self.load()

    def load(self):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.save()

    def save(self):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get_base_currency(self):
        return self.settings.get("base_currency", "USD")

    def set_base_currency(self, currency):
        self.settings["base_currency"] = currency.upper()
        self.save()

    def get_target_currencies(self):
        return self.settings.get("target_currencies", [])

    def add_currency(self, currency):
        currency = currency.upper()
        if currency not in self.settings["target_currencies"]:
            self.settings["target_currencies"].append(currency)
            self.save()
            return True
        return False

    def remove_currency(self, currency):
        currency = currency.upper()
        if currency in self.settings["target_currencies"]:
            self.settings["target_currencies"].remove(currency)
            self.save()
            return True
        return False

class CurrencyRateFetcher:
    def __init__(self, api_key, base_currency):
        self.api_key = api_key
        self.base_currency = base_currency
        self.last_update_time = None

    def update_base_currency(self, new_base):
        self.base_currency = new_base

    def fetch(self, target_currencies):
        url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{self.base_currency}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to fetch data from API.")
        data = response.json()
        if data.get('result') != 'success':
            raise Exception("Invalid data received from API.")

        self.last_update_time = datetime.now()

        rates = data['conversion_rates']
        results = []
        for currency in target_currencies:
            if currency in rates:
                results.append([self.base_currency, currency, rates[currency]])
        return results

    def convert(self, from_currency, to_currency, amount):
        url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/pair/{from_currency}/{to_currency}/{amount}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to fetch conversion data.")
        data = response.json()
        if data.get('result') != 'success':
            raise Exception("Invalid conversion data received from API.")
        return {
            'from': from_currency,
            'to': to_currency,
            'rate': data['conversion_rate'],
            'amount': amount,
            'result': data['conversion_result']
        }

class CurrencyApp:
    def __init__(self, api_key):
        self.settings = SettingsManager()
        self.fetcher = CurrencyRateFetcher(api_key, self.settings.get_base_currency())
        self.all_currencies = self.load_all_currencies()  # dict: {name: code}

    def load_all_currencies(self):
        try:
            with open(CURRENCIES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("currencies", {})
        except FileNotFoundError:
            console.print(f"[red]Error: {CURRENCIES_FILE} not found.[/red]")
            return {}

    def main_menu(self):
        while True:
            console.print("\n[bold green]--- Currency App ---[/bold green]")
            console.print("1. Show Exchange Rates")
            console.print("2. Add Currency")
            console.print("3. Remove Currency")
            console.print("4. Change Base Currency")
            console.print("5. Convert Currency")
            console.print("6. Show Conversion History")
            console.print("7. Show All Available Currencies")
            console.print("8. Quit")

            choice = Prompt.ask("[yellow]Choose an option[/yellow]", choices=[str(i) for i in range(1, 9)])

            if choice == '1':
                self.show_rates()
            elif choice == '2':
                self.add_currency()
            elif choice == '3':
                self.remove_currency()
            elif choice == '4':
                self.change_base_currency()
            elif choice == '5':
                self.convert_currency()
            elif choice == '6':
                self.show_history()
            elif choice == '7':
                self.show_all_currencies()
            elif choice == '8':
                console.print("[magenta]👋 Goodbye![/magenta]")
                break

    def show_rates(self):
        try:
            target_currencies = self.settings.get_target_currencies()
            rates = self.fetcher.fetch(target_currencies)

            table = Table(title=f"Exchange Rates (Base: {self.fetcher.base_currency})", show_lines=True)
            table.add_column("From", style="cyan")
            table.add_column("To", style="cyan")
            table.add_column("Rate", style="green", justify="right")
            for base, target, rate in rates:
                table.add_row(base, target, f"{rate:.4f}")

            console.print(table)
            if self.fetcher.last_update_time:
                console.print(f"[dim]Last update: {self.fetcher.last_update_time.strftime('%Y-%m-%d %H:%M:%S')}[/dim]")

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def add_currency(self):
        new_currency = Prompt.ask("Enter currency code to add (e.g., EUR)").upper()
        if new_currency not in self.all_currencies.values():
            console.print(f"[red]Currency code '{new_currency}' is not in available currencies list.[/red]")
            return
        if self.settings.add_currency(new_currency):
            console.print(f"[green]{new_currency} added.[/green]")
        else:
            console.print(f"[red]{new_currency} already exists.[/red]")

    def remove_currency(self):
        current = self.settings.get_target_currencies()
        console.print("Current currencies: " + ", ".join(current))
        rem_currency = Prompt.ask("Enter currency code to remove").upper()
        if self.settings.remove_currency(rem_currency):
            console.print(f"[green]{rem_currency} removed.[/green]")
        else:
            console.print(f"[red]{rem_currency} not found.[/red]")

    def change_base_currency(self):
        new_base = Prompt.ask("Enter new base currency code").upper()
        if new_base not in self.all_currencies.values():
            console.print(f"[red]Currency code '{new_base}' is not in available currencies list.[/red]")
            return
        self.settings.set_base_currency(new_base)
        self.fetcher.update_base_currency(new_base)
        console.print(f"[green]Base currency changed to {new_base}[/green]")

    def convert_currency(self):
        try:
            from_currency = Prompt.ask("From Currency (e.g., USD)").upper()
            to_currency = Prompt.ask("To Currency (e.g., EUR)").upper()

            if from_currency not in self.all_currencies.values():
                console.print(f"[red]Currency code '{from_currency}' is not available.[/red]")
                return
            if to_currency not in self.all_currencies.values():
                console.print(f"[red]Currency code '{to_currency}' is not available.[/red]")
                return

            amount = FloatPrompt.ask("Amount to convert")

            result = self.fetcher.convert(from_currency, to_currency, amount)

            console.print(f"\n[bold cyan]💱 Conversion Result:[/bold cyan]")
            console.print(f"[green]{amount} {result['from']} = {result['result']:.4f} {result['to']} (Rate: {result['rate']:.4f})[/green]")

            self.log_conversion(result)

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def log_conversion(self, conversion_result):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_exists = False
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                file_exists = True
        except FileNotFoundError:
            file_exists = False

        with open(HISTORY_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['DateTime', 'From', 'To', 'Amount', 'Result', 'Rate']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                'DateTime': now,
                'From': conversion_result['from'],
                'To': conversion_result['to'],
                'Amount': conversion_result['amount'],
                'Result': f"{conversion_result['result']:.4f}",
                'Rate': f"{conversion_result['rate']:.4f}"
            })

    def show_history(self):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                table = Table(title="Conversion History", show_lines=True)
                table.add_column("Date & Time", style="dim")
                table.add_column("From", style="cyan")
                table.add_column("To", style="cyan")
                table.add_column("Amount", justify="right")
                table.add_column("Result", justify="right")
                table.add_column("Rate", justify="right")

                rows = list(reader)
                if not rows:
                    console.print("[yellow]No conversion history found.[/yellow]")
                    return

                for row in rows:
                    table.add_row(row['DateTime'], row['From'], row['To'], row['Amount'], row['Result'], row['Rate'])

                console.print(table)

        except FileNotFoundError:
            console.print("[yellow]No conversion history file found.[/yellow]")

    def show_all_currencies(self):
        if not self.all_currencies:
            console.print("[red]No currencies loaded.[/red]")
            return
        table = Table(title="Available Currencies", show_lines=True)
        table.add_column("Currency Name", style="magenta")
        table.add_column("Currency Symbol", style="cyan")
        for name, code in sorted(self.all_currencies.items(), key=lambda x: x[0]):
            table.add_row(name, code)
        console.print(table)

if __name__ == "__main__":
    with open('api.txt', 'r') as f:
        API_KEY = f.read().strip()

    app = CurrencyApp(API_KEY)
    app.main_menu()
