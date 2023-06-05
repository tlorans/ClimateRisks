# Project 2: ChatGPT as a Carbon Data Analyst


## Knowledge Bases

As we have seen in the previous project, LLMs have a problem about recent data, as they have no idea about recent events. 

It creates problems for any use case that relies on up-to-date information or a specific dataset.

The first challenge is to add this dataset to the LLM. To do so, we can use retrieval augmentation. This approach allows us to retrieve relevant information from an external knowledge based an give that information to our LLM. 
### Getting Data for our Knowledge Base

Let's retrieve our emissions datase:

```Python
import pandas as pd
url = 'https://github.com/shokru/carbon_emissions/blob/main/data_fin.xlsx?raw=true'
data = pd.read_excel(url)
data.rename(columns={"Company":"Symbol"}, inplace = True)
payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
first_table = payload[0]
df = first_table
data = data.merge(df[["Symbol","Security","GICS Sector","GICS Sub-Industry"]], how = "left", on = "Symbol")
data.to_csv('emissions_data.csv', index = None)
```

We can use the `CSVLoader` from `langchain` to load the documents:

```Python
from langchain.document_loaders import CSVLoader
file = 'emissions_data.csv'
loader = CSVLoader(file_path=file)

documents = loader.load()
documents[0]
```
It creates one document per row of the CSV file:

```
Document(page_content='Symbol: AAPL\nDate: 2005-12-30\nPrice: 2.205\nMkt_cap: 60586.5831\nEnergy_consumption: \nGHG_scope_3: \nGHG_total: \nReturn: 1.232609\nYear: 2005\nSecurity: Apple Inc.\nGICS Sector: Information Technology\nGICS Sub-Industry: Technology Hardware, Storage & Peripherals', metadata={'source': 'emissions_data.csv', 'row': 0})
```
### Creating Embeddings

To be retrieved according to a specific query, each document is transformed into a numerical representation (embeddings), such as:

```Python
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
embed = embeddings.embed_query("Exxon emissions in 2012")
len(embed)
```
It is a vector of sizes:
```
1536
```

We now need to install `docarray` and `tiktoken`:

```Python
!pip install docarray
!pip install tiktoken
```

### Vector Base

We can now tranform our CSV document into a vector base :

```Python
from langchain.vectorstores import DocArrayInMemorySearch

db = DocArrayInMemorySearch.from_documents(
    documents, 
    embeddings
)
```

### Similarity Search 

Information retrieval is based on the embeddings of the query and the vector base, with similarity search:

```Python
query = "What are the oil & gas companies in the dataset"

docs = db.similarity_search(query)

docs[0]
```

It will returns rows that seem to corresponds to the query:

```
Document(page_content='Symbol: XOM\nDate: 2005-12-31\nPrice: 33.2424\nMkt_cap: 349511.9557\nEnergy_consumption: 418950.0\nGHG_scope_3: \nGHG_total: \nReturn: 0.117643\nYear: 2005\nSecurity: ExxonMobil\nGICS Sector: Energy\nGICS Sub-Industry: Integrated Oil & Gas', metadata={'source': 'emissions_data.csv', 'row': 473})
```
### Generative Question Answering

We can now expose our knowledge base as a retriever interface and pass it to `ChatGPT` with the `RetrievalQA` chain:

```Python
from langchain.chains import RetrievalQA

retriever = db.as_retriever()

qa_stuff = RetrievalQA.from_chain_type(
    llm=chat, 
    chain_type="stuff", 
    retriever=retriever, 
    verbose=True
)
```

We can test it:

```Python
response = qa_stuff.run(query)
print(response)
```

It gives:

```
> Entering new RetrievalQA chain...

> Finished chain.
The oil & gas companies in the dataset are ExxonMobil (XOM) and Chevron Corporation (CVX).
```

### VectorstoreIndexCreator

The `VectorstoreIndexCreator` is a wrapper around all this logic in the `langchain` library, and allows you to do all of this in a few lines of codes:

```Python
from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import DocArrayInMemorySearch

index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch
).from_loaders([loader])

index.query(query)
```
```
 The oil & gas companies in the dataset are ExxonMobil and Chevron Corporation.
```
## Custom Tools for ChatGPT

As we have seen in the previous projects, agents are a powerful approach to use LLMs. 

Agents allows us to give LLMs access to tools, and tools present an infinite number of possibilities. 

If the `langchain` library provides a selection of prebuilt tools, such as the ones we used in the previous project, we'll often find that we must modify existing tools or build entirely new ones.

This is what we will explose in this section.

The best way to create tools that require multiple inputs is to use the `StructuredTool` class from `langchain`:

```Python
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

llm = ChatOpenAI(temperature=0)

from langchain.tools import StructuredTool

def multiplier(a: float, b: float) -> float:
    """Multiply the provided floats."""
    return a * b

tool = StructuredTool.from_function(multiplier)
```

You need the type `STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION`:

```Python

agent_executor = initialize_agent([tool], 
                                  llm, 
                                  agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
                                  verbose=True)

```

Let's test it:

```Python
agent_executor.run("What is 3 times 4?")
```

We have:

```
> Entering new AgentExecutor chain...
Action:
{
  "action": "multiplier",
  "action_input": {
    "a": 3,
    "b": 4
  }
}

Observation: 12.0
```

## Exercise

With the previous dataset, try to:

1. Implement a tool that compute the WACI each year for the portfolio.
2. Can you try to implement a portfolio decarbonization tool and asks `ChatGPT` to implement the strategy itself?