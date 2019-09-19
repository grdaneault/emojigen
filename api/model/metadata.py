import json

from redis import Redis


class Metadata(object):
    def __init__(self,
                 original_name: str,
                 name: str,
                 path_on_disk: str,
                 id: str,
                 url: str,
                 parent: str = None,
                 type: str = 'original'):
        self.type = type
        self.original_name = original_name
        self.name = name
        self.path_on_disk = path_on_disk
        self.id = id
        self.url = url
        self.parent = parent

    def to_json(self, include_path=False):
        ret = {
            "id": self.id,
            "url": self.url,
            "original_name": self.original_name,
            "name": self.name,
            "type": self.type
        }

        if self.parent:
            ret["parent"] = self.parent

        if include_path:
            ret["path_on_disk"] = self.path_on_disk

        return ret

    def to_json_str(self, include_path=False):
        return json.dumps(self.to_json(include_path=include_path))

    @staticmethod
    def from_json_str(val):
        return Metadata(**json.loads(val))


class MetadataService(object):
    def __init__(self, redis: Redis):
        self.redis = redis

    def save(self, meta: Metadata):
        self.redis.set(self._redis_key_for_md(meta), meta.to_json_str(include_path=True))

    def load(self, id: str, type: str = None, parent: str = None):
        val = self.redis.get(self._redis_key(id, type, parent))
        if val is None:
            return val
        return Metadata.from_json_str(val)

    def _redis_key_for_md(self, meta: Metadata):
        return self._redis_key(meta.id, meta.type, meta.parent)

    @staticmethod
    def _redis_key(id: str, type: str = None, parent: str = None):
        if parent:
            return f'emoji:{parent}:{type}:{id}'
        return 'emoji:{meta.id}:{type}'
