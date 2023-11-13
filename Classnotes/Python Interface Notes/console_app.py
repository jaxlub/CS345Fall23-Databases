from parts_and_suppliers import *

class ConsoleUI:
    def __init__(self):
        self.db = PartsAndSuppliers(rebuild=True)

    def menu(self) -> str:
        pass

    # TODO other functions that implement the menu
