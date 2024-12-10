#Веб-сервіс для обробки зберігання даних про каталог товарів (вінілових платівок) у магазині
from flask import Flask, request, abort
import random

app = Flask(__name__)


@app.route('/items/genre', methods = ['GET'])
def get_fun_genre(): #Якщо задати жанр параметром, видає всі товари з цим жанром
    if check_auth(request.authorization):
        return "Bad auth"
    output_by_genres = []
    for i in range(len(read_catalog_file())):
        if read_catalog_file()[i]['genre'] in request.args:
            output_by_genres.append(read_catalog_file()[i])
    if output_by_genres:
        return output_by_genres
    if request.args.to_dict().keys():
        return "There are no records in this genre available"
    return "Choose a genre"


@app.route('/items', methods = ['GET'])
def get_fun(): #Якщо задати параметр як id, видає інформацію за обраним id
    if check_auth(request.authorization):
        return "Bad auth"
    for i in range(len(read_catalog_file())):
        if read_catalog_file()[i]['id'] in request.args:
            return read_catalog_file(int(next(iter(request.args.to_dict().keys()))))
    if request.args.to_dict().keys():
        return "The product with this id does not exist"
    response_file = read_catalog_file()
    return response_file


@app.route('/items', methods = ['POST'])
def post_handler(): #Додає інф у вигляді id;назва;жанр;ціна;
    if check_auth(request.authorization):
        return "Bad auth"
    if 'Content-Type' not in request.headers:
        abort(400)
    if request.headers['Content-Type'] != 'application/json':
        abort(400)
    if save_fun(request.json):
        return "Data successfully added", 201
    return "check false", 200


@app.route('/items', methods = ['PUT'])
def put_handler(): #Замінює genre і price по параметру id та назві у запиті
    if check_auth(request.authorization):
        return "Bad auth"
    if 'Content-Type' not in request.headers:
        abort(400)
    if request.headers['Content-Type'] != 'application/json':
        abort(400)
    if resave_fun_put(request.json):
        return "Data successfully updated", 201
    return "Somthing wrong", 200


@app.route('/items', methods = ['DELETE'])
def delete_handler(): #Видаляє запис по параметру id у запиті
    if check_auth(request.authorization):
        return "Bad auth"
    if resave_fun_delete(next(iter(request.args.to_dict().keys()))):
        return "Data deleted successfully", 201
    return "Somthing wrong", 200


def save_fun(post_data): #Записує новий товар
    if check_inf_post(post_data):
        file = open("file_catalog.txt", 'a')
        data_to_write = "\n" + str(rand_id()) + ";" + post_data['name']+ ";" + post_data['genre'] + ";" + str(post_data['price']) + ";"
        file.write(data_to_write)
        file.close()
        return True
    return False


def rand_id(start = 100, end = 1000): #Створює id для нового товару
    while True:
        new_id = random.randint(start, end)
        for i in range(len(read_catalog_file())):
            if new_id not in read_catalog_file()[i].values():
                return new_id


def resave_fun_put(put_data): #Перезаписує інф про товар за id
    inter_save = read_catalog_file()
    get_id = next(iter(request.args.to_dict().keys()))
    if check_inf(str(get_id),False,put_data):
        for i in range(len(inter_save)):
            if get_id == inter_save[i]['id']:
                inter_save[i]['price'] = str(put_data['price'])
                inter_save[i]['genre'] = put_data['genre']
                break
        full_overw(inter_save)
        return True
    return False


def resave_fun_delete(get_id): #Видаляє товар за id
    inter_save = read_catalog_file()
    if check_inf(str(get_id),True, 0):
        for i in range(len(inter_save)):
            if get_id == inter_save[i]['id']:
                print(inter_save)
                print(i)
                inter_save.pop(i)
                print(inter_save)
                break
        full_overw(inter_save)
        return True
    return False


def full_overw(list_to_save): #Повне переписування файлу
    file = open("file_catalog.txt", 'w')
    data_to_write = str(list_to_save[0]['id']) + ";" + list_to_save[0]['name'] + ";" + list_to_save[0]['genre'] + ";" + str(list_to_save[0]['price']) + ";"
    file.write(data_to_write)
    for i in range(1, len(list_to_save)):
        data_to_write = "\n" + str(list_to_save[i]['id']) + ";" + list_to_save[i]['name'] + ";" + list_to_save[i]['genre'] + ";" + str(list_to_save[i]['price']) + ";"
        file.write(data_to_write)
    file.close()


def read_catalog_file(get_id=0): #Зчитує файл товарів і видає лист словників всіх товарів
    file= open("file_catalog.txt", 'r')
    my_list = []
    for row in file:
        fields = row.strip().split(';')
        my_dict = {'id': fields[0],'name': fields[1],'genre': fields[2],'price': fields[3]}
        my_list.append(my_dict)
    file.close()
    if get_id != 0:
        for i in range(len(read_catalog_file())):
            if str(get_id) in read_catalog_file()[i]['id']:
                return my_list[i]
    return my_list


def read_auth_file(): #Зчитує файл з аутентифікаційними даними
    file = open("auth.txt", "r")
    user_inf = {}
    for line in file:
        username, password = line.strip().split(":")
        user_inf[username] = password
    file.close()
    return user_inf


def check_inf_post(post_data, start = 100, end = 1000):  #Перевіряє перезаповненість файлу і дублікацію назв
    for i in range(len(read_catalog_file())):
        if len(read_catalog_file()) >= (end - start + 1) or post_data['name'] == read_catalog_file()[i]['name']:
            return False
    return True


def check_inf(get_id, is_delete, data=0):  #Перевіряє чи вже існує вхідний запис
    for i in range(len(read_catalog_file())):
        if  get_id in read_catalog_file()[i]['id']:
            if is_delete or data['name'] == read_catalog_file()[i]['name']:
                return True
    return False


def check_auth(data): #Перевіряє відповідність логіну і паролю
    return not data or read_auth_file().get(data.username) != data.password


if __name__ == '__main__':
    app.run(port=8000, debug=True)