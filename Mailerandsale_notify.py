import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

target_item = 'Pencil' #item to target in Sale

sender_email = "aruncresta12@gmail.com"
sender_password = "pwupraonmzgutetp"
recipient_email = "oldoldphotos123456789@gmail.com"
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Daraz Flash Sale</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #333;
            color: white;
            padding: 10px;
            text-align: center;
        }
        main {
            padding: 20px;
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
        }
        a {
            text-decoration: none; /* Remove underlines if needed */
        }
    </style>
</head>"""

def scrape_items(url):
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(url)
        driver.implicitly_wait(5000)
        
        input("\n\nPress any Key to Continue....\n\n")
        os.system('cls')
        print("\n\nScanning.....\n\n")

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        items = []
        for item in soup.find_all("a"):
            try:
                if item["href"][:28] == '//www.daraz.com.np/products/':
                    try:
                        image_link = item.find("img", class_="image")["src"]
                    except:
                        image_link = 'https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-1-scaled.png'
                    href_link = item["href"]
                    item_name = item.find("div", class_="sale-title").text.strip()
                    sale_price = item.find("div", class_="sale-price").text.strip()
                    origin_price = item.find("span", class_="origin-price-value").text.strip()
                    discount = item.find("span", class_="discount").text.strip()
                    items.append({"name": item_name,"image_link": image_link, "price": sale_price, "href_link": href_link, "original_price": origin_price, "discount": discount})
                    if target_item in item_name:
                        send_alert_mail(items)
            except:
                pass        

        return items
    finally:
        driver.quit()

def send_mail(subject, Body):
    msg = MIMEMultipart()
    msg['To'] = recipient_email
    msg['From'] = sender_email
    msg['Subject'] = subject
    msg.attach(MIMEText(Body, 'html'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    
    server.sendmail(sender_email, recipient_email, msg.as_string())
    print(f"Email sent to {recipient_email}")
    server.quit()

#function to send target item sale alert
def send_alert_mail(target_items):
    html_content1 = html_content + """
    <body>
        <header>
            <h1>Daraz Sale Alert: """ + target_item + """</h1>
        </header>
        <main>
    """ + f'<img src="{target_items[-1]["image_link"]} width="200" height="200">\n<a href="{target_items[-1]["href_link"]}"><p>Name: {target_items[-1]["name"]}</p></a>\n<p>Price: {target_items[-1]["price"]}</p>\n<p>Original Price: {target_items[-1]["original_price"]}</p>\n<p>Discount: {target_items[-1]["discount"]}</p>\n<hr>\n' + """        
        </main>
    </body>
    </html>
    """
    
    send_mail(subject=f'Daraz Sale Alert: {target_item}', Body=html_content1)


#Main program Starts
url = 'https://www.daraz.com.np/wow/i/np/landingpage/flash-sale?spm=a2a0e.11779170.flashSale.1.35812d2bt4CHRT&wh_weex=true&amp;wx_navbar_transparent=true&amp;scm=1003.4.icms-zebra-100031662-2994316.OTHER_5527396501_2640801&skuIds=127975417,115632066,122522989,128114336,120319420,116265005,141032'
items = scrape_items(url)

if items:
    print(f"\n\nTotal items scraped: {len(items)}\n\n")

    sorted_items = sorted(items, key=lambda x: float(x["price"].replace("Rs.", "")))

    final_item = ''
    for item in sorted_items:
        final_item += f'<img src="{item["image_link"]} width="200" height="200">\n<a href="{item["href_link"]}"><p>Name: {item["name"]}</p></a>\n<p>Price: {item["price"]}</p>\n<p>Original Price: {item["original_price"]}</p>\n<p>Discount: {item["discount"]}</p>\n<hr>\n'

    html_content2 = html_content + """
    <body>
        <header>
            <h1>Daraz Flash Sale: """ + str(len(items)) + """</h1>
        </header>
        <main>
    """ + final_item + """        
        </main>
    </body>
    </html>
    """
    send_mail(subject=f"Daraz sale: {datetime.now().date()}", Body=html_content2)
else:
    print("Failed to retrieve the page or scrape items.")
