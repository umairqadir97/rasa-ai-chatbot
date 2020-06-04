import json
import re

file_name = "stories_1.md"
file = open(file_name, "r")
s = file.read().strip()
s = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', s, flags=re.M)
s = s.strip().split('\n')
while '' in s:
    s.remove('')

main_list = []
for idx, i in enumerate(s):
    if i.startswith("##"):
        if idx != 0:
            main_list.append(new_list)
        new_list = []
        new_list.append(i)
    else:
        new_list.append(i)
main_list.append(new_list)


def get_direct_parsed_stories_md_to_json(element):
    data = []
    json_data = {}

    if element.startswith("##"):
        json_data["header"] = element[3:]
        return json_data

    elif element.startswith("*"):
        json_data["section"] = {"type": "intent", "name": element[2:], "value": ""}
        return json_data

    element = re.sub(r"[^a-zA-Z0-9:_.{}\'\"]*", "", element)
    if element.startswith("action_") or element.startswith("utter_"):
        name = re.sub(r"[^a-zA-Z0-9:_.]*", "", element)
        json_data["sub_section"] = {"type": "action", "name": name, "value": "null"}
        return json_data

    elif element.startswith("slot"):
        name, value = re.sub(r"[^a-zA-Z0-9:_]*", "", element.replace("slot", "")).split(":")
        json_data["sub_section"] = {"type": "slot", "name": name, "value": value}
        return json_data

    elif element.startswith("form"):
        name, value = re.sub(r"[^a-zA-Z0-9:_]*", "", element.replace("form", "")).split(":")
        json_data["sub_section"] = {"type": "form", "name": name, "value": value}
        return json_data
    else:
        return False


parsed_data = []
final_data = []
output_json_filepath = file_name.replace('.md', '.json')
for k in main_list:
    final_data = []
    for line in k:
        final_data.append(get_direct_parsed_stories_md_to_json(line))
    parsed_data.append(final_data)

with open(output_json_filepath, "w") as outfile:
    json.dump(parsed_data, outfile, indent=4)


