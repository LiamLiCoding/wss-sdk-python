from .. import operation


def restart():
    operation.restart()


def shutdown():
    operation.shutdown()


def stop_intruder_detect():
    operation.intruder_detect(False)


def start_intruder_detect():
    operation.intruder_detect(True)


NET_OPERATION = {
    'restart': restart,
    'shutdown': shutdown,
}
