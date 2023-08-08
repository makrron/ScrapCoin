"""Module containing functions for web scraping of exchanges."""
import enum
import re
import sqlite3
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium_stealth import stealth

from api.models.price import Price


def get_db_connection():
    """Connect to the database."""
    conn = sqlite3.connect('../../instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def save_price(price: Price):
    """Save price to database."""
    conn = get_db_connection()
    try:
        conn.execute(
            f"INSERT OR REPLACE INTO BITCOIN (EXCHANGE, PAIR, PRICE, TIMESTAMP) VALUES (?, ?, ?, ?) ",
            (str(price.exchange), str(price.pair), str(price.price), price.timestamp)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


class Exchange(enum.Enum):
    """
    Enum class for exchanges.
    """
    Kraken = "Kraken"
    CoinGecko = "CoinGecko"
    Binance = "Binance"
    BLOCKCHAINCOM = "Blockchain.com"
    COIN_BASE_PRO = "CoinBasePro"
    YADIO = "Yadio"


class CoinBaseProTradePair(enum.Enum):
    """
    Enum class for coinbase pro trade pairs.
    """
    BTC_USD = "BTC-USD"
    BTC_EUR = "BTC-EUR"
    BTC_USDT = "BTC-USDT"
    BTC_GBP = "BTC-GBP"


class YadioTradePair(enum.Enum):
    """
    Enum class for yadio trade pairs.
    """
    BTC_USD = "BTC_USD"
    BTC_EUR = "BTC_EUR"
    BTC_RUB = "BTC_RUB"
    BTC_NGN = "BTC_NGN"
    BTC_GBP = "BTC_GBP"
    BTC_INR = "BTC_INR"
    BTC_KES = "BTC_KES"
    BTC_CAD = "BTC_CAD"
    BTC_AUD = "BTC_AUD"
    BTC_GHS = "BTC_GHS"
    BTC_PKR = "BTC_PKR"
    BTC_CNY = "BTC_CNY"
    BTC_PHP = "BTC_PHP"
    BTC_ZAR = "BTC_ZAR"
    BTC_UAH = "BTC_UAH"
    BTC_BRL = "BTC_BRL"
    BTC_CHF = "BTC_CHF"
    BTC_NZD = "BTC_NZD"
    BTC_HKD = "BTC_HKD"
    BTC_SAR = "BTC_SAR"
    BTC_TZS = "BTC_TZS"
    BTC_TRY = "BTC_TRY"
    BTC_AED = "BTC_AED"
    BTC_KZT = "BTC_KZT"
    BTC_JPY = "BTC_JPY"
    BTC_XAF = "BTC_XAF"
    BTC_THB = "BTC_THB"
    BTC_SEK = "BTC_SEK"
    BTC_IDR = "BTC_IDR"
    BTC_VND = "BTC_VND"
    BTC_SGD = "BTC_SGD"
    BTC_MXN = "BTC_MXN"
    BTC_MAD = "BTC_MAD"
    BTC_UGX = "BTC_UGX"
    BTC_MYR = "BTC_MYR"
    BTC_EGP = "BTC_EGP"
    BTC_PLN = "BTC_PLN"
    BTC_XOF = "BTC_XOF"
    BTC_DKK = "BTC_DKK"
    BTC_NOK = "BTC_NOK"
    BTC_CZK = "BTC_CZK"
    BTC_TWD = "BTC_TWD"
    BTC_BWP = "BTC_BWP"
    BTC_KRW = "BTC_KRW"
    BTC_COP = "BTC_COP"
    BTC_CLP = "BTC_CLP"
    BTC_PEN = "BTC_PEN"
    BTC_ARS = "BTC_ARS"
    BTC_DOP = "BTC_DOP"
    BTC_ILS = "BTC_ILS"
    BTC_LKR = "BTC_LKR"
    BTC_GEL = "BTC_GEL"
    BTC_HUF = "BTC_HUF"
    BTC_RON = "BTC_RON"
    BTC_BYN = "BTC_BYN"
    BTC_TND = "BTC_TND"
    BTC_ETB = "BTC_ETB"
    BTC_CRC = "BTC_CRC"
    BTC_ISK = "BTC_ISK"
    BTC_UYU = "BTC_UYU"
    BTC_BOB = "BTC_BOB"
    BTC_UZS = "BTC_UZS"
    BTC_VES = "BTC_VES"
    BTC_PAB = "BTC_PAB"
    BTC_GTQ = "BTC_GTQ"
    BTC_PYG = "BTC_PYG"


class BlockchaincomTradePair(enum.Enum):
    """
    Enum class for blockchain.com available trade pairs.
    """
    BTC_USD = "BTC_USD"
    BTC_EUR = "BTC_EUR"
    BTC_CAD = "BTC_CAD"
    BTC_GBP = "BTC_GBP"
    BTC_RUB = "BTC_RUB"
    BTC_CNY = "BTC_CNY"
    BTC_INR = "BTC_INR"
    BTC_BRL = "BTC_BRL"
    BTC_TRY = "BTC_TRY"


class CoinGeckoTradePair(enum.Enum):
    BTC_USD = "BTC_USD"
    BTC_IDR = "BTC_IDR"
    BTC_TWD = "BTC_TWD"
    BTC_EUR = "BTC_EUR"
    BTC_KRW = "BTC_KRW"
    BTC_JPY = "BTC_JPY"
    BTC_RUB = "BTC_RUB"
    BTC_CNY = "BTC_CNY"
    BTC_AED = "BTC_AED"
    BTC_ARS = "BTC_ARS"
    BTC_AUD = "BTC_AUD"
    BTC_BDT = "BTC_BDT"
    BTC_BHD = "BTC_BHD"
    BTC_BMD = "BTC_BMD"
    BTC_BRL = "BTC_BRL"
    BTC_CAD = "BTC_CAD"
    BTC_CHF = "BTC_CHF"
    BTC_CLP = "BTC_CLP"
    BTC_CZK = "BTC_CZK"
    BTC_DKK = "BTC_DKK"
    BTC_GBP = "BTC_GBP"
    BTC_HKD = "BTC_HKD"
    BTC_HUF = "BTC_HUF"
    BTC_ILS = "BTC_ILS"
    BTC_INR = "BTC_INR"
    BTC_KWD = "BTC_KWD"
    BTC_LKR = "BTC_LKR"
    BTC_MMK = "BTC_MMK"
    BTC_MXN = "BTC_MXN"
    BTC_MYR = "BTC_MYR"
    BTC_NGN = "BTC_NGN"
    BTC_NOK = "BTC_NOK"
    BTC_NZD = "BTC_NZD"
    BTC_PHP = "BTC_PHP"
    BTC_PKR = "BTC_PKR"
    BTC_PLN = "BTC_PLN"
    BTC_SAR = "BTC_SAR"
    BTC_SEK = "BTC_SEK"
    BTC_SGD = "BTC_SGD"
    BTC_THB = "BTC_THB"
    BTC_TRY = "BTC_TRY"
    BTC_UAH = "BTC_UAH"
    BTC_VEF = "BTC_VEF"
    BTC_VND = "BTC_VND"
    BTC_ZAR = "BTC_ZAR"
    BTC_XDR = "BTC_XDR"


class BinanceTradePair(enum.Enum):
    BTC_EUR = "BTC_EUR"
    BTC_RUB = "BTC_RUB"
    BTC_NGN = "BTC_NGN"
    BTC_GBP = "BTC_GBP"
    BTC_ZAR = "BTC_ZAR"
    BTC_UAH = "BTC_UAH"
    BTC_BRL = "BTC_BRL"
    BTC_TRY = "BTC_TRY"
    BTC_PLN = "BTC_PLN"
    BTC_ARS = "BTC_ARS"
    BTC_RON = "BTC_RON"


class KrakenTradePair(enum.Enum):
    BTC_USD = "XXBTZUSD"
    BTC_EUR = "XXBTZEUR"
    BTC_GBP = "XXBTZGBP"
    BTC_CAD = "XXBTZCAD"
    BTC_JPY = "XXBTZJPY"
    BTC_CHF = "XBTCHF"
    BTC_AUD = "XBTAUD"


def coin_base_pro(trade_pair: CoinBaseProTradePair):
    """Returns the current price of a given trade pair on Coinbase Pro.
    :param trade_pair: The trade pair to be searched.
    :type trade_pair: CoinBaseProTradePair
    :return: Price object with the current price of the given trade pair.
    :rtype: Price
    """

    url = "https://pro.coinbase.com/trade/" + trade_pair.value
    # regular expression to change - to _ in trade_pair
    tp = re.sub(r"(\w)-(\w)", r"\1_\2", trade_pair.value)
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Wait until the page is fully loaded
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        price = soup.find("div", {"class": "Flex-sc-1x8cw8c-0 MarketInfo__Section-sc-1acyfpz-3 irrwlQ"}).find("span", {
            "class": "Text-sc-142sraw-0 LocalizedNumber__StyledNumber-sc-1w0xnso-0 dngeTO"}).text
        pattern = r"[^\d,.]+"  # remove non-numeric characters
        price = re.sub(pattern, "", price)  # add . to the last two digits
        # price = float(price.replace(",", ""))  # remove comma and convert to float
        # save price to database
        save_price(Price(price=price, pair=tp, exchange=Exchange.COIN_BASE_PRO.value,
                         timestamp=time.time()))

    except Exception as e:
        print(e)
    finally:
        driver.quit()


def yadio():
    """
    Scrap yadio.io to get all bitcoin price in all fiat currencies available
    """

    url = "https://yadio.io/grid.html"
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(options=options)

    try:
        driver.get(url)
        time.sleep(3)  # Wait until the page is fully loaded
        # click on botton id "btnbtc"
        driver.find_element("id", "btnbtc").click()
        time.sleep(1)  # Wait until the page is fully loaded
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # get all span with class p-1
        price = soup.find_all("span", class_="p-1")
        for i in price:
            # get data-original-title on a tag
            price = i.text
            data = (i.find_all("a")[0].get("data-original-title"))
            # convert data to html
            data = BeautifulSoup(data, 'html.parser')
            # get pair on small tag in data variable
            pair = data.find_all("small")[0].text
            pair = "BTC_" + pair
            # fix price format
            pattern = r"[^\d.,]*([\d.,]+M?)"
            price = re.sub(pattern, r"\1", price)
            # if price start with . remove it
            if price.startswith("."):
                price = price[1:]

            # save price to database
            save_price(Price(price=price, pair=pair, exchange=Exchange.YADIO.value,
                             timestamp=time.time()))
    except Exception as e:
        print(e)
    finally:
        driver.quit()


def blockchaincom():
    """
    Scrap blockchain.com to get all bitcoin price in all fiat currencies available
    """

    url = "https://www.blockchain.com/es/explorer/prices"
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument('--headless')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    try:
        driver.get(url)

        for trade_pair in BlockchaincomTradePair:
            tp = re.search(r"BTC_(\w+)", trade_pair.value).group(1)

            button = driver.find_element(By.CSS_SELECTOR, ".sc-7b19e8be-0")
            select = Select(button)
            select.select_by_value(f'{tp}')

            price = driver.find_element(By.CLASS_NAME, "sc-89fc2ff1-0.iQXnyB").text

            pattern = r"[^\d.,]*(\d+[.,]\d+)"
            price = re.sub(pattern, r"\1", price)
            save_price(Price(price=price, pair=trade_pair.value, exchange=Exchange.BLOCKCHAINCOM.value,
                             timestamp=time.time()))
    except Exception as e:
        print(e)
    finally:
        driver.quit()


def binance(trade_pair: BinanceTradePair):
    """
    Scrap binance.com to get all bitcoin price in all fiat currencies available
    :param trade_pair: The trade pair to be searched.
    :type trade_pair: BinanceTradePair
    """

    url = f"https://www.binance.com/es/trade/{trade_pair.value}"
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(options=options)

    try:
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        price = soup.find("div", {"class": "showPrice"}).text
        save_price(Price(price=price, pair=trade_pair.value, exchange=Exchange.Binance.value,
                         timestamp=time.time()))

    except Exception as e:
        print(e)
    finally:
        driver.quit()


def coingecko():
    """
    Scrap coingecko.com to get all bitcoin price in all fiat currencies available
    """
    url = "https://www.coingecko.com/en/coins/bitcoin"
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument('--headless')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    try:
        driver.get(url)

        for trade_pair in CoinGeckoTradePair:
            tp = re.search(r"BTC_(\w+)", trade_pair.value).group(1)
            # click on class "tw-w-16 tw-text-black tw-cursor-pointer tw-py-1"
            button = driver.find_element(By.XPATH, "//span[contains(@class, 'tw-w-16') and contains(@class, "
                                                   "'tw-text-black') and contains(@class, 'tw-cursor-pointer') and "
                                                   "contains(@class, 'tw-py-1')]")
            button.click()
            # get all currency-selector-item class
            currency = driver.find_elements(By.CLASS_NAME, "currency-selector-item")
            for i in currency:
                # get data-iso-code attribute
                if i.get_attribute("data-iso-code").upper() == tp:
                    # click on currency
                    i.click()
                    # get price
                    price = driver.find_element(By.CLASS_NAME, "no-wrap").text
                    pattern = r"[^\d.,]*(\d+[.,]\d+)(?:\s+[A-Za-z]{1,3})?"
                    price = re.sub(pattern, r"\1", price)
                    price = re.sub(r"\s+[A-Za-z]{1,3}$", "", price)
                    # save price to database
                    save_price(Price(price=price, pair=trade_pair.value, exchange=Exchange.CoinGecko.value,
                                     timestamp=time.time()))

    except Exception as e:
        print(e)
    finally:
        driver.quit()


def kraken(pair: KrakenTradePair):
    """
    Scrap kraken.com to get all bitcoin price in all fiat currencies available
    :param pair: The trade pair to be searched.
    """
    # regular expression to delete _ from pair
    pair = re.sub(r"_", "", pair.value)
    url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            price = data["result"][pair]["c"][0]
            result = re.search(r'([A-Za-z]{3})$', pair)
            save_price(Price(price=price, pair="BTC_" + result.group(1), exchange=Exchange.Kraken.value,
                             timestamp=time.time()))

    except Exception as e:
        print(e)


def main():
    """
    Main function to scrap all exchanges
    """

    while True:
        # start timer to measure execution time
        print("Starting Blockchain.com")
        start_time = time.time()
        try:
            blockchaincom()
        except Exception as e:
            print(e)
        # show execution time
        print("--- %s seconds ---" % (time.time() - start_time))

        # restart timer
        print("Starting Coinbase Pro")
        start_time = time.time()
        try:
            coin_base_pro(CoinBaseProTradePair.BTC_USD)
            coin_base_pro(CoinBaseProTradePair.BTC_EUR)
            coin_base_pro(CoinBaseProTradePair.BTC_USDT)
            coin_base_pro(CoinBaseProTradePair.BTC_GBP)
        except Exception as e:
            print(e)
        # show execution time
        print("--- %s seconds ---" % (time.time() - start_time))

        # restart timer
        print("Starting Yadio")
        start_time = time.time()
        try:
            yadio()
        except Exception as e:
            print(e)
        # show execution time
        print("--- %s seconds ---" % (time.time() - start_time))

        # restart timer
        print("Starting Binance")
        start_time = time.time()
        try:
            for trade_pair in BinanceTradePair:
                binance(trade_pair)
        except Exception as e:
            print(e)
        # show execution time
        print("--- %s seconds ---" % (time.time() - start_time))

        # restart timer
        print("Starting CoinGecko")
        start_time = time.time()
        try:
            coingecko()
        except Exception as e:
            print(e)
        # show execution time
        print("--- %s seconds ---" % (time.time() - start_time))

        # restart timer
        print("Starting Kraken")
        start_time = time.time()
        try:
            for trade_pair in KrakenTradePair:
                kraken(trade_pair)
        except Exception as e:
            print(e)
        # show execution time
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
