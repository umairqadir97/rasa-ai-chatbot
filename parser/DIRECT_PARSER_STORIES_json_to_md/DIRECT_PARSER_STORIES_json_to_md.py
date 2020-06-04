import json


def DIRECT_PARSER_STORIES_json_to_md(input_json_file):
    data = json.load(open(input_json_file))
    master_list = []
    hash_str = "## "
    asterik_str = "* "
    action_str = "    - "
    slot_str = "    - slot"
    form_str = "    - form"
    x = 0
    while x < len(data):
        for line in data:
            main_list = []
            for y in range(len(line)):
                sentence = data[x][y]
                if data[x][y].keys() == {'header'}:
                    header = hash_str + data[x][y]["header"]
                    main_list.append(header + '\n')
                elif data[x][y].keys() == {'section'}:
                    section = asterik_str + data[x][y]["section"]["name"]
                    main_list.append(section + '\n')
                elif data[x][y].keys() == {'sub_section'}:
                    if data[x][y]["sub_section"]["type"] == 'slot':
                        sub_section_slot_name = data[x][y]["sub_section"]["name"]
                        sub_section_slot_value = data[x][y]["sub_section"]["value"]
                        new_dict = {}
                        new_dict[sub_section_slot_name] = sub_section_slot_value
                        dic = slot_str + json.dumps(new_dict)
                        main_list.append(dic + '\n')
                    elif data[x][y]["sub_section"]["type"] == 'action':
                        sub_section_action = action_str + data[x][y]["sub_section"]["name"]
                        main_list.append(sub_section_action + '\n')
                    elif data[x][y]["sub_section"]["type"] == 'form':
                        sub_section_form_name = data[x][y]["sub_section"]["name"]
                        sub_section_form_value = data[x][y]["sub_section"]["value"]
                        new_dict = {}
                        new_dict[sub_section_form_name] = sub_section_form_value
                        dic2 = form_str + json.dumps(new_dict)
                        main_list.append(dic2 + '\n')
                    elif data[x][y]["sub_section"]["type"] == 'intent':
                        sub_section_intent = asterik_str + data[x][y]["sub_section"]["name"]
                        main_list.append(sub_section_intent + '\n')
                    else:
                        False
                else:
                    False

            x += 1
            master_list.append(main_list)
    print(master_list)
    output_md_file = input_json_file.replace('.json', '.md')
    with open(output_md_file, 'w') as file:
        for li in master_list:
            for l in li:
                file.write(l)
            file.write('\n')
    return master_list


DIRECT_PARSER_STORIES_json_to_md("stories.json")
