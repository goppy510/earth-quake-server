from flask import Flask, request, jsonify, make_response
app = Flask(__name__)

@app.route("/api/earthquake", methods=['GET'])
def get_earthquake():
    # URLパラメータ
	params = request.args
	response = {}
    if 'param' in params:
  		response.setdefault('res', 'param is : ' + params.get('param'))
	return make_response(jsonify(response))

@app.route("/hoge", methods=['POST'])
def postHoge():
    # ボディ(application/json)パラメータ
    params = request.json
    response = {}
	if 'param' in params:
  		response.setdefault('res', 'param is : ' + params.get('param'))
	return make_response(jsonify(response))

app.run()