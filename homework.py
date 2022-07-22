import math
from typing import Dict, Type, Union

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    
     
    def get_message(self) -> str:
        """Вывод на экран сообщения о пройденной тренировке."""
        messege: Union[str, float] =  (f'Тип тренировки: {self.training_type}; '
                                      f'Длительность: {self.duration:.3f} ч.; '
                                      f'Дистанция: {self.distance:.3f} км; '
                                      f'Ср. скорость: {self.speed:.3f} км/ч; '
                                      f'Потрачено ккал: {self.calories:.3f}.')
        return messege


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
           
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float                 
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
             
               
    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_km = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance_km = self.action * self.LEN_STEP / self.M_IN_KM
        mean_speed = distance_km / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration, 
                           self.get_distance(), self.get_mean_speed(), self.get_spent_calories())
        

class Running(Training):
    """Тренировка: бег."""
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,                 
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        duration_min = self.duration * 60
        calories = ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
                    * self.weight / self.M_IN_KM * duration_min)
        return calories

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float                 
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height
       
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        duration_min = self.duration * 60
        calories = ((coeff_calorie_1 * self.weight + (self.get_mean_speed()**2 
                    // self.height) * coeff_calorie_2 * self.weight) * duration_min)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float, 
                 count_pool: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool
        
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        mean_speed = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        calories = (mean_speed + coeff_calorie_1) * coeff_calorie_2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings: Dict[str, Type[Training]] = {
        'SWM': Swimming, 
        'RUN': Running,  
        'WLK': SportsWalking
    } 

    if workout_type not in trainings:
        return print(f'Тип тренировки не найден. Доступные типы:{",".join(trainings)}')

    return trainings[workout_type](*data)
    
   

    


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
              


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)