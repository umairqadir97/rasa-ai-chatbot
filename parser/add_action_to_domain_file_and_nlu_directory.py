import json
from pprint import pprint


def action_registration_in_domain_file_and_nlu_directory(json_file):
    """This function takes intent.json file containing intent name and training sentences
       and adds the action name to domain.yml file also adds training sentences under specific
       action"""
    domain_items_list = []
    second_list = []
    third_list = []
    data = json.load(open(json_file))
    action_name = "- utter_" + data["intent_name"]
    action_name_template = "  utter_" + data["intent_name"] + ":"
    print(action_name_template)
    training_sentences = ['  - text: ' + line for line in data['training_samples']]
    training_templates = training_sentences[0:3]

    f = open('domain.yml', 'r+')
    s = f.read().strip().split("\n")
    while '' in s:
        s.remove('')

    forms_index = s.index("forms:")
    domain_items_list = s[:forms_index] + [action_name] + s[forms_index:]
    action_index = domain_items_list.index('actions:')

    answer = action_name_template in domain_items_list
    if answer == True:
        print("Yes")
        action_template_already_index = domain_items_list.index(action_name_template)
        print(action_template_already_index)
        third_list = domain_items_list[:action_template_already_index + 1] + training_templates + domain_items_list[
                                                                                                  action_template_already_index + 1:]
        #         pprint(third_list)
        with open('domain.yml', 'w') as file:
            for item in third_list:
                file.write("%s\n" % item)

    else:
        print("False")
        second_list = domain_items_list[:action_index] + [
            action_name_template] + training_templates + domain_items_list[action_index:]
        #         pprint(second_list)
        with open('domain.yml', 'w') as file:
            for item in second_list:
                file.write("%s\n" % item)
