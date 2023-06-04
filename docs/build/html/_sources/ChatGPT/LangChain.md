# LangChain

Lot of glue code need to be written. LangChain is helping to handle that and building complex systems based on LLM.

Open-source development framework for LLM applications. Focused on composition and modularity.

Components:
1. Models
2. Prompts
3. Indexes for ingesting data
4. Chains
5. Agents

```Python
!pip install langchain
```

## Models, Prompts and Parsers

Model abstraction:

```Python
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(temperature = 0.0)
chat
```

Prompt template:

```Python
template_string = """Translate ..."""

from langchain.Prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate.from_template(template_string)
```

```Python
prompt_template.messages[0].prompt.input_variables
```

Generate the prompt:
```Python
message = prompt_template.format_messages(
    style = xxx,
    text = xxx
)
```

Pass to the LLM:

```Python
chat(message)
```

Prompt templates are useful abstractions to use good prompts.

output parsing. Template to get the JSON format and we can use the LangChain parser:

```Python
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

```

LangChain can give the instruction to have the good format:

```Python
```

## Memory

Naturally models doesn't remember. How do you remember previous requests?

```Python
from langchain.chains import ConversationChains
from langchain.memory import ConversationBufferMemory

llm = ChatOpenAI(temperature = 0.0)
memory = ConversionBufferMemory()
conversation = ConversationChain(llm = llm,
memory = memory,
verbose = False)
```

LLM are stateless: each transaction is independant. We can give him memory only by providing the full conversation as a context.

Additional Memory types:
- vector data;
- entity memories
- stored in traditional database

## Chains

Most important building block.

Carry a sequence of operations.

```Python
# we can load data to pass through our chain
from langchain.chains import LLMChain

llm = ChatOpenAI(temperature = 0.0)
promt = ....
chain = LLMChain(llm = llm, prompt = prompt)

produc = "Queen size sheet set"
chain.run(product)
```

Sequential Chains: run sequence one afer anoth

```Python
from langchain.Chains import SimpleSequentialChain

# chain 1 name from description

# 2 chain 2
SimpleSequentialChain()
```

When there are multiple inputs:

```Python
from langchain.chains import SequentialChain


```

## Question and Answer

## Evaluation

## Agents

## Google Search with ChatGPT