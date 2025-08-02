import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime


MONTHS = {
    "jan": "01",
    "feb": "02",
    "mar": "03",
    "apr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "aug": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12",
}


def parse_date(date_str):
    parts = date_str.split()
    day = parts[0]
    month_key = parts[1][:3].lower()
    month = MONTHS.get(month_key)
    year = parts[2]

    if month:
        formatted = f"{year}-{month}-{day.zfill(2)}"
        return datetime.strptime(formatted, "%Y-%m-%d")
    return None


def get_app_data(bank, app_url):
    # Получаем HTML страницы приложения
    response = requests.get(f"https://apps.apple.com/uz/app/{app_url}")

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Ищем JSON-LD в странице для reviewCount
        script = soup.find("script", type="application/ld+json")
        review_count = 0
        if script:
            try:
                json_data = json.loads(script.string)
                # Извлекаем reviewCount
                if "aggregateRating" in json_data:
                    review_count = json_data["aggregateRating"]["reviewCount"]
                    print(f"AppStore total review count: {review_count}")
                else:
                    print("Aggregate rating data not found")
            except json.JSONDecodeError:
                print("Ошибка декодирования JSON")
        else:
            print("JSON-LD data not found")

        # Парсим гистограмму рейтингов
        histogram_data = {}
        rating_bars = soup.find_all(
            "div", class_="we-star-bar-graph__bar__foreground-bar"
        )
        update_container = soup.find("div", class_="l-row whats-new__content")

        if rating_bars:
            for idx, bar in enumerate(rating_bars, start=1):
                style_attr = bar.get("style", "")
                # Ищем значение процента в width
                width_percentage = (
                    style_attr.split("width: ")[1].replace(";", "")
                    if "width" in style_attr
                    else "0%"
                )
                percentage = float(width_percentage.replace("%", "")) / 100
                histogram_data[6 - idx] = (
                    percentage  # Преобразуем 1-5 звезды, начиная с 5 (самый верхний)
                )

            # Создание DataFrame
            ratings_data = [["total", review_count]]
            for stars, percentage in histogram_data.items():
                # count = review_count * percentage
                # ratings_data.append([stars, int(count)])  # Добавляем количество отзывов для каждого рейтинга
                ratings_data.append([stars, percentage])

            df = pd.DataFrame(ratings_data, columns=["rating", "review count"])
            df.insert(0, "bank", [bank] * df.shape[0])
            df.insert(1, "device", ["apple_mobile"] * df.shape[0])

            ratingCounts = soup.find(
                "script",
                {"type": "fastboot/shoebox", "id": "shoebox-media-api-cache-apps"},
            )
            rating_count_list = [0, 0, 0, 0, 0]
            if ratingCounts:
                script_content = ratingCounts.string.strip()
                # Пробуем распарсить JSON из строки
                try:
                    data_ = json.loads(script_content)
                    data = json.loads(data_[list(data_.keys())[0]])
                    # Достаем ratingCountList из каждого JSON
                    rating_count_list = data["d"][0]["attributes"]["userRating"][
                        "ratingCountList"
                    ]
                except json.JSONDecodeError:
                    print("Ошибка при парсинге JSON ratingCountList")
            ratingCount_df = pd.DataFrame(
                {
                    "rating": ["total", 1, 2, 3, 4, 5],
                    "rating counts": [review_count] + rating_count_list,
                }
            )
            df = df.merge(ratingCount_df, how="left", on="rating")
            update = None
            if update_container:
                time_element = soup.find("time")
                if time_element:
                    update = time_element.get_text()
            df_update = pd.DataFrame(
                data={
                    "bank": [bank],
                    "device": ["apple_mobile"],
                    "update": [parse_date(update)],
                }
            )
            return df, df_update
        else:
            print("Рейтинговая гистограмма не найдена")
            return pd.DataFrame(), pd.DataFrame()

    else:
        print(f"Failed to retrieve page: {response.status_code}")
        return pd.DataFrame(), pd.DataFrame()


# r = get_app_data('TBC UZ', 'tbc-uz-online-mobile-banking/id1450503714')
