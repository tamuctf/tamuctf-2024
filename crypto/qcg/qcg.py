from secrets import randbelow

class QCG:
    def __init__(self):
        self.m = randbelow(pow(2,256)-1)
        self.a = randbelow(self.m-1)
        self.b = randbelow(self.m-1)
        self.c = randbelow(self.m-1)
        self.x = randbelow(self.m-1)
    def __call__(self):
        self.x = (self.a*self.x**2+self.b*self.x+self.c) % self.m
        return self.x
qcg = QCG()

for i in range(10):
    print(qcg())

correct = True
for i in range(5):
    guess = int(input())
    if guess != qcg():
        correct = False
if correct:
    print(open('flag.txt','r').read())
else:
    print("You failed")