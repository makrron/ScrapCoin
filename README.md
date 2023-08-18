**This project is under development and is not ready for use.**


# ScrapCoin Pro API
ScrapCoin Pro is a Rest API developed in Python that allows querying Bitcoin fiat prices through web scraping on different exchanges. The API provides up-to-date Bitcoin price data in various fiat currencies to provide users with reliable and timely information.

## Features

- Query updated Bitcoin prices in fiat for different trading pairs.
- Support for multiple popular exchanges through web scraping.
- Guaranteed privacy and anonymity, no user data storage.
- Private access through the TOR network.
- Periodic price updates to provide reliable data in real time.
- Easy integration with your application


## Installation
1. Clone the GitHub repository and enter en the project folder:

```bash
git clone https://github.com/makrron/ScrapCoin.git
cd ScrapCoin
```

2. Create and activate a virtual environment (Python 3.x is recommended):

```bash
python -m venv venv
source venv/bin/activate
```

3. Install the necessary dependencies:
```bash
pip install -r requirements.txt
```

4. Create instance folder, data base and config files
```bash
mkdir instance
touch config.py
```
5. Edit config file with the following structure:
```json
{
  "DATABASE": "instance/database.db",
  "CHROME_DRIVER_PATH": "/usr/lib/chromium-browser/chromedriver",
  "HOST": "127.0.0.1",
  "PORT": 80
}
```

6. Init database (in the root folder of the project):
```bash
flask --app main init-db
```

7. Run aplication
```bash
python3 main.py
python3 api/utils/web_scraper.py
```


## Documentation
[Check API Documentation](https://scrapcoinpro.gitbook.io/scrapcoin/)

## Contribution
Contributions are welcome! If you find a bug, have a suggestion or want to add a new feature, feel free to create an issue or submit a pull request.

## License
This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) license.
