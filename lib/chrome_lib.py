from lib import import_lib

def abrir_chrome(maximize=True):
    """
    Entrada:
    
    Retornos:
        driver                        # Sucesso ao abrir o chrome.
    """
    print("\n\n[Função]--> abrir_chrome")

    path_id_chrome = r"C:\Users\gamer\Desktop\Projetos_RPA\Flask_Scraping\chromedriver\chrome_id.json"
    path_driver = r"C:\Users\gamer\Desktop\Projetos_RPA\Flask_Scraping\chromedriver\chromedriver.exe"

    while True:

        session_id, remote_machine_url = False, False
        if import_lib.os.path.isfile(path_id_chrome):
            with open(path_id_chrome, "r") as file:
                session_id_as_str = file.read()
                try:
                    remote_machine_url, session_id = session_id_as_str.split(" ")
                except:
                    pass

        # Precisa para manter a sessao do Selenium aberta durante os diferente NoseTests
        global driver

        if session_id:
            driver = attach_to_session(remote_machine_url, session_id)

            if driver:
                try:
                    for handle in driver.window_handles:
                        driver.switch_to.window(handle)
                        break
                    return driver
                except:
                    print("Error attach_to_session")

                    with open(path_id_chrome, "w") as file:
                        file.write("")

        options = import_lib.Options()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        driver = import_lib.webdriver.Chrome(executable_path=path_driver, chrome_options=options)

        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})

        if maximize:
            driver.maximize_window()

        remote_machine_url = driver.command_executor._url
        session_id = driver.session_id
        session_id_as_str = str(remote_machine_url) + " " + str(session_id)

        with open(path_id_chrome, "w") as file:
            file.write(session_id_as_str)

        return driver

def WaitReadyState(driver, timeout = 60, textException = ""):
    indTimeout = 0
    elementFounded = False
    readyState = ""
    if textException == "":
        textException = driver.title
    while indTimeout <= timeout and elementFounded != True:
        try:
            readyState = driver.execute_script("return document.readyState")
            if readyState == "complete" :
                elementFounded = True
        except:
            import_lib.time.sleep(1)
            indTimeout += 1
    if indTimeout > timeout :
        print("Timeout ao esperar carregamento do browser")
    return


def reset_chrome_session():
    path_id_chrome = r"C:\Users\gamer\Desktop\Projetos_RPA\Flask_Scraping\chromedriver\chrome_id.json"

    try:
        with open(path_id_chrome, "w") as f:
            import_lib.json.dump("", f)
        return True
    except FileNotFoundError:
        return False

def attach_to_session(executor_url, session_id):
    try:
        driver = import_lib.webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        driver.close()
        driver.session_id = session_id
        driver.implicitly_wait(0) # seconds
        return driver
    except:
        return None