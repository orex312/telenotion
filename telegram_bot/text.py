# Файл с тестовыми сообщениями для всего проекта целиком (всё берется из одного места, мб потом разобью)

text_tasks_list = "Вот список твоих задач"
text_new_task = "Новая задача"

def main_menu (user_name):
    return "Привет, {name}, чем могу помочь ?".format(name = user_name)

def welcom_text (user_name):
    return "Приветствую, я бот для заметок, начнём работу".format(name = user_name)