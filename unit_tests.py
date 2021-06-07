import unittest
from lib import scraping, chrome_lib

class MyTestCase(unittest.TestCase):

    def test_open_website(self):
        url_site = "https://finance.yahoo.com/screener/new"
        test_case = [
            {
                "test_case": "Caso de Erro",
                "url": 'https://www.google.com.br/',
                "timeout": 5,
                "expected_result": "-1"
            },
            {
                "test_case": "Caso de Sucesso",
                "url": url_site,
                "timeout": 5,
                "expected_result": "0"
            }
        ]

        for case in test_case:

            driver_chrome = chrome_lib.abrir_chrome()

            open_website_result = scraping.open_website(
                url = case['url'],
                driver = driver_chrome
            )
            print("test_open_website() " + str(case['test_case']))
            assert str(open_website_result) == str(case['expected_result'])
            print("test_open_website() Sucesso!!")
            driver_chrome.quit()

    def test_select_stocks(self):
        url_site = "https://finance.yahoo.com/screener/new"
        test_case = [
            {
                "test_case": "Caso de Erro",
                "url": url_site,
                "title": "ERRO NAO ENCONTRAR",
                "timeout": 5,
                "expected_result": "-3"
            },
            {
                "test_case": "Caso de Sucesso",
                "url": url_site,
                "title": "Symbol",
                "expected_result": "0"
            }
        ]

        for case in test_case:

            driver_chrome = chrome_lib.abrir_chrome()
            timeout = case.get("timeout", None) or 60

            open_website_result = scraping.open_website(
                url = case['url'],
                driver = driver_chrome
            )

            select_stocks_result = scraping.select_stocks(
                title_tabela = case['title'],
                driver = driver_chrome,
                timeout = timeout
            )
            print("test_select_stocks() " + str(case['test_case']))
            assert str(select_stocks_result) == str(case['expected_result'])
            print("test_select_stocks() Sucesso!!")
            driver_chrome.quit()

    def test_extract_data(self):
        url_site = "https://finance.yahoo.com/screener/new"
        test_case = [
            {
                "test_case": "Caso de Sucesso",
                "url": url_site,
                "title": "Symbol",
                "expected_result": "list"
            }
        ]

        for case in test_case:

            driver_chrome = chrome_lib.abrir_chrome()
            timeout = case.get("timeout", None) or 60

            open_website_result = scraping.open_website(
                url = case['url'],
                driver = driver_chrome
            )

            select_stocks_result = scraping.select_stocks(
                title_tabela = case['title'],
                driver = driver_chrome,
                timeout = timeout
            )
            extract_data_result = scraping.extract_data(
                driver = driver_chrome
            )
            print("test_extract_data() " + str(case['test_case']))
            type_result = type(extract_data_result)
            print(f"Type do retorno {str(type_result)}")
            assert str(case['expected_result']) in str(type_result)
            print("test_extract_data() Sucesso!!")
            driver_chrome.quit()

if __name__ == '__main__':
    unittest.main()
