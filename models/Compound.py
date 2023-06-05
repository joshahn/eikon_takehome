#/usr/bin/env python

class Compound:
    def __init__(self, lst):
        if len(lst) == 3:
            try:
                self.id = int(lst[0].strip())
            except:
                print("Can't convert to int: {}".format(lst[0]))
                return
            self.name = lst[1].strip()
            self.structure = lst[2].strip()
        else:
            print("Failed to extract User: {}".format(lst))

    def as_list(self):
        return [
            self.id,
            self.name,
            self.structure,
        ]

    def __str__(self):
        return "[ {}, {}, {} ]".format(self.id, self.name, self.structure)