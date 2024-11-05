import json
from datetime import datetime


class Restaurant:
    def __init__(self, name, menu, open_time, close_time):
        self.name = name
        self.menu = menu
        self.open_time = open_time
        self.close_time = close_time

    def is_open(self, current_time):
        return self.open_time <= current_time < self.close_time

    def get_menu(self):
        return self.menu


class Account:
    def __init__(self, user_id, points):
        self.user_id = user_id
        self.points = points

    def make_payment(self, amount):
        if self.points >= amount:
            self.points -= amount
            print(f"{amount}원이 결제되었습니다.")
        else:
            print("잔액이 부족합니다.")

    def reset_points(self):
        self.points = 8000  # 매일 8000원으로 리셋


class MainService:
    def __init__(self):
        self.restaurants = []
        self.accounts = []
        self.load_restaurants()
        self.load_accounts()

    def load_restaurants(self):
        # 메뉴는 JSON 형식으로 하드코딩
        menu_data = {
            "A 식당": {
                "아침": ["고등어 백반", "불고기 백반"],
                "점심": ["육개장", "순대국", "갈비탕", "수육국밥", "뼈해장국"],
                "저녁": []
            },
            "B 식당": {
                "아침": ["짜장면", "짜장밥", "짬뽕", "짬뽕밥", "볶음밥"],
                "점심": ["짜장면", "짜장밥", "짬뽕", "짬뽕밥", "볶음밥"],
                "저녁": ["양꼬치", "짜장면", "짜장밥", "짬뽕", "짬뽕밥", "볶음밥"]
            },
            "C 식당": {
                "메뉴 제공": "x"
            }
        }

        for name, menu in menu_data.items():
            if "메뉴 제공" not in menu:
                self.restaurants.append(Restaurant(name, menu, "07:00", "22:00"))
            else:
                self.restaurants.append(Restaurant(name, {}, "07:00", "22:00"))

    def load_accounts(self):
        # 초기 사용자 계정 데이터 (하드코딩)
        self.accounts.append(Account("user123", 8000))

    def user_login(self, user_id):
        for account in self.accounts:
            if account.user_id == user_id:
                print(f"{user_id}님, 환영합니다.")
                return account
        print("유효하지 않은 사용자입니다.")
        return None

    def select_restaurant(self, user_id):
        current_time = datetime.now().strftime("%H:%M")
        print("식당 목록:")
        for idx, restaurant in enumerate(self.restaurants, start=1):
            if restaurant.is_open(current_time):
                print(f"{idx}. {restaurant.name}")

        choice = int(input("식당 번호를 선택하세요: ")) - 1
        if 0 <= choice < len(self.restaurants):
            selected_restaurant = self.restaurants[choice]
            print(f"{selected_restaurant.name} 선택되었습니다.")
            self.select_menu(selected_restaurant)
        else:
            print("잘못된 선택입니다.")

    def select_menu(self, restaurant):
        print("메뉴:")
        for meal, items in restaurant.get_menu().items():
            print(f"{meal}: {', '.join(items)}")

        menu_choice = input("결제할 메뉴를 선택하세요 (예: 육개장): ")
        if menu_choice in [item for sublist in restaurant.get_menu().values() for item in sublist]:
            amount = int(input("결제할 금액을 입력하세요: "))
            return amount
        else:
            print("잘못된 메뉴 선택입니다.")

    def process_payment(self, account, amount):
        account.make_payment(amount)

    def admin_functions(self):
        # 관리자가 식당을 관리하는 기능 구현
        pass


# 예제 실행
main_service = MainService()

# 사용자 로그인
user_account = main_service.user_login("user123")
if user_account:
    main_service.select_restaurant(user_account.user_id)
