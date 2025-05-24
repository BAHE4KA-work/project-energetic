import json
import os
import re
from typing import List
from googleapiclient.discovery import build

from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
from fastapi import HTTPException
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup as bs
import requests
import h2o

from app.db.models import RawData
from app.schemas.data import DataInputScheme

h2o.init()


class AvitoScraper:
    """
    Scrapes Avito.ru for listings at a given address and determines
    if there may be a hidden legal entity based on the number of private listings.
    """
    BASE_URL = "https://www.avito.ru"

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
        )

    async def _fetch_page(self, context, url: str) -> str:
        page = await context.new_page()
        await page.goto(url, timeout=60000)
        content = await page.content()
        await page.close()
        return content

    async def get_listings_by_address(self, address: str, max_pages: int = 3) -> List[dict] | None:
        listings: List[dict] = []
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=self.headless)
            context = await browser.new_context(user_agent=self.user_agent)
            try:
                for page_num in range(1, max_pages + 1):
                    search_url = f"{self.BASE_URL}/rossiya?p={page_num}&q={address}"
                    html = await self._fetch_page(context, search_url)
                    soup = bs(html, 'html.parser')
                    items = soup.select('div.js-catalog-item')
                    if not items:
                        break
                    for item in items:
                        title_tag = item.select_one('a[itemprop=name]')
                        price_tag = item.select_one('meta[itemprop=price]')
                        seller_type_tag = item.select_one('div.iva-item-body-NPl6W span._2xu9P')
                        link = title_tag['href'] if title_tag else None
                        listings.append({
                            'title': title_tag.get_text(strip=True) if title_tag else '',
                            'price': price_tag['content'] if price_tag else '',
                            'seller_type': seller_type_tag.get_text(strip=True) if seller_type_tag else '',
                            'link': self.BASE_URL + link if link else None
                        })
            finally:
                await context.close()
                await browser.close()
        return listings


def analyze_hidden_entity(listings: List[dict], threshold: int = 5) -> bool:
    private_count = sum(1 for l in listings if re.search(r'Частное', l.get('seller_type', ''), re.IGNORECASE))
    return private_count >= threshold


async def casual_pars_check(address: str) -> bool:
    """
    Проверяет адрес на наличие скрытой коммерческой деятельности через Avito.
    """
    scraper = AvitoScraper(headless=True)
    try:
        listings = await scraper.get_listings_by_address(address)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Ошибка при получении данных с Avito: {e}")

    return analyze_hidden_entity(listings)


async def ya_p_search_selenium(query: str, max_results=5, region=35):
    # Настройка опций Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # без окна браузера
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--lang=ru-RU')

    # Укажите путь к chromedriver, если он не в PATH
    service = Service()  # если нужно, укажите путь: Service('/path/to/chromedriver')

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        encoded_query = quote(query.replace(" ", "+"), safe='')
        url = f'https://ya.ru/search/?text={encoded_query}&lr={region}'

        driver.get(url)

        # Яндекс может подгружать результаты динамически, подождём, пока появятся заголовки
        wait = WebDriverWait(driver, 10)
        h2_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h2.organic__title')))

        titles = []
        for h2 in h2_elements:
            a_tag = h2.find_element(By.TAG_NAME, 'a')
            if a_tag:
                title_text = a_tag.text.strip()
                if title_text:
                    titles.append(title_text)
            if len(titles) >= max_results:
                break

        return titles
    finally:
        driver.quit()
        return None


async def google_search(quest: str):
    service = build('customsearch', 'v1', developerKey='AIzaSyDTtC4MOkMe_h-oGIF1EckW3PhcaMP7v8c')
    res = service.cse().list(q=quest, cx='93252ec01c6ee4161', lr='lang_ru', num=5).execute()
    return [r['title'] for r in res['items']]


async def ya_p_search(quest: str):
    query = quote(quest.replace(" ", "+"), safe='')

    url = f'https://ya.ru/search/?text={query}&lr=35'

    cookies = {
        'is_gdpr': '0',
        'is_gdpr_b': 'CKKpXBDmtwIoAg==',
        'yashr': '4082440901743276026',
        'receive-cookie-deprecation': '1',
        'my': 'YwA=',
        'font_loaded': 'YSv1',
        'yandex_login': '',
        'yandexuid': '5636673711742829353',
        'yandex_csyr': '1748077540',
        'mda2_beacon': '1748077540388',
        'yandex_gid': '35',
        'i': '9VXB6IsV43N8M9wV4SXBjAQ8OY8YlL8xG5cREdhEzdvznrGr9fVK3aD/AAKrrKdN50N3xWhO9qDPIQ7l2qiwYmtR0kA=',
        'bltsr': '1',
        'bh': 'EigiTm90P0FfQnJhbmQiO3Y9Ijk5IiwgIkNocm9taXVtIjt2PSIxMzAiGgUieDg2IiIQIjEzMC4wLjY3MjMuMTc0IioCPzAyAiIiOgkiV2luZG93cyJCCCIxNS4wLjAiSgQiNjQiUjkiTm90P0FfQnJhbmQiO3Y9Ijk5LjAuMC4wIiwgIkNocm9taXVtIjt2PSIxMzAuMC42NzIzLjE3NCJaAj8wYPGIx8EGah7cyuH/CJLYobEDn8/h6gP7+vDnDev//fYPp8jMhwg=',
        '_yasc': '8ZH0o0NQ7pQjMFctO1C7b+mib+1o/6Tgi68n5PTxsRM1pHXdW3w89OL6T+87c7b0WZBHCm55euCb',
        'ys': 'wprid.1748092030562002-17675389868124583806-balancer-l7leveler-kubr-yp-sas-261-BAL#c_chck.1501037105',
        'yp': '1763845545.szm.1%3A1366x768%3A1349x679%3A17#1750669540.ygu.1#2063452032.pcs.1#1748941548.dlp.1#1779628022.swntab.0#1750755949.hdrc.0',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-language': 'yaabxhr=mvYXcxSML5xs-Z7pOMFwdg==',
        'content-type': 'application/json',
        # 'cookie': 'is_gdpr=0; is_gdpr_b=CKKpXBDmtwIoAg==; yashr=4082440901743276026; receive-cookie-deprecation=1; my=YwA=; font_loaded=YSv1; yandex_login=; yandexuid=5636673711742829353; yandex_csyr=1748077540; mda2_beacon=1748077540388; yandex_gid=35; i=9VXB6IsV43N8M9wV4SXBjAQ8OY8YlL8xG5cREdhEzdvznrGr9fVK3aD/AAKrrKdN50N3xWhO9qDPIQ7l2qiwYmtR0kA=; bltsr=1; bh=EigiTm90P0FfQnJhbmQiO3Y9Ijk5IiwgIkNocm9taXVtIjt2PSIxMzAiGgUieDg2IiIQIjEzMC4wLjY3MjMuMTc0IioCPzAyAiIiOgkiV2luZG93cyJCCCIxNS4wLjAiSgQiNjQiUjkiTm90P0FfQnJhbmQiO3Y9Ijk5LjAuMC4wIiwgIkNocm9taXVtIjt2PSIxMzAuMC42NzIzLjE3NCJaAj8wYPGIx8EGah7cyuH/CJLYobEDn8/h6gP7+vDnDev//fYPp8jMhwg=; _yasc=8ZH0o0NQ7pQjMFctO1C7b+mib+1o/6Tgi68n5PTxsRM1pHXdW3w89OL6T+87c7b0WZBHCm55euCb; ys=wprid.1748092030562002-17675389868124583806-balancer-l7leveler-kubr-yp-sas-261-BAL#c_chck.1501037105; yp=1763845545.szm.1%3A1366x768%3A1349x679%3A17#1750669540.ygu.1#2063452032.pcs.1#1748941548.dlp.1#1779628022.swntab.0#1750755949.hdrc.0',
        'device-memory': '8',
        'dnt': '1',
        'downlink': '3.85',
        'dpr': '1',
        'ect': '4g',
        'origin': 'https://ya.ru',
        'priority': 'u=1, i',
        'referer': 'https://ya.ru/search/?text=%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D0%BA%D1%80%D0%B0%D0%B9%2C+%D1%80-%D0%BD+%D0%A2%D0%B1%D0%B8%D0%BB%D0%B8%D1%81%D1%81%D0%BA%D0%B8%D0%B9%2C+%D1%85+%D0%95%D1%80%D0%B5%D0%BC%D0%B8%D0%BD%2C+%D1%83%D0%BB+%D0%A1%D0%B2%D0%B5%D1%82%D0%BB%D0%B0%D1%8F%2C+%D0%B4.+194&lr=35&re=1',
        'rtt': '200',
        'sec-ch-ua': '"Not?A_Brand";v="99", "Chromium";v="130"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"130.0.6723.174"',
        'sec-ch-ua-full-version-list': '"Not?A_Brand";v="99.0.0.0", "Chromium";v="130.0.6723.174"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-ch-viewport-width': '875',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'viewport-width': '875',
        'x-requested-with': 'XMLHttpRequest',
    }

    response = requests.get(url, cookies=cookies, headers=headers)
    response.raise_for_status()

    soup = bs(response.text, 'html.parser')

    titles = []
    for h2 in soup.find_all('h2', class_='organic__title'):
        a_tag = h2.find('a', href=True)
        if a_tag:
            titles.append(a_tag.get_text(strip=True))
        if len(titles) >= 5:
            break

    return list(titles)


async def neuro_pars_check(address):
    try:
        titles = await google_search(address)
    except Exception as e:
        print(e)
        return None

    if titles is None:
        return None

    url = "http://localhost:5242/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }

    system_prompt = (
        "You get list of website titles from a search result for an address.\n\n"
        "Task: decide if there is clear commercial activity at this address.\n\n"
        "Rules:\n"
        "- Answer true only if titles mention clear business indicators like hotel, store, restaurant, office, company, or service.\n"
        "- Do reasoning in Russian"
        "- Do NOT answer true just because titles contain street names, addresses, or general location info without business hints.\n\n"
        "Respond ONLY in JSON:\n\n"
        "{\n"
        "  \"commercial_activity\": true or false,\n"
        "  \"reasoning\": \"short explanation based on titles\"\n"
        "}\n\n"
        "Examples:\n\n"
        "Input:\n"
        "[\n"
        "  \"Hotel Triera in Vityazevo, Krasnodar Krai\",\n"
        "  \"Отель Триера на карте Витязево\",\n"
        "  \"Отель 'Триера' - Витязево, пр-д Летний 2А\",\n"
        "  \"Отель Триера — отзывы и бронирование\",\n"
        "  \"Витязево, Летний проезд 2А — карта\"\n"
        "]\n\n"
        "Output:\n"
        "{\n"
        "  \"commercial_activity\": true,\n"
        "  \"reasoning\": \"Multiple titles mention 'Hotel Triera', indicating a hotel business at this address.\"\n"
        "}\n\n"
        "Input:\n"
        "[\n"
        "  \"Primorskaya Street, 16A on the map of Krasnodar Krai\",\n"
        "  \"Primorskaya St, 16A, Krylovskaya village — 2GIS\",\n"
        "  \"Primorskaya Street, 16A, Krylovskaya\",\n"
        "  \"Krylovsky district, Krasnodar Krai\",\n"
        "  \"Map and location info\"\n"
        "]\n\n"
        "Output:\n"
        "{\n"
        "  \"commercial_activity\": false,\n"
        "  \"reasoning\": \"Titles contain only street names and general location info without any mention of business or commercial activity.\"\n"
        "}"
    )

    # Формируем пользовательский промпт под конкретный запрос и заголовки
    user_prompt = f"Query: {address}\n" \
                  f"1. {titles[0]}\n" \
                  f"2. {titles[1]}\n" \
                  f"3. {titles[2]}\n" \
                  f"4. {titles[3]}\n" \
                  f"5. {titles[4]}"

    data = {
        "model": "gemma-2-2b-it",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.25,
        "max_tokens": -1,
        "stream": False,
        "response_schema": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "CommercialActivityDetection",
            "type": "object",
            "properties": {
                "commercial_activity": {
                    "type": "boolean",
                    "description": "True if commercial activity is detected, false otherwise"
                },
                "reasoning": {
                    "type": "string",
                    "description": "Short explanation based on the input titles ONLY IN RUSSIAN lang"
                }
            },
            "required": ["commercial_activity", "reasoning"],
            "additionalProperties": False
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    try:
        return json.loads(json.loads(response.content.decode())['choices'][0]['message']['content'])
    except Exception as e:
        return None

async def case_check(data: RawData):
    cons: dict = json.loads(data.consumption)
    count: int = 0
    for key, arg in cons.items():
        if key in [1, 2, 3, 4, 10, 11, 12] and arg >= 3000:
            count += 1
    return count


async def neuro_check(data: RawData):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
    model_path = os.path.join(project_root, "h2o_models", "StackedEnsemble_Best1000_1_AutoML_1_20250524_05956")

    model = h2o.load_model(model_path)

    data = DataInputScheme(**data.__dict__)
    data_dict = data.__dict__.copy()

    if 'residents_count' in data_dict:
        data_dict['residentsCount'] = data_dict.pop('residents_count')

    if 'consumption' in data_dict and isinstance(data_dict['consumption'], str):
        data_dict['consumption'] = data_dict['consumption'].replace("'", '"')

    # Создаём DataFrame с единственной строкой
    df = pd.DataFrame([data_dict])

    numeric_cols = ['residentsCount', 'roomsCount', 'totalArea', 'accountId']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    h2o_df = h2o.H2OFrame(df)

    prediction = model.predict(h2o_df)
    pred_df = prediction.as_data_frame()
    prob_true = pred_df.loc[0, 'TRUE']

    return prob_true


async def do_plural_check(our_cr: int, data: RawData):
    address = data.address
    try:
        case_cr = await case_check(data)
    except:
        case_cr = None

    try:
        neuro_cr = await neuro_check(data)
    except:
        neuro_cr = None

    try:
        neuro_pars_cr = await neuro_pars_check(address)
    except:
        neuro_pars_cr = None

    try:
        casual_pars_cr = await casual_pars_check(address)
    except:
        casual_pars_cr = None

    conditions = [int(our_cr), neuro_cr if neuro_cr else False]
    if case_cr >= 4:
        conditions.append(1)
    if neuro_pars_cr['commertial_activty']:
        conditions.append(1)
    if casual_pars_cr:
        conditions.append(1)

    return True if sum(conditions)/len(conditions) >= 3.5 else False
