from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event

def show_inventory(game_state: dict) -> None:
    """Печатает содержимое инвентаря игрока."""
    inventory = game_state['player_inventory']

    if inventory:
        items_list = ', '.join(inventory)
        print(f"В инвентаре: {items_list}")
    else:
        print("Инвентарь пуст.")

def get_input(prompt: str = "> ") -> str:
    """Безопасно читает команду пользователя."""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state: dict, direction: str) -> None:
    """Перемещает игрока, если выход в указанном направлении существует."""
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]

    exits = current_room['exits']

    if direction in exits:
        new_room_name = exits[direction]

        # проверка: идём ли в treasure_room
        if new_room_name == 'treasure_room':
            inventory = game_state['player_inventory']
            if 'rusty_key' in inventory:
                print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
                game_state['current_room'] = 'treasure_room'
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return
        else:
            game_state['current_room'] = new_room_name

        game_state['steps_taken'] += 1
        describe_current_room(game_state)
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state: dict, item_name: str) -> None:
    """Берёт предмет из текущей комнаты, если он там есть."""
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]

    items = room['items']

    if item_name in items:
        # убрать предмет из комнаты
        items.remove(item_name)
        # добавить в инвентарь игрока
        game_state['player_inventory'].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state: dict, item_name: str) -> None:
    """Использует предмет из инвентаря с уникальным эффектом."""
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
            print("Но внутри пусто — вы уже забрали ключ.")
    else:
        print("Вы не знаете, как использовать этот предмет.")