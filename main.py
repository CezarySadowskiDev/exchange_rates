import xml.etree.ElementTree

import requests
import xml.etree.ElementTree as ET


def fetch_data() -> xml.etree.ElementTree.Element:
    try:
        url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        return root

    except requests.exceptions.RequestException as e:
        print(f'Error occurred while fetching data: {e}')


def get_currencies_data_from_fetched_data(currencies: list, root: xml.etree.ElementTree.Element) -> dict:
    currencies_data_dict = {}

    namespaces = {'ns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}

    try:
        for child in root.findall('.//ns:Cube[@currency]', namespaces):
            if child.attrib['currency'] in currencies:
                currencies_data_dict[child.attrib['currency']] = float(child.attrib['rate'])
        return currencies_data_dict

    except ValueError as e:
        print(f"Error occurred during mapping currencies: {e}")


def convert_currencies(data: dict, base_currency: str) -> dict:
    try:
        if base_currency != 'EUR':
            converted_currencies = {'EUR': f'{data[base_currency]:.2f}'}
            base_currency_value = data[base_currency]
            for currency, rate in data.items():
                converted_currencies[currency] = f"{base_currency_value / rate:.2f}"

            converted_currencies.pop(base_currency)

            return converted_currencies
        else:
            return data

    except ValueError as e:
        print(f"Error occurred while converting currencies: {e}")


def format_output(data: dict, base_currency: str) -> str:
    output_string = f"""Exchange rates for {base_currency} currency:\n"""

    for currency, rate in data.items():
        output_string += f'1 {currency} = {rate} {base_currency}\n'

    return output_string


if __name__ == '__main__':
    all_currencies = ['CHF', 'DKK', 'EUR', 'GBP', 'PLN', 'USD']
    user_currency = input("Please provide base currency (CHF, DKK, EUR, GBP, PLN, USD): ").upper()

    if user_currency in all_currencies:
        full_data = fetch_data()
        currencies_data = get_currencies_data_from_fetched_data(all_currencies, full_data)
        converted_currencies_data = convert_currencies(currencies_data, user_currency)

        print(format_output(converted_currencies_data, user_currency))

    else:
        print("Currency not supported!")
