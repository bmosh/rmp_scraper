from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.common.action_chains import ActionChains
import OutputProfessor


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

# Example usage:

# html_file = requests.get("https://www.ratemyprofessors.com/search/professors/298?q=*").content
# professor_data = scrape_professor_data(html_file)

# for professor in professor_data:
#     print(f"Name: {professor['name']}")
#     print(f"Department: {professor['department']}")
#     print(f"Rating: {professor['rating']}")
#     print("---")

def scrape_all_professors_selenium(base_url, total_professors):
    """
    Scrapes professor data from all pages using Selenium.
    """

    all_professors = []
    professors_scraped = 0

    # Set up the Selenium webdriver (make sure you have the appropriate driver installed)
    driver = webdriver.Chrome()  # Or webdriver.Firefox() 
    driver.get(base_url)

    print("Waiting for the cookies popup to appear...")
    close_button = driver.find_element(By.XPATH, "//button[text()='Close']")
    close_button.click()

    while professors_scraped < 100:
        print("Finding 'Show More' button...")
        show_more_button = driver.find_element(By.XPATH, "//button[text()='Show More']")
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH, "//button[text()='Show More']")).perform()
        time.sleep(2)
        print("Scrolling...")
        driver.execute_script("window.scrollBy(0, 350);")
        time.sleep(2)  # Wait for the content to load

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
    professors = scrape_professor_data(driver.page_source)  # Use your existing function

    print(f"Scraped {len(professors)} professors.")
    all_professors.extend(professors)

    professors_scraped = len(all_professors) 

    driver.quit()  # Close the browser
    return all_professors

# Example usage:
base_url = "https://www.ratemyprofessors.com/search/professors/298?q=*"
total_professors = 2883
all_professor_data = scrape_all_professors_selenium(base_url, total_professors)


for professor in all_professor_data:
    print(f"Name: {professor['name']}")
    print(f"Department: {professor['department']}")
    print(f"Rating: {professor['rating']}")
    print("---")

# output to csv
import csv

# Define the CSV file name
csv_file = 'professors.csv'

# Define the field names for the CSV
fieldnames = ['name', 'department', 'rating']

# Write the professor data to the CSV file
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for professor in all_professor_data:
        writer.writerow(professor)
        print(f"Wrote {professor['name']} to CSV.")
        print("---")
print(f"All professor data has been written to {csv_file}.")
