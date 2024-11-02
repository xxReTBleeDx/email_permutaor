import random
import re
from email_verification import verify_email_with_tor

POPULATION_SIZE = 300
GENERATIONS = 10

def generate_initial_email(obfuscated_email, username_hint):
    domain = obfuscated_email.split('@')[1]
    username_variations = generate_username_variations(username_hint)
    base_name = random.choice(username_variations)
    random_suffix = ''.join(random.choice("0123456789") for _ in range(random.randint(1, 3))) + '6'
    email_prefix = base_name + random_suffix
    return email_prefix + '@' + domain

def generate_username_variations(username_hint):
    variations = set()
    base_name = re.sub(r'[^a-zA-Z]', '', username_hint.lower())
    variations.add(base_name)
    variations.add(base_name + str(random.randint(10, 99)))
    return list(variations)

def main_genetic(obfuscated_email, username_hint):
    population = [generate_initial_email(obfuscated_email, username_hint) for _ in range(POPULATION_SIZE)]
    try:
        for generation in range(GENERATIONS):
            print(f"Génération {generation + 1}/{GENERATIONS}")
            
            # Vérification de chaque email dans la population
            for email in population:
                print(f"Vérification de : {email}")
                if verify_email_with_tor(email):
                    print(f"{email} est valide")
                else:
                    print(f"{email} est invalide ou non vérifiable.")

            # Générer une nouvelle population
            population = [generate_initial_email(obfuscated_email, username_hint) for _ in range(POPULATION_SIZE)]

    except KeyboardInterrupt:
        print("\nOpération interrompue par l'utilisateur. Fermeture du programme...")

    except Exception as e:
        print(f"Erreur inattendue : {e}")
    
    finally:
        print("Fin du programme.")

if __name__ == "__main__":
    obfuscated_email = "j*******6@gmail.com"
    username_hint = "julia"
    main_genetic(obfuscated_email, username_hint)

