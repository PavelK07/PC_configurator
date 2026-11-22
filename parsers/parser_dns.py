# parser
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time
from bs4 import BeautifulSoup

'''browser_connection подключение к браузеру'''
def browser_connection():
  options = uc.ChromeOptions()
  options.page_load_strategy = "eager"

  options.add_argument("--window-size=1920,1080")
  options.add_argument("--blink-settings=imagesEnabled=false")
  options.add_argument("--disable-extensions")

  driver = uc.Chrome(options=options, version_main=157)
  driver.set_page_load_timeout(25)
  return driver

def parse_product_characteristics(URL, driver):
  driver.get(URL)
  try:
    button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.product-characteristics__expand")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
    button.click()
  except Exception:
    pass

  soup = BeautifulSoup(driver.page_source, "html.parser")

  specs = {}
  titles = soup.select(".product-characteristics__spec-title")
  values = soup.select(".product-characteristics__spec-value")

  for title, value in zip(titles, values):
    key = title.get_text(strip=True)
    val = value.get_text(strip=True)
    if key:
      specs[key] = val

  return specs


'''collecting_product_card_links возвращает массив ссылок одной страницы'''
def collecting_product_card_links(html):
  all_page_links = []
  soup = BeautifulSoup(html, 'html.parser')
  containers = soup.select("div.catalog-products")
  for container in containers:
    all_page_links.extend(link_parser_single_container(container))
  return all_page_links


'''link_parser_single_container возвращает массив ссылок одного контейнера'''
def link_parser_single_container(container, base_url="https://www.dns-shop.ru"):
  cards = container.find_all(recursive=False)
  links =[]
  for card in cards:
    link = card.find("a").get("href")
    links.append(base_url + link)
  return links


'''category_link_parser возвращает массив с сылками на все товары одной категории (CPU, GPU, motheer_board...)'''
def category_link_parser(driver, base_url):
  all_category_links = []
  driver.get(base_url)
  try:
    WebDriverWait(driver, 6).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/product/']"))
    )
  except:
    print("СТРАНИЦА ПРОПУЩЕНА. Часть ссылок потеряна")
  number_of_pages = int(driver.title.split(' ')[-1]) + 1
  for page_num in range(1, number_of_pages):
    driver.get(f"{base_url}?p={page_num}")
    try:
      WebDriverWait(driver, 6).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/product/']"))
      )
    except:
      print("СТРАНИЦА ПРОПУЩЕНА. Часть ссылок потеряна")

    html_content = driver.execute_script("return document.documentElement.outerHTML")
    all_category_links.extend(collecting_product_card_links(html_content))
  return all_category_links


def webDriverWait_test(driver,URL):
  driver.get(URL)

  start_time = time.time()

  try:
    WebDriverWait(driver, 6).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/product/']"))
    )
  except:
    print("СТРАНИЦА ПРОПУЩЕНА. Часть ссылок потеряна")

  end_time = time.time()
  execution_time = end_time - start_time
  return execution_time



driver = browser_connection()

try:
  start_time = time.time()

  #ТЕСТ ПАРСИНГА КАРТОЧКИ
  specs = parse_product_characteristics("https://www.dns-shop.ru/product/6d7a8c58afebed20/processor-amd-ryzen-5-5600-oem/", driver)
  print(f"Характеристик: {len(specs)}")
  specs = parse_product_characteristics("https://www.dns-shop.ru/product/3ecad0b7a46fed20/processor-amd-ryzen-7-7800x3d-oem/", driver)
  print(f"Характеристик: {len(specs)}")


  #ТЕСТ ССЫЛОК
  # print("Открыли DNS")
  # link_mas = category_link_parser(driver,"https://www.dns-shop.ru/catalog/17a89c5616404e77/korpusa/")
  # for i in link_mas:
  #   print(i)
  # print(len(link_mas))


  #ПОЛУЧЕНИЕ HTML
  # driver.get("https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/?p=3")
  # try:
  #   WebDriverWait(driver, 6).until(
  #     EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/product/']"))
  #   )
  # except:
  #   print("СТРАНИЦА ПРОПУЩЕНА. Часть ссылок потеряна")
  #
  # html_content = driver.execute_script("return document.documentElement.outerHTML")


  end_time = time.time()
  execution_time = end_time - start_time
  print(f"Время выполнения: {execution_time:.5f} секунд")
except Exception as e:
  print("Произошла критическая ошибка:", e)