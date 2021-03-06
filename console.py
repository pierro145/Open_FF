from colorama import Fore, Style

from interaction import Interaction
from api_data import Data
from sql_setup import Sqlconnection
import config


class App:
    """class contains all elements of menu."""

    def __init__(self):
        """initializing variables for input user."""

        self.interaction = Interaction()
        self.api_data = Data()
        self.api_data.categories
        self.sql_setup = Sqlconnection()
        self.menu_selectable = False
        self.menu_get_product = False

    def is_valid(self, liste, choice):
        """check if the choice is valide."""

        if self.choice.isdigit() and 0 < int(choice) <= len(liste):
            return True
        return False

    def input(self, liste, validator):
        """return the selectable products items list."""

        elements = [f"{i+1}: {element}"
                    for i, element in enumerate(liste)]
        elements.append("\n>>> ")
        message = "\n".join(elements)
        while True:
            self.choice = input(message)
            if validator(liste, self.choice):
                return liste[int(self.choice) - 1]
            print(Fore.LIGHTRED_EX +
                  "\n Choix non valide! \n"
                  + Style.RESET_ALL)

    def input_product_detail(self, liste, validator):
        """give the detail of the selected product."""

        if self.menu_get_product is True:
            elements = [
                f"ID: {i[6]} : {i[1]} MARQUE : {i[5]} NUTRISCORE : "
                f"{Fore.YELLOW}{i[3].upper()}{Style.RESET_ALL}"
                for i in liste
            ]
        else:
            elements = [
                f" {i[1]} MARQUE : {i[5]} NUTRISCORE : "
                f"{Fore.YELLOW}{i[3].upper()}{Style.RESET_ALL} "
                f"MAGASINS : {i[0]} "
                f"URL : {Fore.GREEN}{i[4]}{Style.RESET_ALL}"
                for i in liste
            ]
        if self.menu_selectable is True:
            elements = [f"{i+1}: {element}"
                        for i, element in enumerate(elements)]
            elements.append("\n>>> ")
            message = "\n".join(elements)
            while True:
                self.choice = input(message)
                if validator(liste, self.choice):
                    return liste[int(self.choice) - 1]
                print(Fore.LIGHTRED_EX +
                      "\n Choix non valide! \n"
                      + Style.RESET_ALL)
        else:
            elements.append("""\n==Appuyer sur Entrer==\n""")
            message = "\n".join(elements)
        self.choice = input(message)
        return liste

    def welcome(self):
        """update datas at the launch if necessary."""

        print("\n Que voulez vous faire ?\n")

        self.choice = self.input(
            config.WELCOME,
            validator=self.is_valid)
        if self.choice == config.WELCOME[0]:
            self.sql_setup.table_initializing()
            print("Mise à jour des données OpenFoodFact...")
            self.api_data.get_products_from_france()
            print("\n injection des données OK \n")
            self.menu_categories()
        elif self.choice == config.WELCOME[2]:
            self.interaction.show_history()
            self.input_product_detail(
                self.interaction.history_result,
                validator=self.is_valid,
            )
            self.welcome()
        elif self.choice == config.WELCOME[1]:
            self.menu_categories()
        elif self.choice == config.WELCOME[3]:
            quit

    def menu_categories(self):
        """show products category."""

        self.choice = self.input(
                self.api_data.categories,
                validator=self.is_valid
                )
        self.sub_menu_products()

    def sub_menu_products(self):
        """show the product list after the category list selected."""

        self.menu_get_product = True
        self.menu_selectable = True

        if self.choice in self.api_data.categories:
            self.interaction.value = self.choice
            self.interaction.value_2 = self.choice
            self.interaction.get_product()
        self.choice = self.input_product_detail(
            self.interaction.product_list,
            validator=self.is_valid
        )
        self.sub_menu_product_detail()

    def sub_menu_product_detail(self):
        """show the product detail."""

        self.menu_selectable = False

        self.interaction.value = self.choice[6]
        self.interaction.get_product_detail()
        print("\n DETAIL PRODUIT: \n")
        self.choice = self.input_product_detail(
            self.interaction.product_detail, validator=self.is_valid,
        )
        self.sub_menu_product_substitute()

    def sub_menu_product_substitute(self):
        """show the substitute product."""

        self.menu_substitute = True
        self.menu_selectable = False

        print("\n PRODUIT AVEC UN NUTRISCORE PLUS FAIBLE: \n")
        self.interaction.get_product_substitute()
        if (len(self.interaction.product_list)) == 0:
            print(
                Fore.LIGHTGREEN_EX
                + "\n Pas de substitut plus sain \n"
                + Style.RESET_ALL
            )
        self.choice = self.input_product_detail(
            self.interaction.product_list, validator=self.is_valid
        )
        self.sub_menu_history()

    def sub_menu_history(self):
        """menu contains selectable choices for show product or delete products
        saved."""

        self.menu_selectable = False
        self.menu_get_product = False

        self.choice = self.input(config.HISTORY, validator=self.is_valid)
        if self.choice == config.HISTORY[0]:
            self.interaction.save_history()
            self.sub_menu_history()
        elif self.choice == config.HISTORY[1]:
            self.interaction.show_history()
            self.input_product_detail(
                self.interaction.history_result, validator=self.is_valid
            )
            self.sub_menu_history()
        elif self.choice == config.HISTORY[3]:
            self.menu_categories()
        elif self.choice == config.HISTORY[2]:
            self.interaction.delete_history()
            print(
                Fore.LIGHTBLUE_EX
                + "\n Les produits ont été supprimés !\n"
                + Style.RESET_ALL
            )
            self.sub_menu_history()
        elif self.choice == config.HISTORY[3]:
            quit
