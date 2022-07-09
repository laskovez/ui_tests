# Python Web UI end-to-end automated tests for CMM project 

# Before run the tests:
1. Install Python 3.6+
2. Install dependencies: pip install -r requirements.txt
3. Rename ".env.example" to ".env"

## To run tests on Native browser:
1. Install Chrome browser 
2. Install Chrome webdriver to browser/drivers folder: https://chromedriver.chromium.org/downloads
3. Add path where the ChromeDriver file is saved to environment variables if needed. Or 
4. Change browser type to corresponding Native one:
- in **config.py**: `BROWSER_TYPE = BrowserType.CHROME_NATIVE`

## Run Web UI tests via CLI
```
pytest -n=2 tests
```

## Note
Tests are run on the English version of the browser and only 
for the English localization of the site at this stage of implementation