from collections import UserDict
from datetime import datetime, timedelta

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                # Перетворюємо  на об'єкт дати
                bday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                bday_this_year = bday_date.replace(year=today.year)

                # Якщо ДН в цьому році вже минув, --> на наступний рік
                if bday_this_year < today:
                    try:
                        bday_this_year = bday_this_year.replace(year=today.year + 1)
                    except ValueError:
                        # Обробка 29 лютого для невисокосних років
                        bday_this_year = bday_this_year.replace(year=today.year + 1, day=28)
                
                days_until = (bday_this_year - today).days

                # Якщо ДН в межах наступних 7 днів (включно з сьогодні)
                if 0 <= days_until <= 7:
                    # Якщо вихідний - переносимо на понеділок
                    if bday_this_year.weekday() == 5:  # Субота
                        bday_this_year += timedelta(days=2)
                    elif bday_this_year.weekday() == 6:  # Неділя
                        bday_this_year += timedelta(days=1)
                    
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": bday_this_year.strftime("%d.%m.%Y")
                    })

        return upcoming_birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())