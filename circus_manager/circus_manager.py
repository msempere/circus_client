#!/usr/bin/env python

from circus.client import CircusClient
from circus import get_arbiter
from circus_manager import config

class CircusManager(object):

    def __init__(self):
        self._arbiter = get_arbiter([])
        self._arbiter.start()
        self._config = config.watchdog_parameters
        self._client = CircusClient(timeout=15, endpoint=self._config['circus_endpoint'])


    def __call(self, message):
        return self._client.call(message)


    def add_application(self, name, command, arguments=[], autostart=True):
        response = self.__call({
            'command':'add',
            'properties':{
                'cmd': command,
                'name':name,
                'start': autostart,
                'args':arguments,
                'options':{
                    'singleton': True,
                    'shell': True,
                    'stdout_stream': {
                        'class': self._config['logging']['stdout_stream'],
                        'filename': '{path}/{filename}.{ext}'.format(path=self._config['logging']['path'],
                                                                     filename=name,
                                                                     ext=self._config['logging']['stdout_extension'])
                    },
                    'stderr_stream': {
                        'class':self._config['logging']['stderr_stream'],
                        'filename': '{path}/{filename}.{ext}'.format(path=self._config['logging']['path'],
                                                                     filename=name,
                                                                     ext=self._config['logging']['stderr_extension'])
                    }
                }
            }
        })
        return (True, None) if response['status'] == u'ok' else (False, response['reason'])


    def application_status(self, name):
        response = self.__call({
            'command': 'status',
            'properties': {
                'name': name
            }
        })
        return str(response['status']) if response['status'] != u'error' else 'not running'


    def kill_application(self, name):
        self.__call({
            'command': 'signal',
            'properties':{
                'name': name,
                'signal': self._config['stop_signal']
            }
        })


    def remove_application(self, name):
        response = self.__call({
            'command': 'rm',
            'properties':{
                'name': name,
                'waiting': False
            }
        })
        return True if response['status'] == u'ok' else False


    def start_application(self, name, waiting=False):
        response = self.__call({
            'command': 'start',
            'properties':{
                'name': name,
                'waiting': waiting
            }
        })
        return True if response['status'] == u'ok' else False


    def stop_application(self, name, waiting=False):
        response = self.__call({
            'command': 'stop',
            'properties':{
                'name': name,
                'waiting': waiting
            }
        })
        return True if response['status'] == u'ok' else False


    def stop_and_remove_application(self, name):
        self.stop_application(name)
        return self.remove_application(name)


    def get_applications(self, verbose=False):
        response = self.__call({
            'command': 'list'
        })
        if not verbose:
            return [{'name':str(w)} for w in response['watchers']] if response['status'] == u'ok' else []
        return [{'name':str(w), 'status': self.application_status(str(w))} for w in response['watchers']] if response['status'] == u'ok' else []


    def stop(self):
        self._arbiter.stop()


if __name__ == '__main__':
    w = CircusManager()
    print w.add_application('a_ls', 'ls', arguments=['-la'], autostart=False)
    print w.start_application('a_ls')
    print w.get_applications(verbose=True)
    print w.stop_application('a_ls')
    print w.get_applications(verbose=True)
    print w.stop_and_remove_application('a_ls')
    print w.get_applications(verbose=True)
