import json
import time


def args_to_string(*args, **kwargs):
    return f'{json.dumps(args)}_{json.dumps(kwargs)}'


def logging_decorator(**path):
    def decorator(function):
        log_file = {
            'start_time_function': time.asctime(),
            'function_name': function.__name__
        }

        def logging(*args, **kwargs):
            log_file.update(arguments=args_to_string(*args, **kwargs))
            log_file.update(result=function(*args, **kwargs))
            if path:
                with open(path['path'], 'a', encoding='utf-8') as file:
                    file.write(json.dumps(log_file, ensure_ascii=False))
            else:
                pass
            return function

        return logging

    return decorator


class Contact:

    def __init__(self, name, surname, phone, favorite=None, *add_phone, **add_info):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.favorite = favorite
        self.add_phone = add_phone
        self.add_info = add_info
        self.contact_list = {'name': self.name, 'surname': self.surname, 'phone': self.phone, 'favorite': self.favorite,
                             'add_phone': self.add_phone, 'add_info': self.add_info}

    def __str__(self):
        main_info = f'Имя: {self.name}\nФамилия: {self.surname}\nТелефон: {self.phone}\n'
        if not self.favorite:
            favorites = 'В избранных: нет\n'
        else:
            favorites = 'В избранных: да\n'
        add_phones = str()
        if not self.add_phone:
            pass
        else:
            for add_phone in self.add_phone:
                add_phones += f'\t\tдоп. телефон : {add_phone}\n'
        add_infos = str()
        if not self.add_phone and not self.add_info:
            pass
        else:
            add_infos = str('Дополнительная информация:\n')
        if not self.add_info:
            pass
        else:
            for key, value in self.add_info.items():
                add_infos += f'\t\t{key} : {value}\n'
        total_str = main_info + favorites + add_infos + add_phones
        return total_str


class PhoneBook:

    def __init__(self, name_book):
        self.name_book = name_book
        self.contact = {}
        self.contact_list = []

    def add_contact(self, name, surname, phone, favorite=None, *add_phone, **add_info):
        self.contact[name] = Contact(name, surname, phone, favorite, *add_phone, **add_info)
        self.contact_list.append(self.contact[name].contact_list)
        return self.contact_list

    def show_favorites(self, favorite):
        favorites_list = []
        for contact in self.contact_list:
            if contact['favorite'] == favorite:
                favorites_list.append(contact)
        if not favorites_list:
            print('Отсутсвуют пользователи соотв. критериям поиска (избранные контакты)!')
        else:
            print('Условиям поска соответсвуют следующие контакты (избранные контакты):')
            for favorite_contact in favorites_list:
                print(favorite_contact['name'], favorite_contact['surname'])

    def show_contact(self, name, surname):
        search_status = 0
        for contact in self.contact_list:
            if contact['name'] == name and contact['surname'] == surname:
                search_status = 1
                print('Вывожу иноформацию по пользователю: ')
                if not contact['add_phone'] and not contact['add_info']:
                    print(Contact(contact['name'], contact['surname'], contact['phone'], contact['favorite']))
                elif not contact['add_phone']:
                    print(Contact(contact['name'], contact['surname'], contact['phone'], contact['favorite'],
                                  **contact['add_info']))
                elif not contact['add_info']:
                    print(Contact(contact['name'], contact['surname'], contact['phone'], contact['favorite'],
                                  *contact['add_phone']))
                else:
                    print(Contact(contact['name'], contact['surname'], contact['phone'], contact['favorite'],
                                  *contact['add_phone'], **contact['add_info']))
        if search_status == 0:
            print('Соответсвий не найдено!')

    def delete_contact(self, name, surname):
        for contact in self.contact_list:
            if contact['name'] == name and contact['surname'] == surname:
                self.contact_list.remove(contact)
        print('Контакт удален!')


@logging_decorator(path='log_file.json')
def main():
    phone_book = PhoneBook('PhoneBook')
    print('Читаю PhoneBook.json...')
    with open('PhoneBook.json', encoding='utf-8') as file:
        phone_book.contact_list = json.loads(file.read())
    command = str()
    while command != 'q':
        command = input(
            'Введите команду (q - выйти, sp - поиск и вывод информации, a - добавление контакта, f - поиск и вывод '
            'избранных номеров, d - удаление контактов): ')
        if command == 'sp':
            name = input('Введите имя: ')
            surname = input('Введите фамилию: ')
            phone_book.show_contact(name, surname)
        elif command == 'a':
            name = input('Введите имя: ')
            surname = input('Введите фамилию: ')
            phone = input('Введите номер телефона: ')
            favorite = input('Этот контакт избранный? (True - избранный, False - не избранный): ')
            add_phone = str()
            additional_phones = list()
            add_info_name = str()
            add_info_context = str()
            additional_infos_total = dict()
            while add_phone != 'q':
                add_phone = input('Введите доп. номер (q - выйти): ')
                if add_phone != 'q':
                    additional_phones.append(add_phone)
                elif add_phone == 'q':
                    break
            while add_info_name != 'q' or add_info_context != 'q':
                add_info_name = input(
                    'Введите имя доп. информаци, например, для почты - mail (q - выйти): ')
                if add_info_name != 'q':
                    add_info_context = input('Введите значение, например, для почты - aaogoltcov@mail.ru (q - выйти): ')
                    if add_info_context != 'q':
                        additional_infos = {add_info_name: add_info_context}
                        additional_infos_total.update(additional_infos)
                elif add_info_name == 'q':
                    break
            phone_book.add_contact(name, surname, phone, favorite, *additional_phones, **additional_infos_total)
            print('Информация записана!')
        elif command == 'f':
            favorite = input('Введите какие пользователей вы хотите найти (True - избранные, False - не избранные): ')
            phone_book.show_favorites(favorite)
        elif command == 'd':
            name = input('Введите имя: ')
            surname = input('Введите фамилию: ')
            phone_book.delete_contact(name, surname)
        elif command == 'q':
            pass
        else:
            print('Неизвестная комманда!')
            pass
    print('Записываю PhoneBook.json и выхожу...')
    with open('PhoneBook.json', 'w') as file:
        file.write(json.dumps(phone_book.contact_list))
    return phone_book.contact_list


main()

example_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore ' \
               'et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut ' \
               'aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse ' \
               'cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa ' \
               'qui officia deserunt mollit anim id est laborum. '


@logging_decorator(path='log_file.json')
def adv_print(args, **kwargs):
    max_line = int()
    start = str()
    in_file = str()
    for key, value in kwargs.items():
        if key == 'max_line':
            max_line = value
        elif key == 'start':
            start = value
        elif key == 'in_file':
            in_file = value
    # start
    if not start:
        source_string = '\n'  # Если значение start не указано, то печатаем пустую строку
    else:
        source_string = f'{start}\n'  # Если значение start указано, то печатаем start
    # max_line
    if not max_line:
        source_string = f'{start}\n{args}'  # Если значение start не указано, то печатаем пустую строку
    else:
        max_line_start = 0
        max_line_end = max_line
        while max_line_end < len(args):
            source_string = f'{source_string}{args[max_line_start:max_line_end]}\n'
            max_line_start = max_line_end + 1
            max_line_end += max_line
    # in_file
    if not in_file:
        print(source_string)
    else:
        source_file = open(in_file, 'w')
        print(source_string, file=source_file)
        source_file.close()
        print(f'Файл {in_file} записан!')
    return source_string


print('\nЗадание со звездочкой: ')
print('Печать исходного текста:')
print(example_text)

print('\nПример работы max_line:')
adv_print(example_text, max_line=50)

print('\nПример работы start и max_line::')
adv_print(example_text, start='Начинаем работу функции adv_print!', max_line=50)

print('\nПример работы start без max_line:')
adv_print(example_text, start='Начинаем работу функции adv_print!')

print('\nПример работы in_file:')
adv_print(example_text, start='Начинаем работу функции adv_print!', max_line=50, in_file='ExampleText.txt')
