from flask import Flask, make_response, jsonify, request
import dataset

app = Flask(__name__)
db = dataset.connect('sqlite:///api.db')


table = db['livros']


def fetch_db(id_livro):
    return table.find_one(id_livro=id_livro)


def fetch_db_all():
    livros = []
    for livro in table:
        livros.append(livro)
    return livros


@app.route('/api/db_populate', methods=['GET'])
def db_populate():
    table.insert({
        "id_livro": "1",
        "name": "A Game of Thrones.",
        "author": "George R. R. Martin"
    })

    table.insert({
        "id_livro": "2",
        "name": "Lord of the Rings",
        "author": "J. R. R. Tolkien"
    })

    return make_response(jsonify(fetch_db_all()),
                         200)


@app.route('/api/livros', methods=['GET', 'POST'])
def livros():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()), 200)
    elif request.method == 'POST':
        content = request.json
        id_livro = content['id_livro']
        table.insert(content)
        return make_response(jsonify(fetch_db(id_livro)), 201)  # 201 = Created


@app.route('/api/livros/<id_livro>', methods=['GET', 'PUT', 'DELETE'])
def api_each_livro(id_livro):
    if request.method == "GET":
        livro_obj = fetch_db(id_livro)
        if livro_obj:
            return make_response(jsonify(livro_obj), 200)
        else:
            return make_response(jsonify(livro_obj), 404)
    elif request.method == "PUT":  # Updates the book
        content = request.json
        table.update(content, ['id_livro'])

        livro_obj = fetch_db(id_livro)
        return make_response(jsonify(livro_obj), 200)
    elif request.method == "DELETE":
        table.delete(id=id_livro)

        return make_response(jsonify({}), 204)


if __name__ == '__main__':
    app.run(debug=True)