import time

class Card:
    def __init__(self, seria, pin, account):
        self.seria = seria
        self.__pin = pin
        self.account = account

    @property
    def pin(self):
        return self.__pin

    def check_pin(self, pin):
        return self.__pin == pin


class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance
        self.commission_rate = 0.01  # 1% komissiya
        self.history = []  # 🔹 operatsiyalar tarixi

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            self.history.append(f"+{amount} so'm qo‘shildi. Balans: {self.__balance}")
            print(f"{amount} so'm muvaffaqiyatli qo'shildi ✅")
            self.send_sms(
                f"Sizning hisobingiz {amount} so'mga to'ldirildi. "
                f"Joriy balans: {self.__balance} so'm."
            )
        else:
            print("Xato: miqdor musbat bo'lishi kerak!")

    def withdraw(self, amount):
        if amount <= 0:
            print("Xato: miqdor musbat bo'lishi kerak!")
            return

        commission = amount * self.commission_rate
        total = amount + commission

        if total <= self.__balance:
            self.__balance -= total
            self.history.append(
                f"-{amount} so'm yechildi (komissiya {commission:.2f} so'm). Balans: {self.__balance:.2f}"
            )
            print(f"{amount} so'm muvaffaqiyatli yechildi ✅")
            print(f"Xizmat haqi (1%): {commission:.2f} so'm")

            self.send_sms(
                f"Sizning hisobingizdan {amount} so'm yechildi "
                f"({commission:.2f} so'm komissiya bilan). "
                f"Qolgan balans: {self.__balance:.2f} so'm."
            )
        else:
            print("Xato: balansda mablag' yetarli emas!")

    def get_balance(self):
        return self.__balance

    def send_sms(self, message):
        """SMS yuborish (imitatsiya)"""
        print(f"\n📱 SMS ({self.owner.phone_number})")
        print(f"{message}\n")

    def show_history(self):
        print("\n📋 So‘nggi operatsiyalar tarixi:")
        if not self.history:
            print("Hozircha hech qanday operatsiya bajarilmagan.")
        else:
            for item in self.history[-5:]:  # faqat oxirgi 5 tasi
                print(" •", item)
        print()


class User:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.cards: list[Card] = []

    def add_card(self, card):
        self.cards.append(card)


class Atm:
    def __init__(self, users):
        self.users = users
        self.current_user = None
        self.current_card = None
        self.try_count = 0

    def login(self):
        name = input("Ismingizni kiriting: ")
        pin = input("PIN kodni kiriting: ")

        for user in self.users:
            if user.name == name:
                for card in user.cards:
                    if card.check_pin(pin):
                        self.current_user = user
                        self.current_card = card
                        self.try_count = 0
                        print(f"Xush kelibsiz, {user.name}!")
                        return True

        self.try_count += 1
        print("Xato: foydalanuvchi yoki PIN noto‘g‘ri!")

        if self.try_count >= 3:
            print("❌ 3 marta noto‘g‘ri PIN kiritildi. Karta bloklandi!")
            time.sleep(2)
            exit()

        return False

    def show_menu(self):
        print("\n--- 🏧 ATM Menyu ---")
        print("1. Balansni ko‘rish")
        print("2. Pul qo‘shish (deposit)")
        print("3. Pul yechish (withdraw)")
        print("4. Chiqish (logout)")
        print("5. Operatsiyalar tarixini ko‘rish")  # 🔹 yangi menyu bandi

    def run(self):
        print("Bankomat ishga tushdi 🏦\n")
        while True:
            if not self.current_user:
                if not self.login():
                    continue

            self.show_menu()
            tanlov = input("Tanlovni kiriting (1-5): ")

            if tanlov == "1":
                balans = self.current_card.account.get_balance()
                print(f"Sizning balansingiz: {balans:.2f} so'm")

            elif tanlov == "2":
                amount = int(input("Qo‘shiladigan summa: "))
                self.current_card.account.deposit(amount)

            elif tanlov == "3":
                amount = int(input("Yechiladigan summa: "))
                self.current_card.account.withdraw(amount)

            elif tanlov == "4":
                print(f"{self.current_user.name} tizimdan chiqdi 👋")
                self.current_user = None
                self.current_card = None

            elif tanlov == "5":
                self.current_card.account.show_history()

            else:
                print("Noto‘g‘ri tanlov! Iltimos, 1–5 oralig‘ida kiriting.")


# ======= Test ma'lumotlar ========
user1 = User("Ali", "+998901234567")
acc1 = Account(user1, 100000)
card1 = Card("8600 1234 5678 9876", "1111", acc1)
user1.add_card(card1)

user2 = User("Vali", "+998903456789")
acc2 = Account(user2, 50000)
card2 = Card("9860 2345 6789 1234", "2222", acc2)
user2.add_card(card2)

atm = Atm([user1, user2])
atm.run()
