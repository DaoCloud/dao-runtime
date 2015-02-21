
class Runtime(object):
    """ Service in registry
    """

    def __init__(self, name):
        self.name = name


runtimes = {}


def register(runtime):
    runtimes[runtime.name] = runtime


def unregister(runtime_name):
    if runtime_name in runtimes:
        del runtimes[runtime_name]


def size():
    return len(runtimes)


def clear():
    runtimes.clear()


def is_registered(runtime_name):
    return runtime_name in runtimes


def get_runtimes():
    return runtimes.keys()
