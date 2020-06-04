import re
import json


def get_intent_json_from_md(input_md_filepath, output_json_filepath=''):
    """
    Chatbot Intent Parser; will parse single text formatted intent data to json compliant format
    :param input_md_filepath: Complete path to intent file <sample_intent.md>
    :param output_json_filepath: Complete path to output json file, optional parameter.
    :return: Returns parsed json object for provided Intent
    """
    with open(input_md_filepath, "r") as file:
        text = [line for line in file.read().split("\n") if line]

    # sample: "## intent:balance.balance_info"
    intent_name = re.sub(r"##[ ]*intent:[ ]*", '', "text[0]")

    # sample: "- how much is my [balance](account_balance)"
    training_samples = [re.sub(r"[-]*", '', line).strip() for line in text[1:] if line]

    # Extract entites list if needed:
    # entites_with_values = {}
    # should it be text based, or should we store positons as well ??

    # Convert it to JSON
    json_object = {'intent_name': intent_name, 'training_samples': training_samples}
    #
    # write to json file
    if not output_json_filepath:
        output_json_filepath=input_md_filepath.replace('.md', '.json')
    with open(output_json_filepath, 'w') as file:
        json.dump(json_object, file)
    return json_object


def get_intent_md_from_json(input_json_filepath, output_md_filepath=''):
    """
    Chatbot Intent Writer; will write json object back to Chatbot compliant text input format(.md)
    :param input_json_filepath: Complete path to
    :param output_md_filepath:
    :return:
    """
    with open(input_json_filepath, 'r') as file:
        json_object = json.load(file)
    header = json_object['intent_name']
    training_samples = ['- ' + line for line in json_object['training_samples']]
    text = header + "\n" + "\n".join(training_samples)
    #
    # write to json file
    if not output_md_filepath:
        output_md_filepath = input_json_filepath.replace('.json', '.md')
    with open(output_md_filepath, 'w') as file:
        file.write(text)
    return text


# if __name__ == '__main__':
#     pass