from lib import scraping, global_vars, chrome_lib

def main_scraping():
    # Variaveis
    url = global_vars.url_site
    print(f"Utilizando a url {url} para acesso.")

    driver_chrome = chrome_lib.abrir_chrome()

    # Acessa o site
    open_website_result = scraping.open_website(
        url = url,
        driver = driver_chrome
    )
    if open_website_result == 0:
        print(f"Sucesso ao abrir o site {url}!!")
    elif open_website_result == -1:
        print("ERRO: Janela Free Stock Screener não existe!!.")
        return False
    elif open_website_result == -2:
        print("ERRO: Timeout para validação da abertura do site.")
        return False
    else:
        print(f"ERRO: Saida não mapeada para funcao open_website() >> {str(open_website_result)} <<.")
        return False

    # Seleciona as ações desejadas
    select_stocks_result = scraping.select_stocks(
        title_tabela = "Symbol",
        driver = driver_chrome
    )
    if select_stocks_result == 0:
        print(f"Dados das ações carregadas com sucesso!")
    elif select_stocks_result == -1:
        print("ERRO: Botão mid cap não foi encontrado para seleção.")
        return False
    elif select_stocks_result == -2:
        print("ERRO: Botão find stocks não encontrado!!")
        return False
    elif select_stocks_result == -3:
        print("ERRO: Não foi possivel validar o carregamento com os dados das ações.")
        return False
    else:
        print(f"ERRO: Saida não mapeada para funcao select_stocks() >> {str(select_stocks_result)} <<.")
        return False

    # Captura os dados da tabela de ações
    extract_data_result = scraping.extract_data(
        driver = driver_chrome
    )

    if isinstance(extract_data_result, list):
        print(extract_data_result)
        return extract_data_result
    elif extract_data_result == -1:
        print("Falha ao obter os dados da lista.")
        return False
    else:
        print(f"ERRO: Saida não mapeada para funcao extract_data() >> {str(extract_data_result)} <<.")
        return False