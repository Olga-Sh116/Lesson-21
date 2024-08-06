import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# URL сайта
url = "https://www.divan.ru/sankt-peterburg/category/divany"

# Запрос к сайту
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Парсинг данных о диванах
divans = soup.find_all('div', class_='item-idx')
data = []
for divan in divans:
    try:
        name = divan.find('div', class_='item-title').text.strip()
        price = divan.find('span', class_='price').text.strip().replace(' ', '').replace('₽', '')
        price = int(price)
        data.append([name, price])
    except Exception as e:
        print(f"Ошибка при парсинге: {e}")

# Создание DataFrame
df = pd.DataFrame(data, columns=['Название', 'Цена'])

# Запись данных в CSV файл
df.to_csv('divan_prices.csv', index=False)

# Нахождение средней цены
average_price = df['Цена'].mean()
print(f"Средняя цена на диваны: {average_price} ₽")

# Создание гистограммы цен
plt.hist(df['Цена'], bins=30, edgecolor='black')
plt.title('Гистограмма цен на диваны')
plt.xlabel('Цена (₽)')
plt.ylabel('Количество')
plt.show()

