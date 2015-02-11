from flask import request, make_response

from api import api, api_url, Service
from server.registry import register, unregister, Runtime

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
    return 'polling ' + runtime


@api.route(api_url(VERSION, Service.CALLBACK), methods=['POST'])
def callback(runtime):
    return 'callback ' + runtime
