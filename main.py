import scrapy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/sankt-peterburg/category/divany"]

    def parse(self, response):
        divans = response.css('a.ui-GPFV8.qUioe.ProductName.ActiveProduct')
        data = []
        for divan in divans:
            try:
                name = divan.css('::text').get().strip()
                price_parent = divan.xpath('ancestor::div[contains(@class, "lsooF")]')
                price = price_parent.css('span.ui-LD-ZU.KIkOH::text').get().strip().replace(' ', '').replace('₽', '')
                price = int(price)
                url = divan.attrib['href']
                data.append([name, price, url])
            except Exception as e:
                self.logger.error(f"Ошибка при парсинге: {e}")

        # Проверка собранных данных
        if data:
            print(f"Собрано {len(data)} записей")
        else:
            print("Не удалось собрать данные")

        # Создание DataFrame и запись данных в CSV файл
        df = pd.DataFrame(data, columns=['Название', 'Цена', 'URL'])
        df.to_csv('divan_prices.csv', index=False)

        # Обработка данных
        average_price = df['Цена'].mean()
        print(f"Средняя цена на диваны: {average_price} ₽")

        # Создание DataFrame для средней цены и запись в CSV
        avg_df = pd.DataFrame([['Средняя цена', average_price, '']], columns=['Название', 'Цена', 'URL'])
        with open('divan_prices.csv', 'a', newline='', encoding='utf-8') as f:
            avg_df.to_csv(f, header=False, index=False)

        # Создание гистограммы цен и сохранение её в файл
        plt.hist(df['Цена'], bins=30, edgecolor='black')
        plt.axvline(average_price, color='r', linestyle='dashed', linewidth=1)
        min_ylim, max_ylim = plt.ylim()
        plt.text(average_price * 1.1, max_ylim * 0.9, f'Средняя цена: {average_price:.2f}₽', color='r')
        plt.title('Гистограмма цен на диваны')
        plt.xlabel('Цена (₽)')
        plt.ylabel('Количество')
        plt.savefig('divan_prices_histogram.png')  # Сохранение гистограммы
        plt.close()


# Запуск Scrapy Spider
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(DivannewparsSpider)
process.start()
