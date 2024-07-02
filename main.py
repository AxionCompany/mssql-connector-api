import pymssql
import json
from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
# create a health check route
@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/teste', methods=['POST'])
def teste():
    user = request.headers.get('user')
    password = request.headers.get('password')
    port = request.headers.get('port', '1433')  # Default SQL Server port is 1433
    server = request.headers.get('server')
    database = request.headers.get('database')

    if not all([user, password, server]):
        return jsonify({'status': 'error', 'message': 'Missing Headers. Make sure you\'ve set `user`, `password`, `server` headers'}), 400

    name = request.json.get('name')
    params = request.json.get('params')
    __filterTable__ = request.json.get('__filterTable__')

    if __filterTable__ is None:
        __filterTable__ = 0

    if not name:
        return jsonify({'status': 'error', 'message': 'Missing Parameters. Make sure you\'ve set `name` parameter'}), 400

    conn = None  # Initialize conn before the try block
    try:
        conn = pymssql.connect(server=server, user=user, password=password, database=database, port=port, as_dict=True)
        cursor = conn.cursor()
        
        exec_statement = f"EXEC {name} " + ", ".join([f"@{k}=%s" for k in params.keys()])
        cursor.execute(exec_statement, tuple(params.values()))

        current_set_index = 0
        data = [] # Initialize data with an empty array

        # Iterate through result sets until the desired one is found or until there are no more
        while True:
            if current_set_index == __filterTable__:
                data = [row for row in cursor.fetchall()]
                break
            if not cursor.nextset():
                break  # No more result sets available
            current_set_index += 1
        df = pd.DataFrame(data)
        # Convert the DataFrame to JSON and wrap it in a 'data' object
        response_data = {'data': json.loads(df.to_json(orient='records', date_format='iso'))}
        return jsonify(response_data)
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 400
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 9000)))