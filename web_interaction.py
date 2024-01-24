import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
def web_interaction(ip_ls):

    os.environ['PATH'] += r"D:/programs"
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--silent')
    options.add_argument('--disable-logging') 

    # for GUI 
    # options.add_experimental_option("detach", True)
    print("Intialalizing connection...")
    driver = webdriver.Chrome(options=options)

    print("Getting your website...")
    driver.get("https://10.98.35.24:16311/ibm/console/logon.jsp")

    driver.implicitly_wait(10)
    
    print("Authenticating...")
    username = driver.find_element(By.ID,'j_username')
    password = driver.find_element(By.ID,'j_password')
    go = driver.find_element(By.ID,'login-button')
    

    username.send_keys("ahmed.k.gamal")

    with open('C:/Users/Ahmed.K.Gamal/Desktop/netcool.txt','r') as file:
        pswd = file.read()


    password.send_keys(pswd)
    go.click()
    print("Authenticated successfully")
    try:
        print('logging out from other devices...')
        log_me_out = driver.find_element(By.NAME,'submitBtn')
        log_me_out.click()
    except:
        pass
        
    nodes = driver.find_element(By.CLASS_NAME,"bIcon")
    nodes.click()
    fixed_nodes = driver.find_element(By.ID,'dojoUnique10')
    fixed_nodes.click()

    iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[title="Content frame"]')
    driver.switch_to.frame(iframe)


    search_field = driver.find_element(By.CSS_SELECTOR,'input[title="Enter search term"]')
    # time.sleep(5) # need to be more relibale

    # Wait for the element to be present in the DOM
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,"/html[1]/body[1]/table[1]/tbody[1]/tr[2]/td[2]/div[3]/div[1]/div[1]/div[3]/div[3]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]")))

    for ip in ip_ls:
        search_field.send_keys(ip,Keys.ENTER)
        var = {}
        for i in range(1,20):
            var[i] = driver.find_element(By.XPATH,f"/html[1]/body[1]/table[1]/tbody[1]/tr[2]/td[2]/div[3]/div[1]/div[1]/div[3]/div[3]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[{i}]").accessible_name
            
        # log_type = driver.find_element(By.XPATH,"/html[1]/body[1]/table[1]/tbody[1]/tr[2]/td[2]/div[3]/div[1]/div[1]/div[3]/div[3]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[9]").accessible_name
        # time = driver.find_element(By.XPATH,"/html[1]/body[1]/table[1]/tbody[1]/tr[2]/td[2]/div[3]/div[1]/div[1]/div[3]/div[3]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[6]").accessible_name
        # print(log_type)
        print(f"{var[7]} {var[2]} {var[18]} {var[8]}")
        close_icon =driver.find_element(By.CSS_SELECTOR,'span[title="Remove quick filters"]')
        close_icon.click()

    # driver.switch_to.default_content()

ip_ls = ["10.8.0.14","10.33.136.5","10.24.244.101"]
# "10.8.0.14","10.33.136.5","10.24.244.101"
web_interaction(ip_ls)