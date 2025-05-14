from flask import *
from flask_cors import CORS
from json import *

app = Flask(__name__)
CORS(app)


@app.route('/saveResult', methods=['POST'])
def saveResult():
    result = request.get_json()
    print(result)
    R = open("result.txt", "a")
    R.write(dumps(result, ensure_ascii=False, indent=4) + ",\n")
    R.close()
    res = make_response(jsonify(token=123456, gender=0, method=request.method))  # 设置响应体
    res.status = '200'  # 设置状态码
    res.headers['Access-Control-Allow-Origin'] = "*"  # 设置允许跨域
    res.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
