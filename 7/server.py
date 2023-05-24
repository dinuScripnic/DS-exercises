import threading
import zmq
import pickle

context = zmq.Context()
router_socket = context.socket(zmq.ROUTER) # socket to talk to clients
dealer_socket = context.socket(zmq.DEALER)

def bind():
    """
    Binds sockets to ports.
    :return:
    """
    router_socket.bind("tcp://*:7600")
    dealer_socket.bind("inproc://workers")

def check_message(message):
    if 'procedure' not in message:
        return False, 'Error: No procedure name given'
    if 'denominator' not in message:
        return False, 'Error: Missing parameters: \'denominator\''
    if 'numerator' not in message:
        return False, 'Error: Missing parameters: \'numerator\''
    return True, message['procedure']

def calculate(message):
    if message['procedure'] == 'divide':
        if message['denominator'] == 0:
            return False, 'Error: Division by Zero'
        return True, message['numerator'] / message['denominator']
    return False, 'Error: Unknown method: \'%s\'' % message['procedure']

def handle_client():
    socket = context.socket(zmq.REP)
    socket.connect('inproc://workers')
    while True:
        message = pickle.loads(socket.recv())
        print(f'Received message: {message}')
        rc, procedure_or_error = check_message(message)
        if rc is False:
            response = {'error': procedure_or_error}
        else:
            rc2, result_or_error = calculate(message)
            if rc2 is False:
                response = {'error': result_or_error}
            else:
                response = {'result': result_or_error}
        socket.send(pickle.dumps(response))


def main():
    for _ in range(10):
        t = threading.Thread(target=handle_client, args=())
        t.daemon = True
        t.start()

if __name__ == '__main__':
    bind()
    print('Server started')
    main()
    zmq.proxy(router_socket, dealer_socket)