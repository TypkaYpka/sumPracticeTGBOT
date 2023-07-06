import sqlite3
import telebot
from telebot import types
from tasks_checker import TaskChecker
import re
# from telegram.ext import Updater, CommandHandler


bot = telebot.TeleBot('6287597880:AAHT67SRgFyIyJv4V5ThkNz5EQrW5rbsLQg')

total_score = 0

# подключаемся к базе данных
conn = sqlite3.connect('C:\\Users\missc\OneDrive\Рабочий стол\db\database.db', check_same_thread=False)
cursor = conn.cursor()



@bot.message_handler(commands=['start'])
def start(message):
    # Обработчик команды /start
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('1 тест')
    button2 = telebot.types.KeyboardButton('2 тест')
    button3 = telebot.types.KeyboardButton('3 тест')
    button4 = telebot.types.KeyboardButton('Задача')
    keyboard.add(button1, button2, button3, button4)
    bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAEJk5Fko3GkFzM4yEbIAAFh5ITRpMKHWdgAAkADAAK1cdoGuRLw3B1VGFwvBA')
    bot.send_message(message.chat.id, 'Рады вас здесь видеть! Выберите тест:', reply_markup=keyboard)
   

@bot.message_handler(func=lambda message: message.text in ['Задача'])
def callback_message(callback):
	# global n
        
	# strr = cursor.execute('SELECT qestion FROM tests WHERE id = 16')
	# bot.send_message(callback.message.chat.id, strr)
	# bot.delete_message(callback.message.chat.id, callback.message.message_id)
	# n += 1
	# bot.register_next_step_handler(callback.message,  otv)	
			
	# global n
	

			
			
	strr = cursor.execute('''SELECT question FROM tests WHERE test_id = 10''')
	bot.send_message(callback.message.chat.id, strr)
	bot.delete_message(callback.message.chat.id, callback.message.message_id)
	bot.register_next_step_handler(callback.message,  otv)	
			# idtask = i	
		

	

def otv(message):
	global tempr
	
	# max
	if (tempr == 1):
		user_solution = message.text
		test_cases = [
		([0, 2, 3, 4, 5], 5),
		([-1, -5, 0, -10], 0),
		([100, 200, 50, 300], 300),
		([0, 0, 0, 0], 0),
		]
		bot.send_message(message.chat.id,TaskChecker(user_solution, test_cases).check())
		bot.send_message(message.chat.id, "Ты молодец!")
    
    

    
@bot.message_handler(func=lambda message: message.text in ['1 тест', '2 тест', '3 тест'])
def handle_test(message):
    # Обработчик выбора теста
    test_id = int(message.text.split()[0])  # Получаем номер теста из текста сообщения
    user_id = message.chat.id  # Получаем идентификатор пользователя из сообщения
    # Создаем структуру для хранения результатов пользователя
    user_results = {'chat_id': message.chat.id, 'name': message.chat.first_name,  'result': 0}
# Сохраняем результаты пользователя в базе данных
    save_user_results(user_results)
    
    
    
    query = "SELECT question, answer FROM tests WHERE test_id = ?"
    cursor.execute(query, (test_id,))
    questions = cursor.fetchall()
    
    if len(questions) > 0 :
        bot.send_message(message.chat.id, 'Начинаем тест!')
        start_test(user_id, test_id, questions, 0, 0)
  
        
def save_user_results(user_results):
    cursor.execute("INSERT INTO users(chat_id, name, result) VALUES (?, ?, ?)", (user_results['chat_id'], user_results['name'], user_results['result']))
    conn.commit()


def start_test(user_id, test_id, questions, current_question_index, total_score):
    if current_question_index < len(questions):
        question, correct_answer = questions[current_question_index]

        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton('1', callback_data=f'1 {test_id}') # Добавляем test_id в callback_data
        button2 = telebot.types.InlineKeyboardButton('2', callback_data=f'2 {test_id}')
        button3 = telebot.types.InlineKeyboardButton('3', callback_data=f'3 {test_id}')
        button4 = telebot.types.InlineKeyboardButton('4', callback_data=f'4 {test_id}')
        keyboard.add(button1, button2, button3, button4)

        bot.send_message(user_id, f'Вопрос {current_question_index + 1}: {question}', reply_markup=keyboard)
        # otv()
    else:

        # otv()
       # Все вопросы в тесте пройдены
        bot.send_message(user_id, f'Тест завершен. Правильных ответов: {total_score}')
        # Сохранение результата пользователя в БД
        
        
        query = "UPDATE users SET result = ? WHERE chat_id = ?"
        # query = "UPDATE users SET result = ? WHERE user_id = ?"
        cursor.execute(query, (total_score, user_id))
        conn.commit()
        start(user_id) # Возвращаемся в главное меню

@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    # Обработчик выбора ответа
    user_id = call.from_user.id
    selected_answer, test_id = map(int, call.data.split())

    current_question_index = int(call.message.text.split()[1].replace(':', '')) - 1 

    query = "SELECT answer FROM tests WHERE test_id = ? AND id = ?" # Добавляем условие по id вопроса
    cursor.execute(query, (test_id, current_question_index + 1)) # Передаем id вопроса в параметры
    correct_answer = cursor.fetchone()

 # Объявляем и инициализируем переменную total_score
    global total_score   
    if correct_answer is not None and selected_answer == correct_answer[0]:
        bot.send_message(user_id, 'Верно!')
        total_score += 1 # Увеличиваем счет правильных ответов но работать оно не хочет
        query = "UPDATE users SET result = ? WHERE chat_id = ?"
        cursor.execute(query, (total_score, user_id))
        conn.commit()
    else:
        bot.send_message(user_id, 'Неверно!')

    query = "SELECT question, answer FROM tests WHERE test_id = ?"
    cursor.execute(query, (test_id,))
    questions = cursor.fetchall()
    start_test(user_id, test_id, questions, current_question_index + 1, total_score)



if __name__ == '__main__':
    bot.polling()