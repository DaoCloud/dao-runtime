# Copyright 2015 DaoCloud Inc. All Rights Reserved.
from flask import request, make_response
import json

from api import api, api_url, Service
from server.command.command import CommandEncoder
from server.registry import register, unregister, Runtime
from server.queue.in_memory_queue import queue, CommandNotInQueue
from server.queue.in_memory_queue import RuntimeNotFound

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
    payload = request.get_json()

    # TODO: Refactor me! This is such a mess.
    if not payload or 'seq_id' not in payload or 'result' not in payload or \
       'ok' not in payload:
        return make_response('Bad Request', 400)

    seq_id = payload['seq_id']
    result = payload['result']
    ok = payload['ok']

    try:
        queue.set_command_result(runtime, seq_id, ok, result)
        return ''
    except (RuntimeNotFound, CommandNotInQueue) as e:
        return make_response(e.message, 404)
