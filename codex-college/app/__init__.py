from flask import Flask, jsonify, request, render_template
from .codex import CodEX
from flask_cors import CORS

codex = CodEX()

def create_app():
	app = Flask(__name__)
	CORS(app)

	app.config['UNFORGE_URL'] = 'http://127.0.0.1:5000/codex'
	# app.config['UNFORGE_URL'] = 'http://65.1.210.183/codex'
	app.config['UNFORGE_KEY'] = 'temp'

	@app.route('/')
	def get_all_languages():
		return jsonify({'languages':codex.get_available_languages()})

	@app.route('/<language>', methods=['POST'])
	def execute(language):
		try:
			if language not in codex.get_available_languages():
				resp = jsonify({'status':'error','error':'Language not available'})

			if 'code' not in request.json:
				resp = jsonify({'status':'error','error':'requires code to execute'})

			inputs = request.json.get('input','')

			status, output = codex.execute(language, request.json['code'], inputs)
			if status == 'success' or status == 'compilation' or status == 'runtime':
				data = {
					'status':'success',
					'message':status,
					'stdout': output['stdout'],
					'stderr': output['stderr']
				}
			elif status == 'internal':
				data = {
					'status':'failed',
					'message':'internal error'
				}
				print(output)

			resp = jsonify(data)
		except Exception as e:
			resp = jsonify({'status':'internal error'})
		return resp

	@app.route('/ide')
	def ide():
		return render_template('ide.html')

	with app.app_context():
		from .unforge_api import unforge as unforge_blueprint
		app.register_blueprint(unforge_blueprint)

	return app