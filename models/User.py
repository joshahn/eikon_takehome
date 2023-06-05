#/usr/bin/env python

from datetime import datetime 

class User:
    YEAR_MONTH_DAY_FORMAT = "%Y-%m-%d"

    def __init__(self, lst):
        if len(lst) == 4:
            try:
                self.id = int(lst[0].replace(',','').strip())
            except:
                print("Can't convert to int: {}".format(lst[0]))
                return
            self.name = lst[1].strip()
            self.email = lst[2].strip()
            self.signup_date = datetime.strptime(lst[3].strip(), self.YEAR_MONTH_DAY_FORMAT)
        else:
            print("Failed to extract User: {}".format(lst))

    def as_list(self):
        return [
            self.id,
            self.name,
            self.email,
            datetime.strftime(self.signup_date, self.YEAR_MONTH_DAY_FORMAT)
        ]

    def __str__(self):
        return "[ {}, {}, {}, {} ]".format(self.id, self.name, self.email, self.signup_date)
