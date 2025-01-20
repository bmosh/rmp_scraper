from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.common.action_chains import ActionChains
class OutputProfessor(object):
    def __init__(self, name, department, school, courses=[]):
        self.firstName = name.split(" ")[0]
        self.lastName = name.split(" ")[1]
        self.department = department
        self.school = school
        self.courses = courses

    def __str__(self):
        return "Name: " + self.firstName + " " + self.lastName + ", Department: " + self.department

    def toCsvString(self):
        return self.firstName + " " + self.lastName + "," + self.department


def scrape_professor_data(html_file):
    """
    Scrapes professor names, departments, and ratings from an HTML file.

    Args:
        html_file (str): Path to the HTML file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a professor
              and contains their name, department, and rating.
    """

    soup = BeautifulSoup(html_file, 'html.parser')

    professors = []
    # This is a CSS selector that finds all the divs with the specified classes.
    # These classes are used to style the professor cards on the Rate My Professors website.
    professor_cards = soup.select(".TeacherCard__StyledTeacherCard-syjs0d-0.dLJIlx")

    for card in professor_cards:
        # Extracts the professor's name from the HTML content.
        # It uses the `select_one` method with a CSS selector to find the first element that matches the selector.
        # The selector `.CardName__StyledCardName-sc-1gyrgim-0.cJdVEK` targets the HTML element that contains the professor's name.
        name_element = card.select_one(".CardName__StyledCardName-sc-1gyrgim-0.cJdVEK")
        name = name_element.text.strip() if name_element else "N/A"

        # Extracts the professor's department from the HTML content.
        department_element = card.select_one(".CardSchool__Department-sc-19lmz2k-0.haUIRO")
        department = department_element.text.strip() if department_element else "N/A"

        # Extracts the professor's rating from the HTML content.
        rating_element = card.select_one(".CardNumRating__CardNumRatingNumber-sc-17t4b9u-2")
        rating = rating_element.text.strip() if rating_element else "N/A"

        professors.append({
            "name": name,
            "department": department,
            "rating": rating
        })

    return professors

def scrape_professor_IDs(html_file):
    """
    Scrapes professor names, departments, and ratings from an HTML file.

    Args:
        html_file (str): Path to the HTML file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a professor
              and contains their name, department, and rating.
    """

    soup = BeautifulSoup(html_file, 'html.parser')

    professors = set([])
    # This is a CSS selector that finds all the divs with the specified classes.
    # These classes are used to style the professor cards on the Rate My Professors website.
    professor_cards = soup.select(".TeacherCard__StyledTeacherCard-syjs0d-0.dLJIlx")

    for card in professor_cards:
        # Extracts the professor's ID from the HTML content.
        # The Card's outermost div has an href attribute in the format href="/professor/<ID>".
        # We can extract the ID by splitting the href attribute and getting the second part.
        # print("card: ", card)
        card_href = card['href']
        # print("href: ", card_href)
        ID = card_href.split("/")[2]
        print("ID: ", ID)
        professors.add(ID)

    return professors

    print("Scraping professor data...")
    professors = scrape_professor_data(driver.page_source)  # Use your existing function

    print(f"Scraped {len(professors)} professors.")
    all_professors.extend(professors)

    professors_scraped = len(all_professors) 

    driver.quit()  # Close the browser
    return all_professors

def scrape_professor_page(id, driver):
    ratings_seen = 0

    try:
        driver.get("https://www.ratemyprofessors.com/professor/" + id)
    except:
        driver.execute_script("window.stop();")

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    
    all_courses_button = driver.find_element(By.XPATH, "//div[text()='All courses']")
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "//div[text()='All courses']")).perform()

    time.sleep(.5)
    print("Scrolling...")
    driver.execute_script("window.scrollBy(0, 350);")
    time.sleep(1)  # Wait for the content to load

    # Click the "Show More" button
    try:
        print("Clicking 'All Courses' button...")
        all_courses_button.click()
        print("Button clicked. Sleepytime!")
        time.sleep(2)  # Wait for the content to load
    except:
        print("No 'All Courses' button found.")

    try:
        card = soup.find_all("div", class_="PageWrapper__StyledPageWrapper-sc-3p8f0h-0")[0]

        # Extracts the professor's name from the HTML content.
        name = soup.find("h1", class_="erLzyk").text.strip()
        print("name: ", name)

        department = soup.find("a", class_="iMmVHb").text.strip()
        print("department: ", department)

        school = soup.find("div", class_="iLYGwn").text.strip().split("at ")[1]
        print("school: ", school)
        
        courses = []

        # Extracts the professor's rating from the HTML content.
        raw_courses = soup.find_all("div", class_=" css-2b097c-container")
        print("raw_courses: ", raw_courses)
        for course in courses:
            print(course.text.strip())
            courses.append(course.text.strip())

        prof = OutputProfessor(name, department, school, courses)

        return prof

    except Exception as e:
        print("Error:", e)

def scrape_all_professors_selenium(base_url, total_professors):
    """
    Scrapes professor data from all pages using Selenium.
    """

    all_professors = []
    professors_scraped = 0

    # Set up the Selenium webdriver (make sure you have the appropriate driver installed)
    driver = webdriver.Chrome()  # Or webdriver.Firefox() 
    driver.set_page_load_timeout(5)
    
    try:
        driver.get(base_url)
    except Exception:
        driver.execute_script("window.stop();")

    print("Waiting for the cookies popup to appear...")
    close_button = driver.find_element(By.XPATH, "//button[text()='Close']")
    close_button.click()

    while professors_scraped < 0:
        print("Finding 'Show More' button...")
        show_more_button = driver.find_element(By.XPATH, "//button[text()='Show More']")
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "//button[text()='Show More']")).perform()
        time.sleep(.5)
        print("Scrolling...")
        driver.execute_script("window.scrollBy(0, 350);")
        time.sleep(1)  # Wait for the content to load

        # Click the "Show More" button
        try:
            print("Clicking 'Show More' button...")
            show_more_button.click()
            print("Button clicked. Sleepytime!")
            time.sleep(2)  # Wait for the content to load
            professors_scraped += 8
        except:
            print("No more 'Show More' button found.")
            # Break the loop if the button is not found (end of results)
            break  

    print("Scraping professor data...")
    professors = scrape_professor_IDs(driver.page_source)
    print(f"Scraped {len(professors)} professors.")

    print("Scraping professor pages...")
    acc = 0
    for professor in professors:
        prof = scrape_professor_page(professor, driver)
        all_professors.append(prof)
        acc += 1
        if acc > 3:
            break
        
        time.sleep(.5)  # Wait before scraping the next professor
    print(f"Scraped {len(professors)} professor pages.")

    driver.quit()  # Close the browser
    return all_professors

# Example usage:
base_url = "https://www.ratemyprofessors.com/search/professors/298?q=*"
total_professors = 2883
all_professor_data = scrape_all_professors_selenium(base_url, total_professors)

for professor in all_professor_data:
    print(professor)

# # output to csv
# import csv

# # Define the CSV file name
# csv_file = 'professors.csv'

# # Define the field names for the CSV
# fieldnames = ['ID']

# # Write the professor data to the CSV file
# with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()
#     for professor in all_professor_data:
#         writer.writerow(professor)
# print(f"All professor data has been written to {csv_file}.")
