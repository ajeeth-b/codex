from flask import Blueprint, current_app as app, request, jsonify
from . import codex
import json
import requests

unforge = Blueprint('unforge', __name__, url_prefix='/unforge')

def get_testcase(id):
	try:
		data = {'key':app.config['UNFORGE_KEY'], 'testcase_id':id}
		r = requests.post(app.config['UNFORGE_URL']+'/get_testcase',data=json.dumps(data))
		data = r.json()
	except Exception as e:
		print(e)
		return {}, False
	if data['status'] != 'success':
		return {}, False
	return data, True

def put_result(id, output, result):
	try:
		data = {'key':app.config['UNFORGE_KEY'], 'id':id, 'output':str(output),'result':result}
		r = requests.post(app.config['UNFORGE_URL']+'/put_result',data=json.dumps(data))
		data = r.json()
	except Exception as e:
		print(e)
		return False
	if data['status'] != 'success':
		return False
	return True

@unforge.route('/<language>/testcase', methods=['POST'])
def execute_with_testcase(language):
	try:
		if language not in codex.get_available_languages():
			return jsonify({'status':'error','error':'Language not available'})
		if not([i in request.json for i in ['code', 'testcase_id', 's_testcase_id']]):
				return jsonify({'status':'error','error':'insufficient data'})

		testcase, status = get_testcase(int(request.json['testcase_id']))
		if status == False:
			return jsonify({'status':'error','error':'unforge error'})
		inputs = testcase['input']

		status, output = codex.execute(language, request.json['code'], inputs)
		if status == 'success' or status == 'compilation' or status == 'runtime' or status == 'timelimitexceded':
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
	
		if data and data['status'] == 'success':
			stdout = data['stdout']
			# print('outp',stdout, len(stdout))
			# print('exp',testcase['output'], len(testcase['output']))
			# print(testcase['output'] == stdout)
			result = 'passed' if stdout == testcase['output'] else 'failed'
			put_result(int(request.json['s_testcase_id']), stdout, result)
			return jsonify({'status':'success', 'result':result,'message':data['message']})
	except Exception as e:
		print(e,'unknown exception')
		return jsonify({'status':'failed', 'error':'internal error'})
	return jsonify({'status':'failed', 'error':data['message']})
