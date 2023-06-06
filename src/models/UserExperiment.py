#/usr/bin/env python

class UserExperiment:
    def __init__(self, lst):
        if len(lst) == 4:
            try:
                self.experiment_id = int(lst[0].strip())
            except:
                print("Can't convert to int: {}".format(lst[0]))
                return
            try:
                self.user_id = int(lst[1].strip())
            except:
                print("Can't convert to int: {}".format(lst[0]))
                return
            self.experiment_compound_ids = self.convert_to_list(lst[2].strip())
            try:
                self.experiment_run_time = int(lst[3].strip())
            except:
                print("Can't convert to int: {}".format(lst[0]))
                return
        else:
            print("Failed to extract UserExperiment: {}".format(lst))

    def convert_to_list(self, compound_ids):
        ids =  compound_ids.split(";")
        c_ids = []
        for i in ids:
            try:
                c_id = int(i)
                c_ids.append(c_id)
            except:
                print("Not a valid number: {}".format(i))
        return c_ids

    def as_list(self):
        return [
            self.experiment_id,
            self.user_id,
            self.experiment_compound_ids,
            self.experiment_run_time
        ]

    def __str__(self):
        return "[ {}, {}, {}, {} ]".format(self.experiment_id, 
                                           self.user_id, 
                                           self.experiment_compound_ids, 
                                           self.experiment_run_time)