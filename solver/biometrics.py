import random

class Biometrics:
    def __init__(self) -> None:
        self.mbio = ''
        self.last_movement = None
        self.current_x = 0
        self.current_y = 0
        self.current_time = 0
        self.length = 0

        self.set_starting_point()
        self.set_mbio()

    def set_starting_point(self) -> None:
        self.current_time = random.randint(1000, 3000)
        self.current_x, self.current_y = random.randint(100, 300), random.randint(100, 300)

        movement = [self.current_time, 0, self.current_x, self.current_y]
        self.last_movement = movement

        self.mbio += f'{self.current_time},0,{self.current_x},{self.current_y};'
        self.length += 1

    def set_mbio(self) -> None:
        max_amount_of_movements = random.randint(10, 149)
        amount_of_movements = 0

        increase_x, increase_y = random.choice([True, False]), random.choice([True, False])

        amount_of_direction_x = random.randint(1, 3) if random.random() <= 0.7 else random.randint(4, 10)
        amount_of_direction_y = random.randint(1, 3) if random.random() <= 0.7 else random.randint(4, 10)

        while amount_of_movements < max_amount_of_movements:
            self.current_time += random.randint(10, 40)

            if amount_of_direction_x == 0:
                amount_of_direction_x = random.randint(1, 5)
                increase_x = random.choice([True, False])
            
            if amount_of_direction_y == 0:
                amount_of_direction_y = random.randint(1, 5)
                increase_y = random.choice([True, False])

            if increase_x == False and self.current_x - 10 > 0:
                self.current_x -= random.randint(1, 3) if random.random() <= 0.7 else random.randint(4, 10)
            if increase_x and self.current_x + 10 < 500:
                self.current_x += random.randint(1, 3) if random.random() <= 0.7 else random.randint(4, 10)

            if increase_y == False and self.current_y - 10 > 0:
                self.current_y -= random.randint(1, 3) if random.random() <= 0.7 else random.randint(4, 10)
            if increase_y and self.current_x + 10 < 500:
                self.current_y += random.randint(1, 3) if random.random() <= 0.7 else random.randint(4, 10)

            self.mbio += f'{self.current_time},0,{self.current_x},{self.current_y};'
            
            amount_of_direction_x -= 1
            amount_of_direction_y -= 1

            amount_of_movements += 1

    def get_mbio(self) -> str:
        return self.mbio