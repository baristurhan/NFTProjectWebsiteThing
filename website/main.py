import web3.types

from ABI import abi
import time

Web3 = web3.Web3

polling_interval = 300
refresh_interval = 12

address = '0x8D8c8E5cc25DA769f9b48BC62AD993A24dcA550f'

w3 = Web3(Web3.HTTPProvider("https://kovan.infura.io/v3/7f547ea2badc495c8d0bb762dee016a8"))
# noinspection PyTypeChecker
contract = w3.eth.contract(address=address, abi=abi)

cached = {}


def fetch_nft_data(nft_id):
    nft_data = {
        "name": contract.functions.name(nft_id).call(),
        "uri": contract.functions.getURI(nft_id).call(),
        "price": contract.functions.getPrice(nft_id).call()
    }
    return nft_data


def update_html():
    begin = open("document_start.html", "r")
    end = open("document_end.html", "r")
    begin_str = "".join([n for n in begin])
    end_str = "".join([n for n in end])
    begin.close()
    end.close()

    mid_str = ""

    for i in cached:
        data = cached[i]
        mid_str += f"""\n<div class="grid-item">\n<div class="ee c"><p class="c d">{data["name"]}</p></div>\n<div 
        class="ff c"><img class="row" src="{data["uri"]}" alt="{data["name"]}"></div>\n<div class="ee c"><p class="c">
        {data["price"]} CETH</p></div>\n</div>\n """

    full_html = begin_str + mid_str + end_str

    output = open("index.html", "w")
    output.write(full_html)
    output.close()


def refresh(current):
    global cached
    cached = {}
    for i in range(0, current, 1):
        cached[i] = fetch_nft_data(i)


def add_new(current, last):
    global cached
    for i in range(last, current, 1):
        cached[i] = fetch_nft_data(i)


def main():
    last_minted = 0
    last_price_update = 0
    count = 0
    changed = False
    while True:
        current_minted = contract.functions.getMintedCount().call()
        current_price_update = contract.functions.getPriceUpdates().call()

        if current_minted > last_minted:
            add_new(current_minted, last_minted)
            changed = True

        if current_price_update > last_price_update or count == refresh_interval - 1:
            refresh(current_minted)
            changed = True

        if changed:
            update_html()
            changed = False

        last_minted = current_minted
        last_price_update = current_price_update

        count += 1
        count %= refresh_interval
        time.sleep(polling_interval)


cached[0] = {
    "name": "Not The Bees?!?!?",
    "uri": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fyt3.ggpht.com%2F-7zFDHK5X45w%2FAAAAAAAAAAI%2FAAAAAAAAAAA%2FQJfHeLTEZwE%2Fs900-c-k-no-mo-rj-c0xffffff%2Fphoto.jpg&f=1&nofb=1",
    "price": 0xDEADBEEF
}

cached[1] = {
    "name": "Funny Dog",
    "uri": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fyt3.ggpht.com%2F-7zFDHK5X45w%2FAAAAAAAAAAI%2FAAAAAAAAAAA%2FQJfHeLTEZwE%2Fs900-c-k-no-mo-rj-c0xffffff%2Fphoto.jpg&f=1&nofb=1",
    "price": 0xDEADBEEF
}

cached[3] = {
    "name": "Sample Text",
    "uri": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fyt3.ggpht.com%2F-7zFDHK5X45w%2FAAAAAAAAAAI%2FAAAAAAAAAAA%2FQJfHeLTEZwE%2Fs900-c-k-no-mo-rj-c0xffffff%2Fphoto.jpg&f=1&nofb=1",
    "price": 0xDEADBEEF
}

cached[4] = {
    "name": "78 Billion Line Text File",
    "uri": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fyt3.ggpht.com%2F-7zFDHK5X45w%2FAAAAAAAAAAI%2FAAAAAAAAAAA%2FQJfHeLTEZwE%2Fs900-c-k-no-mo-rj-c0xffffff%2Fphoto.jpg&f=1&nofb=1",
    "price": 0xDEADBEEF
}

update_html()

if __name__ != "__main__":
    main()
