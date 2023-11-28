#Namespaces
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import re
import os
import time
import enquiries

# Gobal variables
local_path = os.getcwd()
adblock_extension_path = "Extensions/AdBlock.crx"
download_location = str(local_path)+"/Files"

# Create Firefox options
firefox_options = Options()

# Set the download location in the options
firefox_options.set_preference("browser.download.folderList", 2)
firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
firefox_options.set_preference("browser.download.dir", download_location)
firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
firefox_options.headless = True

# Add the AdBlock extension to the profile (Assuming you want to use an extension)
firefox_options.add_argument(f"extension={adblock_extension_path}")

# Create the WebDriver instance with the custom options
driver = webdriver.Firefox(options=firefox_options)

driver.set_window_size(1200, 700)

def apk_downloader():
    options = [
        '✅ Apkpure.com', 
        '✅ Apkcombo.com', 
        '✅ Apkmirror.com',
        '✅ Androidapksfree.com',
        '✅ Play.google.com',
        '✅ Aptoide.en.com',
        '✅ Apkmonk.com',
        '✅ Apk-dl.com',
        '✅ Luckymodapk.com', 
        '✅ Thinkkers.com',
        '✅ Dlandroid.com',
        '✅ Apkmody.io', 
        '✅ Apkaward.com',
        '✅ Apkdone.com',
        '🟡 Cafebazaar.ir',
        '🛑 Dzapk.com',
        '🛑 Apk4all.io', 
        '🛑 Bazaar.abuse.ch'
    ]

    # Prompt user to choose a platform
    choice = enquiries.choose('Pick your platform: \n ------------------ \n ✅ = Done \n 🟡 = Store \n 🛑 = Special Case  \n ------------------ ', options)
    index_of_choice = options.index(choice)

    print(str(choice)+" at index="+str(index_of_choice))
    
    # Prompt user to enter a search word
    searchWord = input("Enter the searchWord: ")

    # List of search URLs corresponding to each platform
    array_of_searches = [
        f"https://apkpure.com/search?q={searchWord}",
        f"https://apkcombo.com/search/{searchWord}",
        f"https://www.apkmirror.com/?post_type=app_release&searchtype=apk&page=1&s={searchWord}",
        f"https://androidapksfree.com/page/1/?s={searchWord}",
        f"https://play.google.com/store/search?q={searchWord}&c=apps",
        f"https://en.aptoide.com/search?query={searchWord}&type=apps",
        f"https://www.apkmonk.com/ssearch?q={searchWord}",
        f"https://apk-dl.com/search?q={searchWord}",
        f"https://www.luckymodapk.com/search.html?q={searchWord}",
        f"https://thinkkers.com/page/1/?s={searchWord}",
        f"https://dlandroid.com/page/1/?s={searchWord}",
        f"https://apkmody.io/?s={searchWord}",
        f"https://apkaward.com/search/{searchWord}",
        f"https://apkdone.com/page/1/?s={searchWord}&post_type=post",
    ]

    # Get the chosen search URL based on the index
    chosen_search_url = array_of_searches[index_of_choice]
    print(f"Chosen search URL: {chosen_search_url}")
    driver.get(chosen_search_url)

    # 1 - ApkPure downloader
    if index_of_choice == 0:
        # Accept cookies
        time.sleep(1)
        cookiebutton = driver.find_element(By.CSS_SELECTOR, 'body > div.fc-consent-root > div.fc-dialog-container > div.fc-dialog.fc-choice-dialog > div.fc-footer-buttons-container > div.fc-footer-buttons > button.fc-button.fc-cta-consent.fc-primary-button')
        cookiebutton.click()
        print("1 - Cookies_clicked")

        # Scroll the page 50% down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        time.sleep(1) 

        # Click showmore button
        while True:
                try:
                    next_button = WebDriverWait(driver, 1).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'showmore'))
                    )
                    next_button.click()
                    print("2 - Clicked showmore button")
                    time.sleep(1)
                except:
                    print("- Showmore button not found or not visible.")
                    break
   
        # Click showmore button
        while True:
            try:
                next_button = WebDriverWait(driver, 1).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '.loadmore'))
                )
                next_button.click()
                print("3 - Clicked loadmore button")
                time.sleep(1)
            except:
                print("- Loadmore button not found or not visible.")
                break
   
        #Get total number of apps
        total_apps = len(driver.find_elements(By.CSS_SELECTOR, "#search-res > li > dl:nth-child(1) > div:nth-child(2) > a:nth-child(1)"))
        print("4 - Total number of apps = "+str(total_apps))
        
        # Insert hrefs into download_links
        download_links = []
        print("5 - Insert links into array")
        rounds = ["x"] * int(total_apps)
        for count, item in enumerate(rounds):
            element = driver.find_element(By.CSS_SELECTOR, "#search-res > li:nth-child("+str(count+1)+") > dl:nth-child(1) > div:nth-child(2) > a:nth-child(1)")
            link = element.get_attribute("href")
            download_links.append(str(link))

        # Download apps from download_links
        for count, item in enumerate(download_links):
            print("6 - Download App #"+str(count+1))
            driver.get(download_links[count])
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
            time.sleep(1)
            # Try and see if an ad is open
            ad_check()
            driver.find_element(By.CSS_SELECTOR, 'a.btn').click()
            time.sleep(5)
        
        print("7 - Finish downloading "+str(total_apps))
        driver.close()

    #------------------------------------------
    # 2 - ApkCombo downloader
    elif index_of_choice == 1:

        # Accept cookies
        time.sleep(10)
        cookiebutton = driver.find_element(By.CSS_SELECTOR, '.fc-cta-consent')
        cookiebutton.click()
        print("1 - Cookies_clicked")

        #Get total number of apps
        google_enhanched_apps = len(driver.find_elements(By.CSS_SELECTOR, "div.content-apps:nth-child(1) > a"))
        other_apps = len(driver.find_elements(By.CSS_SELECTOR, ".content > a"))
        print("2 - Total number of apps = "+str(int(google_enhanched_apps)+int(other_apps)))
        
        # Insert hrefs into download_links
        download_links = []
        print("3 - Insert links into array")
        rounds = ["x"] * int(google_enhanched_apps)
        for count, item in enumerate(rounds):
            element = driver.find_element(By.CSS_SELECTOR, "div.content-apps:nth-child(1) > a:nth-child("+str(count+1)+")")
            link = element.get_attribute("href")
            download_links.append(str(link))

        rounds = ["x"] * int(other_apps)
        for count, item in enumerate(rounds):
            element = driver.find_element(By.CSS_SELECTOR, ".content > a:nth-child("+str(count+1)+")")
            link = element.get_attribute("href")
            download_links.append(str(link))

        # Download apps from download_links
        for count, item in enumerate(download_links):
            ad_check()
            print("4 - Download App #"+str(count+1))
            driver.get(download_links[count])
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
            time.sleep(1)
            ad_check()
            driver.find_element(By.CSS_SELECTOR, 'div.button-group:nth-child(4) > a:nth-child(1)').click()
            time.sleep(5)
            driver.find_element(By.CSS_SELECTOR, '#best-variant-tab > div:nth-child(1) > ul:nth-child(1) > li:nth-child(1) > ul:nth-child(2) > li:nth-child(1) > a:nth-child(1)').click()
            time.sleep(5)
        
        print("5 - Finish downloading "+str(total_apps))
        driver.close()

    #------------------------------------------
    # 3 - apkmirror downloader
    elif index_of_choice == 2:
        # Accept cookies
        time.sleep(10)
        cookiebutton = driver.find_element(By.CSS_SELECTOR, '.css-47sehv')
        cookiebutton.click()
        print("1 - Cookies_clicked")

        #Total pages & apps
        total_pages_text = driver.find_element(By.CSS_SELECTOR, '.pages').text
        total_pages = total_pages_text.replace('Page 1 of ', '')
        print("Total pages ="+str(total_pages))
        apps_pr_page = len(driver.find_elements(By.CSS_SELECTOR, '#content > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)'))
        print("Total apps pr. page ="+str(apps_pr_page))

        # Make download list
        array_of_apps_download_link_page = ["x"]*int(total_pages)
        array_of_apps_download_link_apps = ["x"]*int(apps_pr_page)
        download_links = []

        # Begin download
        for count, item in enumerate(array_of_apps_download_link_page):
            ad_check()
            new_page = chosen_search_url.replace("page=1",("page="+str(count+1)))
            driver.get(new_page)
            for count2, item in enumerate(array_of_apps_download_link_apps):
                ad_check()
                element = driver.find_element(By.CSS_SELECTOR, "#content > div:nth-child(3) > div:nth-child("+str(count2+6)+") > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > a")
                link = element.get_attribute("href")
                download_links.append(str(link))
            for count3, item in enumerate(download_links):
                ad_check()
                driver.find_element(By.CSS_SELECTOR, "#downloads > div > div > div:nth-child(2) > div:nth-child(5) > a").click()
                time.sleep(3)
                driver.find_element(By.CSS_SELECTOR, "#file > div.row.d-flex.f-a-start > div.center.f-sm-50 > div > a").click()
                time.sleep(3)
            download_links = []  # Reset download_links to an empty list for each iteration
        print("2 - Finish downloading "+str(total_apps))
        driver.close()

   #------------------------------------------
    # 4 - androidapksfree downloader
    elif index_of_choice == 3:

        # Get critical numbers
        time.sleep(2)
        total_apps_text = driver.find_element(By.CSS_SELECTOR, 'div.boxed-content:nth-child(2) > span:nth-child(3)').text
        total_apps_digits = re.sub(r'\D', '', total_apps_text)
        total_apps = int(total_apps_digits)
        print("Total number of apps:", total_apps)
        pages = driver.find_element(By.CSS_SELECTOR, 'a.page-numbers:nth-child(5)').text
        print("Total number of pages:", pages)
        apps_pr_page = len(driver.find_elements(By.CSS_SELECTOR, '.devapk-apps-list > section > div:nth-child(1) > h1:nth-child(2) > a:nth-child(1)'))
        print("Total Max-number of apps pr. page:", apps_pr_page)
        ad_check()
        # Make download list
        array_of_apps_download_link_page = ["x"]*int(pages)
        array_of_apps_download_link_apps = ["x"]*int(apps_pr_page)
        download_links = []

        # Begin download
        for count, item in enumerate(array_of_apps_download_link_page):
            ad_check()
            new_page = chosen_search_url.replace("page/1",("page/"+str(count+1)))
            driver.get(new_page)
            ad_check()
            for count2, item in enumerate(array_of_apps_download_link_apps):
                try:
                    element = driver.find_element(By.CSS_SELECTOR, ".devapk-apps-list > section:nth-child("+str(count2+1)+") > div:nth-child(1) > h1:nth-child(2) > a:nth-child(1)")
                except Exception as E:
                    element = driver.find_element(By.CSS_SELECTOR, ".devapk-apps-list > section:nth-child("+str(count2+2)+") > div:nth-child(1) > h1:nth-child(2) > a:nth-child(1)")
                link = element.get_attribute("href")
                download_links.append(str(link))
            for count3, item in enumerate(download_links):
                driver.get(download_links[count3])
                ad_check()
                driver.find_element(By.CSS_SELECTOR, ".buttonDownload").click()
                time.sleep(3)
                ad_check()
                driver.find_element(By.CSS_SELECTOR, ".buttonDownload").click()
                time.sleep(3)
                ad_check()

            download_links = []  # Reset array
        print("5 - Finish downloading "+str(total_apps))
        driver.close()

   #------------------------------------------
    # 5 - play.google downloader
    elif index_of_choice == 4:
        array_of_names = []
        apk_downloader_combo = "https://apkcombo.com/downloader/"
        total_apps = len(driver.find_elements(By.CSS_SELECTOR, '.fUEl2e > div > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)'))
        print("1 - Total number of apps:", total_apps)
        array_of_apps_download_link_page = ["x"]*int(total_apps)
        for count, item in enumerate(array_of_apps_download_link_page):
            element = driver.find_element(By.CSS_SELECTOR, '.fUEl2e > div:nth-child('+str(count+1)+') > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)')
            link = element.get_attribute("href")
            array_of_names.append(str(link))
        for count2, item2 in enumerate(array_of_names):
            driver.get(apk_downloader_combo)
            # Accept cookies
            time.sleep(2)
            try:
                cookiebutton = driver.find_element(By.CSS_SELECTOR, '.fc-cta-consent')
                cookiebutton.click()
                print("2 - Cookies_clicked")
            except Exception as E:
                pass
            search_ = driver.find_element(By.CSS_SELECTOR, '#package')
            search_.send_keys(str(array_of_names[count2]))
            time.sleep(1)
            search_.send_keys(Keys.RETURN)
            time.sleep(10)
            download_element = driver.find_element(By.CSS_SELECTOR, "#apkcombo-tab > div > ul > li > ul > li:nth-child(1) > a")
            driver.execute_script("arguments[0].scrollIntoView();", download_element)
            time.sleep(1)
            download_element.click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, '.file-list > li:nth-child(1) > a:nth-child(1)').click
            time.sleep(1)
            print("- Downloading "+str(item2))
        print("3 - Finish downloading "+str(total_apps))
        driver.close()

   #------------------------------------------
    # 6 - en.aptoide downloader
    elif index_of_choice == 5:
        # Accept cookies
        time.sleep(1)
        cookiebutton = driver.find_element(By.CSS_SELECTOR, '#__next > div > div._app__MainContainer-sc-hddmdl-1.Tkbhw > div > div.cookie-notice__CookieNoticeWrapper-sc-186p755-0.geaipX > div > div.cookie-notice__CookieNoticeContainer-sc-186p755-2.gJtnCG > div > div:nth-child(2)')
        cookiebutton.click()
        print("1 - Cookies_clicked")

        #Get total number of apps
        total_apps = len(driver.find_elements(By.CSS_SELECTOR, "#__next > div > div._app__MainContainer-sc-hddmdl-1.Tkbhw > div > div.search__SearchPageContainer-sc-12zbr4z-0.gmwLEi > section > div > div > div > div > a"))
        print("2 - Total number of apps = "+str(total_apps))
        
        # Insert hrefs into download_links
        download_links = []
        print("3 - Insert links into array")
        rounds = ["x"] * int(total_apps)
        for count, item in enumerate(rounds):
            element = driver.find_element(By.CSS_SELECTOR, "#__next > div > div._app__MainContainer-sc-hddmdl-1.Tkbhw > div > div.search__SearchPageContainer-sc-12zbr4z-0.gmwLEi > section > div > div > div > div > a:nth-child("+str(count+1)+")")
            link = element.get_attribute("href")
            download_links.append(str(link))

        # Download apps from download_links
        for count, item in enumerate(download_links):
            print("- Download App #"+str(count+1))
            driver.get(download_links[count])
            time.sleep(5)
            try:
                driver.find_element(By.CSS_SELECTOR, '.iZbrWx').click()
            except Exception as E:
                driver.find_element(By.CSS_SELECTOR, '.cUUAti').click()
            time.sleep(5)
        
        print("4 - Finish downloading "+str(total_apps))
        driver.close()

   #------------------------------------------
    # 7 - Apkmonk downloader
    elif index_of_choice == 6:

        #Get total number of apps
        total_apps = len(driver.find_elements(By.CSS_SELECTOR, "body > main > div > div > div > div.section.side-padding-8 > div > div > a"))
        print("1 - Total number of apps = "+str(total_apps))
        
        # Insert hrefs into download_links
        download_links = []
        print("2 - Insert links into array")
        rounds = ["x"] * int(total_apps)
        for count, item in enumerate(rounds):
            element = driver.find_element(By.CSS_SELECTOR, "body > main > div > div > div > div.section.side-padding-8 > div > div:nth-child("+str(count+1)+") > a")
            link = element.get_attribute("href")
            download_links.append(str(link))

        # Download apps from download_links
        for count2, item in enumerate(download_links):
            print("- Download App #"+str(count2+1))
            driver.get(download_links[count2])
            time.sleep(5)
            try:
                driver.find_element(By.CSS_SELECTOR, '#download_button').click()
            except Exception as E:
                pass
            time.sleep(5)
        
        print("4 - Finish downloading "+str(total_apps))
        driver.close()

   #------------------------------------------
    # 8 - apk-dl.com downloader
    elif index_of_choice == 7:

     #Get total number of apps
        total_apps = len(driver.find_elements(By.CSS_SELECTOR, "#contents > div > div.cluster > div > div > div.cover > a"))
        print("1 - Total number of apps = "+str(total_apps))
        
        # Insert hrefs into download_links
        download_links = []
        print("2 - Insert links into array")
        rounds = ["x"] * int(total_apps)
        for count, item in enumerate(rounds):
            element = driver.find_element(By.CSS_SELECTOR, "#contents > div > div.cluster > div:nth-child("+str(count+1)+") > div > div.cover > a")
            link = element.get_attribute("href")
            download_links.append(str(link))

        # Download apps from download_links
        for count2, item in enumerate(download_links):
            print("- Download App #"+str(count2+1))
            driver.get(download_links[count2])
            time.sleep(5)
            try:
                driver.find_element(By.CSS_SELECTOR, 'div > div.mdl-layout__content > div > div > div > div > div > div.main-content > div:nth-child(4) > section.detail > div.download-btn > div > a.mdl-button.mdl-js-button.mdl-button--raised.mdl-js-ripple-effect.fixed-size.mdl-button--primary').click()
            except Exception as E:
                pass
            time.sleep(10)
        
        print("3 - Finish downloading "+str(total_apps))
        driver.close()

   #------------------------------------------
    # 9 - Luckymodapk.com downloader
    elif index_of_choice == 8:
     
     #Get total number of apps
        total_apps = len(driver.find_elements(By.CSS_SELECTOR, "body > div.w1380.clearfix > div.left-all > section.clearfix > div > ul > li > div > div.list-one-btn-box > a"))
        print("1 - Total number of apps = "+str(total_apps))

        # Insert hrefs into download_links
        download_links = []
        print("2 - Insert links into array")
        rounds = ["x"] * int(total_apps)
        for count, item in enumerate(rounds):
            element = driver.find_element(By.CSS_SELECTOR, "body > div.w1380.clearfix > div.left-all > section.clearfix > div > ul > li:nth-child("+str(count+1)+") > div > div.list-one-btn-box > a")
            link = element.get_attribute("href")
            download_links.append(str(link))

        # Download apps from download_links
        for count2, item in enumerate(download_links):
            print("- Download App #"+str(count2+1))
            driver.get(download_links[count2])
            time.sleep(5)
            try:
                driver.find_element(By.CSS_SELECTOR, 'body > div.w1380.clearfix > div.left-all > section:nth-child(2) > div.btntext > a').click()
            except Exception as E:
                pass
            time.sleep(5)
            driver.find_element(By.CSS_SELECTOR, 'body > div.w1380.clearfix > div.left-all > section > div.btntext > a').click()
            time.sleep(5)
            driver.find_element(By.CSS_SELECTOR, 'body > div.w1380.clearfix > div.left-all > section > div.btntext > a').click()
            time.sleep(5)

        print("3 - Finish downloading "+str(total_apps))
        driver.close()

    #------------------------------------------ 
    # 10 - thinkkers.com downloader
    elif index_of_choice == 9:
        
        #Get total number of apps
        total_apps = len(driver.find_elements(By.CSS_SELECTOR, "#primary > section:nth-child(2) > div > div > article > a"))
        print("1 - Total number of apps = "+str(total_apps))
        total_pages = driver.find_element(By.CSS_SELECTOR, '#primary > section:nth-child(3) > div > div > div:nth-child(3) > a').text
        print("2 - Total number of pages = "+str(total_pages))

        # Insert hrefs into download_links
        download_links = []
        print("2 - Insert links into array")
        rounds = ["x"] * int(total_pages)
        round2 = ["x"] * int(total_apps)
        for count, item in enumerate(rounds):
            new_page = chosen_search_url.replace("page/1",("page/"+str(count+1)))
            driver.get(new_page)
            for count2, item in enumerate(round2):
                element = driver.find_element(By.CSS_SELECTOR, "#primary > section:nth-child(2) > div > div > article:nth-child("+str(count2+1)+") > a")
                link = element.get_attribute("href")
                download_links.append(str(link))
            for count3, item in enumerate(download_links):
                driver.get(download_links[count3])
                ad_check()
                driver.find_element(By.CSS_SELECTOR, "#article > div > div:nth-child(7) > div > div > a").click()
                time.sleep(3)
                ad_check()
                driver.find_element(By.CSS_SELECTOR, "#article > div > div:nth-child(5) > div > a:nth-child(1)").click()
                time.sleep(3)
                ad_check()
                driver.find_element(By.CSS_SELECTOR, "#download-button").click()
                time.sleep(3)

            download_links = []  # Reset array
        print("3 - Finish downloading "+str(total_apps))
        driver.close()

  #------------------------------------------
    # 11 - Dlandroid.com downloader
    elif index_of_choice == 10:
        
        #Get total number of apps
        total_apps = len(driver.find_elements(By.CSS_SELECTOR, "body > div.container-fluid.mtop > div:nth-child(1) > div.col-lg-offset-1.col-lg-7 > div > div > div > div.col-lg-10.visible-sm.visible-xs > a.more2"))
        print("1 - Total number of apps = "+str(total_apps))
        total_pages = driver.find_element(By.CSS_SELECTOR, 'body > div.container-fluid.mtop > div:nth-child(1) > div.col-lg-offset-1.col-lg-7 > div > div.g-page > div > a:nth-child(5)').text
        print("2 - Total number of pages = "+str(total_pages))

        # Insert hrefs into download_links
        download_links = []
        print("2 - Insert links into array")
        rounds = ["x"] * int(total_pages)
        round2 = ["x"] * int(total_apps)
        for count, item in enumerate(rounds):
            new_page = chosen_search_url.replace("page/1",("page/"+str(count+1)))
            driver.get(new_page)
            for count2, item in enumerate(round2):
                element = driver.find_element(By.CSS_SELECTOR, "body > div.container-fluid.mtop > div:nth-child(1) > div.col-lg-offset-1.col-lg-7 > div > div:nth-child("+str(count2+1)+") > div > div.col-lg-10.visible-sm.visible-xs > a.more2")
                link = element.get_attribute("href")
                download_links.append(str(link))
            for count3, item in enumerate(download_links):
                driver.get(download_links[count3])
                ad_check()
                driver.find_element(By.CSS_SELECTOR, "body > div.container-fluid > div:nth-child(1) > div.col-lg-7.col-lg-offset-1 > div.post-single > div:nth-child(2) > div.col-xs-12.col-lg-9.col-md-7.col-sm-7.post-matn > a").click()
                time.sleep(3)
                ad_check()
                driver.find_element(By.CSS_SELECTOR, "#dllink").click()
                time.sleep(3)
                ad_check()
            download_links = []  # Reset array
        print("3 - Finish downloading "+str(total_apps))
        driver.close()

  #------------------------------------------
    # 12 - Apkmody.com downloader
    elif index_of_choice == 11:
     #Get total number of apps

        total_apps = len(driver.find_elements(By.CSS_SELECTOR, "#primary > section:nth-child(3) > div > div > div > article > a"))
        print("1 - Total number of apps = "+str(total_apps))

        # Insert hrefs into download_links
        download_links = []
        print("2 - Insert links into array")
        rounds = ["x"] * int(total_apps)
        for count, item in enumerate(rounds):
            element = driver.find_element(By.CSS_SELECTOR, "#primary > section:nth-child(3) > div > div > div:nth-child("+str(count+1)+") > article > a")
            link = element.get_attribute("href")
            download_links.append(str(link))

        # Download apps from download_links
        for count2, item in enumerate(download_links):
            print("- Download App #"+str(count2+1))
            driver.get(download_links[count2])
            time.sleep(5)
            try:
                driver.find_element(By.CSS_SELECTOR, '#article > section.container.with-aside > div:nth-child(2) > div.wp-block-buttons.margin-top-15 > div:nth-child(1) > a').click()
            except Exception as E:
                pass
            time.sleep(5)
            driver.find_element(By.CSS_SELECTOR, '#article > section > div > div.entry-content.entry-block > div > a:nth-child(1)').click()
            time.sleep(5)

        print("3 - Finish downloading "+str(total_apps))
        driver.close()

  #------------------------------------------
    # 13 - Apkaward.com downloader
    elif index_of_choice == 12:

        total_apps = len(driver.find_elements(By.CSS_SELECTOR, "body > div.fixdx > div.content.row.autow > div > div.main-box.row > article > div > a"))
        print("1 - Total number of apps = "+str(total_apps))

        # Insert hrefs into download_links
        download_links = []
        print("2 - Insert links into array")
        rounds = ["x"] * int(total_apps)
        for count, item in enumerate(rounds):
            element = driver.find_element(By.CSS_SELECTOR, "body > div.fixdx > div.content.row.autow > div > div.main-box.row > article:nth-child("+str(count+1)+") > div > a")
            link = element.get_attribute("href")
            download_links.append(str(link))

        # Download apps from download_links
        for count2, item in enumerate(download_links):
            print("- Download App #"+str(count2+1))
            driver.get(download_links[count2])
            time.sleep(5)
            try:
                driver.find_element(By.CSS_SELECTOR, '#DAPK > div > a').click()
            except Exception as E:
                pass
            time.sleep(5)

        print("3 - Finish downloading "+str(total_apps))
        driver.close()

  #------------------------------------------
    # 14 - Apkdone.com downloader
    elif index_of_choice == 13:
      #Get total number of apps

        total_apps = len(driver.find_elements(By.CSS_SELECTOR, "body > main > div > div > div.column.is-9 > div.columns.is-multiline > a"))
        print("1 - Total number of apps = "+str(total_apps))
        total_pages = driver.find_element(By.CSS_SELECTOR, 'body > main > div > div > div.column.is-9 > ul > li:nth-child(4) > a').text
        print("2 - Total number of pages = "+str(total_pages))

        # Insert hrefs into download_links
        download_links = []
        print("2 - Insert links into array")
        rounds = ["x"] * int(total_pages)
        round2 = ["x"] * int(total_apps)
        for count, item in enumerate(rounds):
            new_page = chosen_search_url.replace("page/1",("page/"+str(count+1)))
            driver.get(new_page)
            for count2, item in enumerate(round2):
                element = driver.find_element(By.CSS_SELECTOR, "body > main > div > div > div.column.is-9 > div.columns.is-multiline > a:nth-child("+str(count2+1)+")")
                link = element.get_attribute("href")
                download_links.append(str(link))
            for count3, item in enumerate(download_links):
                driver.get(download_links[count3])
                ad_check()
                driver.find_element(By.CSS_SELECTOR, "body > main > div > div > div > div > div.column.is-9 > div.desc > div.post-tab > section > div.tab1 > div.abuttons > a").click()
                time.sleep(3)
                ad_check()
                driver.find_element(By.CSS_SELECTOR, "#L3MvU2ZNbUtrcUdQQkZwNTllL2Rvd25sb2Fk").click()
                time.sleep(3)
                ad_check()
            download_links = []  # Reset array
        print("3 - Finish downloading "+str(total_apps))
        driver.close()


def ad_check():
    try:
        driver.find_element(By.CSS_SELECTOR, '#dismiss-button').click()
    except NoSuchElementException as e:
        print("- No ads")

apk_downloader()
