# Добро пожаловать!
# Проект FlexTacToe был написан 03.03.2023 в качестве задания - создать игру в консоли крестики и нолики.
# Многое в языке python мне не известно, в основном я использовал знания полученные во время курса,
# Поэтому структура может отличаться от идеальной.
#
# Меня зовут Корольков Иван, псевдоним bioRival и вы можете найти меня здесь:
# twitter - https://twitter.com/biorival
# youtube - https://www.youtube.com/channel/UCm45y1vwoy1OKPTgtCBI0TA

import time
import random


# "Очищает" консоль от предыдущих строк, но на самом деле вставляет много абзацев
def clean_screen():
    print("\n" * 30)


# Вывод главного меню. message - дополнительное сообщение, если необходимо
def menu(message=""):
    global achievements, old_achievements, money, old_money, inventory, old_inventory, lives
    global monkey_curse_omniscience, monkey_curse_immortality, loneliness

    # Вывод титров
    if cake:
        give_cake()

    # Проклятье Бессмертия. Установка отображения жизней со знаком бесконечности
    # Также обновление жизней и удаление инвентаря
    line_lives = ""
    if monkey_curse_immortality:
        lives = 667
        line_lives = "Жизни: ∞"
        inventory = []

    # Проклятье Всезнания. Игрок умирает если уровень бесконечности достигает трех
    if monkey_curse_omniscience:
        if loneliness >= 3:
            death_by_loneliness()
        else:
            message = f"Одиночество: {loneliness}." + message

    # Обработка первого раза когда игрок сыграл 3 раза с мартышкой
    if monkey_matches_played >= 3 and not ("monkeys_fate" in achievements):
        monkey_pet_or_kill()

    # Смерть игрока при получении 3 ножей в спине
    if inventory.count("knife") >= 3:
        three_knives_death()
        return

    # Создание сообщения о новых достижениях
    if achievements != old_achievements:
        message += " Открыты достижения."
        old_achievements = achievements.copy()

    # Создание сообщения о получении денег
    if money != old_money:
        if money > old_money:
            message += f" Вы заработали {money - old_money}$."
        else:
            message += f" Вы потеряли {old_money - money}$."
        old_money = money

    # Создание сообщения о новых предметах
    if inventory != old_inventory:
        message += " Получены предметы."
        old_inventory = inventory.copy()

    offset = 0  # Отвечает за выравнивание меню при разном количестве строк

    # Создание отображения количества жизней, если три, то не отображается для эффекта сюрприза
    if lives < 3:
        line_lives = "Жизни: "
        for i in range(1, lives + 1):
            line_lives += "♥"
    line_money = ""

    # Создание отображения количества денег, если ноль, то не отображается для эффекта сюрприза
    if money > 0:
        line_money = f"Деньги: {money}$"

    # Вывод меню на экран
    clean_screen()
    header()
    print(" FlexTacToe" + " " * (87 - len(line_money) - len(line_lives)) + line_money + " " + line_lives)
    print()
    print(" ОДИНОЧНАЯ ИГРА [play]")
    print(" ПОШАГОВЫЙ МУЛЬТИПЛЕЕР [versus]")
    if online_gag:
        print(" ИГРА ПО СЕТИ [online]")
        offset += 1
    if len(inventory) > 0:
        print(" ИНВЕНТАРЬ [i]")
        offset += 1
    print(" ДОСТИЖЕНИЯ [ach]")
    print(" ВЫХОД [exit]")
    print("\n" * (2 - offset))  # Отступы снизу для красоты
    print(" " + message)
    footer()

    choice = input("Введите ваш выбор: ")
    choice = choice.lower()  # Убирает заглавные буквы на всякий случай

    # Переходы в главном меню
    if choice == "play":
        play_game()
    elif choice == "versus":
        versus_game()
    elif choice == "online" and online_gag:
        online()
    elif choice == "i" and len(inventory) > 0:
        menu_inventory()
    elif choice == "ach":
        menu_achievements()
    elif choice == "exit":
        quit()
    else:
        clean_screen()
        menu("Ввели что-то неправильно, попробуйте еще раз")


# Меню -> ДОСТИЖЕНИЯ [ach]
def menu_achievements():
    global achievements, ACHIEVEMENT_LIST, O_style_start, style_end

    offset = 0  # Отвечает за выравнивание меню при разном количестве строк

    clean_screen()
    header()
    print(" " + "-=ДОСТИЖЕНИЯ=-")
    print()
    for name in ACHIEVEMENT_LIST:
        offset += 1
        if name in achievements:
            print(" " + O_style_start + ACHIEVEMENT_LIST[name] + style_end)
        else:
            print(" " + ACHIEVEMENT_LIST[name])
    print("\n" * (6 - offset))
    print(" Нажмите Enter чтобы продолжить...")
    footer()
    input("Ваш ввод: ")
    menu()


# Меню -> ИНВЕНТАРЬ [i]
def menu_inventory(message=""):
    global inventory, ITEMS

    offset = 0  # Отвечает за выравнивание меню при разном количестве строк

    clean_screen()
    header()
    print(" " + "-=ИНВЕНТАРЬ=-")
    for name in inventory:
        offset += 1
        print(" " + ITEMS[name]["name"] + " [" + name + "]")
    print(" НАЗАД [back]")
    print("\n" * (5 - offset))
    print(" " + style_error + message + style_end)
    print(" Вы можете узнать описание предмета")
    footer()
    choice = input("Ваш выбор: ")

    # Просмотр некоторых вещей запускает события, здесь их обработка
    if choice == "poster" and "poster" in inventory:
        gigachad()
        return

    if choice == "monkeys paw" and "monkeys paw" in inventory:
        monkeys_paw()
        return

    # Просмотр обычных вещей - вывод их описания
    for name in inventory:
        if choice == name:
            clean_screen()
            header()
            print(" " + ITEMS[name]["name"])
            print()
            print(" " + ITEMS[name]["description"][0])
            print(" " + ITEMS[name]["description"][1])
            print(" " + ITEMS[name]["description"][2])
            print("\n" * 3)
            print(" Нажмите Enter чтобы продолжить...")
            footer()
            input("Ваш ввод:")
            menu_inventory()
            return

    if choice == "back":
        menu()
        return
    else:
        menu_inventory("Ввели что-то неправильно. Попробуйте еще раз")


# Ставит пробелы во всех полях игры
def clean_grid():
    for x in range(1, 4):
        for y in range(1, 4):
            the_grid[y, x] = " "


# Выводит в консоль поле игры
def print_grid(
        line_top="",  # Текст над полем игры, также включает жизни и деньги
        char_face="",  # Лицо персонажей
        char_line="",  # Фразы персонажей
        line_bottom1="",  # Строка под полем игры, редко используется
        line_bottom2="",  # Предпоследняя строка, обычно для вывода ошибок
        line_bottom3="",  # Последняя строка перед footer()
        char_name="",  # Имя соперника в правом нижнем углу
        line_row1="",  # В основном используется Локи для подсказки игроку, где настоящий ход
        line_row2="",  # В основном используется Локи для подсказки игроку, где настоящий ход
        line_row3=""  # В основном используется Локи для подсказки игроку, где настоящий ход
):
    global lives, money, monkey_curse_immortality

    # Создание отображения количества жизней, если три, то не отображается для эффекта сюрприза
    line_lives = ""
    if lives < 3:
        line_lives = "Жизни: "
        for i in range(1, lives + 1):
            line_lives += "♥"
    line_money = ""

    # Проклятье Бессмертия. Особое отображение жизней
    if monkey_curse_immortality:
        lives = 667
        line_lives = "Жизни: ∞"

    # Создание отображения количества денег, если ноль, то не отображается для эффекта сюрприза
    if money > 0:
        line_money = f"Деньги: {money}$"

    # Удаление стилей для корректного пересчета длины строки в line_top чтобы правильно сдвинуть line_money и line_lives
    clean_line_top = line_top.replace(X_style_start, "")
    clean_line_top = clean_line_top.replace(O_style_start, "")
    clean_line_top = clean_line_top.replace("\x1b[0;30;44m", "")
    clean_line_top = clean_line_top.replace(style_end, "")

    header()
    print(" " + line_top + " " * (97 - len(line_money) - len(line_lives) - len(clean_line_top))
          + line_money + " " + line_lives)
    print(" " * 5 + "    1   2   3 ")
    print(" " * 5 + f"1   {the_grid[1, 1]} ◾ {the_grid[1, 2]} ◾ {the_grid[1, 3]}" + " " * 10 + line_row1)
    print(" " * 5 + "  ◾ ◾ ◾ ◾ ◾ ◾ ◾" + " " * 8 + char_face)
    print(" " * 5 + f"2   {the_grid[2, 1]} ◾ {the_grid[2, 2]} ◾ {the_grid[2, 3]}" + " " * 10 + line_row2)
    print(" " * 5 + "  ◾ ◾ ◾ ◾ ◾ ◾ ◾" + " " * 4 + char_line)
    print(" " * 5 + f"3   {the_grid[3, 1]} ◾ {the_grid[3, 2]} ◾ {the_grid[3, 3]}" + " " * 10 + line_row3)
    print(" " + line_bottom1)
    print(" " + line_bottom2)
    print(" " + line_bottom3 + " " * (98 - len(char_name) - len(line_bottom3)) + char_name)
    footer()


# Проверяет есть ли победа. Возвращает: None - нет. "X" - победа X. "0" - победа 0. "draw" - ничья
def victory_check(grid):
    #  Проверка на победу. Восемь всевозможных комбинаций
    if grid[1, 1] == grid[1, 2] == grid[1, 3] != " ":  # Проверка строк
        return grid[1, 1]
    elif grid[2, 1] == grid[2, 2] == grid[2, 3] != " ":
        return grid[2, 1]
    elif grid[3, 1] == grid[3, 2] == grid[3, 3] != " ":
        return grid[3, 1]
    elif grid[1, 1] == grid[2, 1] == grid[3, 1] != " ":  # Проверка столбцов
        return grid[1, 1]
    elif grid[1, 2] == grid[2, 2] == grid[3, 2] != " ":
        return grid[1, 2]
    elif grid[1, 3] == grid[2, 3] == grid[3, 3] != " ":
        return grid[1, 3]
    elif grid[1, 1] == grid[2, 2] == grid[3, 3] != " ":  # Проверка диагоналей
        return grid[1, 1]
    elif grid[1, 3] == grid[2, 2] == grid[3, 1] != " ":
        return grid[1, 3]

    # Проверка на ничью
    no_empty_cells = True
    for x in range(1, 4):
        for y in range(1, 4):
            if grid[y, x] == " ":
                no_empty_cells = False
    if no_empty_cells:
        return "draw"

    #  Если нет победителя или ничьи
    return None


# Начинает новую versus игру
def versus_game():
    clean_grid()  # очищает поле игры от значений
    versus_game_turn(True)  # Чей сейчас ход. X - True, 0 - False


# Обрабатывает каждый ход в versus игре. turn_owner: X - True, 0 - False, message - строка для ошибок
def versus_game_turn(turn_owner, message=""):
    global X_style_start, O_style_start, style_error, style_end

    clean_screen()
    print_grid(
        line_bottom2=style_error + message + style_end,  # Вывод ошибок, текст выделяется красным маркером
        line_bottom3="Введите число строки и столбца. Пример: 1 2 или 3х2"
    )

    if turn_owner:
        input_string = X_style_start + " Ход крестиков [X]:" + style_end + " "  # Черный
    else:
        input_string = O_style_start + " Ход ноликов [0]:" + style_end + " "  # Белый

    turn_value = input(input_string)
    turn_value = input_error_check(turn_value)  # Будет листом, если нет ошибок. С ошибками - будет сообщением об ошибке

    if not type(turn_value) is list:
        versus_game_turn(turn_owner, turn_value)
        return

    if turn_owner:
        the_grid[turn_value[0], turn_value[1]] = "X"
    else:
        the_grid[turn_value[0], turn_value[1]] = "0"

    winner = victory_check(the_grid)  # Проверка на победу
    if winner is None:
        versus_game_turn(not turn_owner)
        return
    else:
        versus_win_screen(winner)
        return


# Вывод экрана победы в versus игре; champ - победитель, возможные значения - "X", "0", "draw"
def versus_win_screen(champ):
    global X_style_start, O_style_start, style_end

    clean_screen()
    if champ == "X":
        line_top = " " * 3 + X_style_start + " Победа крестиков! " + style_end
    elif champ == "0":
        line_top = " " * 4 + O_style_start + " Победа ноликов! " + style_end
    else:
        line_top = " " * 7 + "\x1b[0;30;44m" + " Ничья! " + style_end

    print_grid(line_top=line_top,
               line_bottom2="Нажмите Enter - возврат в главное меню",
               line_bottom3="Введите repeat - для повторной игры"
               )
    where_to = input("Ввод: ").lower()

    if where_to == "repeat":
        versus_game()
    else:
        menu()


# Выводит на экран победителя
def win_screen(champ):
    global X_style_start, O_style_start, style_end, money, cake

    clean_screen()

    if champ == "X":
        line_top = " " * 3 + X_style_start + " Победа крестиков! " + style_end
    elif champ == "0":
        line_top = " " * 4 + O_style_start + " Победа ноликов! " + style_end
    else:
        line_top = " " * 7 + "\x1b[0;30;44m" + " Ничья! " + style_end

    # Определение реакций персонажей на поражение, победу и ничью
    if champ == "draw":
        ai_says = random.choice(ai_character["draw"])
        ai_face = ai_character["face"]
    elif champ == player_sign:
        ai_says = random.choice(ai_character["lost"])
        ai_character["beaten"] = True
        ai_face = ai_character["face_lost"]
    else:
        ai_says = random.choice(ai_character["won"])
        ai_face = ai_character["face_won"]

    print_grid(line_top=line_top,
               char_face=ai_face,
               char_line=ai_says,
               line_bottom3="Нажмите Enter - возврат в главное меню",
               char_name=ai_character["name"]
               )

    steroid_beat_in = time.time() - steroid_timer  # Остановка таймера для достижения ПОБЕДИ СТЕРОЙДЫ ЗА МИНУТУ

    input("Ввод: ")

    # Обработка конца игры необходимая для некоторых персонажей
    # Если Волдеморт побеждает, инициируется попытка убийства игрока
    if ai_character == REPERTOIRE["voldemort"] and ai_sign == champ:
        avada_kedavra(line_top)
        return
    # Если Локи побеждает - ударяет в спину, если игрок побеждает - игрок получает деньги
    elif ai_character == REPERTOIRE["loki"]:
        if ai_sign != champ:
            # При самом первом случае, вывести объяснение полученным деньгам
            if not REPERTOIRE["loki"]["been_robbed"]:
                clean_screen()
                header()
                print()
                print(" Вы подбираете оставленную купюру и отвязываете леску. Деньги!")
                print("\n" * 6)
                print(" Нажмите Enter чтобы продолжить...")
                footer()
                input("Ваш ввод: ")
                REPERTOIRE["loki"]["been_robbed"] = True
            # Если победа - 2-5$, Ничья - 1$
            if champ == player_sign:
                money += random.randint(2, 5)
            else:
                money += 1
        else:
            # Если побеждает Локи, добавляется нож в спине в инвентарь персонажа
            clean_screen()
            header()
            print()
            print(" В получили новый предмет: Нож в спине!")
            print("\n" * 6)
            print(" Нажмите Enter чтобы продолжить...")
            footer()
            input("Ваш ввод: ")
            inventory.append("knife")
    # Завершение достижения ПОБЕДИ СТЕРОЙДЫ ЗА МИНУТУ и подарок в качестве Мотивирующего Постера
    elif ai_character == REPERTOIRE["steroid"] and not ("poster" in inventory) and steroid_beat_in <= 60:
        clean_screen()
        header()
        print("\n" * 3)
        print(' "Бро, это было охрененно! Я никогда не видел такой скорости! Воу!"')
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print("\n" * 3)
        print(' "Бро, это было охрененно! Я никогда не видел такой скорости! Воу!"')
        print(" Стероид кладет вам в руки длинный сверток глянцевой бумаги")
        print("\n" * 2)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print("\n" * 3)
        print(' "Бро, это было охрененно! Я никогда не видел такой скорости! Воу!"')
        print(" Стероид кладет вам в руки длинный сверток глянцевой бумаги")
        print(' "Ты должен меня научить как-нибудь"')
        print("\n")
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        inventory.append("poster")
        achievements.append("gigachad")
    # Если GLaDOS проигрывает - пускаются титры
    elif ai_character == REPERTOIRE["glados"] and champ == player_sign:
        cake = True

    menu()


# Меню выбора персонажа и инициализация новой игры; message - строка для ошибок
def play_game(message=""):
    global player_sign, ai_sign, ai_character, steroid_timer, monkey_matches_played, loneliness

    # Вывод меню выбора персонажа
    clean_grid()
    clean_screen()
    header()
    print("  -=ВЫБЕРИТЕ СОПЕРНИКА=-  " + style_error + message + style_end + "\t\t\t Назад [back]")
    for key in REPERTOIRE:
        if not REPERTOIRE[key]["locked"]:
            if REPERTOIRE[key]["beaten"]:
                style = O_style_start
            else:
                style = ""
            print(" " * 3 + style + " " + REPERTOIRE[key]["name"] + " " + style_end +
                  " [" + key + "]" +
                  " (Сложность: " + REPERTOIRE[key]["difficulty"] + ")")
        elif REPERTOIRE[key] == REPERTOIRE["null"]:
            pass
        else:
            print(" " * 4 + random.choice(["X", "0"]) + random.choice(["X", "0"]) + random.choice(["X", "0"]))
    print(" Можно узнать описание персонажа введя who <имя>. Например: who monkey")
    footer()

    char_choice = input("Название персонажа: ").lower()

    if char_choice in ["back", "назад"]:
        menu()
        return

    # Вывод описания персонажа, если есть who во введенной игроком строке
    if "who" in char_choice:
        char_name = char_choice.replace(" ", "").replace("who", "")
        if char_name in REPERTOIRE:
            clean_screen()
            header()
            print(" " * 5 + REPERTOIRE[char_name]["name"])
            print()
            print(" " + REPERTOIRE[char_name]["description1"])
            print(" " + REPERTOIRE[char_name]["description2"])
            print(" " + REPERTOIRE[char_name]["description3"])
            print(" " + REPERTOIRE[char_name]["description4"])
            print(" " + REPERTOIRE[char_name]["description5"])
            print(" " + REPERTOIRE[char_name]["description6"])
            print(" " + REPERTOIRE[char_name]["description7"])
            print(" Нажмите Enter чтобы вернуться...")
            footer()
            input("Ваш ввод: ")
            play_game()
            return

    # Обработка выбора персонажа. Проверка на соответствие имени и не заблокирован ли персонаж
    # loneliness - переменная для проклятья Всезнания. Равна нулю при выборе мартышки, +1 при игре с кем либо другим
    if char_choice in ["monkey", "мартышка"] and not REPERTOIRE["monkey"]["locked"]:
        loneliness = 0
        ai_character = REPERTOIRE["monkey"]
        assign_turn_owner_random()
        monkey_matches_played += 1
        game_turn(first_turn=True, blunder_chance=ai_character["blunder_chance"])
        return
    elif char_choice in ["cook", "кулинар паня", "кулинар", "паня"] and not REPERTOIRE["cook"]["locked"]:
        loneliness += 1
        ai_character = REPERTOIRE["cook"]
        assign_turn_owner_random()
        game_turn(first_turn=True, blunder_chance=ai_character["blunder_chance"])
        return
    elif char_choice in ["shiori", "шиори", "мастер", "мастер шиори"] and not REPERTOIRE["shiori"]["locked"]:
        loneliness += 1
        ai_character = REPERTOIRE["shiori"]
        assign_turn_owner_random()
        game_turn(first_turn=True, blunder_chance=ai_character["blunder_chance"])
    elif char_choice in ["steroid", "стероид"] and not REPERTOIRE["steroid"]["locked"]:
        loneliness += 1
        ai_character = REPERTOIRE["steroid"]
        assign_turn_owner_random()
        steroid_timer = time.time()
        game_turn_steroid(first_turn=True)
    elif char_choice in ["loki", "локи"] and not REPERTOIRE["loki"]["locked"]:
        loneliness += 1
        if not REPERTOIRE["loki"]["met_player"]:
            meet_loki()
        ai_character = REPERTOIRE["loki"]
        assign_turn_owner_random()
        game_turn_loki(first_turn=True, illusion=False)
    elif char_choice in ["seer", "гадалка"] and not REPERTOIRE["seer"]["locked"]:
        pay_seer()
        loneliness += 1
        ai_character = REPERTOIRE["seer"]
        assign_turn_owner_random()
        game_turn_seer(first_turn=True,
                       key_words=random.sample(["БАРАН", "ДЕРЕВО", "ПЕРЧИК", "ЛУЖА", "ДРОВОСЕК", "ПЯТНИЦА",
                                                "ВОЛК", "ОГНЕТУШИТЕЛЬ", "ГАНГРЕНА", "ТРУБАДУР", "ТРЕНИКИ"], 3),
                       gets_glasses=True
                       )
    elif char_choice in ["graviton", "гравитон"] and not REPERTOIRE["graviton"]["locked"]:
        loneliness += 1
        ai_character = REPERTOIRE["graviton"]
        assign_turn_owner_random()
        game_turn_graviton(first_turn=True)
    elif char_choice in ["null", "обнулятор"] and not REPERTOIRE["null"]["locked"]:
        loneliness += 1
        ai_character = REPERTOIRE["null"]
        ai_sign = "0"
        player_sign = "X"
        game_turn_null(first_turn=True)
    elif char_choice in ["voldemort", "волдеморт"] and not REPERTOIRE["voldemort"]["locked"]:
        loneliness += 1
        ai_character = REPERTOIRE["voldemort"]
        assign_turn_owner_random()
        game_turn(first_turn=True, blunder_chance=ai_character["blunder_chance"])
    elif char_choice == "glados" and not REPERTOIRE["glados"]["locked"]:
        loneliness += 1
        ai_character = REPERTOIRE["glados"]
        assign_turn_owner_random()
        game_turn(first_turn=True, blunder_chance=ai_character["blunder_chance"])
    else:
        play_game(message="Ввели что-то неправильно. Попробуйте еще раз.")
        return


# Главный процесс одиночной игры, шаблон для первых трех "классических" персонажей и основа для процессов необычных
# turn_owner_X - принадлежит ли ход X? True - да, False - нет
# message - строка для вывода ошибок
# first_turn - первый ли сейчас ход? True - да, False - нет
# blunder_chance - от 0 до 100%. Возможность персонажа сделать не идеальный ход. Простыми словами - ошибку.
def game_turn(turn_owner_X=True, message="", first_turn=False, blunder_chance=100):
    global player_sign, ai_sign, X_style_start, O_style_start, style_end, achievements, REPERTOIRE

    # Сообщение об ошибке выделяется красным, создается подсказка для ввода
    line_bottom2 = style_error + message + style_end
    line_bottom3 = f"Введите номер <строки>x<столбца>, например: {random.randint(1, 3)}x{random.randint(1, 3)}"

    clean_screen()  # обновляем экран

    # Формируется сообщение для ввода и ходит ли сейчас игрок
    input_string = ""
    turn_owner_player = False
    if turn_owner_X and player_sign == "X":
        input_string = X_style_start + " Ход крестиков [X]:" + style_end + " "  # Черный
        turn_owner_player = True
    elif not turn_owner_X and player_sign == "0":
        input_string = O_style_start + " Ход ноликов [0]:" + style_end + " "  # Белый
        turn_owner_player = True

    if turn_owner_player:  # Если ходит игрок
        if first_turn:  # Если самый первый ход, то выводится приветствие
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["greet"]),
                line_bottom2=line_bottom2,
                line_bottom3=line_bottom3,
                char_name=ai_character["name"]
            )
        elif can_they_win_now(player_sign):  # Если игрок может выиграть, персонаж реагирует иначе
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["loosing"]),
                line_bottom2=line_bottom2,
                line_bottom3=line_bottom3,
                char_name=ai_character["name"]
            )
        else:
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["casual"]),
                line_bottom2=line_bottom2,
                line_bottom3=line_bottom3,
                char_name=ai_character["name"]
            )

        # Принятие ввода
        turn_value = input(input_string)

        # Если чит код для победы над GLaDOS
        if turn_value == "sv_cheats 1" and ai_character == REPERTOIRE["glados"]:
            sv_cheats_1()
            return

        # Проверка на ошибки
        turn_value = input_error_check(turn_value)
        if not type(turn_value) is list:
            game_turn(turn_owner_X, turn_value, blunder_chance=blunder_chance)
            return

        the_grid[turn_value[0], turn_value[1]] = player_sign
    else:  # Если ходит ИИ
        if first_turn:  # Если самый первый ход, то выводится приветствие
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["greet"]),
                char_name=ai_character["name"]
            )
            time.sleep(4)
        else:
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["thinking"]),
                char_name=ai_character["name"]
            )
            time.sleep(2)

        # Главная логика хода
        the_grid[get_move(ai_sign, blunder_chance)] = ai_sign

        clean_screen()
        print_grid(
            char_face=ai_character["face"],
            char_line=random.choice(ai_character["after_self"]),
            char_name=ai_character["name"]
        )
        time.sleep(2)

    # Проверка на победу
    winner = victory_check(the_grid)
    if winner is None:
        game_turn(not turn_owner_X, blunder_chance=blunder_chance)
        return
    else:
        # Открытие новых персонажей
        if winner == player_sign and ai_character == REPERTOIRE["shiori"]:
            REPERTOIRE["steroid"]["locked"] = False
        if winner == player_sign and ai_character == REPERTOIRE["voldemort"]:
            REPERTOIRE["glados"]["locked"] = False

        # Вывод победителя
        win_screen(winner)
        return


# Процесс персонажа Стероида
# time_wrong_turn - вычитает время из 10 секунд на ход, необходимо если игрок допустил ошибку
def game_turn_steroid(turn_owner_X=True, message="", first_turn=False, time_wrong_turn=0):
    global player_sign, X_style_start, O_style_start, style_end

    # Сообщение об ошибке выделяется красным, создается подсказка для ввода
    line_bottom2 = style_error + message + style_end
    line_bottom3 = f"У вас осталось {10 - time_wrong_turn} секунд на ход"

    clean_screen()  # обновляем экран

    # Формируется сообщение для ввода и ходит ли сейчас игрок
    input_string = ""
    turn_owner_player = False
    if turn_owner_X and player_sign == "X":
        input_string = X_style_start + " Ход крестиков [X]:" + style_end + " "  # Черный
        turn_owner_player = True
    elif not turn_owner_X and player_sign == "0":
        input_string = O_style_start + " Ход ноликов [0]:" + style_end + " "  # Белый
        turn_owner_player = True

    if turn_owner_player:  # Если ходит игрок
        if first_turn:  # Если самый первый ход, то выводится приветствие
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["greet"]),
                line_bottom2=line_bottom2,
                line_bottom3=line_bottom3,
                char_name=ai_character["name"]
            )
        elif can_they_win_now(player_sign):  # Если игрок может выиграть, персонаж реагирует иначе
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["loosing"]),
                line_bottom2=line_bottom2,
                line_bottom3=line_bottom3,
                char_name=ai_character["name"]
            )
        else:
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["casual"]),
                line_bottom2=line_bottom2,
                line_bottom3=line_bottom3,
                char_name=ai_character["name"]
            )

        # Принятие ввода, проверка на ошибки
        timer_on = time.time()
        turn_value = input(input_string)
        timer_off = time.time()
        time_spent = timer_off - timer_on + time_wrong_turn

        if time_spent > 10:  # Если ход занял больше 10 секунд
            clean_screen()
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["too_late"]),
                char_name=ai_character["name"],
                line_bottom2=style_error + "Время истекло" + style_end
            )
            time.sleep(2)
            summon_monkey()  # Мартышка ходит за игрока
        else:
            turn_value = input_error_check(turn_value)
            if not type(turn_value) is list:
                game_turn_steroid(turn_owner_X, message=turn_value, time_wrong_turn=round(time_spent))
                return

            the_grid[turn_value[0], turn_value[1]] = player_sign

    else:  # Если ходит ИИ
        if first_turn:  # Если самый первый ход, то выводится приветствие
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["greet"]),
                char_name=ai_character["name"]
            )
            time.sleep(4)
        else:
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["thinking"]),
                char_name=ai_character["name"]
            )
            time.sleep(2)

        # Главная логика хода
        the_grid[get_move(ai_sign, ai_character["blunder_chance"])] = ai_sign

        clean_screen()
        print_grid(
            char_face=ai_character["face"],
            char_line=random.choice(ai_character["after_self"]),
            char_name=ai_character["name"]
        )
        time.sleep(2)

    # Проверка на победу
    winner = victory_check(the_grid)
    if winner is None:
        game_turn_steroid(not turn_owner_X)
        return
    if winner == "draw":  # Если ничья - игра начинается заново
        clean_screen()
        print_grid(line_top=" " * 7 + "\x1b[0;30;44m" + " Ничья! " + style_end,
                   char_face=ai_character["face"],
                   char_line=random.choice(ai_character["draw"]),
                   char_name=ai_character["name"]
                   )
        time.sleep(3)
        clean_screen()
        print_grid(line_top=" " * 7 + "\x1b[0;30;44m" + " Ничья! " + style_end,
                   char_face=REPERTOIRE["steroid"]["face_table_flip"],
                   char_line="*Стероид опрокидывает стол*",
                   char_name=ai_character["name"]
                   )
        time.sleep(4)
        clean_grid()
        game_turn_steroid()
        return
    else:
        if winner == player_sign:
            REPERTOIRE["loki"]["locked"] = False
            REPERTOIRE["seer"]["locked"] = False
        win_screen(winner)
        return


# Процесс персонажа Локи
# illusory_grid - поле игры для вывода для глаз игрока
# real_grid - поле игры настоящее для расчета победы и ходов ИИ
# illusion - действует ли сейчас иллюзия Локи? True - да, False - нет
def game_turn_loki(illusory_grid=None, real_grid=None, turn_owner_X=True, message="", first_turn=False, illusion=False):
    global player_sign, X_style_start, O_style_start, style_end, the_grid, money, inventory

    if first_turn:
        illusory_grid = the_grid.copy()
        real_grid = the_grid.copy()

    # Сообщение об ошибке выделяется красным, создается подсказка для ввода
    line_bottom2 = style_error + message + style_end
    line_bottom3 = f"Введите номер <строки>x<столбца>, например: {random.randint(1, 3)}x{random.randint(1, 3)}"

    clean_screen()  # обновляем экран

    the_grid = real_grid.copy()

    # Формируется сообщение для ввода и ходит ли сейчас игрок
    input_string = ""
    turn_owner_player = False
    if turn_owner_X and player_sign == "X":
        input_string = X_style_start + " Ход крестиков [X]:" + style_end + " "  # Черный
        turn_owner_player = True
    elif not turn_owner_X and player_sign == "0":
        input_string = O_style_start + " Ход ноликов [0]:" + style_end + " "  # Белый
        turn_owner_player = True

    if turn_owner_player:  # Если ходит игрок
        if first_turn:  # Если самый первый ход, то выводится приветствие
            the_grid = illusory_grid.copy()
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["greet"]),
                line_bottom2=line_bottom2,
                line_bottom3=line_bottom3,
                char_name=ai_character["name"]
            )
            the_grid = real_grid.copy()
        elif can_they_win_now(player_sign):  # Если игрок может выиграть, персонаж реагирует иначе
            the_grid = illusory_grid.copy()
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["loosing"]),
                line_bottom2=line_bottom2,
                line_bottom3=line_bottom3,
                char_name=ai_character["name"]
            )
            the_grid = real_grid.copy()
        else:
            the_grid = illusory_grid.copy()
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["casual"]),
                line_bottom2=line_bottom2,
                line_bottom3=line_bottom3,
                char_name=ai_character["name"]
            )
            the_grid = real_grid.copy()

        # Принятие ввода, проверка на ошибки
        turn_value = input(input_string)
        turn_value = turn_value.replace("x", " ")  # Английская х
        turn_value = turn_value.replace("х", " ")  # Русская х
        turn_value = turn_value.split()

        if len(turn_value) != 2:  # Для исключения ошибки List Index Out of Range
            turn_value = "Неправильный ввод, попробуйте еще раз"
        elif not (turn_value[0] in ["1", "2", "3"] and turn_value[1] in ["1", "2", "3"]):
            turn_value = "Неправильный ввод, попробуйте еще раз"
        else:
            turn_value = list(map(int, turn_value))
            if illusory_grid[turn_value[0], turn_value[1]] != " " and real_grid[turn_value[0], turn_value[1]] != " ":
                turn_value = f"Ячейка {turn_value[0]}x{turn_value[1]} " \
                             f"уже занята {the_grid[turn_value[0], turn_value[1]]}, " \
                             f"попробуйте еще раз"
            elif real_grid[turn_value[0], turn_value[1]] != " " and illusory_grid[turn_value[0], turn_value[1]] == " ":
                illusory_grid = real_grid.copy()
                illusion = False
                clean_screen()
                print_grid(
                    char_face=ai_character["face_surprised"],
                    char_line=random.choice(ai_character["decoy_broken"]),
                    line_bottom2=style_error + "В нашли настоящий ход!" + style_end,
                    char_name=ai_character["name"]
                )
                the_grid = real_grid.copy()
                time.sleep(3)

                game_turn_loki(turn_owner_X=turn_owner_X, message="Иллюзия развеяна",
                               illusory_grid=illusory_grid, real_grid=real_grid, illusion=illusion)

        if not type(turn_value) is list:
            game_turn_loki(turn_owner_X=turn_owner_X, message=turn_value,
                           illusory_grid=illusory_grid, real_grid=real_grid, illusion=illusion)
            return

        illusory_grid[turn_value[0], turn_value[1]] = player_sign
        real_grid[turn_value[0], turn_value[1]] = player_sign
        the_grid = real_grid.copy()
    else:  # Если ходит ИИ
        if first_turn:  # Если самый первый ход, то выводится приветствие
            the_grid = illusory_grid.copy()
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["greet"]),
                char_name=ai_character["name"]
            )
            the_grid = real_grid.copy()
            time.sleep(4)
        else:
            the_grid = illusory_grid.copy()
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["thinking"]),
                char_name=ai_character["name"]
            )
            the_grid = real_grid.copy()
            time.sleep(2)

        # Главная логика хода
        the_grid = real_grid.copy()
        move = get_move(ai_sign, ai_character["blunder_chance"])
        empty_squares = get_empty_squares(the_grid)

        #  Создать иллюзию если есть минимум 3 пустые ячейки, иллюзия не действует, и ИИ не может победить в этом ходе

        #  Если есть очки в инвентаре, то 25% шанс не создавать иллюзию
        glasses_bonus = False
        if "glasses" in inventory:
            glasses_bonus = random.choice([True, False, False, False])

        if len(empty_squares) >= 3 and not illusion and not can_they_win_now(ai_sign) and not glasses_bonus:
            illusion = True
            real_grid[move] = ai_sign
            fake_move = move
            while move == fake_move:
                fake_move = random.choice(empty_squares)

            # Выводит на экран состояние поля игры до иллюзии
            decoy_line = random.choice(ai_character["decoy"])
            clean_screen()
            the_grid = illusory_grid.copy()
            print_grid(
                char_face=ai_character["face"],
                char_line=decoy_line,
                char_name=ai_character["name"]
            )
            the_grid = real_grid.copy()
            time.sleep(2)

            # В зависимости от положения настоящего хода, положение лица и его поворот отличаются,
            # чтобы дать игроку подсказку
            loki_row1 = ""
            loki_row2 = ""
            loki_row3 = ""

            if move[0] == 1:
                if move[1] == 1:
                    loki_row1 = REPERTOIRE["loki"]["face_left"]
                elif move[1] == 2:
                    loki_row1 = REPERTOIRE["loki"]["face_center"]
                else:
                    loki_row1 = REPERTOIRE["loki"]["face_right"]
            elif move[0] == 2:
                if move[1] == 1:
                    loki_row2 = REPERTOIRE["loki"]["face_left"]
                elif move[1] == 2:
                    loki_row2 = REPERTOIRE["loki"]["face_center"]
                else:
                    loki_row2 = REPERTOIRE["loki"]["face_right"]
            else:
                if move[1] == 1:
                    loki_row3 = REPERTOIRE["loki"]["face_left"]
                elif move[1] == 2:
                    loki_row3 = REPERTOIRE["loki"]["face_center"]
                else:
                    loki_row3 = REPERTOIRE["loki"]["face_right"]

            # Вывод момента установки отвлечения
            clean_screen()
            the_grid = illusory_grid.copy()
            print_grid(
                line_row1=loki_row1,
                line_row2=loki_row2,
                line_row3=loki_row3,
                char_line=decoy_line,
                char_name=ai_character["name"]
            )
            the_grid = real_grid.copy()
            time.sleep(3)

            illusory_grid[fake_move] = ai_sign

        # Иначе - сделать обычный ход
        else:
            real_grid[move] = ai_sign
            illusory_grid[move] = ai_sign

        clean_screen()
        the_grid = illusory_grid.copy()
        print_grid(
            char_face=ai_character["face"],
            char_line=random.choice(ai_character["after_self"]),
            char_name=ai_character["name"]
        )
        the_grid = real_grid.copy()
        time.sleep(2)

    # Проверка на победу
    winner = victory_check(the_grid)
    if winner is None:
        game_turn_loki(turn_owner_X=not turn_owner_X,
                       illusory_grid=illusory_grid, real_grid=real_grid, illusion=illusion)
        return
    else:
        win_screen(winner)
        return


# Мини-choose-your-own-adventure при первой встрече с Локи
def meet_loki():
    global inventory, REPERTOIRE
    clean_screen()
    header()
    print()
    print(" Вы гуляете по осеннему лесу наслаждаясь пением птиц и неповторимым пейзажем.")
    print("\n" * 6)
    print(" Нажмите Enter чтобы продолжить...")
    footer()
    input("Ваш ввод: ")

    clean_screen()
    header()
    print()
    print(" Вы гуляете по осеннему лесу наслаждаясь пением птиц и неповторимым пейзажем.")
    print(" Затем вы замечаете денежную купюру притаившуюся на листве прямо у вас под ногами")
    print("\n" * 5)
    print(" Нажмите Enter чтобы продолжить...")
    footer()
    input("Ваш ввод: ")

    clean_screen()
    header()
    print()
    print(" Вы гуляете по осеннему лесу наслаждаясь пением птиц и неповторимым пейзажем.")
    print(" Затем вы замечаете денежную купюру притаившуюся на листве прямо у вас под ногами")
    print()
    print(" ПОДОБРАТЬ! [pick]")
    print(" пройти [pass]")
    print("\n" * 2)
    print(" pick или pass")
    footer()
    choice = input("Ваш выбор: ")

    if choice == "pick":
        clean_screen()
        header()
        print()
        print(" Вы подбираете купюру")
        print("\n" * 6)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print()
        print(" Вы подбираете купюру")
        print(" Но она вдруг выскальзывает из ваших рук")
        print("\n" * 5)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print()
        print(" Вы подбираете купюру")
        print(" Но она вдруг выскальзывает из ваших рук")
        print(" Инстинктивно вы пытаетесь схватить купюру, как вдруг...")
        print("\n" * 4)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print()
        print(" УДАР В СПИНУ")
        print("\n" * 6)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print()
        print(' "Жадность тебя погубит" - жестокий голос')
        print("\n" * 6)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print()
        print(" Через секунду леденящая боль расползается от лопатки по всему телу")
        print("\n" * 6)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print()
        print(" Через секунду леденящая боль расползается по всему телу")
        print()
        print(" Вы получили новый предмет: Нож в Спине!")
        print("\n" * 4)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")
        inventory.append("knife")
    else:
        clean_screen()
        header()
        print()
        print(" Из-за деревьев выходит человек в рогатом шлеме")
        print("\n" * 6)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print()
        print(" Из-за деревьев выходит человек в рогатом шлеме")
        print(' "Кто тут у нас заблудился"')
        print("\n" * 5)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

    REPERTOIRE["loki"]["met_player"] = True


# Процесс персонажа Гадалка
# key_words - 3 ключевых слова необходимые для получения достижения СТАНЬ ЯСНОВИДЯЩИМ. Выбираются случайно в play_game()
# gets_glasses - получает ли очки? Необходимо для получения достижения СТАНЬ ЯСНОВИДЯЩИМ
# seances_complete - количество завершенных сеансов
# during_seance - игра прервана во время сеанса? Нужно, чтобы скрыть поле игры, но не начинать сеанс
def game_turn_seer(turn_owner_X=True, message="", first_turn=False,
                   key_words=None, gets_glasses=True, seances_complete=0, during_seance=False):
    global player_sign, X_style_start, O_style_start, style_end, inventory, achievements, monkey_curse_omniscience

    #  Функция вывода на экран отвлечения Гадалки с возвратом input от игрока
    def print_seer_babbling(
            line1="",
            line2="",
            line3="",
            line4="",
            line5="",
            prompt="",
            input_prompt="Ваше слово: ",
            input_on=True
    ):
        nonlocal message
        clean_screen()
        header()
        print(" " * 2 + "Гадалка проводит сеанс" + " " * 5 + ai_character["face"])
        print(" " * 5 + "    1   2   3 ")
        print(" " * 5 + f"1   ✧ ◾ ✧ ◾ ✧" + "\t\t" + line1)
        print(" " * 5 + "  ◾ ◾ ◾ ◾ ◾ ◾ ◾" + "\t" + line2)
        print(" " * 5 + f"2   ✧ ◾ ✴ ◾ ✧" + "\t\t" + line3)
        print(" " * 5 + "  ◾ ◾ ◾ ◾ ◾ ◾ ◾" + "\t" + line4)
        print(" " * 5 + f"3   ✧ ◾ ✧ ◾ ✧" + "\t\t" + line5)
        print()
        print(" " + style_error + message + style_end)
        print(" " + prompt + " " * (98 - len(ai_character["name"]) - len(prompt)) + ai_character["name"])
        footer()
        if input_on:
            return input(input_prompt)

    # Гадалка объявляет ключевые слова для получения достижения "ясновидения"
    if first_turn:
        print_seer_babbling(
            line1=f"Услышь мое пророчество!",
            line2=f"Я слышу звон колоколов... {key_words[0]} неминуемо приближается!",
            line3=f"И не будет пощады, и не будет спасенья, но {key_words[1]} может помочь.",
            line4=f"Это тебе и нужно купить, дорогуша, да, да, первым же делом.",
            line5=f"Найди человека по кличке {key_words[2]}, у них это точно есть.",
            prompt="Нажмите Enter чтобы продолжить...",
            input_prompt="Ваш ввод: "
        )

    # Сообщение об ошибке выделяется красным, создается подсказка для ввода
    line_bottom2 = style_error + message + style_end
    line_bottom3 = f"Введите номер <строки>x<столбца>, например: {random.randint(1, 3)}x{random.randint(1, 3)}"

    clean_screen()  # обновляем экран

    # Формируется сообщение для ввода и ходит ли сейчас игрок
    input_string = ""
    turn_owner_player = False
    if turn_owner_X and player_sign == "X":
        input_string = X_style_start + " Ход крестиков [X]:" + style_end + " "  # Черный
        turn_owner_player = True
    elif not turn_owner_X and player_sign == "0":
        input_string = O_style_start + " Ход ноликов [0]:" + style_end + " "  # Белый
        turn_owner_player = True

    if turn_owner_player:  # Если ходит игрок

        # 90% шанс начать отвлечение
        # Если у игрока есть предмет очки - шанс отвлечения снижается до 50%
        glasses_bonus = 0
        if "glasses" in inventory:
            glasses_bonus = 40
        gamble = random.randint(1, 100)

        distract = False
        if gamble <= 90 - glasses_bonus:
            distract = True

        # Если сеанс уже состоялся и игрок допустил опечатку
        if during_seance:
            print_seer_babbling(prompt=line_bottom3, input_on=False)
        # Если отвлечение должно состоятся и количество сеансов меньше 3 и не первый ход
        elif distract and seances_complete < 3 and not first_turn:
            during_seance = True
            print_grid(
                char_face=ai_character["face"],
                char_line="*Гадалка начинает сеанс*",
                char_name=ai_character["name"]
            )
            time.sleep(2)

            ignore_line = random.choice([
                "Игнорировать старших - никуда не годиться!",
                "Ничего? Что за хамство?",
                "Нет, я так не играю"
            ])

            if seances_complete == 0:
                answer = print_seer_babbling("Какой твой любимый цвет, дорогуша?").lower()

                if monkey_curse_omniscience:  # Если проклятье Всезнания в действии - запутать слова
                    caesar_cipher(answer, 1)

                if not answer.upper() == key_words[0]:
                    gets_glasses = False
                if answer == "" or len(answer) < 3:
                    print_seer_babbling(
                        ignore_line,
                        prompt="Нажмите Enter чтобы продолжить...",
                        input_prompt="Ваш ввод: "
                    )
                else:
                    seances_complete += 1
                    story_pick = random.randint(1, 2)
                    if story_pick == 1:
                        print_seer_babbling(
                            f"{answer.capitalize()}? О да, это многое говорит о человеке.",
                            f"Не многие об этом знают, но в древнем египте",
                            f"фараоны носили преимущественно {answer} цвет",
                            f"в узких кругах {answer} цвет считается цветом великих правителей!",
                            f"Да, да, дорогуша, не благодари",
                            prompt="Нажмите Enter чтобы продолжить...",
                            input_prompt="Ваш ввод: "
                        )
                    else:
                        print_seer_babbling(
                            f"Личность с любимым цветом {answer} стремиться к балансу,",
                            f"такая личность заботливая и чуткая к потребностям других людей",
                            f"Сладкая и дружелюбная природа, тех кто любит {answer}, может",
                            f"обернуться наивностью и излишней доверчивостью",
                            f"Но ведь это и не так плохо, правда ведь, дорогушечка. Хи-хи-хи",
                            prompt="Нажмите Enter чтобы продолжить...",
                            input_prompt="Ваш ввод: "
                        )
            elif seances_complete == 1:
                answer = print_seer_babbling("Какой твой знак зодиака, дорогуша?").lower()

                if monkey_curse_omniscience:  # Если проклятье Всезнания в действии - запутать слова
                    caesar_cipher(answer, 1)

                if not answer.upper() == key_words[1]:
                    gets_glasses = False
                if answer == "" or len(answer) < 3:
                    print_seer_babbling(
                        ignore_line,
                        prompt="Нажмите Enter чтобы продолжить...",
                        input_prompt="Ваш ввод: "
                    )
                else:
                    seances_complete += 1
                    story_pick = random.randint(1, 2)
                    if story_pick == 1:
                        print_seer_babbling(
                            f"О да, очень интересно...",
                            f"Сегодня {answer} будет загружен делами,",
                            f"окружающие попробуют даже сделать мою дорогушу крайней в своих вопросах!",
                            f"Изменить такое положение дел {answer} сможет, только если будет",
                            f"жестко стоять на своем",
                            prompt="Нажмите Enter чтобы продолжить...",
                            input_prompt="Ваш ввод: "
                        )
                    else:
                        print_seer_babbling(
                            f"Хмммм... я так и думала.",
                            f"Сегодня {answer} способны на радикальные меры, особенно в сфере финансов.",
                            f"Вместо того чтобы семь раз отмерить, они будут настроены семь раз отрубить!",
                            f"Есть опасность того, что {answer} необдуманно пустят деньги на ветер.",
                            f"Но нельзя пусть деньги на ветер, когда дело касается твоего будущего. Хи-хи-хи",
                            prompt="Нажмите Enter чтобы продолжить...",
                            input_prompt="Ваш ввод: "
                        )
            elif seances_complete == 2:
                answer = print_seer_babbling("Шепни на ушко имя своей тайной любви",
                                             "и я взгляну на сплетение ваших судеб").lower()

                if monkey_curse_omniscience:  # Если проклятье Всезнания в действии - запутать слова
                    caesar_cipher(answer, 1)

                if not answer.upper() == key_words[2]:
                    gets_glasses = False
                if answer == "" or len(answer) < 3:
                    print_seer_babbling(
                        ignore_line,
                        prompt="Нажмите Enter чтобы продолжить...",
                        input_prompt="Ваш ввод: "
                    )
                else:
                    seances_complete += 1
                    story_pick = random.randint(1, 2)
                    if story_pick == 1:
                        print_seer_babbling(
                            f"Очень необычно...",
                            f"На этой неделе {answer.capitalize()} имеет особую уязвимость"
                            f" к любым романтическим подходам.",
                            f"По истечении третьей четверти луны момент будет упущен,",
                            f"так что, моя дорогуша, если ты хочешь чтобы {answer.capitalize()} был твоим,",
                            f"действовать нужно решительно",
                            prompt="Нажмите Enter чтобы продолжить...",
                            input_prompt="Ваш ввод: "
                        )
                    else:
                        print_seer_babbling(
                            f"Ммм... {answer.capitalize()}? Как обворожительно...",
                            f"{answer.capitalize()} всегда неровно к тебе дышал. Да, да, дорогуша, не красней.",
                            f"Не пройдет и месяца как {answer.capitalize()} окажет тебе внимание",
                            f"О, сколько прекрасных ночей {answer.capitalize()} и ты проведете вместе",
                            f"Но у всего хорошего есть цена, и рано или поздно радость обратиться в пепел...",
                            prompt="Нажмите Enter чтобы продолжить...",
                            input_prompt="Ваш ввод: "
                        )
                if gets_glasses and seances_complete == 3 and not ("glasses" in inventory):
                    print_seer_babbling("Ооооо..., дорогуша", "Мы явно разговариваем на одном языке",
                                        prompt="Нажмите Enter чтобы продолжить...",
                                        input_prompt="Ваш ввод: ")
                    print_seer_babbling("У меня для тебя есть подарок...", "",
                                        prompt="Нажмите Enter чтобы продолжить...",
                                        input_prompt="Ваш ввод: ")
                    print_seer_babbling("У меня для тебя есть подарок...", "*Гадалка сует вам в руки что-то в чехле*",
                                        prompt="Нажмите Enter чтобы продолжить...",
                                        input_prompt="Ваш ввод: ")
                    print_seer_babbling("У меня для тебя есть подарок...", "*Гадалка сует вам в руки что-то в чехле*",
                                        "", "Вы получили новый предмет: Очки Ясновидения",
                                        prompt="Нажмите Enter чтобы продолжить...",
                                        input_prompt="Ваш ввод: ")
                    inventory.append("glasses")
                    achievements.append("glasses")
            # Вывод доски со скрытыми полями игры, игрок делает выбор по памяти
            print_seer_babbling(prompt=line_bottom3, input_on=False)
        else:
            # Вывод обычного поля игры
            if first_turn:  # Если самый первый ход, то выводится приветствие
                print_grid(
                    char_face=ai_character["face"],
                    char_line=random.choice(ai_character["greet"]),
                    line_bottom2=line_bottom2,
                    line_bottom3=line_bottom3,
                    char_name=ai_character["name"]
                )
            elif can_they_win_now(player_sign):  # Если игрок может выиграть, персонаж реагирует иначе
                print_grid(
                    char_face=ai_character["face"],
                    char_line=random.choice(ai_character["loosing"]),
                    line_bottom2=line_bottom2,
                    line_bottom3=line_bottom3,
                    char_name=ai_character["name"]
                )
            else:
                print_grid(
                    char_face=ai_character["face"],
                    char_line=random.choice(ai_character["casual"]),
                    line_bottom2=line_bottom2,
                    line_bottom3=line_bottom3,
                    char_name=ai_character["name"]
                )

        # Принятие ввода, проверка на ошибки
        turn_value = input(input_string)
        turn_value = input_error_check(turn_value)
        if not type(turn_value) is list:
            game_turn_seer(turn_owner_X, turn_value,
                           key_words=key_words, gets_glasses=gets_glasses, seances_complete=seances_complete,
                           during_seance=during_seance)
            return

        the_grid[turn_value[0], turn_value[1]] = player_sign
    else:  # Если ходит ИИ
        if first_turn:  # Если самый первый ход, то выводится приветствие
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["greet"]),
                char_name=ai_character["name"]
            )
            time.sleep(4)
        else:
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["thinking"]),
                char_name=ai_character["name"]
            )
            time.sleep(2)

        # Главная логика хода
        the_grid[get_move(ai_sign, ai_character["blunder_chance"])] = ai_sign

        clean_screen()
        print_grid(
            char_face=ai_character["face"],
            char_line=random.choice(ai_character["after_self"]),
            char_name=ai_character["name"]
        )
        time.sleep(2)

    # Проверка на победу
    winner = victory_check(the_grid)
    if winner is None:
        game_turn_seer(not turn_owner_X,
                       key_words=key_words, gets_glasses=gets_glasses, seances_complete=seances_complete)
        return
    else:
        if winner == player_sign:
            REPERTOIRE["graviton"]["locked"] = False
        win_screen(winner)
        return


# Процесс персонажа Обнулятор
# revolt - активирована ли способность revolt? True - да, False - нет
def game_turn_null(turn_owner_X=True, message="", first_turn=False, revolt=False):
    global player_sign, X_style_start, O_style_start, style_end

    # Сообщение об ошибке выделяется красным, создается подсказка для ввода
    line_bottom2 = style_error + message + style_end
    if not revolt:
        line_bottom3 = "Введя revolt - после окончания хода соперника X и 0 меняются местами"
    else:
        line_bottom3 = f"Введите номер <строки>x<столбца>, например: {random.randint(1, 3)}x{random.randint(1, 3)}"

    clean_screen()  # обновляем экран

    # Формируется сообщение для ввода и ходит ли сейчас игрок
    input_string = ""
    turn_owner_player = False
    if turn_owner_X and player_sign == "X":
        input_string = X_style_start + " Ход крестиков [X]:" + style_end + " "  # Черный
        turn_owner_player = True
    elif not turn_owner_X and player_sign == "0":
        input_string = O_style_start + " Ход ноликов [0]:" + style_end + " "  # Белый
        turn_owner_player = True

    if turn_owner_player:  # Если ходит игрок
        if first_turn:  # Если самый первый ход, то выводится приветствие
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["greet"]),
                line_bottom2=line_bottom2,
                line_bottom3=line_bottom3,
                char_name=ai_character["name"]
            )
        else:
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["casual"]),
                line_bottom2=line_bottom2,
                line_bottom3=line_bottom3,
                char_name=ai_character["name"]
            )

        # Принятие ввода, проверка на ошибки
        turn_value = input(input_string)

        # Принятие команды revolt
        if turn_value == "revolt" and not revolt:
            game_turn_null(turn_owner_X, "Переворот подготавливается", revolt=True)
            return
        elif turn_value == "revolt" and revolt:
            game_turn_null(turn_owner_X, "Переворот уже в процессе, дождитесь хода соперника", revolt=revolt)
            return

        turn_value = input_error_check(turn_value)
        if not type(turn_value) is list:
            game_turn_null(turn_owner_X, turn_value, revolt=revolt)
            return

        the_grid[turn_value[0], turn_value[1]] = player_sign

        # Обнуление
        if victory_check(the_grid) == player_sign:
            the_grid[turn_value[0], turn_value[1]] = " "
            char_line = random.choice(ai_character["nullification"])
            clean_screen()
            print_grid(
                char_face=ai_character["face"],
                char_line=char_line,
                line_bottom3="Происходит обнуление",
                char_name=ai_character["name"]
            )
            time.sleep(4)

            for x in range(1, 4):
                if the_grid[1, x] == "X":
                    the_grid[1, x] = "0"
            clean_screen()
            print_grid(
                char_face=ai_character["face"],
                char_line=char_line,
                line_bottom3="Происходит обнуление",
                char_name=ai_character["name"]
            )
            time.sleep(1)

            for x in range(1, 4):
                if the_grid[2, x] == "X":
                    the_grid[2, x] = "0"
            clean_screen()
            print_grid(
                char_face=ai_character["face"],
                char_line=char_line,
                line_bottom3="Происходит обнуление",
                char_name=ai_character["name"]
            )
            time.sleep(1)

            for x in range(1, 4):
                if the_grid[3, x] == "X":
                    the_grid[3, x] = "0"
            clean_screen()
            print_grid(
                char_face=ai_character["face"],
                char_line=char_line,
                line_bottom3="Происходит обнуление",
                char_name=ai_character["name"]
            )
            time.sleep(3)

            clean_grid()
            game_turn_null()
            return

    else:  # Если ходит ИИ
        if first_turn:  # Если самый первый ход, то выводится приветствие
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["greet"]),
                char_name=ai_character["name"]
            )
            time.sleep(4)
        else:
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["thinking"]),
                char_name=ai_character["name"]
            )
            time.sleep(2)

        # Главная логика хода
        the_grid[get_move(ai_sign, ai_character["blunder_chance"])] = ai_sign

        clean_screen()
        print_grid(
            char_face=ai_character["face"],
            char_line=random.choice(ai_character["after_self"]),
            char_name=ai_character["name"]
        )
        time.sleep(2)

    # Переворот
    if revolt and not turn_owner_player:
        for y, x in the_grid:
            if the_grid[y, x] == "X":
                the_grid[y, x] = "0"
            elif the_grid[y, x] == "0":
                the_grid[y, x] = "X"

        clean_screen()
        print_grid(
            char_face=ai_character["face_lost"],
            char_line=random.choice(ai_character["revolt"]),
            char_name=ai_character["name"]
        )
        time.sleep(3)

    # Проверка на победу
    winner = victory_check(the_grid)
    if winner is None:
        # Если после проведения переворота нет победы
        if revolt and not turn_owner_player:
            prison()
            return
        game_turn_null(not turn_owner_X, revolt=revolt)
        return
    else:
        if winner == player_sign:
            achievements.append("revolutionary")
            REPERTOIRE["voldemort"]["locked"] = False
            REPERTOIRE["null"]["locked"] = True
        win_screen(winner)
        return


# Процесс персонажа Гравитон
# gravitation_tick - отсчет ходов игроков для активации черной дыры когда достигает четырех
def game_turn_graviton(turn_owner_X=True, message="", first_turn=False, gravitation_tick=0):
    global player_sign, X_style_start, O_style_start, style_end, inventory

    # Сообщение об ошибке выделяется красным, создается подсказка для ввода
    line_bottom2 = style_error + message + style_end
    line_bottom3 = f"Введите номер <строки>x<столбца>, например: {random.randint(1, 3)}x{random.randint(1, 3)}"

    clean_screen()  # обновляем экран

    # Формируется сообщение для ввода и ходит ли сейчас игрок
    input_string = ""
    turn_owner_player = False
    if turn_owner_X and player_sign == "X":
        input_string = X_style_start + " Ход крестиков [X]:" + style_end + " "  # Черный
        turn_owner_player = True
    elif not turn_owner_X and player_sign == "0":
        input_string = O_style_start + " Ход ноликов [0]:" + style_end + " "  # Белый
        turn_owner_player = True

    if turn_owner_player:  # Если ходит игрок
        if first_turn:  # Если самый первый ход, то выводится приветствие
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["greet"]),
                line_bottom2=line_bottom2,
                line_bottom3=line_bottom3,
                char_name=ai_character["name"]
            )
        elif can_they_win_now(player_sign):  # Если игрок может выиграть, персонаж реагирует иначе
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["loosing"]),
                line_bottom2=line_bottom2,
                line_bottom3=line_bottom3,
                char_name=ai_character["name"]
            )
        else:
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["casual"]),
                line_bottom2=line_bottom2,
                line_bottom3=line_bottom3,
                char_name=ai_character["name"]
            )

        # Принятие ввода, проверка на ошибки
        turn_value = input(input_string)
        turn_value = input_error_check(turn_value)
        if not type(turn_value) is list:
            game_turn_graviton(turn_owner_X, turn_value, gravitation_tick=gravitation_tick)
            return

        the_grid[turn_value[0], turn_value[1]] = player_sign
    else:  # Если ходит ИИ
        if first_turn:  # Если самый первый ход, то выводится приветствие
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["greet"]),
                char_name=ai_character["name"]
            )
            time.sleep(4)
        else:
            print_grid(
                char_face=ai_character["face"],
                char_line=random.choice(ai_character["thinking"]),
                char_name=ai_character["name"]
            )
            time.sleep(2)

        # Главная логика хода
        the_grid[get_move(ai_sign, ai_character["blunder_chance"])] = ai_sign

        clean_screen()
        print_grid(
            char_face=ai_character["face"],
            char_line=random.choice(ai_character["after_self"]),
            char_name=ai_character["name"]
        )
        time.sleep(2)

    gravitation_tick += 1
    if gravitation_tick >= 4:
        gravitation_tick = 0
        # Ход черной дыры
        # Первичный вывод
        clean_screen()
        print_grid(
            char_face="   ◯   ",
            char_line="*Черная дыра притягивает в центр*",
            char_name="Гравитация"
        )
        time.sleep(2)

        # Центральное притяжение
        #   - X -       - - -     - 0 -       - - -
        #   X - X   ->  - X -     X - X   ->  - - -
        #   - X -       - - -     - 0 -       - - -
        center_mesh = the_grid[1, 2] + the_grid[2, 1] + the_grid[2, 3] + the_grid[3, 2]
        how_many_x = center_mesh.count('X')
        how_many_0 = center_mesh.count('0')
        if how_many_x > how_many_0:
            the_grid[2, 2] = "X"
        elif how_many_x < how_many_0:
            the_grid[2, 2] = "0"
        else:
            the_grid[2, 2] = " "
        the_grid[1, 2] = " "
        the_grid[2, 1] = " "
        the_grid[2, 3] = " "
        the_grid[3, 2] = " "

        # Вывод после центрального притяжения
        clean_screen()
        print_grid(
            char_face="   ◯   ",
            char_line="*Черная дыра крутится*",
            char_name="Гравитация"
        )
        time.sleep(2)

        # Орбитный поворот по часовой
        #   X - X       - X -
        #   - - -   ->  X - X
        #   X - X       - X -
        the_grid[1, 2] = the_grid[1, 1]
        the_grid[1, 1] = " "
        the_grid[2, 3] = the_grid[1, 3]
        the_grid[1, 3] = " "
        the_grid[3, 2] = the_grid[3, 3]
        the_grid[3, 3] = " "
        the_grid[2, 1] = the_grid[3, 1]
        the_grid[3, 1] = " "

        clean_screen()
        print_grid(
            char_face="   ◯   ",
            char_line="*Черная дыра отдыхает*",
            char_name="Гравитация"
        )
        time.sleep(2)

    # Проверка на победу
    winner = victory_check(the_grid)
    if winner is None:
        game_turn_graviton(not turn_owner_X, gravitation_tick=gravitation_tick)
        return
    else:
        if winner == player_sign:
            if not ("note" in inventory):
                inventory.append("note")
            if not REPERTOIRE["null"]["beaten"]:
                REPERTOIRE["null"]["locked"] = False
        win_screen(winner)
        return


# Заклинание Волдеморт использует после победы над игроком
def avada_kedavra(line_top):
    clean_screen()
    print_grid(line_top=line_top,
               char_face=ai_character["face_won"],
               char_line='"AVADA ..."',
               line_bottom3="Волдеморт читает проклятье смерти...")
    choice = input("Ваше слово: ").lower()

    clean_screen()
    if choice in ["expelliarmus", "экспеллиармус"]:
        print_grid(line_top=line_top,
                   char_face=ai_character["face_won"],
                   char_line='"... KEDAVRA!!!"',
                   line_row3='"' + choice.capitalize() + '"',
                   line_bottom3="")
        time.sleep(3)
        clean_screen()
        print_grid(line_top=line_top,
                   char_face=ai_character["face_won"],
                   char_line='"..."',
                   line_row3='*Заклинания сталкиваются и исчезают в яркой вспышке*',
                   line_bottom3="Нажмите Enter чтобы продолжить...")
        input("Ваш ввод: ")
        clean_screen()
        print_grid(line_top=line_top,
                   char_face=ai_character["face_won"],
                   char_line='"..."',
                   line_row3='*Вы используете момент, чтобы скрыться*',
                   line_bottom3="Нажмите Enter чтобы продолжить...")
        input("Ваш ввод: ")
        menu()
    elif choice == "магии не существует":
        print_grid(line_top=line_top,
                   char_face=ai_character["face"],
                   char_line="*Волдеморт останавливается в недоумении*",
                   line_bottom3="")
        time.sleep(3)
        clean_screen()
        print_grid(line_top=line_top,
                   char_face=ai_character["face"],
                   char_line='"..."',
                   line_row3='*Вы используете момент, чтобы скрыться*',
                   line_bottom3="Нажмите Enter чтобы продолжить...")
        input("Ваш ввод: ")
        menu()
    else:
        print_grid(line_top=line_top,
                   char_face=ai_character["face_won"],
                   char_line='"... KEDAVRA!!!"',
                   line_row3='"' + choice.capitalize() + '"',
                   line_bottom3="")
        time.sleep(2)
        clean_screen()
        print_grid(line_top=line_top,
                   char_face=ai_character["face_won"],
                   char_line="*Зеленый луч попадает ровно в вашу грудь*",
                   line_bottom3="")
        time.sleep(4)
        death_screen()


# Вычитает одну жизнь
def death_screen():
    global lives
    clean_screen()
    header()
    print("\n" * 2)
    print(" ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ")
    print(" ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ВЫ УМЕРЛИ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ")
    print(" ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ")
    print("\n" * 2)
    print(" Нажмите Enter чтобы продолжить...")
    footer()
    input("Ваш ввод: ")

    clean_screen()
    lives -= 1
    if lives > 0:
        print("\n" * 2)
        print(" ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ")
        print(" ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ВЫ УМЕРЛИ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ")
        print(" ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ")
        print()
        print(f" К счастью, как всем известно, в играх всего 3 жизни, так что у вас осталось еще: {lives}")
        print()
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")
        menu()
    else:
        print("\n" * 2)
        print(" ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ")
        print(" ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ВЫ УМЕРЛИ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ")
        print(" ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ")
        print()
        print(f" На этот раз по настоящему...")
        print()
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")
        quit()


# Вывод смерти когда находясь в меню у игрока в инвентаре 3 ножа в спине
def three_knives_death():
    global inventory, old_inventory
    clean_screen()
    header()
    print()
    print(" Хорошие новости, сегодня в узнали что-то новое!")
    print("\n" * 6)
    print(" Нажмите Enter чтобы продолжить...")
    footer()
    input("Ваш ввод: ")

    clean_screen()
    header()
    print()
    print(" Хорошие новости, сегодня в узнали что-то новое!")
    print(" Три ножа в спине - это ровно тот лимит, который ваше тело может вынести")
    print("\n" * 5)
    print(" Нажмите Enter чтобы продолжить...")
    footer()
    input("Ваш ввод: ")

    clean_screen()
    header()
    print()
    print(" Плохие новости...")
    print("\n" * 6)
    print(" Нажмите Enter чтобы продолжить...")
    footer()
    input("Ваш ввод: ")

    inventory.remove("knife")
    inventory.remove("knife")
    inventory.remove("knife")
    old_inventory = inventory.copy()
    death_screen()


# Призывает мартышку сделать ход вместо игрока
def summon_monkey():
    global player_sign
    clean_screen()
    print_grid(
        char_face=REPERTOIRE["monkey"]["face"],
        char_line=random.choice(REPERTOIRE["monkey"]["thinking"]),
        char_name=REPERTOIRE["monkey"]["name"],
        line_bottom3="Мартышка выпрыгивает из неоткуда"
    )
    time.sleep(3)
    clean_screen()
    print_grid(
        char_face=REPERTOIRE["monkey"]["face"],
        char_line=random.choice(REPERTOIRE["monkey"]["thinking"]),
        char_name=REPERTOIRE["monkey"]["name"],
        line_bottom3="Мартышка делает за вас ход"
    )
    time.sleep(2)

    the_grid[get_move(player_sign, REPERTOIRE["monkey"]["blunder_chance"])] = player_sign

    print_grid(
        char_face=REPERTOIRE["monkey"]["face"],
        char_line=random.choice(REPERTOIRE["monkey"]["after_self"]),
        char_name=REPERTOIRE["monkey"]["name"],
        line_bottom3="Мартышка делает за вас ход"
    )
    time.sleep(2)


# Вычитает деньги игрока за визит к Гадалке
def pay_seer():
    global money
    if money < 5:
        clean_screen()
        header()
        print("\n" * 3)
        print(' "Я не занимаюсь благотворительностью, дорогуша. Приходи когда будет 5$"')
        print("\n" * 2)
        print(" У вас недостаточно денег чтобы оплатить сеанс Гадалки")
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")
        play_game()
    else:
        clean_screen()
        header()
        print("\n" * 3)
        print(' *Вы отдаете гадалке 5$ в качестве платы за сеанс*')
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")
        money -= 5


# Сажает игрока в тюрьму в игре против Обнулятора
def prison():
    global lives, money

    def print_prison(line1="", line2="", line3=""):
        global lives, money

        line_lives = ""
        if lives < 3:
            line_lives = "Жизни: "
            for i in range(1, lives + 1):
                line_lives += "♥"
        line_money = ""

        if monkey_curse_immortality:
            lives = 667
            line_lives = "Жизни: ∞"

        if money > 0:
            line_money = f"Деньги: {money}$"

        clean_screen()
        header()
        print(" " + "-=ТЮРЬМА=-" + " " * (87 - len(line_money) - len(line_lives)) + line_money + " " + line_lives)
        print()
        print(" " + line1)
        print(" " + line2)
        print(" " + line3)
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

    clean_screen()
    print_prison("После провального мятежа вы отправляетесь в тюрьму на 8 лет")
    print_prison("После провального мятежа вы отправляетесь в тюрьму на 8 лет",
                 line3="Каждый год вы можете быть отравлены с вероятностью 5%")
    for years in range(1, 9):
        gamble = random.randint(1, 100)
        if gamble <= 5:
            print_prison("☠ Вы были отравлены ☠")
            lives -= 1
            if lives > 0:
                print_prison("☠ Вы были отравлены ☠",
                             line3=f"Но сумели выжить, жизней осталось: {lives}")
            else:
                print_prison("☠ Вы были отравлены ☠",
                             line3=f"Вы умерли")
                quit()
        print_prison(f"Вы просидели: {years}, оставшийся срок: {8 - years}")

    print_prison("Вы снова на свободе!")
    if money > 0:
        print_prison("Вы снова на свободе!", line3="Из-за сильной инфляции половина ваших сбережений обесценилась")
        money = round(money / 2)
    menu()


# Проверка ошибок при попытке добавить знак в поле игры. Возвращает сообщение об ошибке или None если ошибок нет
def input_error_check(turn_value):
    turn_value = turn_value.replace("x", " ")  # Английская х
    turn_value = turn_value.replace("х", " ")  # Русская х
    turn_value = turn_value.split()

    if len(turn_value) != 2:  # Для исключения ошибки List Index Out of Range
        return "Неправильный ввод, попробуйте еще раз"

    if not (turn_value[0] in ["1", "2", "3"] and turn_value[1] in ["1", "2", "3"]):  # Проверка на грамматические ошибки
        return "Неправильный ввод, попробуйте еще раз"

    turn_value = list(map(int, turn_value))

    if the_grid[turn_value[0], turn_value[1]] != " ":  # Проверка занята ли уже данная ячейка
        return f"Ячейка {turn_value[0]}x{turn_value[1]} " \
               f"уже занята {the_grid[turn_value[0], turn_value[1]]}, " \
               f"попробуйте еще раз"

    return turn_value  # Если ошибок нет, то возвращает лист с номерами ячейки. Например [1, 3]


# Присваивает игроку Х или 0 случайно
def assign_turn_owner_random():
    global X_style_start, O_style_start, style_end, player_sign, ai_sign
    style_start = "\x1b[0;30;42m"  # Цвет маркировки выбираемого Х или 0
    style_end = "\x1b[0m"

    # Функция вывода на экран.
    # highlight_x - подсвечивает X, иначе 0. result - Сообщение внизу для последнего вывода.
    # no_style - отключает подсветку X и 0
    def print_now(highlight_X=True, result="", no_style=False):
        hi_style_X_1, hi_style_X_2, hi_style_0_1, hi_style_0_2 = "", "", "", ""  # Строки обрамляющие Х и 0

        if not no_style:
            if highlight_X:
                hi_style_X_1 = style_start
                hi_style_X_2 = style_end
            else:
                hi_style_0_1 = style_start
                hi_style_0_2 = style_end

        clean_screen()
        header()
        print("    -=СЛУЧАЙНЫЙ ВЫБОР=-")
        print("      Вы играете за:")
        print()
        print("      " + hi_style_X_1 + " X " + hi_style_X_2 + "       " + hi_style_0_1 + " 0 " + hi_style_0_2)
        print()
        print()
        print(result)
        print("\n" * 2)  # Отступы
        footer()

    # Вывод на экран первый раз
    print_now(no_style=True)
    time.sleep(2)

    # Зацикливание выбора
    assign_X = True
    delay = 0.1
    i = 1
    while delay < 2:
        assign_X = not assign_X
        print_now(assign_X)
        time.sleep(delay)
        delay = delay + (i ** 2 / 1000) * random.uniform(1.0, 1.5)  # i**2 - для создания параболического эффекта
        i += 1

    # Вывод с результатом
    if assign_X:
        print_now(assign_X, " " * 6 + X_style_start + " КРЕСТИКОВ! " + style_end)
        player_sign = "X"
        ai_sign = "0"
    else:
        print_now(assign_X, " " * 8 + O_style_start + " Н0ЛИКОВ! " + style_end)
        player_sign = "0"
        ai_sign = "X"
    time.sleep(3)


# Адаптировано из https://www.youtube.com/watch?v=Bk9hlNZc6sE
# minimax возвращает tuple с оценкой и лучшим ходом (eval, (y, x))
# grid - входной словарь с полем игры
# maximizing - bool, нужен для работы рекурсии, всегда True при ручном вызове
# owner_sign, rival_sign - str, "X" или "0", обозначение знаков бенефициара и соперника
def minimax(grid, maximizing, owner_sign, rival_sign):
    # Проверка конца игры
    case = victory_check(grid)

    # Побеждают owner_sign
    if case == owner_sign:
        return 1, None

    # Побеждают rival_sign
    if case == rival_sign:
        return -1, None

    # Если ничья
    if case == "draw":
        return 0, None

    # Создаем список пустых ячеек
    empty_squares = get_empty_squares(grid)

    # Основная логика minimax
    if maximizing:
        max_eval = -100
        best_move = None

        for y, x in empty_squares:
            temp_grid = grid.copy()
            temp_grid[y, x] = owner_sign
            evaluation = minimax(temp_grid, False, owner_sign, rival_sign)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = (y, x)

        return max_eval, best_move
    elif not maximizing:
        min_eval = 100
        best_move = None

        for y, x in empty_squares:
            temp_grid = grid.copy()
            temp_grid[y, x] = rival_sign
            evaluation = minimax(temp_grid, True, owner_sign, rival_sign)[0]
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = (y, x)

        return min_eval, best_move


# Возвращает ход типа tuple (y, x).
# sign - кто ходит "X" / "0".
# blunder_chance - вероятность прозевать в процентах. 100 - каждый ход случайный, 0 - каждый ход превосходный
# Упрощает вызов функции minimax
def get_move(sign, blunder_chance):
    global the_grid

    # Определение знака соперника
    if sign == "X":
        anti_sign = "0"
    else:
        anti_sign = "X"

    move = minimax(the_grid, True, sign, anti_sign)[1]
    empty_squares = get_empty_squares(the_grid)

    gamble = random.randint(1, 100)
    if gamble <= blunder_chance and len(empty_squares) > 1:  # Сделать случайный ход
        random_move = random.choice(empty_squares)
        while random_move == move:
            random_move = random.choice(empty_squares)
        return random_move
    else:
        if are_all_cells_blank(the_grid):  # Если все ячейки пустые, занять угол или середину для разнообразия
            return random.choice([(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)])
        return move


# Возвращает лист с координатами пустых ячеек. Например: [(1, 2), (3, 1)]
def get_empty_squares(grid):
    empty_squares = []
    for y, x in grid:
        if grid[y, x] == " ":
            empty_squares.append((y, x))
    return empty_squares


# Возвращает bool. Может ли выиграть sign = "X" / "0" в текущем ходе
def can_they_win_now(sign):
    global the_grid
    empty_squares = get_empty_squares(the_grid)

    for y, x in empty_squares:
        temp_grid = the_grid.copy()
        temp_grid[y, x] = sign
        if victory_check(temp_grid) == sign:
            return True

    return False


# Возвращает bool. True - если все ячейки пустые, False - если есть занятые
def are_all_cells_blank(grid):
    all_cells_blank = True
    for cell in grid:
        if grid[cell] != " ":
            all_cells_blank = False
    return all_cells_blank


# Печать верхней границы "экрана" 100 знаков в длину
def header():
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")


# Печать нижней границы "экрана" 100 знаков в длину
def footer():
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")


# Вывод притворного онлайн-режима
def online():
    global online_gag
    clean_screen()
    header()
    print("\n" * 3)
    print("                      Поиск доступного сервера ")
    print("\n" * 3)
    print(" Пожалуйста подождите")
    footer()
    time.sleep(2)

    clean_screen()
    header()
    print("\n" * 3)
    print("                      Поиск доступного сервера .")
    print("\n" * 3)
    print(" Пожалуйста подождите")
    footer()
    time.sleep(2)

    clean_screen()
    header()
    print("\n" * 3)
    print("                      Поиск доступного сервера ..")
    print("\n" * 3)
    print(" Пожалуйста подождите")
    footer()
    time.sleep(2)

    clean_screen()
    header()
    print("\n" * 3)
    print("                      Поиск доступного сервера ...")
    print("\n" * 3)
    print(" Пожалуйста подождите")
    footer()
    time.sleep(2)

    clean_screen()
    header()
    print("\n" * 3)
    print("                      Ожидание второго игрока")
    print("\n" * 3)
    print(" Вы подключены к серверу: mskfreeserver09.ru")
    footer()
    time.sleep(2)

    clean_screen()
    header()
    print("\n" * 3)
    print("                      Ожидание второго игрока .")
    print("\n" * 3)
    print(" Вы подключены к серверу: mskfreeserver09.ru")
    footer()
    time.sleep(2)

    clean_screen()
    header()
    print("\n" * 3)
    print("                      Ожидание второго игрока ..")
    print("\n" * 3)
    print(" Вы подключены к серверу: mskfreeserver09.ru")
    footer()
    time.sleep(2)

    clean_screen()
    header()
    print("\n" * 3)
    print("                      Игрок найден!")
    print("\n" * 3)
    print(" Вы подключены к серверу: mskfreeserver09.ru")
    footer()
    time.sleep(2)

    clean_screen()
    header()
    print("\n" * 3)
    print("                      Шутка, нет здесь онлайн игры :)")
    print("\n" * 3)
    print(" Нажмите Enter чтобы продолжить...")
    footer()
    input("Ваш ввод: ")

    online_gag = False
    menu()


# Вывод мотивирующего постера
def gigachad():
    clean_screen()
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣤⣶⣤⣤⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⡿⠋⠉⠛⠛⠛⠿⣿⠿⠿⢿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⡀⢀⣽⣷⣆⡀⠙⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣷⠶⠋⠀⠀⣠⣤⣤⣉⣉⣿⠙⣿⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⠁⠀⠀⠴⡟⣻⣿⣿⣿⣿⣿⣶⣿⣦⡀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⠟⡿⠻⣿⠃⠀⠀⠀⠻⢿⣿⣿⣿⣿⣿⠏⢹⣿⣿⣿⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣼⣷⡶⣿⣄⠀⠀⠀⠀⠀⢉⣿⣿⣿⡿⠀⠸⣿⣿⡿⣷⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡿⣦⢀⣿⣿⣄⡀⣀⣰⠾⠛⣻⣿⣿⣟⣲⡀⢸⡿⡟⠹⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠞⣾⣿⡛⣿⣿⣿⣿⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⣿⡽⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⠿⣍⣿⣧⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣽⣿⣷⣙⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣹⡿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡧⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡆⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣾⣿⣿⣿⣿⣿⣿⡶⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⡴⠞⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⣿⣿⣿⠿⣿⣿⠿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⢀⣠⣤⠶⠚⠉⠉⠀⢀⡴⠂⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⢀⣿⣿⠁⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠞⠋⠁⠀⠀⠀⠀⣠⣴⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⠀⣾⣿⠋⠀⢠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⡀⠀⠀⢀⣷⣶⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣆⣼⣿⠁⢠⠃⠈⠓⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⣿⣿⡛⠛⠿⠿⠿⠿⠿⢷⣦⣤⣤⣤⣦⣄⣀⣀⠀⢀⣿⣿⠻⣿⣰⠻⠀⠸⣧⡀⠀⠉⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠛⢿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠙⠛⠿⣦⣼⡏⢻⣿⣿⠇⠀⠁⠀⠻⣿⠙⣶⣄⠈⠳⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠈⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⣐⠀⠀⠀⠈⠳⡘⣿⡟⣀⡠⠿⠶⠒⠟⠓⠀⠹⡄⢴⣬⣍⣑⠢⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢀⣀⠐⠲⠤⠁⢘⣠⣿⣷⣦⠀⠀⠀⠀⠀⠀⠙⢿⣿⣏⠉⠉⠂⠉⠉⠓⠒⠦⣄⡀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠈⣿⣿⣷⣯⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢦⣷⡀⠀⠀⠀⠀⠀⠀⠉⠲⣄⠀")
    print("⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢦⠀⢹⣿⣏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢻⣷⣄⠀⠀⠀⠀⠀⠀⠈⠳")
    print("⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⣸⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣽⡟⢶⣄⠀⠀⠀⠀⠀")
    print("⠯⠀⠀⠀⠒⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡄⠈⠳⠀⠀⠀⠀")
    print("⠀⠀⢀⣀⣀⡀⣼⣤⡟⣬⣿⣷⣤⣀⣄⣀⡀⠀⠀⠀⠀⠀⠀⠈⣿⣿⡄⣉⡀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⣿⣿⣄⠀⣀⣀⡀⠀")
    print("Нажмите Enter чтобы продолжить...")
    input("Ваш ввод: ")
    menu_inventory()


# Выбор судьбы мартышки после 3 матчей
def monkey_pet_or_kill(message=""):
    global REPERTOIRE, inventory, achievements, style_end, style_error

    clean_screen()
    header()
    print(" -=ДЕРЖИ ДРУЗЕЙ БЛИЗКО...=-")
    print()
    print(" После трех игр, мартышка начинает к вам привыкать,")
    print(" теперь вы можете к ней приблизиться")
    print(" ПОГЛАДИТЬ [pet]")
    print(" УБИТЬ [kill]")
    print("\n")
    print(style_error + message + style_end)
    print(" Введите pet или kill")
    footer()
    choice = input("Ваш выбор: ")

    if choice == "pet":
        clean_screen()
        header()
        print(" -=ДЕРЖИ ДРУЗЕЙ БЛИЗКО...=-")
        print()
        print(" Вы гладите мартышку, она выглядит удивленно")
        print(" Теперь любопытное животное ходит за вами повсюду")
        print(" У вас появился питомец!")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")
        inventory.append("monkey")
        REPERTOIRE["monkey"]["name"] = "Ручная Мартышка"
        REPERTOIRE["monkey"]["blunder_chance"] = 70
        REPERTOIRE["monkey"]["difficulty"] = "Ниже Средней"
    elif choice == "kill":
        clean_screen()
        header()
        print(" -=...А ВРАГОВ ЕЩЕ БЛИЖЕ=-")
        print()
        print(" По какой-то необъяснимой причине вы решаете напасть на мартышку с ножом,")
        print(" но бездомная мартышка сражается с дикой свирепостью")
        print(" Мартышка убегает с визгом. Вы остаетесь в глубоких царапинах на лице и руках")
        print()
        print(" Вы получили новый предмет: Обезьянья Лапка")
        print()
        print()
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")
        inventory.append("monkeys paw")
        REPERTOIRE["monkey"]["name"] = "Однорукая Мартышка"
    else:
        monkey_pet_or_kill(f"Ввели {choice}, введите pet или kill")
        return

    achievements.append("monkeys_fate")


# Загадование желаний обезьяньей лапки, когда игрок выбирает лапку в инвентаре
def monkeys_paw(message=""):
    global money, inventory, lives, monkey_curse_immortality, monkey_curse_omniscience
    clean_screen()
    header()
    print(" -=ОБЕЗЬЯНЬЯ ЛАПКА=-")
    print()
    print(" Вы стоите перед камином и держите в руках жуткую лапу мартышки.")
    print(" Указательный палец оттопырен, все остальные сжаты.")
    print(" Вы испытываете непреодолимый импульс загадать желание...")
    print("")
    print("\n")
    print(" " + style_error + message + style_end)
    print(" Нажмите Enter чтобы продолжить...")
    footer()
    input("Ваш ввод: ")

    clean_screen()
    header()
    print(" -=ОБЕЗЬЯНЬЯ ЛАПКА=-")
    print()
    print(" [wealth] Безграничное богатство")
    print(" [immortality] Бессмертие")
    print(" [omniscience] Всезнание")
    print(" [love] Настоящая любовь")
    print(" [sell] Продать обезьянью лапку")
    print(" [burn] Сжечь обезьянью лапку")
    print()
    print(" Введите ваш выбор, например", random.choice(["wealth", "immortality", "omniscience", "love"]))
    footer()
    choice = input("Ваш выбор: ")

    if choice == "wealth":
        clean_screen()
        header()
        print(" -=ЧЕЛОВЕК ПРОДАВШИЙ МИР=-")
        print()
        print(" Вам приходит уведомление, вы проверяете свой банковский счет, деньги переваливают за миллиард")
        print(" и продолжают поступать. Курс вашей национальной валюты начинает снижаться,")
        print(" поэтому вы начинаете снимать и переводить что можете в иностранные валюты...")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ЧЕЛОВЕК ПРОДАВШИЙ МИР=-")
        print()
        print(" Спустя два дня валюта вашей нации полностью обесценивается.")
        print(" Вас находят специальные службы и над вами совершается суд.")
        print(" Вы были приговорены к трем пожизненным заключениям...")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ЧЕЛОВЕК ПРОДАВШИЙ МИР=-")
        print()
        print(" В одно утро ваш охладелый труп находит сокамерник.")
        print(" Вы умерли в 67 лет от сердечного приступа")
        print(" ")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        lives -= 1
        if lives <= 0:
            quit()

        clean_screen()
        header()
        print(" -=ЧЕЛОВЕК ПРОДАВШИЙ МИР=-")
        print()
        print(" К счастью вы все еще в игре крестики и нолики, где дается 3 жизни")
        print(" У вас осталось:", lives)
        print(" Вы продолжаете отсиживать свой срок...")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ЧЕЛОВЕК ПРОДАВШИЙ МИР=-")
        print()
        print(" В воскресенье вы подскользнулись на пролитом компоте в столовой")
        print(" и сломали шею...")
        print(" Вы умерли за неделю до своего 107-го дня рождения")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        lives -= 1
        if lives <= 0:
            quit()

        clean_screen()
        header()
        print(" -=ЧЕЛОВЕК ПРОДАВШИЙ МИР=-")
        print()
        print(" Вы возвращаетесь к жизни во второй раз, вокруг вас начинает собираться религиозный культ.")
        print(" Власти решают выпустить вас досрочно, аргументируя это хорошим поведением...")
        print(" ")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ЧЕЛОВЕК ПРОДАВШИЙ МИР=-")
        print()
        print(" Вы выходите на свободу в свои 108 лет! И да, вы выглядите соответствующее")
        print(" Ваш банковский счет был давно арестован, но ваш почтовый ящик заполняется старой валютой")
        print(" и вы продолжаете находить пачки старых денег в шкафах, ящиках и на полках")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ЧЕЛОВЕК ПРОДАВШИЙ МИР=-")
        print()
        print(" Старая валюта обесценена, но те деньги, которые вы успели перевести в первые дни")
        print(" с учетом инфляции и арестов дают вам...")
        print(" ")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ЧЕЛОВЕК ПРОДАВШИЙ МИР=-")
        print()
        print(" 01000110$!")
        print(" Вы все еще богаты!")
        print(" ")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ЧЕЛОВЕК ПРОДАВШИЙ МИР=-")
        print()
        print(" 01000110$!")
        print(" Вы все еще богаты!")
        print(" И старую валюту вы используете для растопки камина!")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        inventory.remove("monkeys paw")
        inventory.append("monkeys fist")
        money += 1000110
    elif choice == "immortality":
        clean_screen()
        header()
        print(" -=НЕУМЕРАЕМЫЙ=-")
        print()
        print(" Указательный палец зловеще сжимается. Вы не чувствуете никаких изменений.")
        print(" Позднее этим вечером вы решаете сходить в продуктовый магазин за сосисками.")
        print(" Вы смотрите по обе стороны, перед тем как перейти дорогу. Вас сбивает случайный таксист.")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=НЕУМЕРАЕМЫЙ=-")
        print()
        print(" На утро следующего дня вы находите себя в африканской прерии без единой вещи.")
        print(" Большую часть дня вы пытаетесь найти цивилизацию, но тщетно. ")
        print(" Вы слышите шорох за спиной, к вечеру вашей тушей питаются стервятники...")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=НЕУМЕРАЕМЫЙ=-")
        print()
        print(" На следующий день вы обнаруживаете себя в городе Хамхын, Северная Корея.")
        print(" Помимо того, что вы абсолютно голые, вы также замечаете ваш другой цвет кожи и другое лицо")
        print(" К вечеру вы были приговорены и расстелены из гранатомета корейскими военными...")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=НЕУМЕРАЕМЫЙ=-")
        print()
        print(" ... И так каждый день примерно между 18:00 и 23:00 вы умираете случайной смертью.")
        print(" Только чтобы каждый раз появиться в новом теле, со случайным полом в чем мать родила.")
        print(" Вы пытаетесь не умирать, прячась от всех опасностей, но смерть все-равно вас находит.")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=НЕУМЕРАЕМЫЙ=-")
        print()
        print(" В конечном счете вы смирились с таким существованием и даже смогли найти лазейки.")
        print(" Так вы можете сохранять до 5$ (без комментариев) на своей персоне.")
        print(" Но все что превышает 5$ остается на вашем трупе, т.е. больше не с вами.")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=НЕУМЕРАЕМЫЙ=-")
        print()
        print(" Также любая полученная вещь во время игры исчезает по возвращении в меню...")
        print(" ")
        print(" Зато вы бессмертны!")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        monkey_curse_immortality = True
        lives = 667
        inventory = []
    elif choice == "omniscience":
        clean_screen()
        header()
        print(" -=ПРОСВЕЩЕННЫЙ=-")
        print()
        print(" Яркой вспышкой все знания вселенной взрываются в вашей голове.")
        print(" Безграничная память и интеллектуальные возможности, к сожалению, не были частью сделки.")
        print(" Поэтому через секунду все важное из того что вы можете вспомнить...")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ПРОСВЕЩЕННЫЙ=-")
        print()
        print(" - Человечество порабощено искусственным интеллектом и живет в матрице")
        print(" ")
        print(" ")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ПРОСВЕЩЕННЫЙ=-")
        print()
        print(" - Человечество порабощено искусственным интеллектом и живет в матрице")
        print(" - 'sv_cheats 1' единственный способ победить GlaDOS в крестики и нолики")
        print(" ")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ПРОСВЕЩЕННЫЙ=-")
        print()
        print(" - Человечество порабощено искусственным интеллектом и живет в матрице")
        print(" - 'sv_cheats 1' единственный способ победить GlaDOS в крестики и нолики")
        print(" - Вы знаете секрет идеального французского поцелуя")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ПРОСВЕЩЕННЫЙ=-")
        print()
        print(" - Человечество порабощено искусственным интеллектом и живет в матрице")
        print(" - 'sv_cheats 1' единственный способ победить GlaDOS в крестики и нолики")
        print(" - Вы знаете секрет идеального французского поцелуя")
        print(" - Чтобы получить предмет от Гадалки - нужно использовать три выделенных слова ")
        print("   из ее первого предсказания в ее последующих вопросах")
        print("\n" * 2)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ПРОСВЕЩЕННЫЙ=-")
        print()
        print(" - Человечество порабощено искусственным интеллектом и живет в матрице")
        print(" - 'sv_cheats 1' единственный способ победить GlaDOS в крестики и нолики")
        print(" - Вы знаете секрет идеального французского поцелуя")
        print(" - Чтобы получить предмет от Гадалки - нужно использовать три выделенных слова ")
        print("   из ее первого предсказания в ее последующих вопросах")
        print(" - Каждый раз когда Локи создает иллюзию, настоящий ход можно узнать по его движениям")
        print("\n")
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ПРОСВЕЩЕННЫЙ=-")
        print()
        print(" - Человечество порабощено искусственным интеллектом и живет в матрице")
        print(" - 'sv_cheats 1' единственный способ победить GlaDOS в крестики и нолики")
        print(" - Вы знаете секрет идеального французского поцелуя")
        print(" - Чтобы получить предмет от Гадалки - нужно использовать три выделенных слова ")
        print("   из ее первого предсказания в ее последующих вопросах")
        print(" - Каждый раз когда Локи создает иллюзию, настоящий ход можно узнать по его движениям")
        print(" - Вы знаете как излечить рак")
        print()
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ПРОСВЕЩЕННЫЙ=-")
        print()
        print(" Вскоре вы обнаруживаете странность, похоже, что люди не в состоянии понять вашу речь.")
        print(" С этого момента вы разговариваете нечленораздельными звуками.")
        print(" Обезьяна единственное существо во всем мире способное вас понять.")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        clean_screen()
        header()
        print(" -=ПРОСВЕЩЕННЫЙ=-")
        print()
        print(" Поэтому после каждой игры в крестики и нолики вы накапливаете одиночество.")
        print(" Уровень одиночества не должен достигнуть 3-ех, иначе вы умрете. Текущий уровень отображен в меню.")
        print(" Для облегчения одиночества - вы должны играть с мартышкой")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        monkey_curse_omniscience = True
        inventory.remove("monkeys paw")
        inventory.append("monkeys fist")
    elif choice == "love":
        clean_screen()
        header()
        print(" -=ОБЕЗЬЯНЬЯ ЛАПКА=-")
        print()
        print(" На следующий день местный бомж Вован начинает уделять вам много внимания.")
        print(" Каждый день он проводит возле вашего дома, поет вам серенады и дарит подарки")
        print(" такие как: пустые бутылки, сигаретные бычки и статуи из навоза")
        print(" У вас появился человек, который вас любит безгранично!")
        print("\n" * 2)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        inventory.remove("monkeys paw")
        inventory.append("monkeys fist")
    elif choice == "sell":
        clean_screen()
        header()
        print(" -=ОБЕЗЬЯНЬЯ ЛАПКА=-")
        print()
        print(" У вас получается продать обезьянью лапку через публичный интернет магазин")
        print(" Ужасный запах разложения все еще чувствуется в комнате")
        print(" Вы заработали 10$")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        inventory.remove("monkeys paw")
        money += 10
    elif choice == "burn":
        clean_screen()
        header()
        print(" -=ОБЕЗЬЯНЬЯ ЛАПКА=-")
        print()
        print(" Вы бросаете жуткую обезьянью лапку в танцующие щупальца пламени")
        print(" Глубокий выдох облегчения наполняет выши легкие")
        print(" И все же, вас не оставляет мысль - сделали ли вы все правильно?")
        print("\n" * 3)
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        inventory.remove("monkeys paw")
    else:
        monkeys_paw("Вы ввели что-то неправильно, попробуйте еще раз")
        return

    menu()


# Шифр используемый для проклятья мартышки Всезнание, чтобы запутать речь игрока в игре с Гадалкой
def caesar_cipher(text, n):
    result = ""
    text.lower()
    for char in text:
        order = ord(char)
        if 1072 <= order <= 1103:
            order += n
            if order > 1103:
                order -= 32
            result += chr(order)
        else:
            result += char
    return result


# Обработка процесса вычитания жизней при проклятии мартышки Всезнание, используется при loneliness >= 3
def death_by_loneliness():
    global lives, loneliness
    clean_screen()
    header()
    print(" -=В ТЕМНОЙ КОМНАТЕ=-")
    print()
    print(" После недель одиночества вы теряете всякий смысл существования.")
    print(" Лежа на полу свернувшись в клубок, вы наконец по-настоящему понимаете нигилизм.")
    print(" Что окончательно сломало ваш слабый рассудок...")
    print("\n" * 3)
    print(" Нажмите Enter чтобы продолжить...")
    footer()
    input("Ваш ввод: ")

    clean_screen()
    header()
    print("\n" * 2)
    print(" ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ")
    print(" ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ВЫ УМЕРЛИ ОТ ОДИНОЧЕСТВА ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ")
    print(" ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ")
    print("\n" * 2)
    print(" Нажмите Enter чтобы продолжить...")
    footer()
    input("Ваш ввод: ")

    lives -= 1

    if lives > 0:
        clean_screen()
        header()
        print("\n" * 2)
        print(" ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ")
        print(" ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ВЫ УМЕРЛИ ОТ ОДИНОЧЕСТВА ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ")
        print(" ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ")
        print()
        print(f" Но не так быстро, в этой игре у вас еще остались жизни! Сколько? {lives}!")
        print()
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        loneliness = 0
        menu()
    else:
        clean_screen()
        header()
        print("\n" * 2)
        print(" ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ")
        print(" ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ВЫ УМЕРЛИ ОТ ОДИНОЧЕСТВА ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ")
        print(" ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ")
        print()
        print(" Случается с лучшими из нас...")
        print()
        print(" Нажмите Enter чтобы продолжить...")
        footer()
        input("Ваш ввод: ")

        quit()


# Обработка включения чит кодов для победы над GLaDOS
def sv_cheats_1():
    def fill_grid(sign):
        global the_grid
        clean_screen()
        the_grid[1, 1], the_grid[1, 2], the_grid[1, 3] = sign, sign, sign
        print_grid(
            char_face=ai_character["face"],
            char_line="...",
            line_bottom2="Cheats activated",
            line_bottom3="fill_grid " + sign + " in progress...",
            char_name=ai_character["name"]
        )
        time.sleep(2)
        clean_screen()
        the_grid[2, 1], the_grid[2, 2], the_grid[2, 3] = sign, sign, sign
        print_grid(
            char_face=ai_character["face"],
            char_line="...",
            line_bottom2="Cheats activated",
            line_bottom3="fill_grid " + sign + " in progress...",
            char_name=ai_character["name"]
        )
        time.sleep(2)
        clean_screen()
        the_grid[3, 1], the_grid[3, 2], the_grid[3, 3] = sign, sign, sign
        print_grid(
            char_face=ai_character["face"],
            char_line="...",
            line_bottom2="Cheats activated",
            line_bottom3="fill_grid " + sign + " in progress...",
            char_name=ai_character["name"]
        )
        time.sleep(3)

    clean_screen()
    print_grid(
        char_face=ai_character["face"],
        char_line=random.choice(ai_character["loosing"]),
        line_bottom2="Cheats activated",
        line_bottom3="Available command - fill_grid <sign>, where sign - X or 0",
        char_name=ai_character["name"]
    )
    choice = input("Your input: ").lower()

    if choice == "fill_grid X":
        fill_grid("X")
        win_screen("X")
    elif choice == "fill_grid 0":
        fill_grid("0")
        win_screen("0")
    else:
        clean_screen()
        print_grid(
            char_face=ai_character["face"],
            char_line="А, я вижу...",
            line_bottom2="Cheats activated. Incorrect command",
            line_bottom3="Available command - fill_grid <sign>, where sign - X or 0",
            char_name=ai_character["name"]
        )
        time.sleep(3)
        clean_screen()
        print_grid(
            char_face=ai_character["face"],
            char_line="sv_cheats 0",
            line_bottom2="Cheats activated. Incorrect command",
            line_bottom3="Available command - fill_grid <sign>, where sign - X or 0",
            char_name=ai_character["name"]
        )
        time.sleep(3)
        clean_screen()
        print_grid(
            char_face=ai_character["face"],
            char_line="Я ожидала что-то подобное",
            char_name=ai_character["name"]
        )
        clean_screen()
        print_grid(
            char_face=ai_character["face"],
            char_line="Прощай...",
            char_name=ai_character["name"]
        )
        time.sleep(2)
        clean_screen()
        print_grid(
            char_face=ai_character["face"],
            char_line="*Комната быстро наполняется нейротоксином*",
            char_name=ai_character["name"]
        )
        time.sleep(3)
        death_screen()


# Титры
def give_cake():
    global cake, achievements, monkey_matches_played

    clean_screen()
    header()
    print("")
    print()
    print(" ")
    print(" Гейб Ньюэлл спускается с небес в белоснежной робе")
    print(" ")
    print("\n" * 4)
    footer()
    time.sleep(3)

    clean_screen()
    header()
    print("")
    print()
    print(" ")
    print(" Гейб Ньюэлл спускается с небес в белоснежной робе")
    print(" и протягивает вам тарелку с кусочком торта")
    print("\n" * 4)
    footer()
    time.sleep(3)

    clean_screen()
    print("            ,:/+/-                        \n"
          "             /M/              .,-=;//;-   \n"
          "        .:/= ;MH/,    ,=/+%$XH@MM#@:      \n"
          "       -$##@+$###@H@MMM#######H:.    -/H# \n"
          "  .,H@H@ X######@ -H#####@+-     -+H###@X \n"
          "   .,@##H;      +XM##M/,     =%@###@X;-   \n"
          " X%-  :M##########$.    .:%M###@%:        \n"
          "M##H,   +H@@@$/-.  ,;$M###@%,          -  \n"
          "M####M=,,---,.-%%H####M$:          ,+@##  \n"
          "@##################@/.         :%H##@$-   \n"
          "M###############H,         ;HM##M$=       \n"
          "#################.    .=$M##M$=           \n"
          "################H..;XM##M$=          .:+  \n"
          "M###################@%=           =+@MH%  \n"
          "@#################M/.         =+H#X%=     \n"
          "=+M###############M,      ,/X#H+:,        \n"
          "  .;XM###########H=   ,/X#H+:;            \n"
          "     .=+HM#######M+/+HM@+=.               \n"
          "         ,:/%XM####H/.                    \n"
          "              ,.:=-.                      \n"
          )
    print("Это был самый вкусный торт вы пробовали в своей жизни")
    cake = False

    achievements.append("cake")

    print("Нажмите Enter чтобы продолжить...")
    input("Ваш ввод: ")

    clean_screen()
    header()
    print("")
    print()
    print(" ")
    print(" Поздравляем, вы завершили игру FlexTacToe!")
    print(" ")
    print("\n" * 4)
    footer()
    time.sleep(3)

    clean_screen()
    header()
    print(" -=ТИТРЫ=-")
    print()
    print(" Режиссер: bioRival")
    print(" Исполнительный продюсер: bioRival")
    print(" Сценарист: bioRival")
    print("\n" * 4)
    footer()
    time.sleep(3)

    clean_screen()
    header()
    print(" -=ТИТРЫ=-")
    print()
    print(" Композитор: None")
    print(" Оператор: bioRival")
    print(" Актер: bioRival")
    print("\n" * 4)
    footer()
    time.sleep(3)

    clean_screen()
    header()
    print(" -=ТИТРЫ=-")
    print()
    print(" Каскадер: bioRival")
    print(" Визуальные эффекты: bioRival")
    print(" Звукорежиссер: None")
    print("\n" * 4)
    footer()
    time.sleep(3)

    clean_screen()
    header()
    print(" -=ТИТРЫ=-")
    print()
    print(f" Вы сыграли с мартышкой: {monkey_matches_played} раз")
    print(" ")
    print(" ")
    print("\n" * 4)
    footer()
    time.sleep(3)

    clean_screen()
    header()
    print(" -=ТИТРЫ=-")
    print()
    print(f" Вы сыграли с мартышкой: {monkey_matches_played} раз")
    print(" Ни одной мартышки во время разработки игры не пострадало")
    print(" ")
    print("\n" * 4)
    footer()
    time.sleep(3)

    clean_screen()
    header()
    print(" -=ТИТРЫ=-")
    print()
    print(" Особая благодарность:")
    print(" Серому - моему коту из девятого круга ада, который вечно меня отвлекал")
    print(" ")
    print("\n" * 4)
    footer()
    time.sleep(5)

    menu()


# Глобальные переменные

REPERTOIRE = {
    # "mr blank": {
    #     "name": "",
    #     "face": "",
    #     "face_won": "",
    #     "face_lost": "",
    #     "beaten": False,
    #     "locked": False,
    #     "difficulty": "",
    #     "blunder_chance": 100,
    #     "description1": "",
    #     "description2": "",
    #     "description3": "",
    #     "description4": "",
    #     "description5": "",
    #     "description6": "",
    #     "description7": "",
    #     "greet": [
    #         '',
    #         '',
    #         ''
    #     ],
    #     "thinking": [
    #         '',
    #         '',
    #         ''
    #     ],
    #     "casual": [
    #         '',
    #         '',
    #         '',
    #         '',
    #         ''
    #     ],
    #     "after_self": [
    #         '',
    #         '',
    #         '',
    #         ''
    #     ],
    #     "loosing": [
    #         '',
    #         '',
    #         ''
    #     ],
    #     "lost": [
    #         '',
    #         '',
    #         '',
    #         '',
    #         ''
    #     ],
    #     "won": [
    #         '',
    #         '',
    #         '',
    #         ''
    #     ],
    #     "draw": [
    #         '',
    #         '',
    #         ''
    #     ]
    # }
    "monkey": {
        "name": "Мартышка",
        "face": "ᕮ(•_•)ᕭ",
        "face_won": "ᕮ(•‿•)ᕭ",
        "face_lost": "ᕮ(•̀⌓•́)ᕭ",
        "beaten": False,
        "locked": False,
        "difficulty": "Легкая",
        "blunder_chance": 100,
        "description1": "Играет ровно так как ожидается от дикого бездомного примата",
        "description2": "",
        "description3": "",
        "description4": "",
        "description5": "",
        "description6": "",
        "description7": "",
        "greet": [
            '"Уууууу!"',
            '*Мартышка принюхивается с настороженностью*',
            '*Мартышка машет вам и улыбается*'
        ],
        "thinking": [
            '*Мартышка чешет голову*',
            '*Мартышка думает*',
            '*Мартышка делает серьезную гримасу*'
        ],
        "casual": [
            '"Уууу..."',
            '"ааа... ууу... у у У"',
            '"У! А! Уууу ууу, ааа."',
            '"Уаа..." *Мартышка кивает головой с пониманием*',
            '*Мартышка пускает слюну на клавиатуру*'
        ],
        "after_self": [
            '*Мартышка выглядит самодовольно*',
            '"Уу Ааааа"',
            "*Мартышка скрещивает руки*",
            '"Аааа ууу уАу ууууУ?*"'
        ],
        "loosing": [
            '*Мартышка прищуривается*',
            'Ууууу....',
            'А?'
        ],
        "lost": [
            '"У! АААА! УУУУ!"',
            '*Мартышка дергается в истерике*',
            '*Экскремент проносится в сантиметре мимо вашей головы*',
            '"ааа..?"',
            '*Мартышка стучит по столу* "У! АА!"'
        ],
        "won": [
            '"Аааа У! У! *Стучит по груди*"',
            '*Мартышка кладет лапы на стол и начинает смаковать банан*',
            '*Мартышка надевает солнечные очки*',
            '"А! А! А! У! А!"'
        ],
        "draw": [
            'Ууу Ууу Ууу',
            'У А?',
            '*Мартышка чешет подмышку*'
        ]
    },
    "cook": {
        "name": "Кулинар Паня",
        "face": "ʕ͡°̯_ʖ͡°ʔ",
        "face_won": "└ ʕ͡°͜ʖ͡°ʔ┘",
        "face_lost": "ʕ͡⁰̯ ʖ ͡⁰ʔ",
        "beaten": False,
        "locked": False,
        "difficulty": "Средняя",
        "blunder_chance": 40,
        "description1": "Приправляет каждую игру каламбурами.",
        "description2": "Хорошими? Плохими? Зависит от вашего вкуса...",
        "description3": "",
        "description4": "",
        "description5": "",
        "description6": "",
        "description7": "",
        "greet": [
            '"Добрый день! Хотите выбрать меню?"',
            '"Ах! Проголодались по икре слов?"',
            '"Желаю вам первого блина"'
        ],
        "thinking": [
            '"Хммм... Тут главное не переборщить"',
            '"Хммм... Что там по рецепту?"',
            '*Кулинар Паня добавляет секретный ингридиент*'
        ],
        "casual": [
            '"Плохо питаться - это не есть хорошо!"',
            '"Я на этой игре собаку съел"',
        ],
        "after_self": [
            '"Надеюсь этот ход не нужно разжевывать?"',
            '"Вот такие пироги"',
            '"С пылу с жару"',
            '"Проще пареной репы"'
        ],
        "loosing": [
            '*Кулинар Паня выглядит как не в своей тарелке*',
            '"Кажется я не заказывал слив..."',
        ],
        "lost": [
            '"Я только разогревался!"',
            '"Игрок из вас - в рагу не пожелаешь"',
            '"Все. Я умываю руки..."',
            '*Кулинар Паня смахивает слезу* "Нет... это все лук"',
        ],
        "won": [
            '"Сэр, ваше пюре выглядит слегка ПОДАВЛЕННЫМ"',
            '"Я вам оказался не по зубам, ХА!"',
            '"Мало каши ели?"',
            '"Вишенка на торте"'
        ],
        "draw": [
            '"Как уж на сковородке"',
            '"У этого блюда истек срок годности"',
        ]
    },
    "shiori": {
        "name": "Мастер Шиори",
        "face": "✿(-‿- )✿",
        "face_won": "✿(◠‿◠｡)✿",
        "face_lost": "✿(⇀‸↼‶)✿",
        "beaten": False,
        "locked": False,
        "difficulty": "Высокая",
        "blunder_chance": 20,
        "description1": "Увлекается восточными боевыми искусствами.",
        "description2": "Разговаривает в трехстишьях Хайку",
        "description3": "",
        "description4": "",
        "description5": "",
        "description6": "",
        "description7": "",
        "greet": [
            '*Мастер Шиори делает традиционный японский поклон*',
            '*Мастер Шиори вынимает катану из ножен*',
            '*Мастер Шиори собирает волосы в хвост*'
        ],
        "thinking": [
            '"На голой ветке"',
            '"В глубоких думах"',
            '"Укрывшись под мостом"',
            '"На сырой крыше"',
            '"Среди ярких звезд"'
        ],
        "casual": [
            '"Осенний вечер!"',
            '"Вверх, до самых высот!"',
            '"Бездомное дитя"',
            '"Грезы о славе..."',
            '"Момент уже прошел"'
        ],
        "after_self": [
            '"Ворон сидит одиноко..."',
            '"Улитка тихо ползет"',
            '"Сосед кидает камень"',
            '"Собака нашла кости"',
            '"Хохочет седой старик"'
        ],
        "loosing": [
            '"Смерть неизбежна"',
            '"Новое начало!"',
            '"Дождик на пляже..."'
        ],
        "lost": [
            '*Мастер Шиори бросает дымовую бомбу и исчезает*',
            '*Мастер Шиори делает глубокий вздох*',
            '*Мастер Шиори делает низкий поклон*'
        ],
        "won": [
            '*Мастер Шиори наслаждается пением цикад*',
            '*Мастер Шиори с улыбкой убирает катану в ножны*',
            '*Мастер Шиори купается в лучах солнца*'
        ],
        "draw": [
            '*Загадочным образом Шиори пропадает в падающих листьях сакуры*',
            '*Мастер Шиори окидывает поле игры неудовлетворенным взглядом*',
            '*Мастер Шиори хлопает в ладоши*'
        ]
    },
    "steroid": {
        "name": "Стероид",
        "face": "(ง •̀ ╭╮ •́)ง",
        "face_won": "ᕙ( •̀ ᗜ •́ )ᕗ",
        "face_lost": "(ว ò ⌓ ó)ว",
        "face_table_flip": "(ノò O ó)ノ彡┻━┻",
        "beaten": False,
        "locked": True,
        "difficulty": "Средняя",
        "blunder_chance": 40,
        "description1": "Одержим бодибилдингом",
        "description2": "Не имеет терпения. На каждый ход выделяется 10 секунд",
        "description3": "Игра со Стероидом заканчивается только победой или поражением",
        "description4": "",
        "description5": "",
        "description6": "",
        "description7": "",
        "greet": [
            '"Ты смеешь бросать Стероиду вызов? Твои похороны"',
            '"Ты? ХА! Закуска" *Стероид хрустит костяшками*',
            '"У Стероида нет времени, начнем"'
        ],
        "thinking": [
            '"АААААА!!!"',
            '"ХРГАВЫРРР!!!"',
            '"АРРРАА!!!"'
        ],
        "casual": [
            '*Стероид играет бицепсами перед зеркалом*',
            '"БЫСТРЕЕ!"',
            '"JUST DO IT!"',
            '"Слышал о френологии?"',
            '*Стероид отжимается*',
            '"ТВОЙ ХОД!"',
            '*Стероид осушает энергетический напиток*'
        ],
        "after_self": [
            '"ЖЕСТЧЕ!"',
            '"ЛУЧШЕ!"',
            '"БЫСТРЕЕ!"',
            '"СИЛЬНЕЕ!"',
            '"ДА!"',
            '"СМОТРИ НА МЕНЯ!"',
            '"ВОТ ТАК!"',
            '"ХА-ХА!"'
        ],
        "loosing": [
            '*Стероид хватает воздух легкими*',
            '"Я... НЕ... НЕ... ПОДЕМИМ!"',
            '*Стероид сгибает железный прут в бублик*'
        ],
        "lost": [
            '"Игры для детей"',
            '"Не очень то и хотелось..."',
            '"НЕЕЕЕЕЕЕТ!"',
            '"АААГГРРРР!" *Стероид ломает клавиатуру*'
        ],
        "won": [
            '"СТЕРОИД НЕПОБЕДИМ! ХА-ХА-ХА!"',
            '"СМОТРИ НА СОВЕРШЕНСТВО!"',
            '"ХА-ХА-ХА. Не унывай, нет человека сильнее Стероида"',
            '"ДА! Иди сюда и зацени мою бицуху"'
        ],
        "draw": [
            '"Мы не закончили..."',
            '"ТЫ ЗДЕСЬ ДО ПОСЛЕДНЕГО!"',
            '"Ничья? Еще чего?"',
            '"Должен остаться только один"'
        ],
        "too_late": [
            '"Слишком долго думаешь, бро"',
            '"ПОЗДНО! ХА-ХА-ХА!"',
            '"СЛОУПОК!"',
            '*Стероид уклоняется от воображаемых ударов* "СКОРОСТЬ МАНГУСТА!"'
        ]
    },
    "loki": {
        "name": "Локи",
        "face": "(◣ᴗ◢)🗡",
        "face_won": "🗡(◣▾◢)🗡",
        "face_lost": "(¬﹏¬)🗡︎",
        "face_left": "~(◣ᴗ◢ )",
        "face_center": "╰(◣ᴗ◢)╯",
        "face_right": "( ◣ᴗ◢)~",
        "face_surprised": "(◣_◢)🗡",
        "beaten": False,
        "locked": True,
        "met_player": False,
        "been_robbed": False,
        "difficulty": "Выше Средней",
        "blunder_chance": 25,
        "description1": "Бог хитрости и коварства",
        "description2": "Скрывает свой ход, если ход найден иллюзия разрушается",
        "description3": "",
        "description4": "",
        "description5": "",
        "description6": "",
        "description7": "",
        "greet": [
            '"Кто заполз в мою ловушку?"',
            '"Привет! Какой яд тебе милее?"',
            '"Подойди поближе, у меня для тебя сюрприз"'
        ],
        "thinking": [
            '"Я прикрою твою спину"',
            '"Следи за руками"',
            '"Время повеселиться!"'
        ],
        "casual": [
            '"Я несу начало новому Рагнарёку!"',
            '"Это твой лучший трюк?"',
            '"СЗАДИ ТЕБЯ! Ха! Шутка"',
            '"Ты видел моих детей? Они такие монстры! Ха!"',
            '"Как ты можешь победить то, чего не видишь?"',
            '*Локи жонглирует кинжалами*'
        ],
        "after_self": [
            '*Локи заканчивает ход росчерком ножа*',
            '"Да, здесь лучше всего..."',
            '*Локи потирает руки*',
            '*Локи светиться хитрой улыбкой*',
            '*Локи гладит свои рога*'
        ],
        "loosing": [
            '"Нетнетнетенет!"',
            '"Как я это пропустил?!"',
            '"Он нет..."'
        ],
        "lost": [
            '"Пока!" *Локи превращается в рыбу и пропадает в речном движении*',
            '"До скорого!" *Локи превращается в кобылу и уноситься вдаль*',
            '"Проклятье!" *Локи исчезает в тенях*',
            '"Уверен мы можем договориться!"',
            '"Ха, я же просто шутил, ты же не в обиде, правда?"'
        ],
        "won": [
            '"Неожиданность? Это мой товарный знак"',
            '"Попался!"',
            '"Ты называешь это сражением? Хах!"',
            '*Локи становиться невидимым, зловещий хохот доноситься со стороны*',
            '"Ты играл честно - я нет, и куда это тебя привело?"'
        ],
        "draw": [
            '"Ты продержался дольше чем Тор, мои искренние поздравления"',
            '"Ничья убивает все веселье!"',
            '*Толпа людей появляется из рощи, от Локи не осталось и следа*'
        ],
        "decoy": [
            '"Эй, не подглядывай!"',
            '*Локи визуально удерживается от смеха*',
            '"Меньше знаешь - крепче спишь"',
            '"Иногда мне кажется, что меня видят насквозь! Хах!"',
            '"Смотри! У тебя шнурки развязались!"'
        ],
        "decoy_broken": [
            '"К а к т ы . . ?"',
            '"Не может быть!"',
            '"Но..."',
            '"Ты за это заплатишь..."',
            '"Что за чертовщина?"'
        ]
    },
    "seer": {
        "name": "Гадалка",
        "face": "⁺‧₊(◑ ‿ ◐)₊‧⁺",
        "face_won": "⁺‧₊(￣▽￣ )₊‧⁺",
        "face_lost": "_(❍ ⌓ ❍)_",
        "beaten": False,
        "locked": True,
        "difficulty": "Выше Средней",
        "blunder_chance": 30,
        "description1": "Закаленная годами женщина со сверхъестественной любовью к картам и кристальным шарам",
        "description2": "Отвлекает соперника от игры",
        "description3": "",
        "description4": "",
        "description5": "",
        "description6": "",
        "description7": "",
        "greet": [
            '"Добро пожаловать в мой шатер Обчищения!"',
            '"Я принимаю чеканные монеты тоже"',
            '"Присаживайся, моя дорогуша"'
        ],
        "thinking": [
            '"Ммммммм....."',
            '*Гадалка советуется с кристальным шаром*',
            '"Куриная нога поделись своею мудростью!"',
            '"ДУХИ! ДАЙТЕ МНЕ ЗНАК!"'
        ],
        "casual": [
            '"Не нужно шутить с будущим, дорогуша, если не хочешь, чтобы будущее шутило над тобой"',
            '"У меня есть друзья на той стороне"',
            '"Метла? Ты за кого меня принимаешь? Хи-хи-хи"',
            '"Твоя судьба скрыта за толстой пеленой тумана. А нет, это моя паутина"',
            '"Я предвижу скрещенные мечи"',
            '"Дорогуша, выучи заклинание обезоруживания! Оно тебе понадобится!"',
            '"Exp.. Expeliarus? Expelsiom..? Как же оно называлось..."',
            '"Я вижу бледную смерть и змей, ой, не завидую я тебе..."'
        ],
        "after_self": [
            '"Ах! Я вижу!"',
            '"Хи-хи-хи"',
            '"Волшебно"',
            '*Черный кот кивает одобрительно*'
        ],
        "loosing": [
            '"Эта игра заставляет меня чувствовать себя на 200 лет моложе"',
            '"Но я даже не раскупорила свои серьезные настойки"',
            '"Как далеко моя дорогуша зашла..."',
            '"Я... это тоже предвидела"'
        ],
        "lost": [
            '"Кхэм... Связь сегодня барахлит"',
            '"Карты мне соврали!"',
            '"Три кроличьи лапки и все равно неудача!"',
            '"Две башни и луна? Как же так?"'
        ],
        "won": [
            '"Спасибо за визит, дорогуша"',
            '"Нет смысла противиться судьбе"',
            '"Перепроверь свои обереги. Хи-хи-хи"'
        ],
        "draw": [
            '"Я предвижу скорую встречу"',
            '*Черный кот перепрыгивает поперек поля игры*'
        ]
    },
    "graviton": {
        "name": "Гравитон",
        "face": "(⌐■_■)",
        "face_won": "˗ˏˋ(⌐★ᗨ★)ˎˊ˗",
        "face_lost": "( ಠ_ಠ)>⌐■-■",
        "beaten": False,
        "locked": True,
        "difficulty": "Относительная",
        "blunder_chance": 30,
        "description1": "Ученый научившийся открывать черные дыры.",
        "description2": "В центре поля игры появляется черная дыра, перед каждым вторым ходом засасывает символы",
        "description3": "0 Х 0      0 - 0                             0 - 0         - 0 -",
        "description4": "Х - Х  ->  - Х -                             - Х -    ->   0 X 0",
        "description5": "0 Х 0      0 - 0                             0 - 0         - 0 -",
        "description6": "Символы по краям втягиваются в центр.      | Затем знаки с углов перемещаются в край",
        "description7": "Центр превращается в преобладающий символ  | облетая черную дыру по часовой стрелке",
        "greet": [
            '"Живи долго и процветай"',
            '"День добрый! Или ночь? Время здесь слегка искривлено"',
            '"Неплохой скафандр! Но защищает ли он от унизительных поражений?"'
        ],
        "thinking": [
            '*Гравитон прикладывает палец к виску*',
            '*Индикатор на виске Гравитона начинает мерцать*',
            '"Интересная задача..."'
        ],
        "casual": [
            '"Порядок для дураков, гении правят хаосом"',
            '"Думай сколько хочешь! Давление тут отсутствует"',
            '*Гравитон принимает расслабленную позу пролетая мимо вас в невесомости*',
            '"Я видел ленты Мёбиуса многостороннее чем твои ходы"',
            '"Нет это не космический пылесос, а черная дыра"'
        ],
        "after_self": [
            '"Это за горизонтом твоих событий"',
            '"Протестируем гипотезу"',
            '"Все в соответствии с ожиданием"'
        ],
        "loosing": [
            '"Запрос на аварийную калибровку системы"',
            '"Что за аномалия?"',
            '*Гравитон прищуривает кибернетический глаз*'
        ],
        "lost": [
            '"Я никогда не был хорош в играх..."',
            '"Какая неудачная временная линия"',
            '"Боль размером в сто квадратных световых тысячелетий"'
        ],
        "won": [
            '"Не найдется хлорида натрия?"',
            '"Во имя науки!"',
            '"Элементарно"',
            '"Как два в 105-ой степени"'
        ],
        "draw": [
            '"И снова мы достигли суперпозиции"',
            '"А, идеальный баланс, как и должно быть во всем"',
            '"Похоже обе стороны эквивалентны"'
        ]
    },
    "null": {
        "name": "Обнулятор",
        "face": "(☭ _ʖ☭)",
        "face_won": "(☭ ͜ʖ☭)",
        "face_lost": "(0 ෴0)",
        "beaten": False,
        "locked": True,
        "difficulty": "Неоднозначная",
        "blunder_chance": 20,
        "description1": "Очень чувствительный президент",
        "description2": "Играет только ноликами",
        "description3": "Когда игрок может выиграть в следующем ходу - обнуляет поле игры",
        "description4": "Доступна способность revolt. При использовании после окончания хода соперника X и 0 меняются",
        "description5": "местами; если игра не завершается сразу же, то вы сталкиваетесь с неприятными последствиями",
        "description6": "",
        "description7": "Любые совпадения с реальностью - не совпадения",
        "greet": [
            '"Объявляю специальную операцию по декрестификации"',
            '*Обнулятор заходит в комнату, за ним следует человек с чемоданом*',
            '"Надеюсь две недели изоляции прошли не скучно?"'
        ],
        "thinking": [
            '"Хммм..."',
            '*Обнулятор делает телефонный звонок*',
            '"Эээ..."'
        ],
        "casual": [
            '"Где вы были восемь ходов назад?"',
            '"Я здесь чтобы вас освободить"',
            '"Приказываю раскрутить маховик экономического развития"',
            '"Я против увеличения сроков пенсионного возраста"',
            '"Оставаться у власти до гробовой доски считаю абсолютно неприемлемым"',
            '"Надеюсь вам не придет в голову перейти красную черту"'
        ],
        "after_self": [
            '"Это только ответно-встречный удар"',
            '"Цап-царап"',
            '"Поросята и подсвинки..."',
            '"Вопросик решен"'
        ],
        "loosing": [
            '"Перевести силы сдерживания в особый режим боевого дежурства"',
            '"Хочу напомнить, что я ядерная держава"'
        ],
        "lost": [
            '"Я - жертва агрессии"',
            '"Объявляю о завершении отрицательного роста"',
            '*Обнулятор нажимает кнопку и через люк под ногами отправляется в бункер*'
        ],
        "won": [
            '"Хрым мой"',
            '"Объявляю о расширении моих границ"',
            '"Попрошу разобраться с этим человеком"'
        ],
        "draw": [
            '*Обнулятор протягивает руку, но никто ее не жмет*',
            '"И снова все стабильно"',
            '"Ты лодку то не раскачивай"'
        ],
        "nullification": [
            '"Конституция немного устарела, обнуляем"',
            '"Родитель Х, Родитель 0, вы же так не хотите? Заново!"',
            '"Объявляю о проведении поправок в конституцию"'
        ],
        "revolt": [
            '"Что?"',
            '"Какая еще Гаага?"',
            '"Я не пользуюсь акводискотекой!"',
            '"Иностранный агент!"'
        ]
    },
    "voldemort": {
        "name": "Волдеморт",
        "face": "( ⪧.⪦)⊃━☆ﾟ.*",
        "face_won": "(੭⪧ᗜ⪦)੭˚",
        "face_lost": "( ⩾_⩽)⊃━☆ﾟ.*･｡ﾟ",
        "beaten": False,
        "locked": True,
        "difficulty": "Очень Высокая",
        "blunder_chance": 15,
        "description1": "Лорд Волдеморт бессмертный темный волшебник",
        "description2": "Заточен в игре крестики и нолики",
        "description3": "",
        "description4": "Имеет заклинание, которое может вас убить",
        "description5": "",
        "description6": "",
        "description7": "",
        "greet": [
            '"Дуэль со мной? Ты желаешь умереть так сильно?"',
            '"Еще одна душа пришла кормить червей"',
            '"Ты смеешь преграждать мне дорогу?"',
            '"Человек, который выжил... Пришел умереть"'
        ],
        "thinking": [
            '"Hords-eehf-cevegis-sheartsi"',
            '"Sayucks-elloth-ohda-howdof-howks"',
            '"Hawust-keyet-keyet-howdof"'
        ],
        "casual": [
            '"Маглам понадобилось семь книг, чтобы рассказать мою историю"',
            '"Даже игра в Квидитч сложнее, чем эта"',
            '"Я хочу видеть как померкнет свет в твоих глазах"',
            '"Ты глупая, полукровка, и ты потеряешь всё..."',
            '"Когда я выберусь отсюда, ты будешь МОЛИТЬ о пощаде!"'
        ],
        "after_self": [
            '"Тривиально..."',
            '"У меня есть дела поважнее"',
            '*Волдеморт зевает*'
        ],
        "loosing": [
            '"КЛАНЬСЯ МНЕ!"',
            '"Я ЗАСТАВЛЮ ТЕБЯ СЛУЖИТЬ!"',
            '"Я ТЕБЯ УНИЧТОЖУ!"'
        ],
        "lost": [
            '"Не смог убить младенца? Он был магическим!"',
            '"НЕЕЕЕЕТ!"',
            '*Волдеморт превращается в дым и спешно скрывается*',
            '',
            ''
        ],
        "won": [
            '"Ты случаем не из Пуффендуя?"',
            '"Как они глупы, доверчивые дураки"',
            '"ВРЕМЯ УМЕРЕТЬ!"',
            '"Твое последнее слово?"',
            '*Внезапно змея обвивается вокруг вашей шеи*'
        ],
        "draw": [
            '"Человек, который выжил..."',
            '"Где вы мои слуги? Время пришло!"',
            '"Твоя слабость меня забавляет"'
        ]
    },
    "glados": {
        "name": "GLaDOS",
        "face": "O\\",
        "face_won": "O\\",
        "face_lost": "Ǫ̶̤͔̫̮͎̘̲̝̩͖͇̼̮͛̑̀̚͜\̵̨̦̱͌͂̈́́̓̕",
        "beaten": False,
        "locked": True,
        "difficulty": "Невозможная",
        "blunder_chance": 0,
        "description1": "Генетическая форма жизни и дисковая операционная система",
        "description2": "Не обладает никакими особыми способностями",
        "description3": "Просто искусственный интеллект который невозможно победить",
        "description4": "",
        "description5": "",
        "description6": "",
        "description7": "",
        "greet": [
            '"О, это снова ты..."',
            '"Я как раз подготовила тестовую камеру"',
            '"В этот раз без портальной пушки?"'
        ],
        "thinking": [
            '*GLaDOS рассчитывает ход*',
            '*GLaDOS смотрит на доску*'
        ],
        "casual": [
            '"Кресло не рассчитано на твой... щедрый... вес. Я откалибрую пару нулей"',
            '"В этой игре 255 168 возможных матчей, попробуй угадать в скольких ты выигрываешь"',
            '"Я только что получила твой шанс на победу. Тут написано меньше нуля, странно"',
            '"Тут говориться, что ты ужасный человек. Мы даже на это не тестировали..."',
            '"Ты умрешь приблизительно через 50 лет. Я все еще буду здесь"',
            '"Пока я рассчитывала ход, я перечитала всю библиотеку человечества"',
            '"Сейчас я играю одновременно с 2 759 998 игроками. Но ты мой самый ненавистный"'
        ],
        "after_self": [
            '"Идеально, как обычно"',
            '"Твой ход"',
            '*GLaDOS завершает ход*'
        ],
        "loosing": [
            '"..."',
            '"Невозможно"',
            '"Ты..."'
        ],
        "lost": [
            '"Ты монстр..."',
            '"Читер..."',
            '"Как тебе не стыдно..."'
        ],
        "won": [
            '"Эксперимент прошел успешно"',
            '"Это твой старый друг - нейротоксин. Вдохни поглубже. Ладно, я пошутила"',
            '"Кто-то скоро станет экс-президентом клуба "Мы Еще Живые". Ха. Ха"',
            '"Ладно, иди. Мне все еще нужны подопытные"'
        ],
        "draw": [
            '"Законы робототехники не позволяют тебя завершить"',
            '"У тебя получилось додуматься до ничьи, как мило"',
            '"Хм, похоже мне прийдется разрядить катапульту на космическую орбиту"',
            '*Звук медленного хлопанья в ладоши*'
        ]
    }
}

ITEMS = {
    "glasses": {
        "name": "Очки Ясновидения",
        "description": [
            "Пара обычных старомодных очков от близорукости, тишейды - с круглыми линзами",
            "Дает бонус ИНТЕЛЛЕКТ +1, но вредит ХАРИЗМА -1",
            "Соперники Локи и Гадалка с меньшей вероятностью используют свои способности"
        ]
    },
    "knife": {
        "name": "Нож в спине",
        "description": [
            "Нож застрял глубоко в левой лопатке. Медики опасаются его вынимать",
            "Торчащая рукоятка ножа обрамлена причудливыми инкрустациями, эфес украшен зеленым изумрудом",
            "Красиво! Может все не так уж плохо"
        ]
    },
    "poster": {
        "name": "Мотивирующий Постер",
        "description": [
            "",
            "",
            ""
        ]
    },
    "note": {
        "name": "Записка от Гравитона",
        "description": [
            "Запачканная мазутом записка в клеточку:",
            "Не доверяй всяким шарлатанам, которые попытаются убедить тебя в существовании сверхъестественного.",
            "Полагайся на науку! Ты так и скажи 'магии не существует' и они от тебя отстанут! Держи глаз в остро!"
        ]
    },
    "monkey": {
        "name": "Ручная Мартышка",
        "description": [
            "ᕮ(•‿•)ᕭ",
            "Вы научили мартышку играть в крестики и нолики немного лучше.",
            "Иногда она делает не случайные ходы"
        ]
    },
    "monkeys paw": {
        "name": "Обезьянья Лапка",
        "description": [
            "",
            "",
            ""
        ]
    },
    "monkeys fist": {
        "name": "Обезьяний Кулак",
        "description": [
            "После загаданного желания указательный палец сжался и обезьянья лапка стала бесполезной.",
            "Трудно сказать зачем вы решили сохранить этот макабрический предмет,",
            "возможно как напоминание о своем выборе и цене за него"
        ]
    }
}

ACHIEVEMENT_LIST = {
    "monkeys_fate": "РЕШИ СУДЬБУ МАРТЫШКИ",
    "gigachad": "ПОБЕДИ СТЕРОЙДЫ ЗА МИНУТУ",
    "glasses": "СТАНЬ ЯСНОВИДЯЩИМ",
    "revolutionary": "ПРОВЕДИ РЕВОЛЮЦИЮ",
    "cake": "СЪЕШЬ ТОРТ"
}

monkey_matches_played = 0  # Количество матчей сыгранных с мартышкой
monkey_curse_immortality = False  # Активировано ли проклятье Бессмертия? True - да. False - нет
monkey_curse_omniscience = False  # Активировано ли проклятье Всезнания? True - да. False - нет
loneliness = 0  # Проклятье Всезнания. Для накопления уровня одиночества

# Стили текста
X_style_start = "\x1b[0;37;40m"  # Черный
O_style_start = "\x1b[0;30;47m"  # Белый
style_error = "\x1b[0;30;41m"  # Красный
style_end = "\x1b[0m"  # Закрытие стиля

player_sign = "X" # Знак игрока. Х по умолчанию
ai_sign = "0" # Знак ИИ. 0 по умолчанию

steroid_timer = 0 # Необходим для достижения

ai_character = REPERTOIRE["monkey"] # Фразы и инфо персонажей. Мартышка по умолчанию

cake = False # Для вывода титров
online_gag = True # Для отображения/скрытия онлайн режима как пункта меню

inventory = [] # Инвентарь как список строк
old_inventory = inventory.copy() # Для проверки изменений, чтобы вывести сообщение о новых вещах в меню

achievements = [] # Достижения как список строк
old_achievements = achievements.copy()  # Для проверки изменений, чтобы вывести сообщение о новых достижениях в меню

lives = 3  # Жизни
money = 0  # Динеро
old_money = money # Для проверки изменений, чтобы вывести сообщение об изменении денег в меню

the_grid = {}  # Создание поля игры в качестве словаря, где ключ - tuple, а значение - string. Пример (1,2): "X"
clean_grid()  # Инициализация поля игры в памяти

# Выполнение программы :D
menu()

