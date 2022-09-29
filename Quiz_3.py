from unicodedata import name
from flask import Flask, jsonify, request
from flask import render_template
app = Flask(__name__)

nama_peserta = [{'nama' : 'Tanu'}, {'nama' : 'Pitra'}, {'nama' : 'Febyanto'}]

@app.route('/', methods=['GET'])
def returnall():
    return jsonify({'nama_peserta' : nama_peserta})

@app.route('/peserta/<string:name>', methods=['GET'])
def returnOne(name):
	langs = [nama for nama in nama_peserta if nama['nama'] == name]
	return jsonify({'nama peserta' : langs[0]})

@app.route('/peserta', methods=['POST'])
def addOne():
    dictionary = {'nama' : request.json['nama']}
    nama_peserta.append(dictionary)
    return jsonify({'nama_peserta' : nama_peserta})
    
@app.route('/peserta/<string:name>', methods=['PUT'])
def editOne(name):
    langs = [nama for nama in nama_peserta if nama['nama'] == name]
    langs[0]['nama'] = request.json['nama']
    return jsonify({'dictionary' : langs[0]})

@app.route('/peserta/<string:name>', methods=['DELETE'])
def deleteOne(name):
    langs = [nama for nama in nama_peserta if nama['nama'] == name]
    nama_peserta.remove(langs[0])
    return jsonify({'nama_peserta' : nama_peserta})
    
if __name__ == '__main__':
    app.run(debug=True, port=8080)