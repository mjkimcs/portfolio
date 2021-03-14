class Car:
    def __init__(self, name, color):
        self.name = name
        self.color = color
    def __del__(self):
        print("인스턴스를 소멸시킵니다.")
    def show_info(self):
        print("이름:", self.name, "/ 색상:", self.color)
    def set_name(self, name):
        self.name = name

class Unit: # 부모 클래스
    def __init__(self, name, power):
        self.name = name
        self.power = power
    def attack(self):
        print(self.name, "이(가) 공격을 수행합니다. [전투력:", self.power, "]")

class Monster(Unit): # 자식 클래스
    def __init__(self, name, power, type):
        self.name = name
        self.power = power
        self.type = type
    def show_info(self):
        print("몬스터 이름:", self.name, "/ 몬스터 종류:", self.type) # 부모 클래스에서는 사용 불가능

car1 = Car("테슬라", "빨간색")
car1.show_info()
del car1

car2 = Car("bmw", "파랑색")
car2.set_name("포르쉐")
print(car2.name, "을(를) 구매했습니다!")

unit1 = Unit("홍길동", 375)
unit1.attack()

monster1 = Monster("슬라임", 10, "초급")
monster1.attack()
monster1.show_info()