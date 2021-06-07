from flask import Flask, jsonify
import main_scraping

def stocks_api(*,data_obj):

    app = Flask(__name__)

    region = data_obj

    @app.route('/region', methods = ['GET'])
    def home():
        return jsonify(region), 200

    @app.route('/region/<string:symbol>', methods = ['GET'])
    def search_region(symbol):
        symbol_search = [search_symbol for search_symbol in region if search_symbol['symbol'] == symbol]
        return jsonify(symbol_search), 200

    if __name__ == "__main__":
        app.run(debug = True)

# Execução da API, chamando o web scraping para retornar a lista de dados capturados para utilizar como parametro na requisição
extracted_data = main_scraping.main_scraping()
stocks_api(data_obj = extracted_data)