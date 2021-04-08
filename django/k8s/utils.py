from datetime import datetime
import json


class DateEncoder(json.JSONDecoder):

    def default(self, obj):
        print('---------------')

        if isinstance(obj, datetime):
            return obj.__str__()

        return json.JSONDecoder.default(self, obj)
