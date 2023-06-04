# Project 1: Reported Emissions with ChatGP

Gathering data needed for portfolio decarbonization can be challenging for three reasons:
- Emissions reporting is not well-standardized yet, and not freely available in a centralized platform
- Data disclosed by companies can be misleading (especially for Scope 3)
- A majority of companies still doesn't disclose any data about carbon emissions, or only disclose partial data (especially without Scope 3 reporting)

In this part, we will test how ChatGPT can help in gathering emissions data disclosed by companies.


First, you need to make sure that both `openai` and `langchain` are installed:

```Python
!pip install openai
!pip install langchain
```

You need to declare your OpenAI API as an environment variable:

```Python
import os
os.environ["OPENAI_API_KEY"] = openai_api_key = open('key.txt','r').read()
```

## ChatIE

In this section, we expose the zero shot information extraction framework, based on ChatGPT capabilities.

### What is Information Extraction?

Information extraction aims to extract structured information from unstructured text into structured data formats. Tasks can be:
- entity-relation extract (RE)
- named entity recognition (NER)
- event extraction (EE)

Information extraction systems are usually build with a supervised learning approach, involving labeling data, which is time-consuming.

On the other side, recent works on large-scale pre-trained language models (LLMs) such as GPT-3 (Brown et al., 2020 {cite:p}`brown2020language`) shows impressive results on various tasks without tuning the initial parameters but only with a few labeled examples (few-shot learning).

### ChatIE Framework for Zero-Shot IE

In their paper, Wei et al. (2023) propose a framework to prompt LLMs, and ChatGPT in particular, to perfom zero-shot IE tasks. More specifically, the authors propose the ChatIE framework that transforms the zero-shot IE task into a multi-turn question answering problem, with a two-stage approach:
- in the first stage, the aim is to find the corresponding element types existing in a sentence
- in the second stage, it performs a chained information extraction to each element from the previous stage
Each stage is implemented with a multi-turn QA process. 
In each turn, the authors construct prompts based on pre-designed templates and previously extracted information as input to ask ChatGPT.
Finally, the results of each are turned into structured data.

The IE task is thus decomposed into two stages, each one containing several turns of QA (dialogue with ChatGPT). 

### IE Tasks and ChatIE

#### Entity-Relation Triple Extraction

Let's denote a sente $x$ and question prompt $q$, the model is built to predict triples (Wei et al., 2023):

\begin{equation}
T(x) = \{(s_1,r_1,o1),\cdots, (s_n, r_n, o_n)\}
\end{equation}

For an output triple $(s,r,o)$ the process can be expressed as (Wei et al., 2023):

\begin{equation}
p((s,r,o)|x,q) = p(r|x, q_1)p((s,o)|q_r)\cdots
\end{equation}

with $q_1$ is the question generated using relation types list $R$ and the corresponding template in the first stage and $q_r$ is the question generated using the template related to the previously extracted relation type in the second stage.

$x$ is omitted in the second stage because ChatGPT can record the relevant information of each turn QA. 

In adition, further several turns QA are needed for complex-object values (ie. object with multiple attributes).

Let's have an example in Python.

We assume the following sentence:

"Bob worked for Google in Beijing, the capital of China"

The relation-types are the followings:
- 'location-located_in'
- 'administrative_division-country'
- 'person-place_lived'
- 'person-company'
- 'person-nationality' 
- 'company-founders'
- 'country-administrative_divisions'
- 'person-children'
- 'country-capital'
- 'deceased_person-place_of_death'
- 'neighborhood-neighborhood_of'
- 'person-place_of_birth'

The subject types are:
- 'organization'
-  'person'
- 'location'
- 'country'

And the object types are:
- 'person'
- 'location'
- 'country'
- 'organization'
- 'city'

Let's first define the `relation_types` dictionnary:

```Python
relation_types = {
            'location-located_in': ['location', 'location'],
            'administrative_division-country': ['location', 'country'],
            'person-place_lived': ['person', 'location'],
            'person-company': ['person', 'organization'],
            'person-nationality': ['person', 'country'],
            'company-founders': ['organization', 'person'],
            'country-administrative_divisions': ['country', 'location'],
            'person-children': ['person', 'person'],
            'country-capital': ['country', 'city'],
            'deceased_person-place_of_death': ['person', 'location'],
            'neighborhood-neighborhood_of': ['location', 'location'],
            'person-place_of_birth': ['person', 'location'],
            }
```

We instantiate our `ChatOpenAI` object:

```Python
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(temperature = 0.0,
                  )
```


#### First Stage RE

We can now begin with the first stage of the process.  

We want to format the answer into an easily parsable format:

```Python
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
response_schemas = [
    ResponseSchema(name="answer", description="answer to the user's question.\
    output it as a comma separated Python list"),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()
```

We create the prompt template for the first stage:

```Python
relation_extraction_template_stage_1 = """The given sentence is "{sentence}\n\n\
List of given relations:"{rtl}"\n\n\
What relations in the given list might be included in this given sentence?\n\
If not present, answer: none.\n\
{format_instructions}
"""

from langchain.prompts import ChatPromptTemplate

first_prompt_template = ChatPromptTemplate.from_template(relation_extraction_template_stage_1)

first_message = first_prompt_template.format_messages(sentence = sentence,
                                          rtl = rtl,
                                          format_instructions = format_instructions)
print(first_message[0].content)
```
The message is:
```
The given sentence is "Bob worked for Google in Beijing, the capital of China.

List of given relations:"['location-located_in', 'administrative_division-country', 'person-place_lived', 'person-company', 'person-nationality', 'company-founders', 'country-administrative_divisions', 'person-children', 'country-capital', 'deceased_person-place_of_death', 'neighborhood-neighborhood_of', 'person-place_of_birth']"

What relations in the given list might be included in this given sentence?
If not present, answer: none.
The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "\`\`\`json" and "\`\`\`":

json
{
	"answer": string  // answer to the user's question.    output it as a comma separated Python list
}
```

And let's ask ChatGPT for the first stage answer:

```Python
response = chat(first_message)
print(response.content)
output = output_parser.parse(response.content)
output["answer"]
```

And the output is:

```
['person-company', 'location-located_in', 'country-capital']
```

#### Second Stage RE

Let's now address the second stage of the RE process.

We first need to create a template for the $n$ chained questions to ChatGPT:

```Python
relation_extraction_template_stage_n = """The given sentence is: "{sentence}" \n\n\
    According to the given sentence,\
    the two entities are of type ('{type_1}', '{type_2}')\
    and the relation between them is '{relation_type}',\
    find the two entities and list them all by group if there are multiple groups.\n\
    If not present, answer: none.\n\

    Extract the following information:
    '{type_1}': the entities of type '{type_1}' and output them as a comma separated Python list \n\
    '{type_2}': the entities of type '{type_2}' and output them as a comma separated Python list \n\

    Respond in the form of a JSON with the following keys:\
    '{type_1}', '{type_2}'
"""

n_prompt_template = ChatPromptTemplate.from_template(relation_extraction_template_stage_n)

relation_type = output["answer"][0]
type_1 = relation_types[relation_type][0]
type_2 = relation_types[relation_type][1]
n_message = n_prompt_template.format_messages(sentence = sentence,
                                          type_1 = type_1,
                                          type_2 = type_2,
                                          relation_type = relation_type)
print(n_message[0].content)
```

The message is:

```
The given sentence is: "Bob worked for Google in Beijing, the capital of China." 

According to the given sentence,the two entities are of type ('person', 'organization')and the relation between them is 'person-company',find the two entities and list them all by group if there are multiple groups.
If not present, answer: none.
Respond in the form of a JSON with the following keys:'person', 'organization'
```

Let's retrieve the answer from ChatGPT:

```Python
second_response = chat(n_message)

import json

json.loads(second_response.content)
```

It results into a readable JSON:

```Json
{'person': ['Bob'], 'organization': ['Google']}
```

#### Format for N Stages

Because we have potentially to ask further questions to ChatGPT, let's create a function to systematize the generation for the second stage:

```Python
def generate_stage_n(chat, relation_type, list_relation_types):
  relation_extraction_template_stage_n = """The given sentence is: "{sentence}" \n\n\
        According to the given sentence,\
        the two entities are of type ('{type_1}', '{type_2}')\
        and the relation between them is '{relation_type}',\
        find the two entities and list them all by group if there are multiple groups.\n\
        If not present, answer: none.\n\

        Extract the following information:
        '{type_1}': the entities of type '{type_1}' and output them as a comma separated Python list \n\
        '{type_2}': the entities of type '{type_2}' and output them as a comma separated Python list \n\

        Respond in the form of a JSON with the following keys:\
        '{type_1}', '{type_2}'
        """
  n_prompt_template = ChatPromptTemplate.from_template(relation_extraction_template_stage_n)
  type_1 = list_relation_types[relation_type][0]
  type_2 = list_relation_types[relation_type][1]
  n_message = n_prompt_template.format_messages(sentence = sentence,
                                            type_1 = type_1,
                                            type_2 = type_2,
                                            relation_type = relation_type)
  second_response = chat(n_message)
  if second_response == "none":
    formated_response = None
  else:
    formated_response = json.loads(second_response.content)
  return formated_response

```

Let's test it:

```Python
generate_stage_n(chat = chat, relation_type = output["answer"][0],
                    list_relation_types=relation_types)
```

```
{'person': ['Bob'], 'organization': ['Google']}
```

```Python
generate_stage_n(chat = chat, relation_type = output["answer"][2],
                    list_relation_types=relation_types)
```

```
{'country': ['China'], 'city': ['Beijing']}
```

#### RE Framework

We can now create a function to define the two-stages process:

```Python
def chatie_re(sentence, list_relation_types):
  
  chat = ChatOpenAI(temperature = 0.0,
                    )
  
  # First stage
  response_schemas = [
    ResponseSchema(name="answer", description="answer to the user's question.\
    output it as a comma separated Python list"),
]
  output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
  format_instructions = output_parser.get_format_instructions()

  relation_extraction_template_stage_1 = """The given sentence is "{sentence}\n\n\
  List of given relations:"{rtl}"\n\n\
  What relations in the given list might be included in this given sentence?\n\
  If not present, answer: none.\n\
  {format_instructions}
  """
  first_prompt_template = ChatPromptTemplate.from_template(relation_extraction_template_stage_1)
  first_message = first_prompt_template.format_messages(sentence = sentence,
                                          rtl = rtl,
                                          format_instructions = format_instructions)
  response = chat(first_message)
  output = output_parser.parse(response.content)

  list_jsons = []
  for i in range(len(output["answer"])):
    answer = generate_stage_n(chat = chat, relation_type = output["answer"][i],
                              list_relation_types=list_relation_types)
    if answer is not None:
      list_jsons.append(answer)

  return list_jsons

```

We can test it:

```Python
test = chatie_re(sentence = sentence,
                 list_relation_types=relation_types)
test
```

The result is:
```
[{'person': ['Bob'], 'organization': ['Google']},
 {'country': ['China'], 'city': ['Beijing']},
 {'location': ['Beijing', 'China']}]
```

It worked!

### Named Entity Recognition

In the NER task, the first stage is to filter out the existing entity types in the sentence given the desired type list. Once the framework returns the entity types, the input for the second stage can be constructed accordingly.

In the second stage, each turn aims to extract the entities of one type. Then, the number of turns in the second stage corresponds to the number of turns in the first stage.

Let's also have an example in Python.

We have the following entity types:

- 'LOC'
- 'PER'
- 'ORG'
- 'MISC'

Let's declare it in a list format in Python:

```Python
entity_types = ["LOC","MISC", "ORG", "PER"]
```

#### First Stage NER

We first create our prompt template:

```Python
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
response_schemas = [
    ResponseSchema(name="answer", description="answer to the user's question.\
    output it as a comma separated Python list"),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

ner_template_stage_1 = """The given sentence is "{sentence}\n\n\
Given a list of entity types:"{list_entity_types}"\n\n\
What entity types may be included in this sentence?\n\
If not present, answer: none.\n\
{format_instructions}
"""

from langchain.prompts import ChatPromptTemplate

first_prompt_template = ChatPromptTemplate.from_template(ner_template_stage_1)

first_message = first_prompt_template.format_messages(sentence = sentence,
                                          list_entity_types = entity_types,
                                          format_instructions = format_instructions)
print(first_message[0].content)
```

Our prompt is:

```
The given sentence is "Bob worked for Google in Beijing, the capital of China.

Given a list of entity types:"['LOC', 'MISC', 'ORG', 'PER']"

What entity types may be included in this sentence?
If not present, answer: none.
The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "\`\`\`json" and "\`\`\`":

json
{
	"answer": string  // answer to the user's question.    output it as a comma separated Python list
}
```

And we can get the answer as a nicely formated Python list:

```Python
response = chat(first_message)
output = output_parser.parse(response.content)
output["answer"]
```

```
['LOC', 'ORG', 'PER']
```

#### Second Stage NER

We can now move to the second stage of the process, with a new prompt template:

```Python
ner_template_stage_n = """The given sentence is: "{sentence}" \n\n\
According to the given sentence,\
please identify the entity whose type is '{entity_type}'
If not present, answer: none.\n\

Extract the following information: \n\
'entity_type': the entity types and output them as a comma separated Python list \n\
'entity_name': the entities names and output them as a comma separated Python list \n\

Respond in the form of a JSON with the following keys:\
'entity_type', 'entity_name'

Make sure to return only the information for entity of type '{entity_type}'
"""

n_prompt_template = ChatPromptTemplate.from_template(ner_template_stage_n)
```

We retrieve the information from the first answer:

```Python
entity_type = output["answer"][0]
```

And we create our second prompt:

```Python
n_message = n_prompt_template.format_messages(sentence = sentence,
                                          entity_type = entity_type)
print(n_message[0].content)
```

```
The given sentence is: "Bob worked for Google in Beijing, the capital of China." 

According to the given sentence,please identify the entity whose type is 'LOC'
If not present, answer: none.

Extract the following information: 
'entity_type': the entity types and output them as a comma separated Python list 
'entity_name': the entities names and output them as a comma separated Python list 

Respond in the form of a JSON with the following keys:'entity_type', 'entity_name'

Make sure to return only the information for entity of type 'LOC'
```

And ask to ChatGPT:

```Python
second_response = chat(n_message)

json.loads(second_response.content)
```

Which gives the expected result:

```JSON
{'entity_type': ['LOC'], 'entity_name': ['Beijing', 'China']}
```

#### Format for N Stages

We can now create our `generate_stage_n_ner` function:

```Python
def generate_stage_n_ner(chat, entity_type, list_entity_types):
  ner_template_stage_n = """The given sentence is: "{sentence}" \n\n\
  According to the given sentence,\
  please identify the entity whose type is '{entity_type}'
  If not present, answer: none.\n\

  Extract the following information: \n\
  'entity_type': the entity types and output them as a comma separated Python list \n\
  'entity_name': the entities names and output them as a comma separated Python list \n\

  Respond in the form of a JSON with the following keys:\
  'entity_type', 'entity_name'

  Make sure to return only the information for entity of type '{entity_type}'
  """
  n_prompt_template = ChatPromptTemplate.from_template(ner_template_stage_n)

  n_message = n_prompt_template.format_messages(sentence = sentence,
                                          entity_type = entity_type)
  
  second_response = chat(n_message)
  if second_response == "none":
    formated_response = None
  else:
    formated_response = json.loads(second_response.content)
  return formated_response
```

And test it:

```Python
generate_stage_n_ner(chat = chat,
                     entity_type=output["answer"][0],
                     list_entity_types=entity_types)
```
```JSON
{'entity_type': ['LOC'], 'entity_name': ['Beijing', 'China']}
```

```Python
generate_stage_n_ner(chat = chat,
                     entity_type=output["answer"][1],
                     list_entity_types=entity_types)
```
```JSON
{'entity_type': ['ORG'], 'entity_name': ['Google']}
```

#### NER Framework

We can now create our `chatie_ner` function, implementing the two stages process:

```Python
def chatie_ner(sentence, list_entity_types):
    chat = ChatOpenAI(temperature = 0.0,
                    )
    
    # First stage
    response_schemas = [
      ResponseSchema(name="answer", description="answer to the user's question.\
      output it as a comma separated Python list"),
  ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    ner_template_stage_1 = """The given sentence is "{sentence}\n\n\
    Given a list of entity types:"{list_entity_types}"\n\n\
    What entity types may be included in this sentence?\n\
    If not present, answer: none.\n\
    {format_instructions}
    """

    first_prompt_template = ChatPromptTemplate.from_template(ner_template_stage_1)

    first_message = first_prompt_template.format_messages(sentence = sentence,
                                              list_entity_types = entity_types,
                                              format_instructions = format_instructions)


    response = chat(first_message)
    output = output_parser.parse(response.content)

    list_jsons = []

    for i in range(len(output["answer"])):
      answer = generate_stage_n_ner(chat = chat, entity_type = output["answer"][i],
                                list_entity_types=entity_types)
      if answer is not None:
        list_jsons.append(answer)

    return list_jsons
```

And test it:

```Python
test = chatie_ner(sentence = sentence,
                 list_entity_types=entity_types)
test
```

```
[{'entity_type': ['LOC'], 'entity_name': ['Beijing', 'China']},
 {'entity_type': ['ORG'], 'entity_name': ['Google']},
 {'entity_type': ['PER'], 'entity_name': ['Bob']}]
```

Seems to work quite well too!

### Event Extraction

The zero-shot EE task is solved with two stages:
- in the first stage, event classification is performed, formalized as a text classification problem getting event types from a given text
- the second stage is then devoted to argument extraction, formalized as n extraction machine read comprehension (MRC) problem that identifies arguments of specific roles associated with predicted event types from the first stage

Let's test it with Python with a simple example.

We start with a new sentence: 
"Yesterday Bob and his wife got divorced in Guangzhou."

The event type list is:
- 'Personnel:Elect'
- 'Business:Declare-Bankruptcy'
- 'Justice:Arrest-Jail'
- 'Life:Divorce'
- 'Life:Injure'

The argument roles are:
- 'Person'
- 'Entity'
- 'Position'
- 'Time'
- 'Place'
- 'Org'
- 'Agent'
- 'Crime'
- 'Victim'
- 'Instrument'

Let's first create our new illustrative sentence and the event type list:

```Python
sentence = "Yesterday Bob and his wife got divorced in Guangzhou."
event_types = {'Personnel:Elect': ['Person', 'Entity', 'Position', 'Time', 'Place'], 'Business:Declare-Bankruptcy': ['Org', 'Time', 'Place'], 'Justice:Arrest-Jail': ['Person', 'Agent', 'Crime', 'Time', 'Place'], 'Life:Divorce': ['Person', 'Time', 'Place'], 'Life:Injure': ['Agent', 'Victim', 'Instrument', 'Time', 'Place']}
```

#### First Stage EE

Let's first create our first stage template:

```Python
response_schemas = [
    ResponseSchema(name="answer", description="answer to the user's question.\
    output it as a comma separated Python list"),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

ee_template_stage_1 = """The list of event types: {list_event_types} \n\
Given the sentence: '{sentence}' \n\
What types of events are included in this sentence? \n\
Please return the most likely answer according to the list of event types above. \n\
Require the answer in the form: Event type
"""

first_prompt_template = ChatPromptTemplate.from_template(ee_template_stage_1)

first_message = first_prompt_template.format_messages(sentence = sentence,
                                          list_event_types = event_types)
print(first_message[0].content)
```
```
The list of event types: {'Justice:Appeal': ['Defendant', 'Adjudicator', 'Crime', 'Time', 'Place'], 'Justice:Extradite': ['Agent', 'Person', 'Destination', 'Origin', 'Crime', 'Time'], 'Justice:Acquit': ['Defendant', 'Adjudicator', 'Crime', 'Time', 'Place'], 'Life:Be-Born': ['Person', 'Time', 'Place'], 'Life:Divorce': ['Person', 'Time', 'Place'], 'Personnel:Nominate': ['Person', 'Agent', 'Position', 'Time', 'Place'], 'Life:Marry': ['Person', 'Time', 'Place'], 'Personnel:End-Position': ['Person', 'Entity', 'Position', 'Time', 'Place'], 'Justice:Pardon': ['Defendant', 'Prosecutor', 'Adjudicator', 'Crime', 'Time', 'Place'], 'Business:Merge-Org': ['Org', 'Time', 'Place'], 'Conflict:Attack': ['Attacker', 'Target', 'Instrument', 'Time', 'Place'], 'Justice:Charge-Indict': ['Defendant', 'Prosecutor', 'Adjudicator', 'Crime', 'Time', 'Place'], 'Personnel:Start-Position': ['Person', 'Entity', 'Position', 'Time', 'Place'], 'Business:Start-Org': ['Agent', 'Org', 'Time', 'Place'], 'Business:End-Org': ['Org', 'Time', 'Place'], 'Life:Injure': ['Agent', 'Victim', 'Instrument', 'Time', 'Place'], 'Justice:Fine': ['Entity', 'Adjudicator', 'Money', 'Crime', 'Time', 'Place'], 'Justice:Sentence': ['Defendant', 'Adjudicator', 'Crime', 'Sentence', 'Time', 'Place'], 'Transaction:Transfer-Money': ['Giver', 'Recipient', 'Beneficiary', 'Money', 'Time', 'Place'], 'Justice:Execute': ['Person', 'Agent', 'Crime', 'Time', 'Place'], 'Justice:Sue': ['Plaintiff', 'Defendant', 'Adjudicator', 'Crime', 'Time', 'Place'], 'Justice:Arrest-Jail': ['Person', 'Agent', 'Crime', 'Time', 'Place'], 'Justice:Trial-Hearing': ['Defendant', 'Prosecutor', 'Adjudicator', 'Crime', 'Time', 'Place'], 'Movement:Transport': ['Agent', 'Artifact', 'Vehicle', 'Price', 'Origin', 'Destination', 'Time'], 'Contact:Meet': ['Entity', 'Time', 'Place'], 'Personnel:Elect': ['Person', 'Entity', 'Position', 'Time', 'Place'], 'Business:Declare-Bankruptcy': ['Org', 'Time', 'Place'], 'Transaction:Transfer-Ownership': ['Buyer', 'Seller', 'Beneficiary', 'Artifact', 'Price', 'Time', 'Place'], 'Justice:Release-Parole': ['Person', 'Entity', 'Crime', 'Time', 'Place'], 'Conflict:Demonstrate': ['Entity', 'Time', 'Place'], 'Contact:Phone-Write': ['Entity', 'Time'], 'Justice:Convict': ['Defendant', 'Adjudicator', 'Crime', 'Time', 'Place'], 'Life:Die': ['Agent', 'Victim', 'Instrument', 'Time', 'Place']} 
Given the sentence: 'Yesterday Bob and his wife got divorced in Guangzhou.' 
What types of events are included in this sentence? 
Please return the most likely answer according to the list of event types above. 
Require the answer in the form: Event type
```

We can ask to ChatGPT:

```Python
response = chat(first_message)
response.content
```
```
Life:Divorce
```

#### Second Stage EE

We can now create the second stage template:

```Python
ee_template_stage_n = """The list of argument roles corresponding to the event type \
'{event_type}' is '{list_argument_roles}'. \n\
In the sentece '{sentence}', please extract the following information: \n\
'Argument_Role': the list of argument roles corresponding to the event type and output them as a comma separated Python list \n\
'Argument_Content': the list of event argument content corresponding to the argument roles and output them as a comma separated Python list \n\

If not present, answer: none.\n\

Respond in the form of a JSON with the following keys:\
'Argument_Role', 'Argument_Content'
"""

n_prompt_template = ChatPromptTemplate.from_template(ee_template_stage_n)

event_type = response.content
argument_roles = event_types[event_type]

n_message = n_prompt_template.format_messages(sentence = sentence,
                                          event_type = event_type,
                                          list_argument_roles = argument_roles)
print(n_message[0].content)
```
It generates the following prompt based on the previous answer:

```
The list of argument roles corresponding to the event type 'Life:Divorce' is '['Person', 'Time', 'Place']'. 
In the sentece 'Yesterday Bob and his wife got divorced in Guangzhou.', please extract the following information: 
'Argument_Role': the list of argument roles corresponding to the event type and output them as a comma separated Python list 
'Argument_Content': the list of event argument content corresponding to the argument roles and output them as a comma separated Python list 

If not present, answer: none.

Respond in the form of a JSON with the following keys:'Argument_Role', 'Argument_Content'
```

Let's ask again to ChatGPT:

```Python
second_response = chat(n_message)

json.loads(second_response.content)
```

And we have:

```JSON
{'Argument_Role': ['Person', 'Time', 'Place'],
 'Argument_Content': ['Bob and his wife', 'Yesterday', 'Guangzhou']}
```

#### EE Framework

Because we've asked in the first stage to return the most likely event type, we do not need to process n stages. We thus can directly implement our function `chatie_ee` with the two stages:

```Python
def chatie_ee(sentence, list_event_types):
    chat = ChatOpenAI(temperature = 0.0,
                  )
    
    # First stage
    response_schemas = [
    ResponseSchema(name="answer", description="answer to the user's question.\
      output it as a comma separated Python list"),
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    ee_template_stage_1 = """The list of event types: {list_event_types} \n\
    Given the sentence: '{sentence}' \n\
    What types of events are included in this sentence? \n\
    Please return the most likely answer according to the list of event types above. \n\
    Require the answer in the form: Event type
    """

    first_prompt_template = ChatPromptTemplate.from_template(ee_template_stage_1)

    first_message = first_prompt_template.format_messages(sentence = sentence,
                                              list_event_types = event_types) 
    

    response = chat(first_message)

    # Second Stage
    ee_template_stage_n = """The list of argument roles corresponding to the event type \
    '{event_type}' is '{list_argument_roles}'. \n\
    In the sentece '{sentence}', please extract the following information: \n\
    'Argument_Role': the list of argument roles corresponding to the event type and output them as a comma separated Python list \n\
    'Argument_Content': the list of event argument content corresponding to the argument roles and output them as a comma separated Python list \n\

    If not present, answer: none.\n\

    Respond in the form of a JSON with the following keys:\
    'Argument_Role', 'Argument_Content'
    """

    n_prompt_template = ChatPromptTemplate.from_template(ee_template_stage_n)
    event_type = response.content
    argument_roles = event_types[event_type]

    n_message = n_prompt_template.format_messages(sentence = sentence,
                                          event_type = event_type,
                                          list_argument_roles = argument_roles)
    
    second_response = chat(n_message)
    if second_response == "none":
      formated_response = None
    else:
      formated_response =  json.loads(second_response.content)
    return formated_response
```

And test it:

```Python
test = chatie_ee(sentence = sentence,
                 list_event_types=event_types)
test
```

```
{'Argument_Role': ['Person', 'Time', 'Place'],
 'Argument_Content': ['Bob and his wife', 'Yesterday', 'Guangzhou']}
```

## Information Retrieval with the ReAct Framework

Language models have demonstrated impressive capabilities across tasks in language understanding and abilities for reasoning (e.g. chain-of-thought prompting), such as illustrated by the ChatIE framework in the case of information extraction for example.

In a seminal paper, Yao et al. (2022) {cite:p}`yao2022react` proposed a new paradigm combining reasoning and acting paradigms, on which large language models capabilities have been previously applied.

In this framework, actions lead to observation feedback from an external environment. Reasoning traces affect the internal state of the model by reasoning over the context and updating it with information to support future reasoning and acting.

```{figure} react.png
---
name: react
---
Figure: ReAct Framework, from Yao et al. (2022)
```

The `langchain` library uses this paradigm to allow ChatGPT interacting with its environment (eg. `tools`). 

We illustrate it with an information retrieval task with `duckduckgo-search`.

You need first to install the `duckduckgo-search` package:

```Python
!pip install duckduckgo-search
```

Let's make a test with a simple search request:

```Python
from langchain.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
search.run("Tesla stock price?")
```

We obtain the following result:

```
Get the latest Tesla Inc (TSLA) real-time quote, historical performance, charts, and other financial information to help you make more informed trading and investment decisions. Quotes Summary May 26, 2023 6:00 am 8:00 am 10:00 am 12:00 pm 2:00 pm 4:00 pm 6:00 pm 182.5 185 187.5 190 192.5 195 197.5 200 Previous Close $184.47 Key Data Bid Price and Ask Price The bid &... $203.93USD 2.77 1.38% PRE MARKET 4:37 AM EDT 06/01/23 $203.20 -0.73 -0.36% PRE MARKET Vol 67,058 Volume 150,711,736 65 Day Avg Vol 133,130,503 1 Day Range 195.12 - 203.95 52 Week Range 101.81 -... Discover historical prices for TSLA stock on Yahoo Finance. View daily, weekly or monthly format back to when Tesla, Inc. stock was issued. ﻿ intraday 1w 1m 6m ytd 1y 3y 5y max Mountain-Chart Date Compare with Remove all Compare with up to 5 Stocks On Tuesday 05/30/2023 the closing price of the Tesla share was $201.16 on NAS....
```

Let's load all the modules needed and instantiate our endpoint with the ChatGPT API:

```Python
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0)
```

We now create the tool that ChatGPT will have access to:

```Python
from langchain.tools import BaseTool, StructuredTool, Tool, tool


duckduckgo_tool = Tool(
    name='DuckDuckGo Search',
    func= search.run,
    description="Useful for when you need to do a search on the internet to find information that another tool can't find. be specific with your input."
)

tools = [
    duckduckgo_tool
]
```

We can now instantiate our `Agent` (ie. ChatGPT, with a specific ReAct prompt template):

```Python
from langchain.agents import initialize_agent

zero_shot_agent = initialize_agent(
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    tools=tools, 
    llm=llm,
    verbose=True,
    max_iterations=3,
    handle_parsing_errors=True,
)
```

Let's have a test:

```Python
zero_shot_agent.run("When was Barak Obama born?")
```

ChatGPT asks himself this question:
```
> Entering new AgentExecutor chain...
Question: When was Barak Obama born?
Thought: I don't know the answer to this question off the top of my head, so I will need to use a search engine to find the answer.
```

The following action is decided:
```
Action:
{
  "action": "DuckDuckGo Search",
  "action_input": "Barack Obama birthdate"
}
```

The following observation from the web search:
```
Observation: August 4, 1961 (age 61) Honolulu Hawaii Title / Office: presidency of the United States of America (2009-2017), United States United States Senate (2005-2008), United States ... (Show more) Political Affiliation: Democratic Party Awards And Honors: Barack Hussein Obama II (/ b ə ˈ r ɑː k h uː ˈ s eɪ n oʊ ˈ b ɑː m ə / bə-RAHK hoo-SAYN oh-BAH-mə; born August 4, 1961) is an American politician who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, he was the first African-American president of the United States. Obama previously served as a U.S. senator representing Illinois ... Barack Hussein Obama, the 44th and first African-American President of the United States, served from 2008 until 2016. is celebrating his 60th Birthday in 2021. ... Birth date: August 4, 1961. Age: 61. Zodiac Sign: Leo. Background. Barack Obama was the first African American president elected as the 44th president of the United States of ... Politics On Barack Obama's 61st Birthday, He Remembers His Late Mother — and Reveals New Project to Honor Her Former President Obama announced the Ann Dunham Water Garden in honor of his... August 4, 2022 at 2:09 PM · 3 min read. barack Obama in hawaii as a child. Courtesy The Obama Foundation From left: former President Barack Obama with his mother, Ann Dunham, in Hawaii in the '60s. Barack Obama is celebrating his 61st birthday by naming a new addition to the Obama Presidential Center in Chicago after his mother, Ann Dunham.
```

And the thought is:

```
Thought:The answer to the question "When was Barack Obama born?" is August 4, 1961. 
Final Answer: August 4, 1961.
```

The chain-of-thoughts if finished:

```
> Finished chain.
August 4, 1961.
```

## Exercice: Reported Emissions Extraction with ChatGPT

With the ChatIE framework and Information Retrieval with the ReAct paradigm, you know have a toolkit you need for retrieving reported emissions with ChatGPT.

Let's download a dataset with emissions for a handful of stocks:

```Python
import pandas as pd
url = 'https://github.com/shokru/carbon_emissions/blob/main/data_fin.xlsx?raw=true'
data = pd.read_excel(url)
data.rename(columns={"Company":"Symbol"}, inplace = True)

payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
first_table = payload[0]
df = first_table
data = data.merge(df[["Symbol","Security","GICS Sector","GICS Sub-Industry"]], how = "left", on = "Symbol")
set(data["Security"].tolist())
```

```
{'AT&T',
 'Apple Inc.',
 'Bank of America',
 'Boeing',
 'CVS Health',
 'Chevron Corporation',
 'Cisco',
 'Citigroup',
 'Disney',
 'Dominion Energy',
 'ExxonMobil',
 'Ford Motor Company',
 'General Electric',
 'Home Depot (The)',
 'IBM',
 'Intel',
 'JPMorgan Chase',
 'Johnson & Johnson',
 "Kellogg's",
 'McKesson',
 'Merck & Co.',
 'Microsoft',
 'Oracle Corporation',
 'Pfizer',
 'Procter & Gamble',
 'United Parcel Service',
 'UnitedHealth Group',
 'Verizon',
 'Walmart',
 'Wells Fargo'}
```

Let's try to retrieve emissions data for those companies, and compare your results with the emissions in the dataset!


