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

#### Few Shot Prompt Templates 

LLMs success comes from their ability to store knowledge within the model parameters, learned during model training. 

However, there are ways to pass more knowledge to an LLM:

1. Parametric knowledge: the knowledge mentioned above is anything that has been learned by the model during training time and stored within the model weights
2. Source knowledge: any knowledge provided to the model at inference time via the prompt

Few shot prompt template aims to add source knowledge to the prompt. The idea is to train the model on a few examples (few-shot learning).





## Memory

### ConversationChain

### Forms of Conversational Memory

#### ConversationBufferMemory


#### ConversationSummaryMemory

#### ConversationBufferWindowMemory

#### ConversationSummaryBufferMemory

#### Other Memory Types