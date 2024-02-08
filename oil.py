import os

import paho.mqtt.publish as publish
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By

display = Display(visible=0, size=(800, 600))
display.start()

# browser = webdriver.Chrome(options="--no-sandbox")
browser = webdriver.Chrome()

browser.set_window_size(1440, 900)

user_name = os.getenv("SMART_OIL_USERNAME")
password = os.getenv("SMART_OIL_PASSWORD")
mqtt_server = os.getenv("MQTT_SERVER")
mqtt_user = os.getenv("MQTT_USER")
mqtt_password = os.getenv("MQTT_PASSWORD")

browser.get("https://app.smartoilgauge.com/app.php")
browser.find_element(By.ID, "inputUsername").send_keys(user_name)
browser.find_element(By.ID, "inputPassword").send_keys(password)
browser.find_element(By.CSS_SELECTOR, "button.btn").click()
browser.implicitly_wait(3)

nav = browser.find_element(By.XPATH, '//p[contains(text(), "/")]').text
nav_value = nav.split(r"/")
browser.quit()
print(nav_value[0])
publish.single(
    "oilgauge/tanklevel",
    nav_value[0],
    hostname=mqtt_server,
    port=1883,
    auth={"username": mqtt_user, "password": mqtt_password},
)

display.stop()
