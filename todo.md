## Rasa_Chatbot, TODO
-- kepp rasa-x out_of_requirements file
rasa-x==0.22.1




sudo apt-get update -y

sudo apt-get install docker.io

sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

cd base_docker; 

bash ./base_docker.sh

cd ..

bash ./run.sh


### Documentation
-- done for parsers

add doc-strigns for:
- parsers
- actions
- api
- api helper
- endpoints
- spell checker module
- Format (standard Python docString format):
    """
    Parse 'domain.yml' file to json object and write to file
    :param path_to_domain_yml: 
    :param path_to_domain_json:
    :return:
    """

- General Layout:
    project_root/
    │
    ├── project/  # Project source code
    ├── docs/
    ├── README
    ├── HOW_TO_CONTRIBUTE
    ├── CODE_OF_CONDUCT
    ├── examples.py

- example.py: A Python script file that gives simple examples of how to use the projects.

### Parsers
- compiler for Domain Parser (json_domain to yml_domain)
- make classes for all parsers (intent_parser, sotyr_parser, domain_parser)


### Dockerize
- dockerize the whole solution
- check for required ports & endpoints


## Sepll Checker
- need to refine code
- code for generating delbrate misspells need to be ingrated with current InvertedIndex generator function
    in this module 'generate_inverted_index.generate_misspells' 
- add in API pipeline



## Random

"""
Done
-> intent parser
-> stories parser
--> documentation, user manual, api reference
--> UI iteration will only be done through json format
--> domain parser
	1) parse domain to json formats first
	2):
	- dialogflow single click train/test model
	- domain file dependencies (intents, actions, utter_actions, entities, synonyms)
	- validation of above files?? UI/Backend??
	- source for domain.yml dependencies	(==> resources folder in agent)
		-- entities, synonyms, lookup tables**, utter_actions
		-- entities and synonyms in a single json file
		-- actions/utter_hello_user.json	==> separate file for eachlist-of-all-utter-action
--> separate model testing for nlu & core
	- testing through code rather than terminal commands, results manipulation would be easy

- transcribing the latent space of POS
--> train/test split for NLU data & dialogue management
rasa agent dependencies:
	- nlu.md (or .md files for each intent)
	- stories.md
	- domain.yml
	- config.yml
	- endpoints.yml

test dependencies:
(separately is preffered)
	- test_data for nlu
	- test data for dialogue management
	- including all above....


scripts and DB created for intent wise analytics
	- calling above functions and passing out relent parameters(intent name, )

something to create markdown files
create stories with drag & drop
	- .md to json to flowchat
	- flowchart to json to .md

? does entity chagnes the accuracy score 
"""


## Types of Program Documentation
Good developers understand the types of documentation and their importance and 
   that the importance and role varies from type to type.

1- User manuals. This is the how-to software to which users turn when they're figuring things out. 
    How do you configure the software? How do you convert a file? Can you add images? 
    How do you fix a mistake? Even if the solution is a single click on the toolbar or the menu, 
    there may be a lot of potential clicks through which to wade. Good user documentation makes it easier.
    
2- Project documentation. Details of the project's development are valuable to your team as they work on it and 
    possibly to users who want to customize an open-source program, for instance. The documentation can include 
    contribution policies, best practices, change logs, product requirements, design guidelines and road maps.
    
3- Requirements documentation. You'll usually draw this up at the start of the project. It defines the expectations 
    for the software, including functional requirements, hardware requirements, compatibility and limitations.
    
4- Architecture documentation. Defines the high-level architecture of the system: the components, their functions and 
    the data and control flow.

5- Technical documentation. Written for a technical audience, this covers the code, algorithms and interface.
