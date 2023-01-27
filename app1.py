from flask import Flask, request, abort

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = True

students = [
    {
        "id": 1,
        "name": "Igor",
        "surname": "Erenev",
        "patronimyc": "Aleksandrovich"
    },
    {
        "id": 2,
        "name": "Nikolay",
        "surname": "Oronov",
        "patronimyc": "Petrovich"
    },
    {
        "id": 3,
        "name": "Artem",
        "surname": "Aranov",
        "patronimyc": "Grigor'evich"
    },
    {
        "id": 4,
        "name": "Vasiliy",
        "surname": "Urunev",
        "patronimyc": "Valer'evich"
    }]


# !!!!!!! ВСЕ ИМЕНА ВЫМЫШЛЕННЫЕ !!!!!!!

@app.route("/")
def start_page():
    return "Hello everyone"


@app.route("/igor")
def igorinfo():
    return {students[0][1], [0][2], [0][3]}


# подойдет для выгрузки сервера в интернет

@app.route("/nikolay")
def nikolayinfo():
    return students[1]


@app.route("/artem")
def arteminfo():
    return students[2]


@app.route("/vasiliy")
def vasiliyinfo():
    return students[3]


@app.route("/students")
def get_students():
    return students


@app.route("/students/<letter>")
def get_student(letter):
    for student in students:
        if letter in student["name"]:
            return student


# такой урл до подключения фильтров и авторизации
@app.route('/students/<letter>/<surletter>')
def get_stud_usng_2_lttrs(letter, surletter):
    for student in students:
        if letter in student["name"] and surletter in student["surname"]:
            return student
        elif letter != str or surletter != str:
            abort(404, "Указанного ученика не существует")


@app.route('/students', methods=['POST'])
def create_student():
    data = request.json
    last_id = students[-1]["id"]
    data["id"] = last_id + 1
    students.append(data)
    #    print("data = ", data)
    return data, 201


@app.route("/students/<int:id>", methods=['DELETE'])
def delete(id):
    for student in students:
        if id == student['id']:
            students.remove(student)
            return f"Student with id {id} is deleted.", 200
    abort(404, f"Указанного id = {id}, не существует")


if __name__ == "__main__":
    app.run(debug=True)
