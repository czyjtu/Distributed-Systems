from server import ROOT_PATH
from gen.chat_pb2 import ChatMessage
from collections import defaultdict
from pathlib import Path


class MessageRepository:
    def __init__(self, cache_path: Path = ROOT_PATH / "chat_cache/cache.json"):
        self._cache_path = cache_path

        cache = {}
        # if os.path.exists(cache_path):
        #     with open(cache_path, "r") as f:
        #         cache = json.load(f)

        self._data: dict[str, list[ChatMessage]] = defaultdict(cache, list)
        self._client_position: dict[str:int] = defaultdict(0)

    def get_messages(self, group_id: str) -> list[ChatMessage]:
        return self._data.get(group_id, [])

    def add_message(self, group_id: str, msg: ChatMessage) -> None:
        self._data[group_id].append(msg)

    def fetch_messages(self, client_id: str, group_id: str) -> list[ChatMessage]:
        last_msg_pos = len(self._data[group_id])
        current_pos = self._client_position[client_id]
        result = self._data[group_id][current_pos:last_msg_pos]
        return [msg for msg in result if msg.sender_id != client_id]

    def save(self) -> None:
        raise NotImplementedError
        # cache_dir = self._cache_path.aprent
        # if not os.path.exists(cache_dir):
        #     os.makedirs(cache_dir)

        # with open(self._cache_path, "w") as f:
        #     json.dump(self._data, f)
