from server import api, api_url, Service

VERSION = "v1"


@api.route(api_url(VERSION, Service.REGISTER), methods=['POST'])
def register():
    return ''


@api.route(api_url(VERSION, Service.UNREGISTER), methods=['DELETE'])
def unregister(runtime):
    return 'unregister ' + runtime


@api.route(api_url(VERSION, Service.POLLING), methods=['GET'])
def polling(runtime):
    return 'polling ' + runtime


@api.route(api_url(VERSION, Service.CALLBACK), methods=['POST'])
def callback(runtime):
    return 'callback ' + runtime
