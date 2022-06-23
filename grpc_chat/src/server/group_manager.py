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
        logger.debug(f"{type(request)}: \n{request}, {type(context)}")

        if request.userId in self._group_members:
            logger.debug(f"Refused - user connected in {self._group_members[request.userId]}")

            return StatusResponse(
                status=StatusResponse.Status.NOT_OK,
                info=f"user alread belongs to group {self._group_members[request.userId]}",
            )

        self._group_members[request.userId] = request.groupId
        logger.debug(f"Joined - user connected in {self._group_members[request.userId]}")

        return StatusResponse(
            status=StatusResponse.Status.OK,
            info=f"",
        )


    def GetMessages(self, request, context):
        logger.debug(f"{type(request)}: \n\t{request}")

        OPEN = True

        def _unregister_peer():
            nonlocal OPEN 
            logger.debug(f"user {request.userId} disconnected")
            OPEN = False 

        if not context.add_callback(_unregister_peer):
            return 
        
        if request.userId not in self._group_members:
            print("returned")
            return

        while OPEN:
            messages = self._repo.fetch_messages(request.userId, self._group_members[request.userId])
            for msg in messages:
                print(f"yielded: {msg}")
                yield msg


    def SendMessage(self, request, context):
        logger.debug(f"{type(request)}: \n\t{request}")

        if request.userId not in self._group_members:
            logger.debug(f"unknown user - Refused")

            return StatusResponse(
                status=StatusResponse.Status.NOT_OK,
                info=f"user don't belong to any group"    
            )
        self._repo.add_message(self._group_members[request.userId], request)
        logger.debug(f"Message added to the chat")

        return StatusResponse(
            status=StatusResponse.Status.OK,
            info=f"",
            processedAt=request.processedAt # this one is set in repository
        )
