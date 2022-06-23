from threading import Thread
from gen.chat_pb2 import GetMessagesRequest, JoinRequest, ChatMessage, Multimedia
import grpc
from gen.chat_pb2_grpc import GroupManagerStub
from server.const import PORT_NUMBER
import sys, signal

RUNNING = True
HISTORY = []

def display_msg(msg):
    multimedia = len(msg.attachment.mime) > 0
    print(f"id={msg.processedAt} | user={msg.userId} | reply={msg.repliesTo} | {msg.msg} | attachment={multimedia}")
    print()

def join(stub, group_id: str, usr_id: str):
    print(f"{usr_id} wants to join {group_id}")
    request = JoinRequest(
        userId=usr_id,
        groupId=group_id
    )
    status = stub.JoinGroup(request)
    print(status)


def send_msg(stub, text: str, usr_id: str, reply_idx: int=0, multimedia: bytes=b"\0", mime: str=""):
    def find_in_history(last_idx: int):
        ordered_hist = sorted(HISTORY, key=lambda msg: msg.processedAt)
        return ordered_hist[last_idx]

    replies_to = find_in_history(reply_idx).processedAt if reply_idx < 0 else 0
    multi = Multimedia(
        mime=mime,
        data=multimedia
    )
    print(f"sending: '{text}'")
    msg = ChatMessage(
        msg=text,
        userId=usr_id,
        priority=0,
        repliesTo=replies_to,
        attachment=multi
    )

    status = stub.SendMessage(msg)
    msg.processedAt = status.processedAt
    HISTORY.append(msg)

    display_msg(msg)


def listen_for_messages(stub, usr_id):
    
    request = GetMessagesRequest(userId=usr_id)
    for msg in stub.GetMessages(request):
        HISTORY.append(msg)       
        display_msg(msg)

        if not RUNNING:
            break
    

def listen_for_input(stub, usr_id):

    while RUNNING:
        text = input(">>")
        if text == 'stop':
            break
        if text:
            reply_idx = 0
            multi = b'\0'
            mime = ""

            if text[:2] == "-r":
                reply_idx = -1
                text = text.replace("-r", "")
            if "-m" in text:
                multi = bytes([1, 2, 3, 4])     
                text = text.replace("-m", "")
                mime = "image/jpeg"
            send_msg(stub, text, usr_id, reply_idx, multi, mime)


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
        th_write.join()
    