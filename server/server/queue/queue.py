# Copyright 2015 DaoCloud Inc. All Rights Reserved.

import abc


class RuntimeNotFound(Exception):
    pass


class CommandNotInQueue(Exception):
    pass


class CommandQueue(object):
    """ Abastract class for command queue. Every runtime should have separate
    queue. The real implementation should be backed with persistent layer. For
    example, redis or a database.

    It's not a queue. But I cannot find a better name. Feel free to rename it.
    """

    @abc.abstractmethod
    def add_command(self, runtime_name, command):
        """ Add a new command in queue.

        :param runtime_name: name of runtime
        :type runtime_name: str
        :param command: command to be added
        :type command: Command
        """
        pass

    @abc.abstractmethod
    def get_queued_commands(self, runtime_name, seq_id):
        """ Get all queued commands owned by runtime, whose seq_id is bigger
        than the given one. After the commands are fetched, set them as
        STARTED.

        :param runtime_name: name of runtime
        :type runtime_name: str
        :param seq_id: the command newer than this will be returned
        :type seq_id: int
        :returns: list of commands
        :rtype: list of Command
        """
        pass

    @abc.abstractmethod
    def set_command_result(self, runtime_name, seq_id, success, result):
        """ Update command result.

        :param runtime_name: name of runtime
        :type runtime_name: str
        :param seq_id: command sequence id
        :type seq_id: int
        :param success: success or fail
        :type success: bool
        :param result: result
        :type result: TODO to be defined
        :raises: RuntimeNotFound if runtime not found
        :raises: CommandNotInQueue if command not found
        """
        pass
