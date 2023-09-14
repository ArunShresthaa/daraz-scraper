from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

url = 'https://www.daraz.com.np/wow/i/np/landingpage/flash-sale?spm=a2a0e.11779170.flashSale.1.35812d2bt4CHRT&wh_weex=true&amp;wx_navbar_transparent=true&amp;scm=1003.4.icms-zebra-100031662-2994316.OTHER_5527396501_2640801&skuIds=127975417,115632066,122522989,128114336,120319420,116265005,141032'
# Use the ChromeDriverManager to automatically download and manage ChromeDriver
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(url)  # Replace with your URL

# Wait for some time for the page to load and JavaScript to execute
driver.implicitly_wait(10)  # You can adjust the timeout as needed

# Open the DevTools Network tab
driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.F12)

# You can capture network requests here by interacting with the Developer Tools UI using Selenium

# After capturing the desired network requests, save them to a file
network_traffic = driver.execute_cdp_cmd("Network.getAllInterceptions", {})
with open('network_traffic.json', 'w', encoding='utf-8') as f:
    f.write(str(network_traffic))

# Close the browser
driver.quit()
