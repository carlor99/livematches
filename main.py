from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.headless = False
driver = webdriver.Chrome(executable_path="C:\\Users\\carlo\\IdeaProjects\\chromedriver.exe", options=options)

class Match:
    def __init__(self, time, homescore, awayscore, hometeam, awayteam):
        self.time = time
        self.homescore = homescore
        self.awayscore = awayscore
        self.hometeam = hometeam
        self.awayteam = awayteam

def validate_time(time_text):
    
    if "+" in time_text:        
        time_to_validate = time_text.replace("+","").replace("\'","")[0:2]
        if time_to_validate.isnumeric():
            return int(time_to_validate)
        else:
            return 999
    elif "\'" in time_text:
        time_to_validate = time_text.replace("\'","")
        if time_to_validate.isnumeric():
            return int(time_to_validate)
        else:
            return 999
    elif time_text == 'HT':
        return 45
    else:
        return 999


available_matches = []
def start_browser():
    global driver
    
    
    driver.maximize_window()
    driver.get("https://www.livescore.com/en/football/live/")
       
    WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        'button#onetrust-accept-btn-handler'))
                                        
        )
    driver.find_element(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler').click()
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
def find_match(match_element):
    global available_matches
    WebDriverWait(match_element, 120).until(
            EC.visibility_of_element_located((By.XPATH,
                                        './/span[contains(@data-testid, "__match-row__live__status-or-time")]'))
        )
    match_time_text = match_element.find_element(By.XPATH, './/span[contains(@data-testid, "__match-row__live__status-or-time")]').text
    match_time = validate_time(match_time_text)
    """if match_time_text:
    match_time = 0"""
    if match_time < 90:
            
        WebDriverWait(match_element, 120).until(
        EC.visibility_of_element_located((By.XPATH,
                                    './/div[contains(@id, "__match-row__live__home-team-score")]'))
        )  #//span[contains(@id, "__match-row__live__home-team-score")]
        match_homescore = match_element.find_element(By.XPATH, './/div[contains(@id, "__match-row__live__home-team-score")]').text
        WebDriverWait(match_element, 120).until(
            EC.visibility_of_element_located((By.XPATH,
                                    './/div[contains(@id, "__match-row__live__away-team-score")]'))
        )
        match_awayscore = match_element.find_element(By.XPATH, './/div[contains(@id, "__match-row__live__away-team-score")]').text
        WebDriverWait(match_element, 120).until(
            EC.visibility_of_element_located((By.XPATH,
                                    './/div[contains(@id, "__match-row__live__home-team-name")]'))
        )
        match_hometeam = match_element.find_element(By.XPATH, './/div[contains(@id, "__match-row__live__home-team-name")]').text
        WebDriverWait(match_element, 120).until(
            EC.visibility_of_element_located((By.XPATH,
                                    './/div[contains(@id, "__match-row__live__away-team-name")]'))
        )
        match_awayteam = match_element.find_element(By.XPATH, './/div[contains(@id, "__match-row__live__away-team-name")]').text

        print(f"{str(match_time)}: {match_hometeam} {match_homescore} - {match_awayscore} {match_awayteam}")

        match = Match(time=match_time,
                        homescore=match_homescore,
                        awayscore=match_awayscore,
                        hometeam=match_hometeam,
                        awayteam=match_awayteam
                        ) 
        
        available_matches.append(match)
    
def return_matchlist():
    global available_matches
    return available_matches

# Function to scroll and fetch new elements
def scroll_and_fetch_elements():
    global driver
    last_height = driver.execute_script("return document.body.scrollHeight")  # Get initial height
    current_elements = driver.find_elements(By.XPATH, './/div[contains(@id, "__category-header")]/following-sibling::div[contains(@id, "__match-row")]')

    for match_element in current_elements:      
        find_match(match_element)    
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Pause to allow content to load

        # Get the new height and check for new elements
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Find elements (replace with your actual element selector)
        new_elements = driver.find_elements(By.XPATH, './/div[contains(@id, "__category-header")]/following-sibling::div[contains(@id, "__match-row")]')

        for match_element in new_elements:      
            find_match(match_element)   

        # If the height has not changed, break the loop
        if new_height == last_height:
            print("No new elements found.")
            break

        last_height = new_height  # Update last height for the next iteration

    return current_elements  # Return the set of collected elements


try:       
    start_browser()    

    # Call the function
    match_elements = scroll_and_fetch_elements()

    
            
except Exception as error:
    print(error)
    driver.quit()  

    