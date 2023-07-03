# Parameters:
num_whiskies_to_be_considered_major_distillery = 300

# Crawling and scraping packages:
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Basic and math packages:
import pandas as pd

# Timing the code:
import time
zero_time = time.perf_counter()

# STEP 1: Scraping the Whisky.com website

# Initializing the driver and loading the main page on WhiskyBase:
DRIVER_PATH = r'C:/Users/yonif/Downloads/chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://www.whisky.com/whisky-database/bottle-search/whisky.html')
page_source = driver.page_source
soup = BeautifulSoup(page_source,'html.parser')


# Initializing the database (TODO use a dataframe?)
whiskies = []

# Extracting the data from the table - TODO replace with relevant tag
HTML_data = soup.find_all("table")[0].find_all("tr")[1:]

#core_range_data_header = [["Whisky", "Distillery", "Country/Region", "Age", "Rating"]]
data = []
whisky_urls = []

# TODO extract all URLS and relevant info found in main page.
# TODO add filter/cache able to establish if whisky is already in database, since there are different sizes
for element in HTML_data:
    sub_data = []
    for sub_element in element:
        try:
            if sub_element.get_text().strip(' \n\t') != '':
                sub_data.append(sub_element.get_text().strip(' \n\t')) # Jump of two because site has extra columns
        except:
            continue
    data.append(sub_data)

    try:  # Extracting the links for major distilleries for in-depth analysis:
        if float(sub_data[2]) > num_whiskies_to_be_considered_major_distillery:
            whisky_url = element.find('a').get('href')
            whisky_urls.append(whisky_url)
    except:
        continue


# Storing the data from the main page into dataframe, then as a CSV file:
distillery_df = pd.DataFrame(data=data, columns=list_header) # TODO find a header
#major_distillery_df = distillery_df[distillery_df['Whiskies'].astype(float) > num_whiskies_to_be_considered_major_distillery]


# TODO Crawler: for every URL in whiskies go to page, extract all relevant data

for whisky_url in whisky_urls:

    # TODO get the descriptions

    # TODO get the flavor profile overview. Consider a dictionary so that you can add new flavors on the fly, or find list of flavors

    # TODO (long-term) get comments, save in separate dataframe

    # open question - get raw data and then parse later, or does parsing already happen here?

    # old code
    driver.get(distillery_url)
    distillery_page_source = driver.page_source
    soup = BeautifulSoup(distillery_page_source, 'html.parser')
    distillery_name = soup.find_all(id="company-name")[0].find_all("h1")[0].get_text().strip(' \n\t')
    region_name = soup.find_all(id="company-name")[0].find_all("li")[0].get_text().strip(' \n\t')
    if region_name == "Scotland":
        region_name = region_name + " " + soup.find_all(id="company-name")[0].find_all("li")[1].get_text().strip(' \n\t')
    all_whiskies_from_distillery = soup.find_all("table")[0].find_all("tbody")[0].find_all("tr")[1:]
    for whisky in all_whiskies_from_distillery:
        try:  # Iterating all core-range whiskies (HTML tags have no class), until the seperator item which has a class.
            if whisky.attrs['class']:
                break
        except: pass
        whisky_attributes = whisky.find_all("td")
        whisky_url = whisky_attributes[2].find('a').get('href')
        whisky_name = whisky_attributes[2].get_text().strip(' \n\t')
        whisky_age_text = whisky_attributes[3].get_text()
        try: whisky_age = float(whisky_age_text)
        except: whisky_age = "NAS"
        #whisky_strength = whisky_attributes[4]
        try: whisky_rating = float(whisky_attributes[7].get_text())
        except: continue
        core_range_data.append([whisky_name, distillery_name, region_name, whisky_age, whisky_rating])

        # Now we move on to the URL in order to extract the tertiary information: the reviews.
        driver.get(whisky_url)
        whisky_page_source = driver.page_source
        soup = BeautifulSoup(whisky_page_source, 'html.parser')
        whisky_reviews = soup.find_all(attrs={"class": "wb--note-content-wrapper"})
        for review in whisky_reviews:
            print(review)
            review_text = ""
            try: review_text = review_text + review.find_all(attrs={"data-translation-field": "message"})[0].get_text().strip(' \n\t')
            except: pass
            try: review_text = review_text + review.find_all(attrs={"data-translation-field": "nose_text"})[0].get_text().strip(' \n\t')
            except: pass
            try: review_text = review_text + review.find_all(attrs={"data-translation-field": "taste_text"})[0].get_text().strip(' \n\t')
            except: pass
            try: review_text = review_text + review.find_all(attrs={"data-translation-field": "finish_text"})[0].get_text().strip(' \n\t')
            except: pass

            reviews_data.append([whisky_name, review_text])

# TODO export the file as CSV / parquet
# Storing the data from the main page into dataframe, then as a CSV file:
whiskies_df = pd.DataFrame(data=core_range_data, columns=core_range_data_header)
whiskies_df.to_csv('Whiskies.csv')
#reviews_df = pd.DataFrame(data=reviews_data, columns=reviews_data_header)
#reviews_df.to_csv('Reviews.csv')