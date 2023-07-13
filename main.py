from undetected_chromedriver import ChromeOptions, Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Traductor:
    def __init__(self, traducir: str, idioma='ES_EN'):
        self.respuesta = None
        self.traducir = traducir
        self.driver = self.start_webdriver(pos="right")
        self.wait = WebDriverWait(self.driver, 30)
        self.idioma = idioma

    def traducir_texto(self):
        self.driver.get('https://translate.google.es')

        self.rechazar_cookies()

        self.idiomas()

        # Input de lo que quieres traducir
        e = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea')))
        e.send_keys(self.traducir)

        # Respuesta
        e = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div/div[9]/div/div[1]/span[1]/span/span')))

        self.respuesta = e.text

        self.driver.quit()

        return self.respuesta
    
    def idiomas(self):
        if self.idioma == 'ES_EN':
            # Botón de español parte izquierda (ES - EN)
            button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[1]/c-wiz/div[2]/div/div[2]/div/div/span/button[3]')))
            button.click()
        elif self.idioma == 'EN_ES':
            # Botón de inglés parte izquierda
            button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="i9"]')))
            button.click()

    def rechazar_cookies(self):
        # Rechazar Cookies
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[1]/div/div/button')))
        button.click()

    @staticmethod # Permite llamar como Traductor.start_webdriver()
    def start_webdriver(headless=False, pos="max", lang='en', proxy=False, proxylist='', proxy_type='http'):
        '''
        Inicia un navegador de Chrome y devuelve el objeto Webdruver instanciado.
        pos: indica la posición del navegador en la pantalla ("max" | "left" | "right").
        '''

        options = ChromeOptions()

        # Idioma Inglés
        options.add_argument(f"--lang={lang}")

        # Desactivar guardado de credenciales
        options.add_argument('--password-store=basic')
        options.add_experimental_option(
            'prefs',
            {
                'credentials_enable_service': False,
                'profile.password_manager_enabled': False,
            },
        )

        # Proxies
        if proxy:
            options.add_argument(f'--proxy-server={proxy_type}://{proxylist}')

        # Iniciar driver
        driver = Chrome(
            version_main=114,
            options=options,
            headless=headless,
            log_level=3,
        )

        if not headless:
            # maximizar ventana
            driver.maximize_window()
            if pos != 'max':
                ancho, alto = driver.get_window_size().values()
                if pos == "left":
                    driver.set_window_rect(x=0, y=0, width=ancho//2, height=alto)
                elif pos == "right":
                    driver.set_window_rect(x=ancho//2, y=0, width=ancho//2, height=alto)
        return driver


if __name__ == '__main__':
    traductor1 = Traductor("Hi, I'm Paco", idioma='EN_ES').traducir_texto()
    print(traductor1)

    traductor2 = Traductor("Hola, soy Paco", idioma='ES_EN').traducir_texto()
    print(traductor2)