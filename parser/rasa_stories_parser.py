import json
import re


def get_story_element_meta(element_string):
    """Helper function to Stories Parser, for formatting single element in a story block"""
    element_string = re.sub(r"[^a-zA-Z0-9:_{}\'\"]*", "", element_string)
    if element_string.startswith("action_") or element_string.startswith("utter_"):
        return {"type": "action", "name": re.sub(r"[^a-zA-Z0-9:_]*", "", element_string), "value": "null"}
    elif element_string.startswith("slot"):
        name, value = re.sub(r"[^a-zA-Z0-9:_]*", "", element_string.replace("slot", "")).split(":")
        return {"type": "slot", "name": name, "value": value}
    elif element_string.startswith("form"):
        name, value = re.sub(r"[^a-zA-Z0-9:_]*", "", element_string.replace("form", "")).split(":")
        return {"type": "form", "name": value, "value": ""}
    else:
        return False


def get_story_element_text_format(element_json):
    """Helper function to Stories Parser, for converting story element from from json format to text"""
    if element_json['type'] == 'action':
        return element_json['name']
    elif element_json['type'] == 'slot':
        return 'slot{{"{slot_name}" : "{slot_value}"}}'.format(slot_name=element_json['name'],
                                                               slot_value=element_json['value'])
    elif element_json['type'] == 'form':
        return 'form{{"name": "{form_name}"}}'.format(form_name=element_json['name'])
    else:
        return False


def get_stort_json_from_md(story):
    """Helper function to Stories Parser, for parsing a single story section text to json"""
    story_json = {}
    story_json["header"], sections = story.split("\n")[0].strip(), \
        [section for section in "\n".join(story.split("\n")[1:]).split("*") if section]
    story_json["sections"] = []
    for section in sections:
        section_json = dict()
        section_json["intent"], section_json["elements"] = section.split("\n")[0], section.split("\n")[1:]
        section_json["elements"] = [get_story_element_meta(elt) for elt in section_json["elements"] if elt
                                    and get_story_element_meta(elt)]
        story_json["sections"].append(section_json)
    return story_json


def get_story_md_from_json(story_json):
    """Helper function to Stories PArser, for converting single story section from json object to text"""
    story_text = "## " + story_json['header'] + "\n"
    for section in story_json['sections']:
        section_text = "* " + section['intent'] + "\n"
        section_text += "\n".join(['    - '+ get_story_element_text_format(elt) for elt in section['elements'] if elt and get_story_element_text_format(elt)])
        story_text += section_text + "\n"
    return story_text


def parse_stories_text_to_json(path_to_stories_md, path_to_output_json=''):
    """
    Chatbot Stories Parser; will convert chatbot storoies file to Json format.
    :param path_to_stories_md: Complete path to 'stories.md'
    :param path_to_output_json: Complete path to output json file <sample_stories.json>
    :return: Returns the parsed json object
    """
    with open(path_to_stories_md, "r") as file:
        stories = file.read().split("##")
    stories = [get_stort_json_from_md(story) for story in stories if story]
    if path_to_output_json:
        with open(path_to_output_json, 'w') as file:
            json.dump(stories, file,  indent=4)
    return stories


def get_stories_text_from_json(path_to_stories_json, path_to_output_md=''):
    """
    Chatbot Stories Writer; will convert given json stories object to chatbot compliant text format(stories.md)
    :param path_to_stories_json: Complete path to Stories json file
    :param path_to_output_md: Complete path to output Stories text file(.md)
    :return: Return text string for chatbot stories
    """
    with open(path_to_stories_json, 'r') as file:
        stories = json.load(file)
    stories_text = "\n".join([get_story_md_from_json(story_json) for story_json in stories])
    if path_to_output_md:
        with open(path_to_output_md,'w') as file:
            file.write(stories_text)
    return stories_text
