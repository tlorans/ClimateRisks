# Project 0: An Introduction to ChatGPT with LangChain

Large Language Models (LLMs) have enjoyed a growth in popularity since the release of OpenAI's GPT-3 in 2020 (Brown et al., 2020 {cite:p}`brown2020language`).

After further impressive improvements in LLMs, those models gained the non-specialists when OpenAI released `ChatGPT`.

At the same time, `LangChain` appeared. This open-source development framework has incredible features for building tools around LLMs. 

In this part, we are going to introduce this library and start with straightforward interactions with `ChatGPT`.

## LangChain

`LangChain` is a development framework built around LLMs. The core idea of the library is the chain of different components (modularity) to create advanced use cases with LLMs. 

Chains consists of multiple components from modules such as:
- Prompt templates
- LLMs
- Agents
- Memory

## First Prompts

We'll strart with some basics behind prompt templates for `ChatGPT`.

Prompts are often structured in different ways so that we can get different results. 

Let's begin with a simple question-answering prompt template.

We first need to install the `langchain` and `openai` libraries:

```Python
!pip install langchain
!pip install openai
```

We also need to load our API key:

```Python
import os
os.environ["OPENAI_API_KEY"] = openai_api_key = open('key.txt','r').read()
```

From here, we can import the `ChatPromptTemplate` class and initialize a template like so:

```Python
from langchain.prompts import ChatPromptTemplate

template = """Question: {question}
Answer: """

prompt = ChatPromptTemplate.from_template(template)

question = "Which country emits the most GHG emissions?"
```

Now, we can create our first `LLMChain` and obtain our first answer:

```Python
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(temperature = 0.0,
                  )


from langchain import LLMChain

llm_chain = LLMChain(
    prompt = prompt,
    llm = chat
)

print(llm_chain.run(question))
```
And the answer we get is:

```
As an AI language model, I do not have access to the latest data. However, according to the latest available data from 2019, China is the country that emits the most greenhouse gas emissions, followed by the United States and India.
```

### Multiple Questions

If we want to ask multiple questions, there is two approaches:

1. Iterate through all questions using the `generate` method, answering them one at a time
2. Place all questions into a single prompt. 

Let's tests with the first option:

```Python
qs = [
    {'question': "Which country emits the most GHG emissions?"},
    {'question': "What Scope 1, 2 and 3 emissions are?"},
    {'question': "What are Climate Risks?"},
]
res = llm_chain.generate(qs)
res
```

And we get:
```
LLMResult(generations=[[ChatGeneration(text='As of 2021, China is the country that emits the most greenhouse gas (GHG) emissions, followed by the United States, India, Russia, and Japan.', generation_info=None, message=AIMessage(content='As of 2021, China is the country that emits the most greenhouse gas (GHG) emissions, followed by the United States, India, Russia, and Japan.', additional_kwargs={}, example=False))], [ChatGeneration(text='Scope 1, 2, and 3 emissions are categories used to classify greenhouse gas emissions. \n\nScope 1 emissions refer to direct emissions from sources that are owned or controlled by the reporting entity, such as emissions from combustion of fossil fuels in boilers or vehicles.\n\nScope 2 emissions refer to indirect emissions from the consumption of purchased electricity, heat, or steam.\n\nScope 3 emissions refer to all other indirect emissions that occur in the value chain of the reporting entity, including emissions from the production of purchased goods and services, transportation of goods, and employee commuting.', generation_info=None, message=AIMessage(content='Scope 1, 2, and 3 emissions are categories used to classify greenhouse gas emissions. \n\nScope 1 emissions refer to direct emissions from sources that are owned or controlled by the reporting entity, such as emissions from combustion of fossil fuels in boilers or vehicles.\n\nScope 2 emissions refer to indirect emissions from the consumption of purchased electricity, heat, or steam.\n\nScope 3 emissions refer to all other indirect emissions that occur in the value chain of the reporting entity, including emissions from the production of purchased goods and services, transportation of goods, and employee commuting.', additional_kwargs={}, example=False))], [ChatGeneration(text='Climate risks refer to the potential negative impacts of climate change on human and natural systems. These risks can include more frequent and severe weather events such as floods, droughts, and heatwaves, as well as rising sea levels, ocean acidification, and loss of biodiversity. Climate risks can also have economic and social impacts, such as reduced agricultural productivity, increased healthcare costs, and displacement of communities due to extreme weather events or sea level rise.', generation_info=None, message=AIMessage(content='Climate risks refer to the potential negative impacts of climate change on human and natural systems. These risks can include more frequent and severe weather events such as floods, droughts, and heatwaves, as well as rising sea levels, ocean acidification, and loss of biodiversity. Climate risks can also have economic and social impacts, such as reduced agricultural productivity, increased healthcare costs, and displacement of communities due to extreme weather events or sea level rise.', additional_kwargs={}, example=False))]], llm_output={'token_usage': {'prompt_tokens': 67, 'completion_tokens': 237, 'total_tokens': 304}, 'model_name': 'gpt-3.5-turbo'})
```

We can also test the option 2:

```Python
multi_template = """Answer the following questions one at a time.

Questions:
{questions}

Answers:
"""

long_prompt = ChatPromptTemplate.from_template(multi_template)

llm_chain = LLMChain(
    prompt = long_prompt,
    llm = chat
)

qs_str = ["Which country emits the most GHG emissions?\n" +
    "What Scope 1, 2 and 3 emissions are?\n"+
     "What are Climate Risks?"
]

print(llm_chain.run(qs_str))
```

And the result is:

```
1. Which country emits the most GHG emissions?
- According to recent data, China is currently the country that emits the most greenhouse gas (GHG) emissions, followed by the United States and India.

2. What Scope 1, 2 and 3 emissions are?
- Scope 1, 2 and 3 emissions are categories used to classify greenhouse gas (GHG) emissions. Scope 1 emissions refer to direct emissions from sources that are owned or controlled by a company, such as emissions from combustion of fossil fuels. Scope 2 emissions refer to indirect emissions from the generation of purchased electricity, heat or steam. Scope 3 emissions refer to all other indirect emissions that occur in a company's value chain, such as emissions from the production of purchased goods and services, employee commuting, and waste disposal.

3. What are Climate Risks?
- Climate risks refer to the potential negative impacts of climate change on human and natural systems. These risks can include more frequent and severe weather events, sea level rise, changes in precipitation patterns, and impacts on ecosystems and biodiversity. Climate risks can have significant economic, social and environmental consequences, and are a major concern for governments, businesses and communities around the world.
```

## Prompt Engineering with LangChain

In Natural Language Processing (NLP), we used to train different models for different tasks. 

With the versatility of LLMs, this has changed. The time when we needed separate models for classification, named entity recognition (NER) or question-answering (QA) is over.

With the introduction of transformers model and transfer learning, all that was needed to adapt a language model for different tasks was a few small layers at the end of the network (the head) and fine-tuning. 

Today, even this approach is outdated. Rather than changing these last few model layers and go through a fine-tuning process, we can now prompt the model to do classification or QA.

The `LangChain` library puts this prompt engineering at the center, and has built an entire set of objects for them. 

In this section, we are going to focus on `ChatPromptTemplate` and how implementing them effectively.

### Prompt Engineering

A prompt is typically composed of multiple parts:

- Instructions: tell the model what to do, how to use external information and how to construct the output
- External information: context as an additional source of knowledge for the model. It can be manually inserted or retrieved via an external database
- User input or query: a query input by the human user
- Output indicator: it is the beginning of the future generated text. If generating Python code for example, we can use `import` to indicate the model it must begin writing Python code

Each component is usually placed in the prompt in that order.

Let's test it:

```Python
prompt = """Answer the question based on the context below. If the
question cannot be answered using the information provided answer
with "I don't know".

Context: Transitioning to a lower-carbon economy may entail extensive policy, legal, technology, and
market changes to address mitigation and adaptation requirements related to climate change.
Depending on the nature, speed, and focus of these changes, transition risks may pose varying
levels of financial and reputational risk to organizations.

Question: What market changes entailed by the transition towards a low-carbon economy?

Answer: """

template = ChatPromptTemplate.from_template(prompt)
print(chat(template.format_messages()).content)
```

And the answer is:

```
The context mentions that transitioning to a lower-carbon economy may entail extensive market changes, but it does not provide specific details on what those changes may be. Therefore, the answer is "I don't know."
```

In reality, we don't want to hardcore the context and user question. We are going to use a template to generate it.
### Prompt Templates


#### Introduction to Templates

Prompt template classes in `LangChain` are built to make constructing prompts with dynamic inputs easier. 

We can test this by adding a single dynamic input, the user query:

```Python
from langchain.prompts import ChatPromptTemplate

template = """Answer the question based on the context below. If the
question cannot be answered using the information provided answer
with "I don't know".

Context: Transitioning to a lower-carbon economy may entail extensive policy, legal, technology, and
market changes to address mitigation and adaptation requirements related to climate change.
Depending on the nature, speed, and focus of these changes, transition risks may pose varying
levels of financial and reputational risk to organizations.

Question: {query}

Answer: """

prompt_template = ChatPromptTemplate.from_template(template)
```

When we use the `format_messages` from our `ChatPromptTemplate`, we need to pass the query:

```Python
message = prompt_template.format_messages(query = "What are the market changes entailed by the transition towards a low-carbon economy?")
print(message[0].content)
```

It gives:

```
Answer the question based on the context below. If the
question cannot be answered using the information provided answer
with "I don't know".

Context: Transitioning to a lower-carbon economy may entail extensive policy, legal, technology, and
market changes to address mitigation and adaptation requirements related to climate change.
Depending on the nature, speed, and focus of these changes, transition risks may pose varying
levels of financial and reputational risk to organizations.

Question: What are the market changes entailed by the transition towards a low-carbon economy?

Answer: 
```

#### Output Parsers

Answers from `ChatGPT` are obtained as string. However, we may want to obtain it in a more specific format for further treatments. 

For example, you may want to obtain a Python list:

```JSON
{
  "answer": ['China','United States']
}
```

The `langchain` library proposes output parsers with the `ResponseSchema` and `StructuredOutputParser`. 


First, we need to add format instructions to the prompt:

```Python
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

response_schemas = [
    ResponseSchema(name="answer", description="answer to the user's question.\
    output it as a comma separated Python list, such as ['country_1','country_2']"),
]


output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

template_format = """{query}\n\

{format_instructions}
"""

prompt = ChatPromptTemplate.from_template(template_format)
messages = prompt.format_messages(query = "What are the top 5 countries that produce the most carbon dioxide?",
                                format_instructions = format_instructions)
print(messages[0].content)
```

```
What are the top 5 countries that produce the most carbon dioxide?

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "\`\`\`json" and "\`\`\`":

{
	"answer": string  // answer to the user's question.    output it as a comma separated Python list, such as ['country_1','country_2']
}
```

Now we can use the output parser to get the Python list:

```Python
response = chat(messages)
output = output_parser.parse(response.content)
print(output['answer'])
```

```
['China', 'United States', 'India', 'Russia', 'Japan']
```

#### Few Shot Prompt Learning 

LLMs success comes from their ability to store knowledge within the model parameters, learned during model training. 

However, there are ways to pass more knowledge to an LLM:

1. Parametric knowledge: the knowledge mentioned above is anything that has been learned by the model during training time and stored within the model weights
2. Source knowledge: any knowledge provided to the model at inference time via the prompt

Few shot prompt learning aims to add source knowledge to the prompt. The idea is to train the model on a few examples (few-shot learning).

With `ChatGPT`, this is mostly done by giving instructions via Human / AI interaction.

Rather than starting directly with `ChartPromptTemplate`, we need to decompose our prompt template construction with:

- `SystemMessagePromptTemplate`
- `AIMessagePromptTemplate`
- `HumanMessagePromptTemplate`

It will generate:

- a `SystemMessage`
- an `AIMessage`
- a `HumanMessage`

These messages will be used to create the `ChatPromptTemplate` using this time the `from_messages` method.

Let's have an illustration:

```Python
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

template="You are a helpful assistant that provides provides ranking of countries."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
example_human = HumanMessagePromptTemplate.from_template("What are the \
top 3 richest countries in the World by GNI per Capita?")
example_ai = AIMessagePromptTemplate.from_template("1. Liechtenstein,\n\
2. Switzerland\n\
3. Luxembourg")
human_template="{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, example_human, example_ai, human_message_prompt])
chain = LLMChain(llm=chat, prompt=chat_prompt)
# get a chat completion from the formatted messages
print(chain.run("What are the top 5 Oil producers countries?"))
```

And the asnwer is:

```
The top 5 oil-producing countries in the world are:

1. United States
2. Saudi Arabia
3. Russia
4. Canada
5. China
```

## Memory

Conversational memory is what allows a chatbot to response to multiple queries in a coherent conversation. Without it, every new query is treated as an independent input without considering past interactions.

By default, LLMs are stateless. It means that each query is processed independently of other interactions.

However, in many cases it can be interesting that LLMs remember previous interaction. 

In the `langchain` library, conversational memory is done through the use of `ConversationChain` classes.

### ConversationChain

We can start by initializing the `ConversationChain`:

```Python
from langchain.chains import ConversationChain

llm = ChatOpenAI(temperature = 0.)

conversation = ConversationChain(llm = llm)
```

We can see the prompt template used by the `ConversationChain`:

```Python
print(conversation.prompt.template)
```

```
The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
Human: {input}
AI:
```

Here the prompts tells to the model that it is a conversation between a user and an AI. We see two parameters: `{history}` and `{input}`.

In the `{input}` will be placed the latest human query, while the `{history}` is where conversational memory is used. 

We can test it:

```Python
conversation.run("My name is Thomas")
```

```
Hello Thomas! It's nice to meet you. Is there anything I can help you with today?
```

Does it remembers my name?

```Python
conversation.run("What is my name?")
```

```
Your name is Thomas, as you just told me. Is there anything else you would like to know?
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
os.environ["OPENAI_API_KEY"] = openai_api_key = open('key.txt','r').read()

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

wikipedia = WikipediaAPIWrapper()
print(wikipedia.run('Tesla, Inc.'))
```

```
Page: Tesla, Inc.
Summary: Tesla, Inc. ( TESS-lə or  TEZ-lə) is an American multinational automotive and clean energy company headquartered in Austin, Texas. Tesla designs and manufactures electric vehicles (electric cars and trucks), battery energy storage from home to grid-scale, solar panels and solar roof tiles, and related products and services. Tesla is one of the world's most valuable companies and, as of 2023, is the world's most valuable automaker. In 2022, the company had the most worldwide sales of battery electric vehicles, capturing 18% of the market. Through its subsidiary Tesla Energy, the company develops and is a major installer of photovoltaic systems in the United States. Tesla Energy is also one of the largest global suppliers of battery energy storage systems, with 6.5 gigawatt-hours (GWh) installed in 2022.
Tesla was incorporated in July 2003 by Martin Eberhard and Marc Tarpenning as Tesla Motors. The company's name is a tribute to inventor and electrical engineer Nikola Tesla. In February 2004, via a $6.5 million investment, Elon Musk became the largest shareholder of the company. He has served as CEO since 2008. According to Musk, the purpose of Tesla is to help expedite the move to sustainable transport and energy, obtained through electric vehicles and solar power. Tesla began production of its first car model, the Roadster sports car, in 2008. This was followed by the Model S sedan in 2012, the Model X SUV in 2015, the Model 3 sedan in 2017, the Model Y crossover in 2020, and the Tesla Semi truck in 2022. The company plans production of the Cybertruck light-duty pickup truck in 2023. The Model 3 is the all-time bestselling plug-in electric car worldwide, and in June 2021 became the first electric car to sell 1 million units globally. Tesla's 2022 full year deliveries were around 1.31 million vehicles, a 40% increase over the previous year, and cumulative sales totaled 3 million cars as of August 2022. In October 2021, Tesla's market capitalization reached $1 trillion, the sixth company to do so in U.S. history.
Tesla has been the subject of several lawsuits, government scrutiny, journalistic criticism, and public controversies arising from statements and acts of CEO Elon Musk and from allegations of whistleblower retaliation, worker rights violations, and defects with their products.

Page: History of Tesla, Inc.
Summary: This is the corporate history of Tesla, Inc., an electric vehicle manufacturer and clean energy company founded in San Carlos, California in 2001 by American entrepreneurs Martin Eberhard and Marc Tarpenning. The company is named after Croatian-American inventor Nikola Tesla. Tesla is the world's leading electric vehicle manufacturer, and, as of the end of 2021, Tesla's cumulative global vehicle sales totaled 2.3 million units.



Page: Tesla Cybertruck
Summary: The Tesla Cybertruck is an upcoming battery electric light-duty truck announced by Tesla, Inc. in November 2019. Three models have been announced, with EPA range estimates of 400–800 kilometers (250–500 mi) and an estimated 0–100 km/h (0–62 mph) time of 2.9–6.5 seconds, depending on the model.The stated goal of Tesla in developing the Cybertruck is to provide a sustainable energy substitute for the roughly 6,500 fossil-fuel-powered trucks sold per day in the United States of America.The base price of the rear-wheel drive (RWD) model of the vehicle was announced to be US$39,900, with all-wheel drive (AWD) models starting at US$49,900. Production of the dual-motor AWD and tri-motor AWD Cybertruck were initially slated to begin in late 2021, with the RWD model release date in late 2022, but production dates were pushed back multiple times. As of July 2022, the start of limited production is estimated to start in mid-2023. As of January 2023, the start of mass production was estimated to be in 2024. However, as of February 2023, Elon Musk stated that the Cybertruck will be available later in 2023 with deliveries planned to begin
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