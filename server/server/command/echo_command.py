from server.command.command import Command


class EchoCommand(Command):

    def __init__(self, message):
        super(EchoCommand, self).__init__('echo')
        self.message = message
