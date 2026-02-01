from labyrinth_game.constants import ROOMS
import math

def describe_current_room(game_state: dict) -> None:
    room_name = game_state['current_room']
    room = ROOMS[room_name]
    print(f"== {room_name.upper()} ==")

    # Описание комнаты
    print(room['description'])

    # Видимые предметы
    if room['items']:
        items_list = ', '.join(room['items'])
        print(f"Заметные предметы: {items_list}")
    else:
        print("Заметных предметов нет.")

    # Доступные выходы
    exits_list = ', '.join(room['exits'].keys())
    print(f"Выходы: {exits_list}")

    # Наличие загадки
    if room['puzzle'] is not None:
        print("Кажется, здесь есть загадка.")

def solve_puzzle(game_state: dict) -> None:
    """Пытается решить загадку в текущей комнате."""
    from labyrinth_game.player_actions import get_input

    room_name = game_state['current_room']
    room = ROOMS[room_name]
    puzzle = room['puzzle']

    if puzzle is None:
        print("Загадок здесь нет.")
        return

    question, answer = puzzle
    print(question)

    user_answer = get_input("Ваш ответ: ")
    normalized = user_answer.strip().lower()

    # допускаем несколько вариантов ответа
    if isinstance(answer, (list, tuple, set)):
        correct = any(normalized == str(opt).strip().lower() for opt in answer)
    else:
        correct = normalized == str(answer).strip().lower()

    if correct:
        print("Верно! Вы разгадали загадку.")
        inventory = game_state['player_inventory']

        # Награды только для нужных комнат по методичке
        if room_name == 'hall':
            if 'rusty_key' not in inventory:
                inventory.append('rusty_key')
                print("Вы находите ржавый ключ и кладёте его в инвентарь.")
        elif room_name == 'library':
            if 'sword' not in inventory:
                inventory.append('sword')
                print("Вы находите меч и кладёте его в инвентарь.")

        # загадку можно решить только один раз
        room['puzzle'] = None
    else:
        print("Неверный ответ.")
        if room_name == 'trap_room':
            print("Ловушка активируется из-за неверного ответа!")
            trigger_trap(game_state)

def attempt_open_treasure(game_state: dict) -> None:
    """Пытается открыть сундук с сокровищами и завершить игру победой."""
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    if room_name != "treasure_room":
        print("Здесь нет сокровищницы.")
        return

    # проверка ключа
    inventory = game_state["player_inventory"]
    has_key = "treasure_key" in inventory

    if has_key:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        if "treasure_chest" in room["items"]:
            room["items"].remove("treasure_chest")
        print("Вы нашли сокровища! Вы победили!")
        game_state["game_over"] = True
        return

    # ключа нет, предлагаем ввести код
    response = get_input("Сундук заперт... Ввести код? (да/нет): ")
    if response != "да":
        print("Вы отступаете от сундука.")
        return

    puzzle = room["puzzle"]
    if puzzle is None:
        print("Кода для этого сундука нет.")
        return

    question, answer = puzzle
    print(question)
    code = get_input("Введите код: ")

    if code == str(answer).lower():
        print("Код верный! Сундук открыт.")
        if "treasure_chest" in room["items"]:
            room["items"].remove("treasure_chest")
        print("Вы нашли сокровища! Вы победили!")
        game_state["game_over"] = True
    else:
        print("Неверный код. Сундук остаётся запертым.")

def show_help(commands: dict) -> None:
    """Печатает список доступных команд."""
    print("Доступные команды:")
    for cmd, desc in commands.items():
        # выравнивание имени команды до 16 символов
        print(f"{cmd:<16} - {desc}")

def pseudo_random(seed: int, modulo: int) -> int:
    """Простой псевдослучайный генератор на основе синуса."""
    x = math.sin(seed * 12.9898)  
    x = x * 43758.5453            
    frac = x - math.floor(x)      
    value = frac * modulo        
    return int(math.floor(value)) 

def trigger_trap(game_state: dict) -> None:
    """Имитация срабатывания ловушки."""
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']

    # Если инвентарь не пуст
    if inventory:
        # seed можно взять из количества сделанных шагов
        seed = game_state['steps_taken']
        index = pseudo_random(seed, len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы уронили предмет: {lost_item}")
    else:
        # Инвентарь пуст — риск «смерти»
        seed = game_state['steps_taken']
        danger = pseudo_random(seed, 10)  # число от 0 до 9

        if danger < 3:  # порог, как в задании
            print("Ловушка сработала смертельно. Вы провалились в бездну!")
            game_state['game_over'] = True
        else:
            print("Вам повезло, вы чудом удержались и выбрались.")

def random_event(game_state: dict) -> None:
    """Случайные события при перемещении игрока."""
    # 1. Решаем, будет ли вообще событие
    seed = game_state['steps_taken']
    roll = pseudo_random(seed, 10)  # число 0–9

    if roll != 0:
        return  # ничего не произошло

    # 2. Выбираем, какое именно событие
    event_type = pseudo_random(seed + 1, 3)  # 0, 1 или 2

    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    inventory = game_state['player_inventory']

    if event_type == 0:
        # Сценарий 1: находка монетки
        print("Вы замечаете на полу монетку.")
        room['items'].append('coin')
    elif event_type == 1:
        # Сценарий 2: шорох
        print("Вы слышите странный шорох в темноте.")
        if 'sword' in inventory:
            print("Вы крепче сжимаете меч — существо отступает.")
    else:
        # Сценарий 3: срабатывание ловушки
        if current_room_name == 'trap_room' and 'torch' not in inventory:
            print("Кажется, здесь может быть ловушка...")
            trigger_trap(game_state)