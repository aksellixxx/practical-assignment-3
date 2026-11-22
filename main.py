import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# Створив клас для роботи з API НБУ, щоб було по ООП
class CurrencyTracker:
    def __init__(self):
        # Базова адреса API
        self.api_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"

    # Метод для завдання 2: просто виводимо курси
    def print_rates(self):
        print("=== Завдання 2: Курси валют ===")
        # Робимо GET запит, просимо відповідь у JSON
        response = requests.get(self.api_url, params={'json': 'true'})

        # Перевіряємо, чи все ок з запитом
        if response.status_code == 200:
            data = response.json()
            # Пройдемось по списку і знайдемо потрібні нам валюти
            for item in data:
                if item['cc'] in ['USD', 'EUR', 'PLN']:
                    print(f"{item['cc']}: {item['rate']} грн")
        else:
            print("Помилка запиту, сервер НБУ не відповідає")

    # Метод для завдання 3: будуємо графік за тиждень
    def build_week_chart(self):
        print("\n=== Завдання 3: Графік курсу USD ===")
        dates = []
        rates = []
        today = datetime.now()

        # Циклом збираємо дані за 7 днів
        for i in range(7):
            day = today - timedelta(days=i)
            # Форматуємо дату як треба для API (РРРРММДД)
            date_str = day.strftime('%Y%m%d')

            # Запит конкретно по долару на цю дату
            req = requests.get(self.api_url, params={'valcode': 'USD', 'date': date_str, 'json': 'true'})
            json_data = req.json()

            if json_data:
                dates.append(day.strftime('%d.%m'))
                rates.append(json_data[0]['rate'])

        # Оскільки ми йшли від сьогодні назад, треба перевернути списки для графіка
        dates.reverse()
        rates.reverse()

        # Налаштовуємо вікно графіка
        plt.figure(figsize=(9, 5))
        plt.plot(dates, rates, marker='o', color='green', linewidth=2)

        plt.title("Зміна курсу Долара США за останній тиждень")
        plt.xlabel("Дата")
        plt.ylabel("Вартість в гривнях")
        plt.grid(True, linestyle='--')

        # Показуємо результат
        plt.show()


# Точка входу в програму
if __name__ == "__main__":
    # Створюємо об'єкт нашого класу
    tracker = CurrencyTracker()

    # Викликаємо методи
    tracker.print_rates()
    tracker.build_week_chart()
