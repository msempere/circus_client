
watchdog_parameters = {
    'circus_endpoint': 'tcp://127.0.0.1:5555',
    'logging':{
        'stdout_stream': 'circus.stream.FileStream',
        'stderr_stream': 'circus.stream.FileStream',
        'stderr_extension': 'err',
        'stdout_extension': 'out',
        'path': '/tmp',
    },
    'stop_signal': 9
}
