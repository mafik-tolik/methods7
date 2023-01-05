from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from random import randint
from datetime import datetime


async def hi_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Привет, {update.effective_user.first_name}!')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'/hello\n/help\n/abc\n/candy\n/game\n/calculator\n/phone_book')


async def abc_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.split()
    if len(text) < 3:
        await update.message.reply_text(f'Введите сообщение в формате: /abc <что удалить> <текст>')
    else:
        await update.message.reply_text(f'Результат: {" ".join(list(filter(lambda x: text[1] not in x, text[2:])))}')


async def candy_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    if update.message.text == '/candy':
        with open('candy.txt', 'w', encoding='utf-8') as file:
            file.write('2021')
        await update.message.reply_text(f'Новая игра. Введите ваш ход в формате: /candy <количество конфет>:')
    else: 
        step = 29

        with open('candy.txt', 'r', encoding='utf-8') as file:
            quantity = int(file.read())

        player = int(update.message.text.split()[1])
        if player > 28 or player < 1:
            await update.message.reply_text(f'Играй честно, ход должен быть от 1 до 28. Попробуй ещё раз:')
            return
        quantity -= player
        await update.message.reply_text(f'Остаток конфет: {quantity}')
        if quantity <= 0:
            await update.message.reply_text('Ура, ты победил!')
            with open('candy.txt', 'w', encoding='utf-8') as file:
                file.write('2021')
            return    
        if quantity < 29:
            bot = quantity
        else:
            if quantity % step == 0:
                bot = randint(1, 28)
            else:
                bot = quantity % step
        await update.message.reply_text(f'Ход бота: {bot}')
        quantity -= bot
        if quantity <= 0:
            await update.message.reply_text('Победил бот!')
            with open('candy.txt', 'w', encoding='utf-8') as file:
                file.write('2021')
            return
        await update.message.reply_text(f'Остаток конфет: {quantity}')
        with open('candy.txt', 'w', encoding='utf-8') as file:
            file.write(f'{quantity}')
        await update.message.reply_text(f'Твой ход:')


def win(k, tab):
    if (tab[0][0] == k and tab[0][1] == k and tab[0][2] == k)\
            or (tab[1][0] == k and tab[1][1] == k and tab[1][2] == k)\
            or (tab[2][0] == k and tab[2][1] == k and tab[2][2] == k)\
            or (tab[0][0] == k and tab[1][0] == k and tab[2][0] == k)\
            or (tab[0][1] == k and tab[1][1] == k and tab[2][1] == k)\
            or (tab[0][2] == k and tab[1][2] == k and tab[2][2] == k)\
            or (tab[0][0] == k and tab[1][1] == k and tab[2][2] == k)\
            or (tab[0][2] == k and tab[1][1] == k and tab[2][0] == k):
        return 1
    else:
        return 0


async def game_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    if update.message.text == '/game':
        with open('game.txt', 'w', encoding='utf-8') as file:
            file.write('₁, ₂, ₃\n₄, ₅, ₆\n₇, ₈, ₉')
        with open('game1.txt', 'w', encoding='utf-8') as file:
            file.write('0')
        await update.message.reply_text(f'Новая игра. Вводите ходы в формате: /game <номер ячейки от 1 до 9>:')
        await update.message.reply_text('₁, ₂, ₃\n₄, ₅, ₆\n₇, ₈, ₉')
        await update.message.reply_text('Ход 1-го игрока (крестики)')

    else: 
        moves = {'1': (0, 0), '2': (0, 1), '3': (0, 2), '4': (1, 0), '5': (1, 1),
         '6': (1, 2), '7': (2, 0), '8': (2, 1), '9': (2, 2)}

        with open('game.txt', 'r', encoding='utf-8') as file:
            table = list(map(lambda x: x.split(', '), file.read().splitlines()))

        with open('game1.txt', 'r', encoding='utf-8') as file:
            motion = file.read()

        if motion == '0':
            step = update.message.text.split()[1]
            table[moves[step][0]][moves[step][1]] = 'X'
            text1 = (str(table)).replace("'], ['", "\n").replace("[", "").replace("]", "").replace("'", "")
            await update.message.reply_text(f'{text1}')
            if win('X', table) == 1:
                await update.message.reply_text('Победил 1-ый игрок (крестики)!')
                return
            with open('game1.txt', 'w', encoding='utf-8') as file:
                file.write('1')
            await update.message.reply_text('Ход 2-го игрока (нолики)')
            
        if motion == '1':
            step = update.message.text.split()[1]
            table[moves[step][0]][moves[step][1]] = '0'
            text1 = (str(table)).replace("'], ['", "\n").replace("[", "").replace("]", "").replace("'", "")
            await update.message.reply_text(f'{text1}')
            if win('0', table) == 1:
                await update.message.reply_text('Победил 2-ой игрок (нолики)!')
                return
            with open('game1.txt', 'w', encoding='utf-8') as file:
                file.write('0')
            await update.message.reply_text('Ход 1-го игрока (крестики)')

        flag = False
        for i in table:
            for j in i:
                if j != 'X' and j != '0':
                    flag = True
                    break

        if flag == False:
            await update.message.reply_text('Ничья!')
            return

        with open('game.txt', 'w', encoding='utf-8') as file:
                    for i in table:
                        file.write(f'{", ".join(i)}\n')


def log_operation(left_operand, right_operand, operation, result):
    with open('calculator.txt', 'a') as file:
        oper_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        file.write(f'{oper_time} -> {left_operand} {operation} {right_operand} = {result}\n')


async def calculator_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text == '/calculator':
        await update.message.reply_text(f'Введите формулу в формате: /calculator <racional_or_complex> <формула (например: 1 + 2)>')
    else:
        text = update.message.text.split()

        if len(text) == 5:
            if '/calculator racional' in update.message.text:
                a = float(text[2])
                oper = text[3]
                b = float(text[4])
            elif '/calculator complex' in update.message.text:
                a = complex(text[2])
                oper = text[3]
                b = complex(text[4])

            if oper == '+':
                res = a + b

            elif oper == '-':
                res = a - b

            elif oper == '/':
                res = a / b

            elif oper =='*':
                res = a * b

            await update.message.reply_text(f'Результат: {res}')
            log_operation(a, b, oper, res)
        
        else:
            await update.message.reply_text(f'Неверный ввод, возможно пропущен пробел. Попробуйте ещё раз')


async def phone_book_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text == '/phone_book':
        await update.message.reply_text(f'Введите команду в формате: /phone_book <export_or_import> <ФИО, телефон, комментарий через запятую (export), либо данные для поиска (import)>')
    else:
        
        if '/phone_book export' in update.message.text:
            text = update.message.text[19:].split(', ')
            with open('phone_book.txt', 'a', encoding='utf-8') as file:
                file.write(f'{", ".join(text)}\n')
            await update.message.reply_text(f'Сделана запись: {", ".join(text)}')

        elif '/phone_book import' in update.message.text:
            list1 = []
            search = update.message.text[19:]
            with open('phone_book.txt', 'r', encoding='utf-8') as file:
                list0 = file.read().splitlines()
                for i in range(len(list0)):
                    if search in list0[i]:
                        list1.append(list0[i])

            if len(list1) == 1:
                await update.message.reply_text(f'Запись по запросу "{search}":\n{list1[0]}')

            elif len(list1) > 1:
                await update.message.reply_text(f'Записи по запросу "{search}":')
                for i in range(len(list1)):
                    await update.message.reply_text(f'{list1[i]}')
            else:
                await update.message.reply_text(f'Записи не найдены по запросу "{search}"')
