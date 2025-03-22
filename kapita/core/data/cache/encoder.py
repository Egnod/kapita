import base64
import datetime
import decimal
import gzip
import json
import typing as t


class CacheEncoder:
    datetime_tag = 0
    decimal_tag = 1

    @classmethod
    def json_to_dt(cls, obj: dict[str, t.Any]) -> datetime.datetime | decimal.Decimal | dict[str, t.Any]:
        tag_type = obj.pop("__type__", None)

        if tag_type == cls.datetime_tag:
            return datetime.datetime.fromisoformat(obj["__data__"])
        elif tag_type == cls.decimal_tag:
            return decimal.Decimal(obj["__data__"])

        return obj

    @classmethod
    def dt_to_json(cls, obj: t.Any) -> dict[str, t.Any]:
        if isinstance(obj, datetime.datetime):
            return {"__type__": cls.datetime_tag, "__data__": obj.replace(tzinfo=datetime.UTC).isoformat()}
        elif isinstance(obj, decimal.Decimal):
            return {"__type__": cls.decimal_tag, "__data__": str(obj)}
        else:
            raise TypeError("Cant serialize {}".format(obj))

    @classmethod
    def loads(cls, data: bytes, from_base64: bool = False) -> t.Any:
        """loads.

        :param data:
        :type data: bytes
        :rtype: dict[str, typing.Any] | typing.Any
        """
        if from_base64:
            data = base64.b85decode(data)

        return json.loads(gzip.decompress(data), object_hook=cls.json_to_dt)

    @classmethod
    def dumps(cls, data: t.Any, to_base64: bool = False) -> bytes:
        """dumps.

        :param data:
        :type data: typing.Any
        :rtype: bytes
        """
        data = gzip.compress(json.dumps(data, default=cls.dt_to_json).encode())

        if to_base64:
            data = base64.b85encode(data)

        return data
