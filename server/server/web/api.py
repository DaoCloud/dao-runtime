# Copyright 2015 DaoCloud Inc. All Rights Reserved.
import enum
from flask import Flask

api = Flask(__name__)


@enum.unique
class Service(enum.Enum):

    REGISTER = "/api/#{version}/runtimes"
    UNREGISTER = "/api/#{version}/runtimes/<runtime>"
    POLLING = "/api/#{version}/runtimes/<runtime>/requests"
    CALLBACK = "/api/#{version}/runtimes/<runtime>/callback"


def api_url(version, service):
    return service.value.replace("#{version}", version)
