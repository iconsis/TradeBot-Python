import time
import logging
from fyers_api import accessToken
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

#Auth
client_id = "P8JMXB4RGN-100"
fyers_id = "XR05892"
password = "Password@888"
app_secret = "YCMRRAL664"
digit = ["8", "0", "8", "0"]
redirect_uri = "https://192.168.55.203:8080/fyers/fyers-auth-redirect"

def get_access_token():
    session = accessToken.SessionModel(
        client_id=client_id,
        secret_key=app_secret,
        redirect_uri=redirect_uri,
        response_type="code",
        grant_type="authorization_code",
        state="abcdef",
    )

    generate_auth_code_url = session.generate_authcode()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome("tools/chromedriver.exe", options=options)

    driver.get(generate_auth_code_url)

    from selenium.webdriver.common.by import By

    login_id = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(By.XPATH, '//*[@id="fy_client_id"]')
    )

    login_id.send_keys(fyers_id)

    submit = WebDriverWait(driver, 300).until(
        lambda x: x.find_element(By.XPATH, '//*[@id="clientIdSubmit"]')
    )

    submit.click()

    wait = WebDriverWait(driver, 10)

    fy_client_pwd = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fy_client_pwd"]')))
    fy_client_pwd.send_keys(password)
    driver.implicitly_wait(20)
    submit = WebDriverWait(driver, 20).until(
        lambda x: x.find_element(By.XPATH, '//*[@id="loginSubmit"]')
    )

    submit.click()

    from selenium.webdriver.common.by import By
    digit_1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/section[8]/div[3]/div[3]/form/div[2]/input[1]")))
    digit_2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/section[8]/div[3]/div[3]/form/div[2]/input[2]")))
    digit_3 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/section[8]/div[3]/div[3]/form/div[2]/input[3]")))
    digit_4 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/section[8]/div[3]/div[3]/form/div[2]/input[4]")))

    digit_1.send_keys(digit[0])
    digit_2.send_keys(digit[1])
    digit_3.send_keys(digit[2])
    digit_4.send_keys(digit[3])

    driver.implicitly_wait(10)
    submit = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(By.XPATH, '//*[@id="verifyPinSubmit"]')
    )

    submit.click()
    time.sleep(1)

    result_url = driver.current_url
    logging.warning(result_url)
    auth_code = result_url.split("auth_code=")[1].split("&")[0]
    driver.close()

    session.set_token(auth_code)
    response = session.generate_token()

    return response['access_token']


if __name__ == '__main__':
    access_token = get_access_token()
    logging.warning(access_token)
