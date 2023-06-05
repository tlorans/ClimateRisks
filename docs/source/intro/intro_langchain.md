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



### Prompt Engineering

### Prompt Templates

## Memory

### ConversationChain

### Forms of Conversational Memory

#### ConversationBufferMemory


#### ConversationSummaryMemory

#### ConversationBufferWindowMemory

#### ConversationSummaryBufferMemory

#### Other Memory Types