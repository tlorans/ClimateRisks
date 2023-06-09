# Project 2: Estimating Emissions with ChatGPT

In this project, we are investigating if we can directly use `ChatGPT` for simple estimate of Scope 3 upstream emissions (supply chain emissions).

As we have seen in the previous project, LLMs have a problem about recent events or specific domain knowledge 

It creates problems for any use case that relies on up-to-date information or a specific dataset.

The first challenge is to add this dataset to the LLM. To do so, we can use retrieval augmentation. This approach allows us to retrieve relevant information from an external knowledge based an give that information to our LLM. 

First, we need to make sure our libraries are installed and the API key loaded:

```Python
!pip install openai
!pip install langchain

import os
os.environ["OPENAI_API_KEY"] = open('key.txt','r').read()
```
## Getting Data for our Knowledge Base

Let's retrieve a CSV file and save it in our working path directory:

```Python
url = "https://github.com/tlorans/ClimateRisks/blob/main/DEXUSEU.csv?raw=true"

import pandas as pd 
data = pd.read_csv(url)
data.rename(columns = {"DEXUSEU":"Exchange Rate Dollar to Euro"}, inplace = True)
data.to_csv("exchange_rate.csv", index = None)
```

We can use the `CSVLoader` from `langchain` to load the documents:

```Python
from langchain.document_loaders import CSVLoader

file = "exchange_rate.csv"
loader = CSVLoader(file_path = file)
data = loader.load()
print(data[0])
```
It creates one document per row of the CSV file:

```
page_content='DATE: 2018-06-04\nExchange Rate Dollar to Euro: 1.1696' metadata={'source': 'exchange_rate.csv', 'row': 0}
```
## Creating Knowledge Base with Embeddings

We need to install other libraries:

```Python
!pip install docarray
!pip install tiktoken
```

We can now create our knowledge base:

```Python
from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import DocArrayInMemorySearch

index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch
).from_loaders([loader])
```

And let's test a query:

```Python
index.query("What is the last exchange rate? Gives the date")
```

It gives:

```
 The last exchange rate is 1.0979 on 2022-03-14.
```

What happened here? 

The object we've instantiated has transformed each row of our CSV file into a numeric vector representation, with the use of an embedding model.

```{figure} numeric_transform.png
---
name: numeric_transform
---
Figure: Embedding Model and Vector Representation, from the LangChain AI Handbook, Pinecone
```

Once all our CSV elements are transformed into a numerical vector, and stored as a Vector base, our query is also transformed into a numerical vector and the most similar elements into our CSV file are returned, based on the calculation of the distance between embeddings in vector space (with cosine similarity for example).

```{figure} similarity.png
---
name: similarity
---
Figure: Similarity for Knowledge Base Element Retrieval, from the LangChain AI Handbook, Pinecone
```

## Knowledge Base as a Tool

We can now give access to this tool to `ChatGPT`:

```Python
from langchain.tools import Tool

knowledge_tool = Tool(
    name = "FX Rate",
    func = index.query,
    description = "Useful for when you need to search for the exchange rate. Provides your input as a search query."
)
```

```Python
from langchain.agents import AgentType
from langchain.agents import load_tools, initialize_agent
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(temperature = 0.)


tools = [knowledge_tool]

agent = initialize_agent(
    tools,
    chat,
    agent = AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors = True,
    verbose = True
)

agent.run("What was the exchange rate in April 2022?")
```
And `ChatGPT` understands the need to use this tool:

```
> Entering new AgentExecutor chain...
Question: What was the exchange rate in April 2022?
Thought: I need to use the FX Rate tool to get the exchange rate for April 2022.
Action:
{
  "action": "FX Rate",
  "action_input": "exchange rate April 2022"
}

Observation:  The exchange rate for the US Dollar to the Euro in April 2022 ranged from 1.079 to 1.1043.
Thought:I have found the exchange rate range for the US Dollar to the Euro in April 2022. 
Final Answer: The exchange rate for the US Dollar to the Euro in April 2022 ranged from 1.079 to 1.1043.

> Finished chain.
The exchange rate for the US Dollar to the Euro in April 2022 ranged from 1.079 to 1.1043.
```

## Interacting with Other Tools

We can now give to `ChatGPT` a task to test its capacity for using tools in interaction. 

Let's ask for:
1. Finding Tesla's Revenue in 2022
2. Finding the FX rate in December 2022
3. Convert Tesla's Revenue into Euro.

```Python
!pip install duckduckgo-search
```

```Python
tools = load_tools(["llm-math"], llm = chat)

from langchain.tools import DuckDuckGoSearchRun
search = DuckDuckGoSearchRun()

duckduckgo_tool = Tool(
    name = 'DuckDuckGo Search',
    func = search.run,
    description = "Useful for when you need to do a search on the internet to find information that another tool can't find. be specific with your input."
)

tools.append(knowledge_tool)
tools.append(duckduckgo_tool)

agent = initialize_agent(
    tools,
    chat,
    agent = AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors = True,
    verbose = True
)
```

```Python
query = """Process as follow:\n\
1. Search for Tesla's revenue in 2022. \n\
2. Find the exchange rate in December 2022. \n\
3. Multiply Tesla's revenue in 2022 with the exchange rate. \n\
"""
agent.run(query)
```

And we get:

```
> Entering new AgentExecutor chain...
Thought: I need to find Tesla's revenue in 2022. I'm not sure where to find this information.
Action:

{
  "action": "DuckDuckGo Search",
  "action_input": "Tesla revenue 2022"
}


Observation: The automaker's full-year 2022 earnings statement, released at the close of market Wednesday, revealed it delivered 405,278 electric cars in the fourth quarter -- up from 343,830 deliveries in... AUSTIN, Texas, January 25, 2023 - Tesla has released its financial results for the fourth quarter and full year ended December 31, 2022 by posting an update on its Investor Relations website. Please visit https://ir.tesla.com to view the update. Tesla's revenue grew to nearly 81.5 billion U.S. dollars in the 2022 fiscal year, a 51 percent increase from the previous year. The United States is Tesla's largest sales market. Revenue... 540 Tesla published its financial results for the fourth quarter of 2022 on Wednesday afternoon. The company brought in $24.3 billion in revenue, a 37 percent increase on Q4 2021. Automotive... Sep 8, 2022,07:30am EDT Listen to article Share to Facebook Share to Twitter Share to Linkedin An aerial view of Tesla Shanghai Gigafactory. Getty Images Key takeaways: There's more to Tesla...
Thought:I need to find the exchange rate for December 2022. I'm not sure where to find this information.
Action:

{
  "action": "FX Rate",
  "action_input": "Exchange rate December 2022"
}


Observation:  The exchange rate for December 2022 was between 1.0588 and 1.0622.
Thought:Now I need to multiply Tesla's revenue in 2022 with the exchange rate for December 2022 to get the revenue in another currency.
Action:
{
  "action": "Calculator",
  "action_input": "81500000000 * 1.0605"
}


Observation: Answer: 86430750000.0
Thought:I now know the final answer.
Final Answer: Tesla's revenue in December 2022, converted to the exchange rate of 1.0605, is $86,430,750,000.

> Finished chain.
Tesla's revenue in December 2022, converted to the exchange rate of 1.0605, is $86,430,750,000.
```

## Exercise

We are going to use the Supply Chain Greenhouse Gas Emissions Factors by NAICS-6 from the United States Environmental Protection Agency as a source for our knowledge base.

Let's download it and put it into our working path directory:

```Python
emissions.to_csv("emissions_factors.csv", index = None)

file = "emissions_factors.csv"
loader = CSVLoader(file_path = file)
data = loader.load()

index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch
).from_loaders([loader])
```

Let's have a test:

```Python
index.query("What is the emission factor with margins for automobile industry?")
```

And we get:

```
 The emission factor with margins for the automobile industry is 0.279 kg CO2e/2021 USD, purchaser price.
```

What you need for this exercise is:
1. Determine the main activity of a company.
2. Find the revenue for this company.
3. Apply the corresponding emission factor.

You need to do it with a chained approach. You want the output to be expressed in million tons of CO2eq. You want the final output to be only the numerical value. You may need to use specific prompts to check for the formating component. You may need to use agent.

Once you've achieved to do it for one company, scale your process to obtain an estimate for the following list of companies:

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
