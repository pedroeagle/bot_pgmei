import os
from flask import Flask, request, send_file #import main Flask class and request object
import re

app = Flask(__name__) #create the Flask app
@app.route('/pgmei/check_invoice', methods=['POST'])
def contaazul_get_extrato():
    from pgmei import pgmei
    return pgmei.check_invoice()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=port, debug=True)