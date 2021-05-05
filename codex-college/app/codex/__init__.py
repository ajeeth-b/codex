from .Docker import Docker, LanguageNotSupported, TimeLimitExceeded, CodeCompliationError, CodeRuntimeError, InternalError, ExecutionError
from uuid import uuid4
from .settings import BASE_MOUNTPOINT
from os import path, mkdir
from .utils import lang_exec
from shutil import rmtree

class CodEX:
	docker = Docker()
	def __init__(self):
		self.languages = self.docker.get_all_language()

	def get_available_languages(self):
		return self.languages

	def execute(self, language, code, inputs=''):
		if language not in self.languages:
			return (-1, 'Language not supported')

		lang_utils = lang_exec[language]

		folder_name = str(uuid4())
		folder = path.join(BASE_MOUNTPOINT, folder_name)
		mkdir(folder)

		code_file = path.join(folder, lang_utils['filename'])
		self._write_file_content(code_file, code)

		input_file = path.join(folder, 'inp.txt')
		self._write_file_content(input_file, inputs)

		try:
			output = self.docker.run_container(language, lang_utils, folder)
			self.delete_docker_volume(folder)
			return ('success',{'stdout':output[0], 'stderr':output[1]})
		except CodeCompliationError as e:
			self.delete_docker_volume(folder)
			return ('compilation', {'stdout':e.output, 'stderr':e.error})
		except CodeRuntimeError as e:
			self.delete_docker_volume(folder)
			return ('runtime', {'stdout':e.output, 'stderr':e.error})
		except TimeLimitExceeded as e:
			self.delete_docker_volume(folder)
			return ('timelimitexceded', {'stdout':None, 'stderr':None})
		except Exception as e:
			self.delete_docker_volume(folder)
			print('internal error', 'codex - line 44',e)
			return ('internal', {'error':e})

	def _write_file_content(self, file_path, content):
		with open(file_path, 'w') as f:
			f.write(content)

	def delete_docker_volume(self, folder):
		try:
			rmtree(folder)
		except FileNotFoundError:
			pass
