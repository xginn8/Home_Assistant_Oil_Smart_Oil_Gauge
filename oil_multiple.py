import json
import os

import paho.mqtt.publish as publish
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By

display = Display(visible=0, size=(800, 600))
display.start()

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

var = browser.find_element(By.XPATH, '//p[contains(text(), "/")]').text
fill_level = browser.find_element(
    By.XPATH, "//div[@class='ts_col ts_level']//div[@class='ts_col_val']//p"
).get_attribute("innerHTML")
fill_level = fill_level.split(r"/")
current_fill_level = fill_level[0]
current_fill_proportion = round(
    (float(str(fill_level[0])) / float(str(fill_level[1]))) * 100, 1
)
battery_status = browser.find_element(
    By.XPATH, "//div[@class='ts_col ts_battery']//div[@class='ts_col_val']//p"
).get_attribute("innerHTML")
days_to_low = browser.find_element(
    By.XPATH, "//div[@class='ts_col ts_days_to_low']//div[@class='ts_col_val']//p"
).get_attribute("innerHTML")

print(current_fill_level)
print(current_fill_proportion)
print(battery_status)
print(days_to_low)

msgs = [
    {
        "topic": "oilgauge/tanklevel",
        "payload": json.dumps(
            {
                "current_fill_level": current_fill_level,
                "current_fill_proportion": current_fill_proportion,
                "battery_status": battery_status,
                "days_to_low": days_to_low,
            }
        ),
    }
]
browser.quit()
publish.multiple(
    msgs,
    hostname=mqtt_server,
    port=1883,
    auth={"username": mqtt_user, "password": mqtt_password},
)
