p = 6

class test:
    def __init__(self,w = 2,h = 2):
        self.p = 2
        self.width = w
        self.height = h
        print(w,h)
        self.p +=1

    def addtoW(self, a = 2):
        self.width = self.width + a
        print(self.width)


obj = test(5, 4)


print(obj.width, obj.height)
obj.addtoW()

