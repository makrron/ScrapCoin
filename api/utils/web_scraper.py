"""Module containing functions for web scraping of exchanges."""
import enum
import re
import sqlite3
import time
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from api.models.price import Price


def get_db_connection():
    """Connect to the database."""
    conn = sqlite3.connect('../controllers/database.db')
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
        return True
    except Exception as e:
        print(e)
        return False


class Exchange(enum.Enum):
    """
    Enum class for exchanges.
    """
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
        price = soup.find("div", {"class": "Flex-sc-ap3nvf Wrapper-sc-1hfcjcf xPniB"}).find("span", {
            "class": "Text-sc-qybbog StyledNumber-sc-8mik7o jPvMed"}).text
        pattern = r"[^\d,.]+"  # remove non-numeric characters
        price = re.sub(pattern, "", price)  # add . to the last two digits
        # price = float(price.replace(",", ""))  # remove comma and convert to float
        driver.quit()
        # save price to database
        save_price(Price(price=price, pair=tp, exchange=Exchange.COIN_BASE_PRO.value,
                         timestamp=time.time()))

    except Exception as e:
        print(e)


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


def blockchaincom(trade_pair: BlockchaincomTradePair):
    """
    Scrap blockchain.com to get all bitcoin price in all fiat currencies available
    :param trade_pair: The trade pair to be searched.
    :type trade_pair: BlockchaincomTradePair
    """

    url = "https://www.blockchain.com/es/explorer/prices"
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(options=options)
    tp = re.search(r"BTC_(\w+)", trade_pair.value).group(1)

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        select_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sc-7b19e8be-0.eQEwmk")))

        select = Select(select_element)
        select.select_by_value(f'{tp}')

        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        price = soup.find_all("div", class_="sc-89fc2ff1-0 iQXnyB")
        price = price[0].text

        pattern = r"[^\d.,]*(\d+[.,]\d+)"
        price = re.sub(pattern, r"\1", price)

        save_price(Price(price=price, pair=trade_pair.value, exchange=Exchange.BLOCKCHAINCOM.value,
                         timestamp=time.time()))
        driver.quit()
    except Exception as e:
        print(e)


def main():
    """
    Main function to scrap all exchanges
    """
    while True:
        blockchaincom(BlockchaincomTradePair.BTC_EUR)
        blockchaincom(BlockchaincomTradePair.BTC_USD)
        blockchaincom(BlockchaincomTradePair.BTC_CAD)
        blockchaincom(BlockchaincomTradePair.BTC_GBP)
        blockchaincom(BlockchaincomTradePair.BTC_RUB)
        blockchaincom(BlockchaincomTradePair.BTC_CNY)
        blockchaincom(BlockchaincomTradePair.BTC_INR)
        blockchaincom(BlockchaincomTradePair.BTC_BRL)
        blockchaincom(BlockchaincomTradePair.BTC_TRY)

        coin_base_pro(CoinBaseProTradePair.BTC_USD)
        coin_base_pro(CoinBaseProTradePair.BTC_EUR)
        coin_base_pro(CoinBaseProTradePair.BTC_USDT)
        yadio()

        time.sleep(300)


if __name__ == "__main__":
    main()
