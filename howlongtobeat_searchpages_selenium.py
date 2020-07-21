from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

game_links = open('game_links.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(game_links, dialect='excel')

search_url = "https://howlongtobeat.com/#search"

driver = webdriver.Chrome()
driver.get(search_url)

try:
    page_tab_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//span[@class="search_list_page back_secondary shadow_box"]'))
    )
except:
    raise Exception('Can\'t find page count.')
finally:
    pass

number_of_pages = int(page_tab_elements[-1].text)

# print(f'There are {number_of_pages} total pages to scrape.')

search_url_list = [f'{search_url}{i+1}' for i in range(number_of_pages)]

 # Test with just the first 3 pages
for search_page_url in search_url_list[:3]:
# for search_page_url in search_url_list:
    driver.get(search_page_url)

    # Page seems to auto-refresh after loading.  Below try would succeed, then I get an error that element no longer exists when trying
    # to use page_tab_elements further down.  This slight delay resolved that issue. 
    time.sleep(.5)
    
    try:
        page_tab_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="search_list_details"]'))
        )
    except:
        raise Exception('Can\'t find game IDs.')
    finally:
        pass

    game_urls = []

    for page_tab_element in page_tab_elements:
        try:
            playstyle_types = page_tab_element.find_elements_by_xpath('.//div/div/div')
             # Check that the game includes a Main Story and that a significant number of users have submitted data (based on color coding grabbed from class)
            if ((playstyle_types[0].text == 'Main Story') & (playstyle_types[1].get_attribute('class') in ['search_list_tidbit center time_70', 'search_list_tidbit center time_80', 'search_list_tidbit center time_90', 'search_list_tidbit center time_100'])):
                game_urls.append(page_tab_element.find_element_by_xpath('.//h3/a').get_property('href'))
            else:
        except:
            continue

    # game_urls = [page_tab_element.find_element_by_xpath('.//h3/a').get_property('href') for page_tab_element in page_tab_elements]
    
    for game_url in game_urls:
        writer.writerow([game_url])

game_links.close()
driver.close()