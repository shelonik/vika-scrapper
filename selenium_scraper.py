from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from google_play_scraper import app
from datetime import datetime


MONTHS = {
    "янв": "01",
    "февр": "02",
    "мар": "03",
    "апр": "04",
    "ма": "05",
    "июн": "06",
    "июл": "07",
    "авг": "08",
    "сент": "09",
    "окт": "10",
    "ноя": "11",
    "дек": "12",
}


def parse_date(date_str):
    parts = date_str.split()
    day = parts[0]
    month_raw = parts[1]
    month = next((num for prefix, num in MONTHS.items() if prefix in month_raw), None)
    year = parts[2].replace("г.", "").strip()

    if month:
        formatted = f"{year}-{month}-{day.zfill(2)}"
        return datetime.strptime(formatted, "%Y-%m-%d")
    return None


class Main_driver:
    def __init__(self, headless: bool = True):
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")

        # Selenium Manager will locate/download the correct ChromeDriver automatically
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def get_data_by_id(self, name, app_id, tablet):
        self.driver.get(
            f"https://play.google.com/store/apps/details?id={app_id}&hl=ru&gl=Uz"
        )
        try:
            page_source_before = self.driver.page_source
            soup_before = BeautifulSoup(page_source_before, "html.parser")
            print("Исходный код страницы до нажатия кнопки получен.")

            if tablet:
                button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "formFactor_3"))
                )
                button.click()
                print("Кнопка нажата!")

                WebDriverWait(self.driver, 10).until(
                    lambda d: d.page_source != page_source_before
                )

                page_source_after = self.driver.page_source
                soup_after = BeautifulSoup(page_source_after, "html.parser")
                print("Исходный код страницы после нажатия кнопки получен.")

        except Exception as e:
            print(f"Ошибка: {e}")
            self.driver_quit()

        rating_list = []
        feedback_title_list = []
        mobile_tablet = []
        update_list = []
        update_mobile_tablet = []

        gps_result = app(app_id, lang="en", country="uz")

        rating_list.append("google_real_installs")
        feedback_title_list.append(gps_result["realInstalls"])
        mobile_tablet.append("google_mobile")

        for_cycle = [soup_before]
        if tablet:
            for_cycle = [soup_before, soup_after]

        for i, soup in enumerate(for_cycle, start=1):
            print(f"\nПарсинг страницы {i} (до/после нажатия):")
            try:
                all_divs = soup.find_all("div", class_="JzwBgb")
                update = soup.find("div", class_="xg1aie").get_text(strip=True)
                update_list.append(
                    str(update).replace("\xa0", "").replace("\u202f", " ")
                )

                if i == 1:
                    update_mobile_tablet.append("google_mobile")
                else:
                    update_mobile_tablet.append("google_tablet")

                for div in all_divs:
                    rating = div.find("div", class_="Qjdn7d").get_text(strip=True)
                    feedback_div = div.find("div", class_="RutFAf wcB8se")
                    feedback_title = feedback_div.get("title") if feedback_div else None

                    rating_list.append(int(str(rating).replace("\xa0", "")))
                    feedback_title_list.append(
                        int(str(feedback_title).replace("\xa0", ""))
                    )
                    if i == 1:
                        mobile_tablet.append("google_mobile")
                    else:
                        mobile_tablet.append("google_tablet")

                    print(
                        f"Google Play rating: {rating}, review count: {feedback_title}"
                    )
            except AttributeError as e:
                print(f"Ошибка при парсинге рейтинга: {e}")
                self.driver_quit()

        return pd.DataFrame(
            data={
                "bank": [name] * len(rating_list),
                "device": mobile_tablet,
                "rating": rating_list,
                "review count": feedback_title_list,
            }
        ), pd.DataFrame(
            data={
                "bank": [name] * len(update_list),
                "device": update_mobile_tablet,
                "update": [parse_date(date) for date in update_list],
            }
        )

    def driver_quit(self):
        self.driver.quit()
