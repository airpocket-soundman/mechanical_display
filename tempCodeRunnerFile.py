unit_layout = [2, 2]

class test:
    def __init__(self, unit_layout = [3, 3]):
        self.unit_layout = unit_layout
        print("self.unit_layout",self.unit_layout)
        print("unit_layout",unit_layout)



obj = test(unit_layout)

print(obj.unit_layout)