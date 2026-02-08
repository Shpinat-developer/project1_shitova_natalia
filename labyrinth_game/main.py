#!/usr/bin/env python3

#мпортируем необходимые модули и переменные
from labyrinth_game.constants import COMMANDS
from labyrinth_game.utils import describe_current_room, solve_puzzle, attempt_open_treasure, show_help
from labyrinth_game.player_actions import show_inventory, get_input, move_player, take_item, use_item

#текущее состояние игрока
game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
  }

#приветствие
def main() -> None:
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = get_input("\nВведите команду: ")
        process_command(game_state, command)

#текущая команда
def process_command(game_state: dict, command: str) -> None:
    parts = command.split(maxsplit=1)
    if not parts:
        print("Введите команду.")
        return
    action = parts[0]
    argument = parts[1] if len(parts) > 1 else ""
    # однословные направления без "go"
    direction_commands = {"north", "south", "east", "west"}
    if action in direction_commands:
        move_player(game_state, action)
        return
    match action:
        case "look":
            describe_current_room(game_state)
        case "go":
            if argument:
                move_player(game_state, argument)
            else:
                print("Укажите направление (например, 'go north').")
        case "take":
            if argument:
                take_item(game_state, argument)
            else:
                print("Укажите предмет, который хотите взять.")
        case "use":
            if argument:
                use_item(game_state, argument)
            else:
                print("Укажите предмет, который хотите использовать.")
        case "solve":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "help":
            show_help(COMMANDS)	
        case "inventory":
            show_inventory(game_state)
        case "help":
            show_help()
        case "quit" | "exit":
            print("Игра окончена.")
            game_state["game_over"] = True
        case _:
            print("Неизвестная команда.")




if __name__ == "__main__":
    main()
