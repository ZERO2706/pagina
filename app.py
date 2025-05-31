from flask import Flask

app = Flask(__name__)

@app.route('/carpeta_opti_alfin_PRIMERO', methods=['GET'])
def ejecutar():
    # Aquí va tu lógica Python
    return "¡Python ejecutado correctamente!"

if __name__ == '__main__':
    app.run(host='localhost', port=5000)