"""Module containing functions for web scraping of exchanges."""
import enum
import time

from bs4 import BeautifulSoup
from selenium import webdriver

from api.models.price import Price


class Exchange(enum.Enum):
    """
    Enum class for exchanges.
    """
    COIN_BASE_PRO = "CoinBasePro"


class CoinBaseProTradePair(enum.Enum):
    """
    Enum class for coinbase pro trade pairs.
    """
    BTC_USD = "BTC_USD"
    BTC_EUR = "BTC_EUR"
    BTC_USDT = "BTC_USDT"


def coin_base_pro(trade_pair: CoinBaseProTradePair) -> Price:
    """Returns the current price of a given trade pair on Coinbase Pro.
    :param trade_pair: The trade pair to be searched.
    :type trade_pair: CoinBaseProTradePair
    :return: Price object with the current price of the given trade pair.
    :rtype: Price
    """

    url = "https://pro.coinbase.com/trade/" + trade_pair.value
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

        price = ''.join(filter(str.isdigit, price))  # remove non-numeric characters
        price = price[:-2] + "." + price[-2:]  # add . to the last two digits
        price = float(price.replace(",", ""))  # remove comma and convert to float

        driver.quit()
        return Price(price=price, pair=trade_pair.value, exchange=Exchange.COIN_BASE_PRO.value,
                     timestamp=time.time())

    except Exception as e:
        print(e)


if __name__ == "__main__":
    print(coin_base_pro(CoinBaseProTradePair.BTC_USDT).to_dict())
