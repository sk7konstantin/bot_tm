from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

kb1 = KeyboardButton(text='Получить случайную статью')
kb2 = KeyboardButton(text='Показать кол-во оставшихся статей')
kb3 = KeyboardButton(text='Обновить БД')
kb4 = KeyboardButton(text='Искать статью')

# kb_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_user = ReplyKeyboardMarkup(resize_keyboard=True)
kb_user.row(kb1, kb4).row(kb2, kb3)

# Кнопки для выбора законодательства
kb_code1 = KeyboardButton(text='УК РФ')
kb_code2 = KeyboardButton(text='ГК РФ')
kb_code3 = KeyboardButton(text='ГПК РФ')
kb_code4 = KeyboardButton(text='Отмена')

kb_code_search = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_code_search.row(kb_code1, kb_code2, kb_code3).add(kb_code4)

# Кнопка отмены выбора
kb_code_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_code_cancel.add(kb_code4)

