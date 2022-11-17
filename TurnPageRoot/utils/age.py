import datetime

def ageCalc(birth_date : datetime.date):
    if birth_date is None:
        return -1
    
    today = datetime.date.today()
    try:
        birthday = birth_date.replace(year=today.year)
    except ValueError:  # Feb 29th on non-leap years
        birthday = birth_date.replace(
            year=today.year, month=birth_date.month + 1, day=1
        )
    if birthday > today:
        return today.year - birth_date.year - 1
    else:
        return today.year - birth_date.year