import requests
from requests.auth import HTTPBasicAuth
import json
from rich.console import Console
import math
import numpy as np
import os
from rich.table import Column, Table


console = Console()

console.print("[bold cyan]Hi ..[/bold cyan]")

def login(u, p):
    # Making a get request
    response = requests.get('https://zccmustafa1.zendesk.com',
                auth = HTTPBasicAuth(u, p))

    assert response.status_code == 200, "Login unsuccessful ... Please check password or username again.."

def fetch_tickets(username, password):
    response = requests.get('https://zccmustafa1.zendesk.com/api/v2/tickets',
                auth = HTTPBasicAuth(username, password))

    result = json.loads(response.content)
    
    res = paginate(result)

    current_page = 0

    last_page = len(result)
    
    return result, res, last_page

def paginate(result):
    num_of_results = len(result['tickets'])
    console.print(f"[bold cyan]Fetched {num_of_results} tickets..[/bold cyan]")
    num_of_pages = math.ceil(num_of_results/25)
    res = []
    for tick in result['tickets']:
        res.append((tick['subject'], tick['requester_id'], tick['created_at']))

    res = np.array_split(res, num_of_pages)

    return res

def user_interface_all_tickets(res, last_page):
    load = console.input("[bold cyan]Load tickets? (Y/N) [/bold cyan]")
    current_page = 0
    if load == "Y" or load == "y":
        load_page(res)

    while load != "N" or "n":
        load = console.input("[bold cyan]Next page? (Y/N) [/bold cyan]")
        current_page += 1
        if current_page >= last_page:
            console.print("[bold cyan]End of pages ...[/bold cyan]")
            break
        else:
            load_page(res, current_page)

def user_interface_single_ticket(result):
    load = console.input("[bold cyan]Enter ticket number ...[/bold cyan]")
    load = int(load)
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Subject")
    table.add_column("Creator")
    table.add_column("Time", justify="right")
    print(result['tickets'][load]['subject'])
    print(result['tickets'][load]['requester_id'])
    table.add_row(result['tickets'][load]['subject'],str(result['tickets'][load]['requester_id']), result['tickets'][load]['created_at'])
    console.print(table)
    return



 
def load_page(res, current_page = 0):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Subject")
    table.add_column("Creator")
    table.add_column("Time", justify="right")
    for tick in res[current_page]:
        table.add_row(tick[0], tick[1], tick[2])

    console.print(table)


if __name__ == "__main__":
    u = input("Enter username ... ")
    p = input("Enter password ... ")
    login(u, p)
    result, res, last_page = fetch_tickets(u, p)
    while True:
        option = console.input("[bold cyan]Do you want to print all tickets or by number ? (A/N/Q)")
        if option == "A" or option == "a":
            user_interface_all_tickets(res, last_page)
        elif option == "N" or option == "n":
            user_interface_single_ticket(result)
        elif option == "Q" or option == "q":
            break

