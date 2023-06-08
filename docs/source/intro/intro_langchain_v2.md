# Project 0: Information Extraction with ChatGPT

Large Language Models (LLMs) have enjoyed a growth in popularity since the release of OpenAI's GPT-3 in 2020 (Brown et al., 2020 {cite:p}`brown2020language`).

After further impressive improvements in LLMs, those models gained the non-specialists when OpenAI released `ChatGPT`.

In this part, we investigate the use of `ChatGPT` for zero-shot information extraction. We begin by introducing the `LangChain` development framework, then we will use `ChatGPT` as a knowledge graph extractor.
## LangChain

`LangChain` is a development framework built around LLMs. The core idea of the library is the chain of different components (modularity) to create advanced use cases with LLMs. 

### Prompt Template

Let's begin with a simple question-answering prompt template.

We first need to install the `langchain` and `openai` libraries:

```Python
!pip install langchain
!pip install openai
```

We also need to load our API key:

```Python
import os
os.environ["OPENAI_API_KEY"] = open('key.txt','r').read()
```

Let's instantiate a `ChatOpenAI` object that will allow us to interact with `ChatGPT`:

```Python
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(temperature = 0.0,
                  )
```


From here, we can import the `ChatPromptTemplate` class and initialize a template like so:

```Python
from langchain.prompts import ChatPromptTemplate

template = """Question: {query} \n
Answer: """

prompt = ChatPromptTemplate.from_template(template)
```
The `{query}` component makes our template 'dynamic'. It means that you will be able to change the content of your message to `ChatGPT` by inserting whatever you want in place of `{query}`.

To illustrate it, let's store into a variable our future question:

```Python
question = "What is 2+2?"
```

Now, we can create our first `LLMChain` and obtain our first answer:

```Python
from langchain import LLMChain

llm_chain = LLMChain(
    prompt = prompt,
    llm = chat
)

print(llm_chain.run(query = question))
```
Note that we assign to the query parameter the variable `question`.

It will insert the question in place of the `{query}`.

The answer we get is:
```
4
```

### Prompt Template: Prompts at Scale

Having a prompt template with a dynamic variable where you can insert different inputs programatically is useful for prompting at scale, that is using the same templace but with a list of different inputs. 

For example:
```Python
questions = [
    {"query":"What is 2+2?"},
    {"query":"What is 3+3?"},
    {"query":"What is 4+4?"}
]
```

Here in `questions` we have a list of questions. We can use it as an input to our `LLMChain`:

```Python
print(llm_chain.run(questions))
```

And we obtain:
```
[{'answer': '4', 'type': 'NUMBER'}, {'answer': '6', 'type': 'NUMBER'}, {'answer': '8', 'type': 'NUMBER'}]
```

### Other Example: Inserting Context to ChatGPT

Another use of dynamic input via prompt templating is to give different context to `ChatGPT`. For example:

```Python
template = """
Given the following context: {context} \n
Question: Who is Bob's wife? \n
Answer: """

prompt = ChatPromptTemplate.from_template(template)

llm_chain = LLMChain(
    prompt = prompt,
    llm = chat
)
```

Let's run our `LLMChain` assigning a specific sentence stored in our variable `sentence`:

```Python
sentence = "Bob is married with Mary"

print(llm_chain.run(context = sentence))
```
We get:
```
Mary
```

### Simple Sequential Chain

You may want to execute further requests to `ChatGPT`, that is a `LLMChain` with the input depending on the output from a previous `LLMChain`.

Let's have an example with a gift recommender, according to the age of a specific person. We have two steps:
1. Determining the age of the person.
2. Given the age of the person, the recommender will give a list of potential gifts.

Let's implement the first stage:

```Python
first_template = """Given the following context: {query} \n
Question: How old is John? \n
Answer: 
"""

first_prompt = ChatPromptTemplate.from_template(first_template)


first_chain = LLMChain(
    prompt = first_prompt,
    llm = chat
)

first_question = "John's age is half dad's age. Dad is 42 years old."

first_response = first_chain.run(query = question)
print(first_response)
```
The answer is:
```
John is 21 years old.
```
Please note that we have assigned the answer to the variable `first_response`.

Let's implement the second stage:

```Python
second_template = """Given the following context:
You are are a gift recommender. Given a person's age, \
it is your job to suggest an approapriate gift for them. \n\

Person Age: \n\
{input} \n\
Suggest gift:
"""

second_prompt = ChatPromptTemplate.from_template(second_template)

second_chain = LLMChain(
    prompt = second_prompt,
    llm = chat
)

final_response = second_chain.run(input = first_response)
print(final_response)
```
Please note that we have used the output from the previous stage `first_response` as an input for the second stage.

The answer is:
```
A nice watch or a gift card to his favorite store would be a great gift for John. Alternatively, you could consider a tech gadget or a book on a topic he is interested in.
```

Rather than proceding step by step, we can make a use of a `SimpleSequentialChain`. It is built with the two `LLMChain` that we have created.

```Python
from langchain.chains import SimpleSequentialChain

overall_chain = SimpleSequentialChain(
    chains = [first_chain, second_chain],
    verbose = True
)
```

And now we only need to give the input of the first stage to the overall process. It will understand automatically that it needs to use the output from the first stage as the input of the second stage:

```Python
overall_chain.run("John's age is half dad's age. Dad is 42 years old.")
```
And the output is:
```
> Entering new SimpleSequentialChain chain...
John is 21 years old.
For John who is 21 years old, a good gift suggestion would be a trendy watch or a gift card to his favorite clothing store. Alternatively, you could consider a tech gadget such as a wireless speaker or a gaming console.

> Finished chain.
For John who is 21 years old, a good gift suggestion would be a trendy watch or a gift card to his favorite clothing store. Alternatively, you could consider a tech gadget such as a wireless speaker or a gaming console.
```

## Exercise

We are going to test if `ChatGPT` can be useful for information extraction (IE). 

Short answer: it is, as confirmed by Wei et al. (2023) {cite:p}`wei2023zero` for zero-shot IE or Shi et al. (2023) {cite:p}`shi2023chatgraph`.

First, reinstantiate everything that we need for this exercise:

```Python
!pip install langchain
!pip install openai
```

```Python

import os
os.environ["OPENAI_API_KEY"] = open('key.txt','r').read()

from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(temperature = 0.0,
                  )
```

We are going to extract information from Wikipedia, in the format of a knowledge graph. 

A knowledge graph is a representation of information (knowledge), such as the following:

```{figure} knowledgegraph.png
---
name: knowledgegraph
---
Figure: Knowledge Graph sample, from WWWC (2014) {cite:p}`world2014rdf`
```

It requires to identify, in a triplet format:
- the head entity
- the relation
- the tail entity

You need to install the `wikipedia` library:

```Python
!pip install wikipedia
```

And you can retrieve information from Wikipedia:

```Python
from langchain.utilities import WikipediaAPIWrapper

wikipedia = WikipediaAPIWrapper(top_k_results = 1)
print(wikipedia.run('Tesla, Inc.'))
```

```
Page: Tesla, Inc.
Summary: Tesla, Inc. ( TESS-lə or  TEZ-lə) is an American multinational automotive and clean energy company headquartered in Austin, Texas. Tesla designs and manufactures electric vehicles (electric cars and trucks), battery energy storage from home to grid-scale, solar panels and solar roof tiles, and related products and services. Tesla is one of the world's most valuable companies and, as of 2023, is the world's most valuable automaker. In 2022, the company had the most worldwide sales of battery electric vehicles, capturing 18% of the market. Through its subsidiary Tesla Energy, the company develops and is a major installer of photovoltaic systems in the United States. Tesla Energy is also one of the largest global suppliers of battery energy storage systems, with 6.5 gigawatt-hours (GWh) installed in 2022.
Tesla was incorporated in July 2003 by Martin Eberhard and Marc Tarpenning as Tesla Motors. The company's name is a tribute to inventor and electrical engineer Nikola Tesla. In February 2004, via a $6.5 million investment, Elon Musk became the largest shareholder of the company. He has served as CEO since 2008. According to Musk, the purpose of Tesla is to help expedite the move to sustainable transport and energy, obtained through electric vehicles and solar power. Tesla began production of its first car model, the Roadster sports car, in 2008. This was followed by the Model S sedan in 2012, the Model X SUV in 2015, the Model 3 sedan in 2017, the Model Y crossover in 2020, and the Tesla Semi truck in 2022. The company plans production of the Cybertruck light-duty pickup truck in 2023. The Model 3 is the all-time bestselling plug-in electric car worldwide, and in June 2021 became the first electric car to sell 1 million units globally. Tesla's 2022 full year deliveries were around 1.31 million vehicles, a 40% increase over the previous year, and cumulative sales totaled 3 million cars as of August 2022. In October 2021, Tesla's market capitalization reached $1 trillion, the sixth company to do so in U.S. history.
Tesla has been the subject of several lawsuits, government scrutiny, journalistic criticism, and public controversies arising from statements and acts of CEO Elon Musk and from allegations of whistleblower retaliation, worker rights violations, and defects with their products.
```

In this exercise, your task is to implement knowledge graph extraction following Shi et al. (2023) two stages process:


```{figure} knowledgeextractor.png
---
name: knowledgeextractor
---
Figure: Two Stage Knowledge Graph Extraction, from Shi et al. (2023)
```

The text refinement prompt to implement is the following:

```text
Please generate a refined document of the following document. And please ensure that the refined document meets the following criteria:
1. The refined document should be abstract and does not change any original meaning of the document.
2. The refined document should retain all the important objects, concepts, and relationships between them.
3. The refined document should only contain information that is from the document.
4. The refined document should be readable and easy to understand without any abbreviations and misspellings.
Here is the content: [x]
```

The knowledge extraction prompt to implement is:
```
You are a knowledge graph extractor, and your task is to extract and return a knowledge graph from a given text.Let’s extract it step by step:
(1). Identify the entities in the text. An entity can be a noun or a noun phrase that refers to a real-world object or an abstract concept. You can use a named entity recognition (NER) tool or a part-of-speech (POS) tagger to identify the entities.
(2). Identify the relationships between the entities. A relationship can be a verb or a prepositional phrase that connects two entities. You can use dependency parsing
to identify the relationships.
(3). Summarize each entity and relation as short as possible and remove any stop words.
(4). Only return the knowledge graph in the triplet format: (’head entity’, ’relation’, ’tail entity’).
(5). Most importantly, if you cannot find any knowledge, please just output: "None".
Here is the content: [x]
```

For example, the final output with Tesla is something as:

```
('Tesla, Inc.', 'is', 'a multinational automotive and clean energy company')
('Tesla, Inc.', 'designs and manufactures', 'electric vehicles, battery energy storage systems, solar panels, and related products and services')
('Tesla, Inc.', 'recognized as', "one of the world's most valuable companies and the world's most valuable automaker as of 2023")
('Tesla, Inc.', 'captured', '18% of the market for battery electric vehicles in 2022')
('Tesla, Inc.', 'is', 'a major installer of photovoltaic systems in the United States')
('Tesla Energy', 'is', 'one of the largest global suppliers of battery energy storage systems')
('Tesla Energy', 'installed', '6.5 gigawatt-hours in 2022')
('Tesla', 'founded', 'in 2003 by Martin Eberhard and Marc Tarpenning as Tesla Motors')
('Elon Musk', 'became', 'the largest shareholder of the company in 2004')
('Elon Musk', 'has served as', 'CEO since 2008')
('Tesla', 'produced', 'several car models, including the Roadster sports car, Model S sedan, Model X SUV, Model 3 sedan, Model Y crossover, and Tesla Semi truck')
('Model 3', 'is', 'the all-time bestselling plug-in electric car worldwide and the first electric car to sell 1 million units globally')
('Tesla', '2022 full year deliveries were', 'around 1.31 million vehicles, a 40% increase over the previous year')
('cumulative sales', 'totaled', '3 million cars as of August 2022')
('Tesla', 'market capitalization reached', '$1 trillion in October 2021')
('Tesla', 'faced', 'lawsuits, government scrutiny, journalistic criticism, and public controversies related to statements and acts of CEO Elon Musk, allegations of whistleblower retaliation, worker rights violations, and defects with their products')
```

## Solution

We need to create two prompts according to the prompt design given above. We have for the first prompt:

```Python
from langchain.prompts import ChatPromptTemplate


first_template = """Please generate a refined document of the following document. \n\
And please ensure that the refined document meets the following criteria: \n\
1. The refined document should be abstract and does not change any original \
meaning of the document. \n\
2. The refined document should retain all the important objects, concepts, and \
relationship between them. \n\
3. The refined document should only contain information that is from \
the document. \n\
4. The refined document should be readable and easy to understand without any \
abbrevations and misspellings. \n\
Here is the content: {content}
"""

first_prompt = ChatPromptTemplate.from_template(first_template)
```

We create the first chain:

```Python
from langchain.chains import LLMChain

first_chain = LLMChain(
    prompt = first_prompt,
    llm = chat
)
```

We create the second prompt and second `LLMChain`:

```Python
second_template = """You are a knowledge graph extractor, and your task is to extract\
and return a knowledge graph from a given text. Let's extract it step by step:\n\
(1). Identify the entities in the text. An entity can be a noun or noun phrase \
that refers to a real-world object or an abstract concept. You can use a named entity\
recognition (NER) tool or a part-of-speech (POS) tagger to identify the entities. \n\
(2). Identify the relationships between the entities. A relationship can be a verb \
or a prepositional phrase that connects two entities. You can use dependency parsing \
to identify the relationships. \n\
(3). Summarize each entity and relation as short as possible and remove any stop words. \n\
(4). Only return the knowledge graph in the triplet format: ('head entity', 'relation', 'tail entity'). \n\
(5). Most importantly, if you cannot find any knowledge, please just output: "None". \n\
Here is the content: {content} 
"""
second_prompt = ChatPromptTemplate.from_template(second_template)

second_chain = LLMChain(
    prompt = second_prompt,
    llm = chat
)
```

And now we can make use of `SimpleSequentialChain`:

```Python
from langchain.chains import SimpleSequentialChain

overall_chain = SimpleSequentialChain(
    chains = [first_chain, second_chain],
    verbose = True
)
```

Let's retrieve the page from Wikipedia:

```Python
from langchain.utilities import WikipediaAPIWrapper

wikipedia = WikipediaAPIWrapper(top_k_results = 1)
wiki_pages = wikipedia.run('Tesla, Inc.')
```

Please note that we have stored the resulting page into the variable `wiki_pages`.

We can now run the entire `SimpleSequentialChain`, by giving the `wiki_pages` as the initial input:

```Python
overall_chain.run(wiki_pages)
```

And we get:

```
> Entering new SimpleSequentialChain chain...
Tesla, Inc. is a multinational automotive and clean energy company based in Austin, Texas. The company designs and manufactures electric vehicles, battery energy storage systems, solar panels, and related products and services. Tesla is the world's most valuable automaker and captured 18% of the battery electric vehicle market in 2022. The company's subsidiary, Tesla Energy, is a major installer of photovoltaic systems in the United States and one of the largest global suppliers of battery energy storage systems. 

Tesla was founded in 2003 by Martin Eberhard and Marc Tarpenning and named after inventor Nikola Tesla. Elon Musk became the largest shareholder in 2004 and has served as CEO since 2008. The company's mission is to expedite the move to sustainable transport and energy through electric vehicles and solar power. Tesla has produced several car models, including the Roadster, Model S, Model X, Model 3, Model Y, and Tesla Semi. The Model 3 is the all-time bestselling plug-in electric car worldwide and the first electric car to sell 1 million units globally. 

Tesla's 2022 full year deliveries were around 1.31 million vehicles, a 40% increase over the previous year, and cumulative sales totaled 3 million cars as of August 2022. In October 2021, Tesla's market capitalization reached $1 trillion, making it the sixth company in U.S. history to do so. However, the company has faced lawsuits, government scrutiny, journalistic criticism, and public controversies related to CEO Elon Musk's statements and actions, whistleblower retaliation, worker rights violations, and product defects.
('Tesla, Inc.', 'is', 'multinational automotive and clean energy company')
('Tesla, Inc.', 'based in', 'Austin, Texas')
('company', 'designs and manufactures', 'electric vehicles, battery energy storage systems, solar panels, and related products and services')
('Tesla', 'is', "world's most valuable automaker")
('Tesla', 'captured', '18% of the battery electric vehicle market in 2022')
('Tesla Energy', 'is', 'major installer of photovoltaic systems in the United States')
('Tesla Energy', 'one of', 'largest global suppliers of battery energy storage systems')
('Tesla', 'founded in', '2003')
('Tesla', 'named after', 'inventor Nikola Tesla')
('Elon Musk', 'became', 'largest shareholder in 2004')
('Elon Musk', 'has served as', 'CEO since 2008')
('company', 'mission is to', 'expedite the move to sustainable transport and energy through electric vehicles and solar power')
('Tesla', 'produced', 'several car models')
('Roadster', 'is', 'car model')
('Model S', 'is', 'car model')
('Model X', 'is', 'car model')
('Model 3', 'is', 'car model')
('Model Y', 'is', 'car model')
('Tesla Semi', 'is', 'car model')
('Model 3', 'is', 'all-time bestselling plug-in electric car worldwide')
('Model 3', 'first', 'electric car to sell 1 million units globally')
('Tesla', '2022 full year deliveries were', 'around 1.31 million vehicles')
('Tesla', 'cumulative sales totaled', '3 million cars as of August 2022')
('Tesla', 'market capitalization reached', '$1 trillion in October 2021')
('Tesla', 'faced', 'lawsuits, government scrutiny, journalistic criticism, and public controversies related to CEO Elon Musk statements and actions, whistleblower retaliation, worker rights violations, and product defects')

> Finished chain.
(\'Tesla, Inc.\', \'is\', \'multinational automotive and clean energy company\')\n(\'Tesla, Inc.\', \'based in\', \'Austin, Texas\')\n(\'company\', \'designs and manufactures\', \'electric vehicles, battery energy storage systems, solar panels, and related products and services\')\n(\'Tesla\', \'is\', "world\'s most valuable automaker")\n(\'Tesla\', \'captured\', \'18% of the battery electric vehicle market in 2022\')\n(\'Tesla Energy\', \'is\', \'major installer of photovoltaic systems in the United States\')\n(\'Tesla Energy\', \'one of\', \'largest global suppliers of battery energy storage systems\')\n(\'Tesla\', \'founded in\', \'2003\')\n(\'Tesla\', \'named after\', \'inventor Nikola Tesla\')\n(\'Elon Musk\', \'became\', \'largest shareholder in 2004\')\n(\'Elon Musk\', \'has served as\', \'CEO since 2008\')\n(\'company\', \'mission is to\', \'expedite the move to sustainable transport and energy through electric vehicles and solar power\')\n(\'Tesla\', \'produced\', \'several ca
```

## Agent

In fact, we can make the wikipedia content retrieval part of the `SimpleSequentialChain`. To do so, we need to use the concet of 'agent' and 'tools'.

We need to load some new classes and functions:

```Python
from langchain.agents import initialize_agent 
from langchain.agents import AgentType
from langchain.agents import load_tools

chat = ChatOpenAI(temperature = 0.)
```

Wikipedia scrapper is part of the pre-built tools in `langchain`. We can declare a list of tools as such:

```Python
tools = load_tools(["wikipedia"], llm = chat, top_k_results = 1)
```

We need to initialize our agent, specifying the list of tools:

```Python

agent = initialize_agent(tools,
                         llm = chat,
                         agent = AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                        handle_parsing_errors=True,
                         verbose = True
                         )
```

Let's try to see if `ChatGPT` can handle the use of the wikipedia tool:

```Python
agent.run("Tesla, Inc.")
```

It does:
```
> Entering new AgentExecutor chain...
Question: What is Tesla, Inc.?
Thought: I should use Wikipedia to get information about Tesla, Inc.
Action:
{
  "action": "Wikipedia",
  "action_input": "Tesla, Inc."
}

Observation: Page: Tesla, Inc.
Summary: Tesla, Inc. ( TESS-lə or  TEZ-lə) is an American multinational automotive and clean energy company headquartered in Austin, Texas. Tesla designs and manufactures electric vehicles (electric cars and trucks), battery energy storage from home to grid-scale, solar panels and solar roof tiles, and related products and services. Tesla is one of the world's most valuable companies and, as of 2023, is the world's most valuable automaker. In 2022, the company had the most worldwide sales of battery electric vehicles, capturing 18% of the market. Through its subsidiary Tesla Energy, the company develops and is a major installer of photovoltaic systems in the United States. Tesla Energy is also one of the largest global suppliers of battery energy storage systems, with 6.5 gigawatt-hours (GWh) installed in 2022.
Tesla was incorporated in July 2003 by Martin Eberhard and Marc Tarpenning as Tesla Motors. The company's name is a tribute to inventor and electrical engineer Nikola Tesla. In February 2004, via a $6.5 million investment, Elon Musk became the largest shareholder of the company. He has served as CEO since 2008. According to Musk, the purpose of Tesla is to help expedite the move to sustainable transport and energy, obtained through electric vehicles and solar power. Tesla began production of its first car model, the Roadster sports car, in 2008. This was followed by the Model S sedan in 2012, the Model X SUV in 2015, the Model 3 sedan in 2017, the Model Y crossover in 2020, and the Tesla Semi truck in 2022. The company plans production of the Cybertruck light-duty pickup truck in 2023. The Model 3 is the all-time bestselling plug-in electric car worldwide, and in June 2021 became the first electric car to sell 1 million units globally. Tesla's 2022 full year deliveries were around 1.31 million vehicles, a 40% increase over the previous year, and cumulative sales totaled 3 million cars as of August 2022. In October 2021, Tesla's market capitalization reached $1 trillion, the sixth company to do so in U.S. history.
Tesla has been the subject of several lawsuits, government scrutiny, journalistic criticism, and public controversies arising from statements and acts of CEO Elon Musk and from allegations of whistleblower retaliation, worker rights violations, and defects with their products.
```

The `agent` is a specific type of chain, and can thus be included in our `SimpleSequentialChain`:

```Python
overall_chain = SimpleSequentialChain(
    chains = [agent,
              first_chain,
              second_chain],
    verbose = True
)
```

We can thus run the entire process, starting from the Wikipedia research:

```Python
overall_chain.run("Tesla, Inc.")
```

And it handles the entire process by itself:

```
> Entering new SimpleSequentialChain chain...


> Entering new AgentExecutor chain...
Question: What is Tesla, Inc.?
Thought: I should use Wikipedia to get information about Tesla, Inc.

Action:

{
  "action": "Wikipedia",
  "action_input": "Tesla, Inc."
}


Observation: Page: Tesla, Inc.
Summary: Tesla, Inc. ( TESS-lə or  TEZ-lə) is an American multinational automotive and clean energy company headquartered in Austin, Texas. Tesla designs and manufactures electric vehicles (electric cars and trucks), battery energy storage from home to grid-scale, solar panels and solar roof tiles, and related products and services. Tesla is one of the world's most valuable companies and, as of 2023, is the world's most valuable automaker. In 2022, the company had the most worldwide sales of battery electric vehicles, capturing 18% of the market. Through its subsidiary Tesla Energy, the company develops and is a major installer of photovoltaic systems in the United States. Tesla Energy is also one of the largest global suppliers of battery energy storage systems, with 6.5 gigawatt-hours (GWh) installed in 2022.
Tesla was incorporated in July 2003 by Martin Eberhard and Marc Tarpenning as Tesla Motors. The company's name is a tribute to inventor and electrical engineer Nikola Tesla. In February 2004, via a $6.5 million investment, Elon Musk became the largest shareholder of the company. He has served as CEO since 2008. According to Musk, the purpose of Tesla is to help expedite the move to sustainable transport and energy, obtained through electric vehicles and solar power. Tesla began production of its first car model, the Roadster sports car, in 2008. This was followed by the Model S sedan in 2012, the Model X SUV in 2015, the Model 3 sedan in 2017, the Model Y crossover in 2020, and the Tesla Semi truck in 2022. The company plans production of the Cybertruck light-duty pickup truck in 2023. The Model 3 is the all-time bestselling plug-in electric car worldwide, and in June 2021 became the first electric car to sell 1 million units globally. Tesla's 2022 full year deliveries were around 1.31 million vehicles, a 40% increase over the previous year, and cumulative sales totaled 3 million cars as of August 2022. In October 2021, Tesla's market capitalization reached $1 trillion, the sixth company to do so in U.S. history.
Tesla has been the subject of several lawsuits, government scrutiny, journalistic criticism, and public controversies arising from statements and acts of CEO Elon Musk and from allegations of whistleblower retaliation, worker rights violations, and defects with their products.


Thought:I have a good understanding of what Tesla, Inc. is and its history. 
Final Answer: Tesla, Inc. is an American multinational automotive and clean energy company that designs and manufactures electric vehicles, battery energy storage, solar panels and solar roof tiles, and related products and services. It was incorporated in July 2003 by Martin Eberhard and Marc Tarpenning as Tesla Motors, and named after inventor and electrical engineer Nikola Tesla. Elon Musk became the largest shareholder of the company in February 2004 and has served as CEO since 2008. Tesla's purpose is to help expedite the move to sustainable transport and energy, obtained through electric vehicles and solar power. The company has produced several car models, including the Roadster, Model S, Model X, Model 3, Model Y, and Tesla Semi, and plans to produce the Cybertruck light-duty pickup truck in 2023. Tesla is also a major installer of photovoltaic systems in the United States and one of the largest global suppliers of battery energy storage systems. As of 2023, Tesla is the world's most valuable automaker and had the most worldwide sales of battery electric vehicles in 2022, capturing 18% of the market.

> Finished chain.
Tesla, Inc. is an American multinational automotive and clean energy company that designs and manufactures electric vehicles, battery energy storage, solar panels and solar roof tiles, and related products and services. It was incorporated in July 2003 by Martin Eberhard and Marc Tarpenning as Tesla Motors, and named after inventor and electrical engineer Nikola Tesla. Elon Musk became the largest shareholder of the company in February 2004 and has served as CEO since 2008. Tesla's purpose is to help expedite the move to sustainable transport and energy, obtained through electric vehicles and solar power. The company has produced several car models, including the Roadster, Model S, Model X, Model 3, Model Y, and Tesla Semi, and plans to produce the Cybertruck light-duty pickup truck in 2023. Tesla is also a major installer of photovoltaic systems in the United States and one of the largest global suppliers of battery energy storage systems. As of 2023, Tesla is the world's most valuable automaker and had the most worldwide sales of battery electric vehicles in 2022, capturing 18% of the market.
Tesla, Inc. is a multinational company that specializes in designing and manufacturing electric vehicles, battery energy storage, solar panels, solar roof tiles, and related products and services. The company was founded in July 2003 by Martin Eberhard and Marc Tarpenning as Tesla Motors, named after inventor and electrical engineer Nikola Tesla. Elon Musk became the largest shareholder in February 2004 and has been the CEO since 2008. Tesla's mission is to accelerate the transition to sustainable transport and energy through the use of electric vehicles and solar power. The company has produced several car models, including the Roadster, Model S, Model X, Model 3, Model Y, and Tesla Semi, and plans to release the Cybertruck light-duty pickup truck in 2023. Tesla is also a major installer of photovoltaic systems in the United States and one of the largest global suppliers of battery energy storage systems. As of 2023, Tesla is the world's most valuable automaker and had the highest worldwide sales of battery electric vehicles in 2022, accounting for 18% of the market.
('Tesla, Inc.', 'is', 'a multinational company')
('Tesla, Inc.', 'specializes in', 'designing and manufacturing electric vehicles, battery energy storage, solar panels, solar roof tiles, and related products and services')
('Martin Eberhard and Marc Tarpenning', 'founded', 'Tesla Motors')
('Tesla Motors', 'named after', 'Nikola Tesla')
('Elon Musk', 'became', 'the largest shareholder')
('Elon Musk', 'has been', 'the CEO since 2008')
('Tesla', 'has produced', 'several car models including the Roadster, Model S, Model X, Model 3, Model Y, and Tesla Semi')
('Tesla', 'plans to release', 'the Cybertruck light-duty pickup truck in 2023')
('Tesla', 'is', 'also a major installer of photovoltaic systems in the United States')
('Tesla', 'is', 'one of the largest global suppliers of battery energy storage systems')
('Tesla', 'is', "the world's most valuable automaker as of 2023")
('Tesla', 'had', 'the highest worldwide sales of battery electric vehicles in 2022, accounting for 18% of the market')

> Finished chain.
(\'Tesla, Inc.\', \'is\', \'a multinational company\')\n(\'Tesla, Inc.\', \'specializes in\', \'designing and manufacturing electric vehicles, battery energy storage, solar panels, solar roof tiles, and related products and services\')\n(\'Martin Eberhard and Marc Tarpenning\', \'founded\', \'Tesla Motors\')\n(\'Tesla Motors\', \'named after\', \'Nikola Tesla\')\n(\'Elon Musk\', \'became\', \'the largest shareholder\')\n(\'Elon Musk\', \'has been\', \'the CEO since 2008\')\n(\'Tesla\', \'has produced\', \'several car models including the Roadster, Model S, Model X, Model 3, Model Y, and Tesla Semi\')\n(\'Tesla\', \'plans to release\', \'the Cybertruck light-duty pickup truck in 2023\')\n(\'Tesla\', \'is\', \'also a major installer of photovoltaic systems in the United States\')\n(\'Tesla\', \'is\', \'one of the largest global suppliers of battery energy storage systems\')\n(\'Tesla\', \'is\', "the world\'s most valuable automaker as of 2023")\n(\'Tesla\', \'had\', \'the highest worldwi
```
