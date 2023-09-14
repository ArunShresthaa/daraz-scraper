from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from datetime import datetime
from tqdm import tqdm

item = 'Razor'

sender_email = "aruncresta12@gmail.com"
sender_password = "pwupraonmzgutetp"
subject = f"{item}: Sale Alert"
recipient_email = "oldoldphotos123456789@gmail.com"

url = 'https://www.daraz.com.np/wow/i/np/landingpage/flash-sale?spm=a2a0e.11779170.flashSale.1.35812d2bt4CHRT&wh_weex=true&amp;wx_navbar_transparent=true&amp;scm=1003.4.icms-zebra-100031662-2994316.OTHER_5527396501_2640801&skuIds=127975417,115632066,122522989,128114336,120319420,116265005,141032'

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    driver.get(url)
    driver.implicitly_wait(5000)
    page_source = driver.page_source
    
    if item in page_source:
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
        </head>
        <body>
            <header>
                <h1>Daraz Flash Sale:</h1>
            </header>
            <main>
        """ + item + 'in Sale' + """        
            </main>
        </body>
        </html>
        
        
        """
        
        msg = MIMEMultipart()
        msg['To'] = recipient_email
        msg['From'] = sender_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Email sent to {recipient_email}")
        
        server.quit()
    else:
        print("Item Not on Sale:")
    
finally:
    driver.quit()