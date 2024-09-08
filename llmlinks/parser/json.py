import re
import json


def parse(text):
    matcher_json = r'\{[\s\S]*?\}'  # 仕様に正確に従っているわけではないので注意
    json_strings = re.findall(matcher_json, text)

    json_data = []
    for json_string in json_strings:
        try:
            json_data += [json.loads(json_string)]
        except json.JSONDecodeError:
            print(f'decode error: {json_string}')
    return json_data
