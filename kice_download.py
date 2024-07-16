from selenium import webdriver
import time, os, zipfile
from selenium.webdriver.common.by import By

res = r"C:\Users\lg\OneDrive\Desktop\-Symposion_\-Symposion_\resolutions\\"
zip = r"C:\Users\lg\OneDrive\Desktop\-Symposion_\-Symposion_\zip_tmp\\"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": res
})

print("starting chromeDriver..")
driver = webdriver.Chrome(options = chrome_options)
print("done!")

def rename(fm, to):
    try:
        os.rename(fm, to)
    except:
        print("error")
        os.remove(to)
        os.rename(fm, to)

def download(pages, title, index, file_cond, cond_txt, url_code, totr):
    for page in range(1, 1+pages):
        print(page)
        
        driver.get(f"https://www.suneung.re.kr/boardCnts/list.do?type=default&page={page}&searchStr=&m=0403&C06=&boardID={url_code}&C05=&C04=&C03=&C02=&searchType=S&C01=&s=suneung#;")
        for file_count in range(1, len(driver.find_elements(By.XPATH, totr)) +1):
            ksat = driver.find_elements(By.XPATH, totr+f"[{file_count}]/td")
            if ((ksat[index].text) == "외국어" or (ksat[index].text) == "영어") and (file_cond or ksat[2].text == cond_txt):
                for file in driver.find_elements(By.XPATH, totr + f"[{file_count}]/td[7]/a"):

                    if (file.get_attribute("title").find(".pdf") != -1 and (file.get_attribute("title").find("정답") == -1 and file.get_attribute("title").find("듣기") == -1)):
                        file.click()
                        print(file.get_attribute("title"))
                        time.sleep(1)
                        rename(res + file.get_attribute("title"), res + f"{ksat[1].text}_{title}.pdf")

                    if (file.get_attribute("title").find("문제지.zip") != -1 or file.get_attribute("title").find("영어.zip") != -1 or file.get_attribute("title").find("영역.zip") != -1):
                        file.click()
                        print(file.get_attribute("title"))
                        time.sleep(2)
                        zipfile.ZipFile(res + (file.get_attribute("title").replace(" " , ""))).extractall(path = zip)
                        rename(zip + [i for i in os.listdir(zip) if int(os.path.getsize(zip + i)) > 1024**2][0], res + f"{ksat[1].text}_{title}.pdf")
                        for dir in os.listdir(zip):
                            os.remove(zip + dir)
                        os.remove(res +file.get_attribute("title").replace(" " , ""))


totr = "//*[@id='sub_container']/div[2]/form/div[2]/div[1]/table[1]/tbody/tr"
download(17, "s", 2, True, -1, 1500234, totr)
totr = "//*[@id='sub_container']/div[2]/div/div[1]/table[1]/tbody/tr"   
download(34, "6", 3, False, "6월", 1500236, totr)
download(34, "9", 3, False, "9월", 1500236, totr)