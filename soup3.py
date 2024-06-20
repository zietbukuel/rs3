import selenium
from selenium import webdriver

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open the Facebook login page
url = 'https://facebook.com/'
driver.get(url)

# Locate the email input field and enter the email
driver.find_element(by='name', value='email').send_keys('21100401@ue.edu.pe')

# Locate the password input field and enter the password
driver.find_element(by='name', value='pass').send_keys('3Feb48560e?')

# Locate the "Iniciar sesión" button and click it
driver.find_element(by='name', value='login').click()

html = driver.page_source
print(html)
# Pausar el script hasta que el usuario presione Enter
input("Presiona Enter para cerrar el navegador...")

# Close the browser
driver.quit()
