# PS-Bot
Bot to play Pokemon Showdown for you
## Requirements
- [Chromedriver 84](https://chromedriver.chromium.org/downloads)
- Run `bash setup.sh` in the project directory if on mac or linux
- Install the libraries below if on windows
- [Selenium](https://selenium-python.readthedocs.io/installation.html)
- [Chromedriver binary](https://pypi.org/project/chromedriver-binary/)
- [Requests](https://pypi.org/project/requests/2.7.0/)
- If you want to use a non-chromium based browser, look at the selenium installation page to see how to setup those webdrivers. Also edit 
```
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'browser':'ALL' }
driver = webdriver.Chrome(desired_capabilities=d)
```
in bot.py to whatever code is needed for your browser
## How To Use
- Download the repository
- Run bot.py
