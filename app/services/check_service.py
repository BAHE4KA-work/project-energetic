import json
import re
from typing import List, Optional

from fastapi import HTTPException
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup as bs
import requests

from app.db.models import RawData


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


async def ya_p_search(quest: str):
    query = quest.replace(" ", "+")
    # Формируем URL с параметрами
    url = f'https://ya.ru/search/?text={query}&lr=35'

    cookies = {
        'yandex_csyr': '1743276026:1',
        'is_gdpr': '0',
        'is_gdpr_b': 'CKKpXBDmtwIoAg==',
        'i': 'fl+8CuPNXwIwF/bnow1cuG3R5Vs+cA6G35jnZvPiBwwEuc9t6kfDSY0z8Z7Rzt3Mhnck9fGXSOGEg0Zb+B0F8imzS7I=',
        'yandexuid': '1092615151743276026',
        'yashr': '4082440901743276026',
        'receive-cookie-deprecation': '1',
        'yandex_gid': '35',
        'bh': 'EigiTm90P0FfQnJhbmQiO3Y9Ijk5IiwgIkNocm9taXVtIjt2PSIxMzAiGgUieDg2IiIQIjEzMC4wLjY3MjMuMTc0IioCPzAyAiIiOgkiV2luZG93cyJCCCIxNS4wLjAiSgQiNjQiUjkiTm90P0FfQnJhbmQiO3Y9Ijk5LjAuMC4wIiwgIkNocm9taXVtIjt2PSIxMzAuMC42NzIzLjE3NCJaAj8wYPqPob8Gah7cyuH/CJLYobEDn8/h6gP7+vDnDev//fYPp8jMhwg=',
        'my': 'YwA=',
        'bltsr': '1',
        '_yasc': 'TQ/lyyNTkqTFrpfbtmMy31P2+L5k5HVk1No5o0FOcnR6pvAnQWtSjsF8lnJDmR0W/NbXmSXuvuK+',
        'ys': 'wprid.1743276297951193-976075052604559674-balancer-l7leveler-kubr-yp-vla-133-BAL',
        'yp': '1745868026.ygu.1#1744140034.dlp.2#2058636299.pcs.1#1759044031.szm.1%3A1366x768%3A858x679%3A17#1748460297.atds.1#1745954447.hdrc.0#1774812253.swntab.0',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'referer': f'https://ya.ru/search/?text={query}&lr=35',
        'origin': 'https://ya.ru',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'dnt': '1',
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
        titles = await ya_p_search(address)
    except:
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
                    "description": "Short explanation based on the input titles"
                }
            },
            "required": ["commercial_activity", "reasoning"],
            "additionalProperties": False
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    try:
        return response.json()['commercial_activity']
    except:
        return None

async def case_check(data: RawData):
    cons: dict = json.loads(data.consumption)
    count: int = 0
    for key, arg in cons.items():
        if key in [1, 2, 3, 4, 10, 11, 12] and arg >= 3000:
            count += 1
    return count


async def do_plural_check(address: str, our_cr: int, data: RawData):
    case_cr = await case_check(data)
    neuro_pars_cr = await neuro_pars_check(address)
    casual_pars_cr = await casual_pars_check(address)

    conditions = [our_cr]
    if case_cr >= 4:
        conditions.append(1)
    if neuro_pars_cr:
        conditions.append(1)
    if casual_pars_cr:
        conditions.append(1)

    return True if sum(conditions)/len(conditions) >= 3 else False
