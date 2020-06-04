import re
import json
import yaml


def domain_parser_yml_to_json(path_to_domain_yml, path_to_domain_json):
    """
    Chatbot Domain Parser, will parse 'domain.yml' file to json object and write to file
    :param path_to_domain_yml: Complete path to YML domain file
    :param path_to_domain_json: Complete path to file where Json Object will be written
    :return: Json string of parsed object
    """
    with open(path_to_domain_yml, "r") as file:
        json_domain = yaml.load(file)
    json_domain["entities"] = parse_entities_to_json(path_to_domain_yml)

    with open(path_to_domain_json, "w") as file:
        json.dump(json_domain, file)
    return json.dumps(json_domain)


def parse_entities_to_json(path_to_domain):
    """
    Helper function for domain_parser, will parser entities and their synonyms
    :param path_to_domain: Complete path to YML domain file
    :return: Json object for all entities in domain
    """
    with open(path_to_domain, "r")as file:
        lines = file.read().split("\n")
    domain_sections = {"intents:": [], "entities:": [], "slots:": [], "actions:": [], "forms:": [], "templates:": []}
    section_name = ""
    for line in lines:
        if line.strip().endswith(tuple(domain_sections.keys())):
            section_name = line
        else:
            domain_sections[section_name].append(line)

    # Parse Entities separately, otherwise 'synonyms' will get mixed
    entity_splits = "\n".join(domain_sections["entities:"]).split("##")
    entities = {re.sub(r"[^a-zA-Z0-9_.]", "", entity): [] for entity in entity_splits[0].split("\n") if entity}
    for elt in entity_splits[1:]:
        lines = elt.split("\n")
        entity_name, synonyms = re.sub(r"[^a-zA-Z0-9_.]", "", lines[0].replace("synonym", "")),\
            [re.sub(r"[^a-zA-Z0-9_.]", "", line) for line in lines[1:] if line]
        if entity_name in entities.keys():
            entities[entity_name] = synonyms
    return entities
