from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

money_machine = MoneyMachine()
coffee_maker = CoffeeMaker()
menu = Menu()

money_machine.report()
coffee_maker.report()

if coffee_maker.is_resource_sufficient(menu.menu[0]):
    print(f"Latte is Available.,{menu.menu[0].name}")