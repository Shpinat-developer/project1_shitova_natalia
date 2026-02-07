#импортируем нужные модули и переменные
from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event

#функция отображения инвентаря
def show_inventory(game_state: dict) -> None:

    inventory = game_state['player_inventory']
#Если инвентарь не пусой
    if inventory:
        items_list = ', '.join(inventory)
        print(f"В инвентаре: {items_list}")
    else:
        print("Инвентарь пуст.")

#ввод пользователя
def get_input(prompt: str = "> ") -> str:
 
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

#функция перемещения
def move_player(game_state: dict, direction: str) -> None:

    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]

    exits = current_room['exits']

    if direction in exits:
        new_room_name = exits[direction]

        # проверка: идём ли в treasure_room
        #if new_room_name == 'treasure_room':
        #    inventory = game_state['player_inventory']
        #    if 'treasure_key' in inventory:
        #        print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
        #        game_state['current_room'] = 'treasure_room'
        #    else:
        #        print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        #        return
        #else:
        #    
        game_state['current_room'] = new_room_name

        game_state['steps_taken'] += 1
        describe_current_room(game_state)
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

#функция взятия предмета
def take_item(game_state: dict, item_name: str) -> None:
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]

    items = room['items']

    if item_name in items:
        # если пытаются взять сундук с сокровищами
        if item_name == "treasure_chest":
            print("Вы не можете поднять сундук, он слишком тяжёлый.")
            return

        # убрать предмет из комнаты
        items.remove(item_name)
        # добавить в инвентарь игрока
        game_state['player_inventory'].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

#юзаем предметы
def use_item(game_state: dict, item_name: str) -> None:

    inventory = game_state['player_inventory']

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Вы зажгли факел. Стало светлее.")
    elif item_name == "sword":
        print("Вы сжимаете меч в руке и чувствуете уверенность.")
    elif item_name == "bronze_box":
        print("Вы открыли бронзовую шкатулку.")
        if "rusty_key" not in inventory:
            inventory.append("rusty_key")
            print("Внутри вы нашли ржавый ключ.")
        else:
            print("Но внутри пусто")
    else:
        print("Вы не знаете, как использовать этот предмет.")