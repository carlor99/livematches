import requests
from bs4 import BeautifulSoup

# URL for live matches
url = "https://www.livescore.com/en/football/live/"

# Make a request to the website
response = requests.get(url)
html_content = response.content

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Placeholder for storing results
matches = []

# Scraping logic (assume matches are contained in a certain tag, needs refinement based on the actual structure)
for match in soup.find_all("div", class_="live-match-row"):  # adjust class to fit the actual HTML structure
    time_element = match.find("div", class_="time")  # Find the time of the match
    score_element = match.find("div", class_="score")  # Find the score of the match
    
    if time_element and score_element:
        match_time = time_element.text.strip()
        score = score_element.text.strip()
        
        if score == "0-0" and int(match_time[:-1]) > 65:  # Example: checking if time is after 65'
            match_name = match.find("div", class_="team-name").text.strip()
            matches.append(match_name)

# Output the matches that are 0-0 after 65 minutes

if len(matches) == 0:
    print("No matches")
else:
    for m in matches:
        print(m)
