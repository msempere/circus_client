
manager_parameters = {
    'circus_endpoint': 'tcp://127.0.0.1:5555',
    'logging':{
        'stdout_stream': 'circus.stream.FileStream',
        'stderr_stream': 'circus.stream.FileStream',
        'stderr_extension': 'err',
        'stdout_extension': 'out',
        'path': '/mnt/logs/agentgateway/agents',
    },
    'stop_signal': 9,
    'graceful_timeout': 5,
    'max_retry': 10,
    'environment': {
        'PATH':"/home/rtbkit/local/bin",
        'LD_LIBRARY_PATH':"/home/rtbkit/local/lib",
        'PKG_CONFIG_PATH':"/home/rtbkit/local/lib/pkgconfig/:/home/rtbkit/local/lib/pkg-config/"
    }
}
