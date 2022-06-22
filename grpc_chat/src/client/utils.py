from threading import Thread
from gen.chat_pb2 import GetMessagesRequest, JoinRequest, ChatMessage
import grpc
from gen.chat_pb2_grpc import GroupManagerStub
from server.const import PORT_NUMBER
import tkinter as tk 
from tkinter import Tk, Text, Label, Button
import sys 

RUNNING = True

def join(stub, group_id: str, usr_id: str):
    print(f"{usr_id} wants to join {group_id}")
    request = JoinRequest(
        userId=usr_id,
        groupId=group_id
    )
    status = stub.JoinGroup(request)
    print(status)


def send_msg(stub, text: str, usr_id: str):
    print(f"sending: '{text}'")
    msg = ChatMessage(
        msg=text,
        userId=usr_id,
        priority=0
    )
    status = stub.SendMessage(msg)
    print(status)


def listen_for_messages(stub, usr_id):

    listening = True

    def update(label, stub, usr_id):
        request = GetMessagesRequest(userId=usr_id)
        for msg in stub.GetMessages(request):
            print(f"{msg.userId} say {msg.msg}")

            label.insert(tk.END, f"{msg.userId}: {msg.msg}")

            if not listening:
                break

    root = Tk()
    root.geometry("250x170")
    T = Text(root, height = 5, width = 52)

    b1 = Button(root, text = "Next", )
    b2 = Button(root, text="Exit", command = root.destroy)

    T.pack()
    b1.pack()
    b2.pack()

    th = Thread(target=update, args=(T, stub, usr_id))
    th.start()
    tk.mainloop()

    listening = False
    th.join()

    print("finished listening")
    

def listen_for_input(stub, usr_id):
    while RUNNING:
        text = input(">>")
        if text == 'stop':
            break
        if text:
            send_msg(stub, text, usr_id)


if __name__ == '__main__':
    USER = sys.argv[1]
    GROUP = sys.argv[2] 
    options = [
        # ('grpc.keepalive_time_ms', 10000),
        # # send keepalive ping every 10 second, default is 2 hours
        # ('grpc.keepalive_timeout_ms', 5000),
        # # keepalive ping time out after 5 seconds, default is 20 seoncds
        # ('grpc.keepalive_permit_without_calls', True),
        # # allow keepalive pings when there's no gRPC calls
        # ('grpc.http2.max_pings_without_data', 0),
        # # allow unlimited amount of keepalive pings without data
        # ('grpc.http2.min_time_between_pings_ms', 10000),
        # # allow grpc pings from client every 10 seconds
        # ('grpc.http2.min_ping_interval_without_data_ms',  5000),
        # # allow grpc pings from client without data every 5 seconds

    ]
    
    with grpc.insecure_channel(f'localhost:{PORT_NUMBER}', options=options) as channel:
        stub = GroupManagerStub(channel)
        join(stub, GROUP, USER)
        th_listen = Thread(target=listen_for_messages, args=(stub, USER))
        th_write = Thread(target=listen_for_input, args=(stub, USER))

        th_listen.start()
        th_write.start()

        th_listen.join()
        RUNNING = False
        th_write.join()
    