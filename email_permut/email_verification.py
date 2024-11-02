import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from stem import Signal
from stem.control import Controller
import time

def get_ip():
    """Obtenir l'IP publique et le pays en utilisant le proxy Tor, avec une alternative si ipinfo.io échoue."""
    session = requests.Session()
    session.proxies = {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}

    # Premier essai avec ipinfo.io
    try:
        response = session.get("http://ipinfo.io/json", timeout=10)
        if response.status_code == 200:
            ip_info = response.json()
            return ip_info.get("ip", "IP inconnue"), ip_info.get("country", "Pays inconnu")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la connexion à ipinfo.io : {e}")

    # Si ipinfo.io échoue, utiliser ip-api.com comme alternative
    try:
        response = session.get("http://ip-api.com/json", timeout=10)
        if response.status_code == 200:
            ip_info = response.json()
            return ip_info.get("query", "IP inconnue"), ip_info.get("country", "Pays inconnu")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la connexion à ip-api.com : {e}")

    # Si toutes les tentatives échouent, retourner des valeurs par défaut
    print("Erreur : impossible de récupérer les informations IP.")
    return "IP inconnue", "Pays inconnu"


def renew_tor_connection():
    """Renouveler le circuit Tor."""
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="remplace par le mot de passe dans que tu as choisis dans le fichier torrc")  # Remplace par le mot de passe de /etc/tor/torrc/
        controller.signal(Signal.NEWNYM)
        time.sleep(3)  # Pause pour permettre à Tor de mettre en place le nouveau circuit

def verify_email_with_tor(email_to_check):
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--headless")
    options.add_argument("--proxy-server=socks5://127.0.0.1:9050")
    
    driver = webdriver.Chrome(options=options)
    try:
        renew_tor_connection()
        current_ip, country = get_ip()
        print(f"----> Circuit Tor ---> IP actuelle : {current_ip} ({country})")
        
        driver.get("https://www.verifyemailaddress.org/email-validation")
        
        email_input = driver.find_element(By.NAME, "email")
        email_input.send_keys(email_to_check)
        email_input.send_keys(Keys.RETURN)
        
        time.sleep(5)
        
        results = driver.find_elements(By.CSS_SELECTOR, "ul li.status, ul li.success, ul li.failure")
        for result in results:
            print(result.text)
        return True  # Si l'email est vérifié avec succès
    except Exception as e:
        print(f"Erreur lors de la vérification de l'email : {e}")
        return False
    finally:
        driver.quit()

