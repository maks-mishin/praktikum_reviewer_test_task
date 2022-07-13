import datetime as dt

# Добавить docstring
class Record:
    # date по умолчанию должно быть None
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Слишком громоздкая конструкция, лучше развернуть в
        # обычный if-else
        self.date = (
            # т.к. работаем с датами, лучше получать текущую дату
            # через dt.date.today()
            dt.datetime.now().date() if
            # Сравнение с None лучше делать так:
            # if date is not None
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment

# Добавить docstring
class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    # Добавить docstring
    def add_record(self, record):
        self.records.append(record)

    # Добавить docstring
    def get_today_stats(self):
        today_stats = 0
        # обычные переменные принято называть строчными символами, 
        # см. PEP8 https://peps.python.org/pep-0008/#naming-conventions
        for Record in self.records:
            # т.к. работаем с датами, лучше получать текущую дату
            # через dt.date.today()
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    # Добавить docstring
    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                # Можно сделать сравнение менее громоздким, поскольку
                # python позволяет делать сравнения так: left < x < right
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats

# Добавить docstring
class CaloriesCalculator(Calculator):
    # Комментарий возле сигнатуры метода вынести в docstring метода
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Не используем бэкслеши для переноса
            # лучше обернуть вовзращаемую строку в круглые скобки
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # else уже не нужен, поскольку в блоке if есть return
        else:
            # Лишние скобки
            return('Хватит есть!')

# Добавить docstring
class CashCalculator(Calculator):
    # Числа с плавающей точкой лучше записывать как 60.0
    # так избавляемся от ненужного преобразования типов
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Добавить docstring
    # Константы незачем передавать в качестве аргументов,
    # они доступны внутри всего класса
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Мы далее присваиваем новое значение currency_type,
        # поэтому присвоим ей пустую строку в качестве начального значения
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Ненужная строка, идет сравнение без присваивания
            cash_remained == 1.00
            currency_type = 'руб'
        # Не хватает пустой строки для отделения смысловых блоков
        if cash_remained > 0:
            return (
                # Внутри f-строк не делаем никаких вычислений, только подстановку 
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Это последнее условие в блоке, лучше заменить else
        elif cash_remained < 0:
            # В if блоке используются f-строки для возврата.
            # Лучше придерживаться одного стиля и использовать их и здесь.
            # Бэкслеш - не используем для переноса
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    # Этот метод не реализует своей логики, лучше его просто убрать. 
    def get_week_stats(self):
        super().get_week_stats()
