from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/items', methods = ['GET'])
def get_fun():
    response_file = read_file()
    print(response_file)
    return response_file


@app.route('/items', methods = ['POST'])

def read_file():
    file= open("my_file.txt", 'r')

    my_list = []
    for row in file:
        my_dict = {}
        my_dict['id'] = row.split(' ')[0]
        my_dict['name'] = row.split(' ')[1]
        my_dict['price'] = row.split(' ')[2]
        my_list.append(my_dict)
    file.close()
    return my_list

def post_fun():
    if 'Content-Type' not in request.headers:
        abort(400)
    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    if saver(request.json):
        return "written", 201

    print(request.json['price'])
    print(request.json['name'])

    return "ok", 200

def saver(post_data):
    file = open("my_file.txt", 'a')
    data_to_write = "1 " +post_data['name']+ " " + str(post_data['price'] + " " + "\n")
    file.write(data_to_write)
    file.close()
    return True


if __name__ == '__main__':
    app.run(port=8000, debug=True)