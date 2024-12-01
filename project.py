import os
import csv


class PriceMachine():

    def __init__(self):
        self.data = []

    def load_prices(self, folder_path):
        """
        Создает словарь, который сопоставляет ключевые слова с возможными вариантами их названий в CSV-файлах.
        Перебирает все файлы в указанной папке (folder_path). Проверяет, заканчивается ли файл на .csv.
        Открывает CSV-файл, если он соответствует условиям. Использует csv.DictReader для чтения данных из файла.
        Для каждой строки в CSV-файле создает словарь data, который содержит информацию о файле. Для каждого ключа
        в key_mapping перебирает возможные варианты названий и, если один из них присутствует в строке, присваивает
        значение этому ключу. Добавляет созданный словарь data в список self.data.
        """
        key_mapping = {
            'название': ['название', 'продукт', 'товар', 'наименование'],
            'цена': ['цена', 'розница'],
            'вес': ['фасовка', 'масса', 'вес']
        }

        for file in os.listdir(folder_path):
            if file.endswith('.csv'):
                with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as csv_file:
                    csv_reader = csv.DictReader(csv_file, delimiter=',')
                    for row in csv_reader:
                        data = {'файл': file}
                        for key, possible_keys in key_mapping.items():
                            for possible_key in possible_keys:
                                if possible_key in row:
                                    data[key] = row[possible_key]
                                    break
                        self.data.append(data)

    def export_to_html(self, output_file_path=r'C:\files\output.html'):
        """
        Метод проверяет, есть ли данные в списке self.data. Если данные есть, создает HTML-файл с таблицей.
        Таблица содержит информацию о продуктах, отсортированных по возрастанию цены за килограмм,
        и выводит сообщение о создании файла.
        """
        if self.data:
            sorted_data = sorted(self.data, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write('''
                <!DOCTYPE html>
                <html lang='ru'>
                <head>
                    <meta charset='UTF-8'>
                    <title>Позиции продуктов</title>
                </head>
                <body>
                    <table>
                        <tr>
                            <th>№</th>
                            <th>Наименование</th>
                            <th>Цена</th>
                            <th>Вес</th>
                            <th>Файл</th>
                            <th>Цена за кг.</th>
                        </tr>
                ''')
                for idx, row in enumerate(sorted_data, start=1):
                    item_name = row.get('название', '')
                    price_per_kg = round(float(row.get('цена', 0)) / float(row.get('вес', 1)), 2)
                    file.write(
                        f"<tr><td>{idx}</td>"
                        f"<td>{item_name}</td>"
                        f"<td>{row.get('цена', '')}</td>"
                        f"<td>{row.get('вес', '')}</td>"
                        f"<td>{row.get('файл', '')}</td>"
                        f"<td>{price_per_kg:.1f}</td></tr>"
                    )
                file.write('''
                    </table>
                </body>
                </html>
                ''')
            print(f"HTML файл успешно создан: {output_file_path}")
        else:
            print("Нет данных для экспорта в HTML файл.")

    def find_text(self, search_query):
        """
        Создает список results, который содержит все продукты из списка self.data, где поисковый запрос search_query
        содержится в нижнем регистре в названии продукта.
        Сортирует список в порядке возрастания цены за килограмм, используя функцию sorted с функцией lambda.
        """
        results = [row for row in self.data if 'название' in row and search_query.lower() in row['название'].lower()]
        sorted_results = sorted(results, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
        return sorted_results

price_machine = PriceMachine()
price_machine.load_prices(r'C:\files')

try:
    while True:
        search_query = input("Введите фрагмент наименования товара для поиска (или 'exit' для выхода): ")

        if search_query.lower() == 'exit':
            price_machine.export_to_html()
            print("Работа завершена.")
            break

        results = price_machine.find_text(search_query)

        if results:
            sorted_results = sorted(results, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
            for idx, result in enumerate(sorted_results, 1):
                print(
                    f"{idx}. Название: {result.get('название')},"
                    f" Цена: {result.get('цена')},"
                    f" Вес: {result.get('вес')},"
                    f" Файл: {result.get('файл')},"
                    f" Цена за кг: {round(float(result.get('цена', 0)) / float(result.get('вес', 1)), 2)}")
        else:
            print("Нет результатов по вашему запросу.")
            print(f"Вы искали: {search_query}")

except Exception as e:
    print(f"Произошла ошибка: {e}")