from flask import request, make_response
import json

from api import api, api_url, Service
from server.command.command import CommandEncoder
from server.registry import register, unregister, Runtime
from server.queue.in_memory_queue import queue

VERSION = "v1"


@api.route(api_url(VERSION, Service.REGISTER), methods=['POST'])
def register_runtime():
    payload = request.get_json()
    if not payload or 'name' not in payload:
        return make_response('Bad Request', 400)
    else:
        runtime = payload['name']
        register(Runtime(runtime))
        return ''


@api.route(api_url(VERSION, Service.UNREGISTER), methods=['DELETE'])
def unregister_runtime(runtime):
    unregister(runtime)
    return ''


@api.route(api_url(VERSION, Service.POLLING), methods=['GET'])
def polling(runtime):
    seq_id = int(request.args.get('seq_id') or 0)
    if not seq_id:
        seq_id = 0
    commands = queue.get_queued_commands(runtime, seq_id)
    return json.dumps(commands, cls=CommandEncoder)


@api.route(api_url(VERSION, Service.CALLBACK), methods=['POST'])
def callback(runtime):
    return 'callback ' + runtime
