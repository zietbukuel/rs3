import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open the Facebook login page
url = 'https://facebook.com/'
driver.get(url)

# Locate the email input field and enter the email
driver.find_element(By.NAME, 'email').send_keys('21100401@ue.edu.pe')

# Locate the password input field and enter the password
driver.find_element(By.NAME, 'pass').send_keys('3Feb48560e?')

# Locate the "Iniciar sesión" button and click it
driver.find_element(By.NAME, 'login').click()

# Wait for the login process to complete
time.sleep(5)

# Navigate to the El Comercio Facebook page
el_comercio_url = 'https://www.facebook.com/elcomerciope'
driver.get(el_comercio_url)

# Pause to allow the page to load
time.sleep(5)

# Scroll down to load more content
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# Extract the page source
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Extract posts
posts = soup.find_all('div', class_='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0')

for post in posts:
    content = post.find('div', class_='ecm0bbzt e5nlhep0 a8c37x1j').text
    print(content)

# Pause the script until the user presses Enter
input("Presiona Enter para cerrar el navegador...")

# Close the browser
driver.quit()
