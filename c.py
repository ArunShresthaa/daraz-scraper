import requests
from bs4 import BeautifulSoup

# Send an HTTP GET request to the flash sale page
url = 'https://www.daraz.com.np/wow/i/np/landingpage/flash-sale?spm=a2a0e.11779170.flashSale.1.287d2d2bVTc17u&wh_weex=true&amp;wx_navbar_transparent=true&amp;scm=1003.4.icms-zebra-100031662-2994316.OTHER_5527396501_2640801&skuIds=128188269,127912102,128023365,127994713,117795303,125265960,141032'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    with open('c.html','w',encoding = 'utf-8') as f:
        f.write(response.text)
    # Extract item names and prices
    items = []
    for item in soup.find_all("div", class_="flash-sale-item"):
        name = item.find("div", class_="sale-title").text.strip()
        price = item.find("div", class_="sale-price").text.strip()
        items.append({"name": name, "price": price})

    # Sort the items by price in ascending order
    sorted_items = sorted(items, key=lambda x: float(x["price"].replace("Rs. ", "")))

    # Display the sorted items
    for item in sorted_items:
        print(f"Name: {item['name']}, Price: {item['price']}")
    print(len(sorted_items))
else:
    print("Failed to retrieve the page.")
