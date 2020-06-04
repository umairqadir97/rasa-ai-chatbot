import json


def add_intent_to_domain_file_and_nlu_directory(intent_json_file):
    """This function takes intent.json file containing intent name and training sentences
        and adds intent name in the domain.yml file also makes a .md file of the intent
        and writes it to the english_agent/data/nlu/added_intent.md"""
    neww_list = []
    path_to_domain_file = "domain.yml"
    data = json.load(open(intent_json_file))
    intent_from_json = data["intent_name"] + ".md"
    intent_name = "- " + data["intent_name"]
    header = "## intent:" + data["intent_name"]
    training_sentences = ['- ' + line for line in data['training_samples']]
    text = header + "\n" + "\n".join(training_sentences)

    f = open(path_to_domain_file, 'r+')
    s = f.read().strip().split("\n")
    while '' in s:
        s.remove('')
    entities_index = s.index("entities:")
    neww_list = s[:entities_index] + [intent_name] + s[entities_index:]

    with open(path_to_domain_file, 'w') as file:
        for item in neww_list:
            file.write("%s\n" % item)
    print("- Intent name:" + intent_from_json + " added in the domain file.")

    file_path = "./data/nlu/"
    output_md_filepath = file_path + intent_from_json
    print("- Intent.md:" + intent_from_json + " file added to the nlu directory")
    with open(output_md_filepath, 'w') as f2:
        f2.write(text)


def action_registration_in_domain_file(action_json_file):
    """This function takes action.json file containing action name and training sentences
       and adds the action name to domain.yml file also adds training sentences under specific
       action"""
    domain_items_list = []
    second_list = []
    third_list = []
    path_to_domain_file = "domain.yml"
    data = json.load(open(action_json_file))
    action_name = "- " + data["action_name"]
    action_name_template = "  " + data["action_name"] + ":"
    training_templates = ['  - text: ' + line for line in data['training_samples']]
    #     training_templates = training_sentences[0:3]

    f = open(path_to_domain_file, 'r+')
    s = f.read().strip().split("\n")
    while '' in s:
        s.remove('')

    forms_index = s.index("forms:")
    domain_items_list = s[:forms_index] + [action_name] + s[forms_index:]
    action_index = domain_items_list.index('actions:')

    answer = action_name_template in domain_items_list
    if answer == True:
        print("- Action already present,training sentences added under the actions section in the domain.yml file.")
        action_template_already_index = domain_items_list.index(action_name_template)
        third_list = domain_items_list[:action_template_already_index + 1] + training_templates + domain_items_list[
                                                                                                  action_template_already_index + 1:]
        #         pprint(third_list)
        with open(path_to_domain_file, 'w') as file:
            for item in third_list:
                file.write("%s\n" % item)

    else:
        print("- Action is not present in the domain.yml, so the action and there template sentences are added.")
        second_list = domain_items_list[:action_index] + [
            action_name_template] + training_templates + domain_items_list[action_index:]
        #         pprint(second_list)
        with open(path_to_domain_file, 'w') as file:
            for item in second_list:
                file.write("%s\n" % item)


def add_new_functionality(path_to_intent_json, path_to_action_json):
    add_intent_to_domain_file_and_nlu_directory(path_to_intent_json)
    action_registration_in_domain_file(path_to_action_json)


if __name__ == '__main__':
    intent_file_json = "./sample_data/sample_intent_json.json"
    action_file_json = "./sample_data/sample_action_json.json"
    add_new_functionality(intent_file_json, action_file_json)
