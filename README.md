1. Описание проекта:

Adventure игра "Лабиринт сокровищ": игрок блуждает по комнатам, собирает артефакты в инвентарь, разгадывает ребусы и охотится за главным призом, избегая ловушек

2. Установка poetry (если он еще не установлен):

откройте терминал или PowerShell в Windows и выполните:  

sudo apt install python3-poetry
poetry config virtualenvs.in-project true  

3. Установите зависимости проекта (в корневой дериктории):

откройте терминал или PowerShell в Windows и выполните: 
poetry install

3. Зауск игры

Открой терминал или PowerShell в Windows и выполните в корневой дериктории проекта: 
poetry run python -m labyrinth_game.main

Если возникли сложности с запуском, можно попробоватьэквивалентную программу: 
py -m poetry run python -m labyrinth_game.main


