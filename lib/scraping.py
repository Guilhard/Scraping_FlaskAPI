from lib import import_lib, chrome_lib, classes

def open_website(url, driver, *, timeout = 60):
    """
    Inputs
        url                    # Url de entrada para acessar site finance  yahoo
    Outputs
        -1                     # Janela Free Stock Screener não existe!!.
        -2                     # Timeout para validação da abertura do site.
        0                      # Site aberto com sucesso
    """
    # -- Variaveis Função -- #
    all_options = ""
    valida_tag = ""

    print("[Função]--> open_website")

    driver.get(url)
    wait = import_lib.WebDriverWait(driver, 10)
    original_window = driver.current_window_handle
    assert len(driver.window_handles) == 1
    wait.until(import_lib.EC.number_of_windows_to_be(1))
    for window_handle in driver.window_handles:

        if window_handle != original_window:
            print("Switch window")
            driver.switch_to.window(window_handle)
            break

    chrome_lib.WaitReadyState(driver)
    try:
        import_lib.autoit.win_activate("Free Stock Screener")
        print("Janela Free Stock Screener ativada com sucesso!!")
    except:
        print("Janela Free Stock Screener não existe!!")
        return -1

    # Valida durante 1 minuto a abertura da tela
    timer = classes.Timer(timeout)
    while timer.not_expired:
        print("Buscando a tag para confirmação da abertura do site.")
        try:
            all_options = driver.find_elements_by_tag_name("span")
            print(all_options)
        except:
            continue

        for option in all_options:
            try:
                valida_tag = option.get_attribute("innerText")
                print(f"InnerText da option capturada: {valida_tag}.")
            except:
                continue

            if "United States" in valida_tag:
                print(f"Site {url} aberto com sucesso!!")
                return 0

    if timer.expired:
        print(f"Timeout para validação da abertura do site {url}")
        return -2

def select_stocks(title_tabela, driver, *, timeout = 60):
    """
        Inputs
            url                    # Url de entrada para acessar site finance  yahoo
        Outputs
            -1                     # Botão mid cap não foi encontrado para seleção.
            -2                     # Botão find stocks não encontrado!!
            -3                     # Não foi possivel validar o carregamento com os dados das ações.
            0                      # Dados das ações carregadas com sucesso!
        """
    # -- Variaveis Função -- #
    all_buttons = ""
    valida_btn = ""
    text_btn_stock = ""
    valida_acao = ""
    span_acao = ""
    flag_btn = False

    print("[Função]--> select_stocks")
    # Valida durante 1 minuto buscando o botão mid range
    timer = classes.Timer(timeout)
    while timer.not_expired:
        print("Buscando a os botões para clicar.")
        try:
            all_buttons= driver.find_elements_by_tag_name("button")
            print(all_buttons)
        except:
            continue

        for button in all_buttons:
            try:
                valida_btn = button.get_attribute("innerText")
                print(f"InnerText do botao capturado: {valida_btn}.")
            except:
                continue

            if "Mid Cap" in valida_btn:
                print(f"Botão {valida_btn} encontrado, clicando!!")
                button.click()
                flag_btn = True
                break

        if flag_btn:
            print("Aguarda a liberação do botão.")
            import_lib.time.sleep(2)
            break

    if timer.expired:
        print(f"Botão mid cap não foi encontrado para seleção.")
        return -1

    # Clicando no botão Find Stocks
    text_btn_stock = driver.execute_script('return document.getElementsByTagName("button")[17].innerText')

    if "Find Stocks" in text_btn_stock:
        print("Clicando em Find Stocks")
        driver.execute_script('document.getElementsByTagName("button")[17].click()')
    else:
        print("Botão find stocks não encontrado!!")
        return -2

    timer = classes.Timer(timeout)
    while timer.not_expired:
        print("Buscando a os botões para clicar.")
        try:
            valida_acao = driver.find_elements_by_tag_name("span")
            print(valida_acao)
        except:
            continue

        for txt_acao in valida_acao:
            try:
                span_acao = txt_acao.get_attribute("innerText")
                print(f"InnerText das acoes capturada: {span_acao}.")
            except:
                continue

            if title_tabela in span_acao:
                print("Dados das ações carregadas com sucesso!")
                return 0

    if timer.expired:
        print(f"Não foi possivel validar o carregamento com os dados das ações.")
        return -3

def extract_data(driver):
    """
            Inputs
                url                    # Url de entrada para acessar site finance  yahoo
            Outputs
                -1                     # Falha ao tentar capturar os dados da tabela.
                lista                  # Sucesso: Retorna os dados capturados
            """
    # -- Variaveis Função -- #
    linha_captura = 0
    linhas_tabela = ""
    lista = []
    symbol = ""
    name = ""
    price = ""

    print("[Função]--> extract_data")

    linhas_tabela = driver.execute_script(
        'return document.getElementsByTagName("tbody")[0].getElementsByTagName("tr").length'
    )
    print(f"Linhas tabela {str(linhas_tabela)}")

    while linha_captura < linhas_tabela:

        obj_captura = {}

        obj_captura['symbol'] = driver.execute_script(
            'return document.getElementsByTagName("tbody")[0].getElementsByTagName("tr")["' + str(linha_captura) + '"].children[0].innerText'
        )

        obj_captura['name'] = driver.execute_script(
            'return document.getElementsByTagName("tbody")[0].getElementsByTagName("tr")["' + str(linha_captura) + '"].children[1].innerText'
        )

        obj_captura['price'] = driver.execute_script(
            'return document.getElementsByTagName("tbody")[0].getElementsByTagName("tr")[' + str(linha_captura) + '].children[2].innerText'
        )

        lista.append(obj_captura)
        linha_captura += 1

    if len(lista) > 0:
        print("Dados capturados com sucesso!")
        return lista
    else:
        print("Falha ao tentar capturar os dados da tabela.")
        return -1
