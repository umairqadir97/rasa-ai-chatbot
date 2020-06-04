import json


def add_intent_to_domain_file(json_file):
    """This fuction takes intent.json file containing intent name and training sentences
        and adds intent name in the domain.yml file also makes a .md file of the intent
        and wites it to the english_agent/data/nlu/added_intent.md"""
    neww_list = []

    data = json.load(open(json_file))
    intent_name = "- " + data["intent_name"]
    header = "## intent:" + data["intent_name"]
    training_sentences = ['- ' + line for line in data['training_samples']]
    text = header + "\n" + "\n".join(training_sentences)

    f = open('domain.yml', 'r+')
    s = f.read().strip().split("\n")
    while '' in s:
        s.remove('')
    entities_index = s.index("entities:")
    neww_list = s[:entities_index] + [intent_name] + s[entities_index:]

    with open('domain.yml', 'w') as file:
        for item in neww_list:
            file.write("%s\n" % item)

    file_path = "english_agent/data/nlu/"
    output_md_filepath = file_path + json_file.replace('.json', '.md')
    with open(output_md_filepath, 'w') as f2:
        f2.write(text)
