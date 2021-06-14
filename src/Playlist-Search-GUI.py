import tkinter as tk
from client import Client
def GUI():
    pass

client = Client()
search_by_name = input("Would you like to search by name: (Yes/No)\n")
run = True
while(run):
    if(search_by_name.lower() == "yes"):
        client.search("name")
        search_by_name = input("----------------"+
        "\nWould you like to search again: (Yes/No)\n")
    elif(search_by_name.lower() == "no"):
        run = False
    else:
        search_by_name = input()
