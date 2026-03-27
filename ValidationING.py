import re
import os
import platform
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


# =======================================
# BUSSINESS RULES CLASS
# =======================================

class PolicyRules:

    PREFIX_COMPANY_MAP = {
        "AAA": "31",
        "UDG": "31",
        "UCG": "31",
        "VCG": "40",
        "VDG": "40",
    }

    @staticmethod
    def detect_company(policy):

        prefix = policy[:3].upper()
        return PolicyRules.PREFIX_COMPANY_MAP.get(prefix, None)


# =======================================
# VALIDATION CLASS
# =======================================

class CardValidator:

    @staticmethod
    def validate_card(text):
        pattern = (
            r'^271701U('
            r'(PE|LN|LA|SQ|PS|LS)\d{2}[A-Z]{3}\d{7}\d{3}'
            r'|'
            r'(BI|BP|S2)\d{2}[A-Z]{3}\d{7}'
            r'|'
            r'(CE\d{7})'
            r')$'
        )
        return bool(re.match(pattern, text))


# =======================================
# GENERATOR CLASS
# =======================================

class CardGenerator:

    VALID_ELEMENT_TYPES = ['PE', 'LN', 'LA', 'SQ', 'PS', 'LS']
    VALID_NO_ELEMENT_TYPES = ['BI', 'BP', 'S2']

    @staticmethod
    def validate_policy(policy):
        return (
            len(policy) == 10 and
            policy[:3].isalpha() and
            policy[:3].isupper() and
            policy[3:].isdigit()
        )

    @staticmethod
    def generate_with_element(type_code, company, policy, element):
        if type_code not in CardGenerator.VALID_ELEMENT_TYPES:
            raise ValueError(f"Invalid type code: {type_code}")
        if not company.isdigit() or len(company) != 2:
            raise ValueError(f"Invalid company code: {company}")
        if not CardGenerator.validate_policy(policy):
            raise ValueError(f"Invalid policy format: {policy}")
        if not (element.isdigit() and len(element) == 3):
            raise ValueError(f"Invalid element format: {element}")
        return f"271701U{type_code}{company}{policy}{element}"

    @staticmethod
    def generate_without_element(type_code, company, policy):
        if type_code not in CardGenerator.VALID_NO_ELEMENT_TYPES:
            raise ValueError(f"Invalid type code: {type_code}")
        if not company.isdigit() or len(company) != 2:
            raise ValueError(f"Invalid company code: {company}")
        if not CardGenerator.validate_policy(policy):
            raise ValueError(f"Invalid policy format: {policy}")
        return f"271701U{type_code}{company}{policy}"

    @staticmethod
    def generate_ce_card(reference):
        if not (reference.isdigit() and len(reference) == 7):
            raise ValueError(f"Invalid reference format: {reference}")
        return f"271701UCE{reference}".format(reference)

# =======================================
# UTILITY FUNCTIONS
# =======================================


def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# =======================================
# MAIN APPLICATION CLASS
# =======================================


class Application:

    def menu(self):
        print(Fore.CYAN + "=== Card Validation and Generation ===")
        print(Fore.CYAN + "======================================")

        while True:
            print(Fore.YELLOW + "=== \nOptions ===")
            print(Fore.GREEN + "1." + Fore.WHITE + " Validate a CARD")
            print(Fore.GREEN + "2." + Fore.WHITE + " Generate a CARD" +
                  Fore.MAGENTA + " with" + Fore.CYAN + " element (PE, LN, LA, SQ, PS, LS)")
            print(Fore.GREEN + "3." + Fore.WHITE + " Generate a CARD" +
                  Fore.MAGENTA + " without" + Fore.YELLOW + " element (BI, BP, S2)")
            print(Fore.GREEN + "4." + Fore.WHITE + " Generate a CE CARD" +
                  Fore.MAGENTA + " (CE)" + Fore.GREEN+ " with Client-Reference")
            print(Fore.GREEN + "5." + Fore.RED + " Exit")
            option = input(Fore.YELLOW + "Enter your choice: ")

            if option == '1':
                self.validate_card()
            elif option == '2':
                self.generate_with_element()
            elif option == '3':
                self.generate_without_element()
            elif option == '4':
                self.generate_ce_card()
            elif option == '5':
                print(Fore.GREEN + "\nExiting the application. Goodbye!")
                time.sleep(3)  # Wait for 3 seconds before exiting
                clear_screen()
                break
            else:
                print(Fore.RED + "Invalid choice. Please try again.")

            input(Fore.YELLOW + "Press Enter to continue...")
            clear_screen()

    def validate_card(self):
        text = input(Fore.CYAN + "Enter the card text to validate: ").strip()
        if CardValidator.validate_card(text):
            print(Fore.GREEN + " \n✅ The card is valid.\n")
        else:
            print(Fore.RED + " ❌ The card is invalid.")

    def detect_company_or_ask(self, policy):
        detected = PolicyRules.detect_company(policy)
        if detected:
            print(Fore.MAGENTA + f"Company Cord is: {detected}")
            return detected
        return input(Fore.YELLOW + "Enter the company code (2 digits): ").strip()

    def generate_with_element(self):
        print(Fore.YELLOW + "\nTypes:" + Fore.LIGHTMAGENTA_EX + " (PE, LN, LA, SQ, PS, LS)")
        type_code = input("Select type: ").strip().upper()
        policy = input("Enter policy number (AAA1234567): ").strip()

        try:
            card = CardGenerator.generate_with_element(
                type_code,
                self.detect_company_or_ask(policy),
                policy,
                input("Enter element (3 digits): ").strip()
            )
            print(Fore.GREEN + f" \n✅ Generated card: {card} \n")
        except ValueError:
            print(Fore.RED + " ❌ Failed to generate card. Please check your inputs.")

    def generate_without_element(self):
        print(Fore.YELLOW + "\nTypes: BI, BP, S2")
        type_code = input("Select type: ").strip().upper()
        policy = input("Enter policy number (AAA1234567): ").strip()

        try:
            card = CardGenerator.generate_without_element(
                type_code,
                self.detect_company_or_ask(policy),
                policy
            )
            print(Fore.GREEN + f" \n✅ Generated card: {card} \n")
        except ValueError:
            print(Fore.RED + " ❌ Failed to generate card. Please check your inputs.")

    def generate_ce_card(self):
        reference = input(
            Fore.YELLOW + "Enter CE reference (7 digits): ").strip()
        try:
            card = CardGenerator.generate_ce_card(reference)
            print(Fore.GREEN + f" \n✅ Generated CE card: {card} \n")
        except ValueError:
            print(Fore.RED + " ❌ Failed to generate CE card. Please check your input.")


if __name__ == "__main__":
    app = Application()
    app.menu()
