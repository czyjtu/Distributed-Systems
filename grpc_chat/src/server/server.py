from gen.chat_pb2_grpc import GroupManagerServicer
from gen.chat_pb2 import StatusResponse
from server.repository import MessageRepository
import logging


logger = logging.getLogger(__name__)


class GroupManager(GroupManagerServicer):
    def __init__(self, repository: MessageRepository):
        self._repo = repository
        self._group_members: dict[str, str] = {}  # userId -> groupId


    def JoinGroup(self, request, context):
        if request.userId in self._group_members:
            return StatusResponse(
                status=StatusResponse.Status.NOT_OK,
                info=f"user alread belongs to group {self._group_members[request.userId]}",
            )
        self._group_members[request.userId] = request.groupId
        return StatusResponse(
            status=StatusResponse.Status.OK,
            info=f"",
        )


    def GetMessages(self, request, context):
        if request.userId not in self._group_members:
            return

        while True:
            messages = self._repo.fetch_messages(request.userId, self._group_members[request.userId])
            for msg in messages:
                yield msg


    def SendMessage(self, request, context):
        if request.userId not in self._group_members:
            return StatusResponse(
                status=StatusResponse.NOT_OK,
                info=f"user don't belong to any group"    
            )
        self._repo.add_message(self._group_members[request.userId], request)
        return StatusResponse(
            status=StatusResponse.Status.OK,
            info=f"",
        )
        