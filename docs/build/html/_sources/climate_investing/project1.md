# Project 1: Emissions Data Search with ChatGPT


Gathering data needed for portfolio decarbonization can be challenging for three reasons:
- Emissions reporting is not well-standardized yet, and not freely available in a centralized platform
- Data disclosed by companies can be misleading (especially for Scope 3)
- A majority of companies still doesn't disclose any data about carbon emissions, or only disclose partial data (especially without Scope 3 reporting)


Let's test if we can use `ChatGPT` to find data about corporate emissions on internet.

In the first part, we are going to introduce the custom tools to give `ChatGPT` an access to a search engine.

Before starting the project, please make sure that libraries are installed and your API key is loaded:

```Python
!pip install openai
!pip install langchain
```
```Python
import os
os.environ["OPENAI_API_KEY"] = open('key.txt','r').read()
```

You will also need to instantiate your access to `ChatGPT`:

```Python
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(temperature = 0.0,
                  )
```

## Custom Tools

A known issue with LLMs is that they don't have access to external information and need to rely on knowledge that was captured from its training data, which cuts off at a certain data.

For example:
```Python
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

template = """Question: {question}
Answer:
"""
prompt = ChatPromptTemplate.from_template(template)

llm_chain = LLMChain(
    prompt = prompt,
    llm = chat
)

print(llm_chain.run("What are Tesla's revenue in 2022?"))
```

We get:
```
As an AI language model, I do not have access to future information or predictions. Therefore, I cannot provide an accurate answer to this question.
```

To fix the issue regarding access to more recent data, we can give `ChatGPT` access to a web search engine tool.

Let's install `duckduckgo-search`:

```Python
!pip install duckduckgo-search
```

Let's test it:

```Python
from langchain.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
search.run("Tesla stock price?")
```
It gives us:

```
Get the latest Tesla Inc (TSLA) real-time quote, historical performance, charts, and other financial information to help you make more informed trading and investment decisions. Quotes Summary May 26, 2023 6:00 am 8:00 am 10:00 am 12:00 pm 2:00 pm 4:00 pm 6:00 pm 182.5 185 187.5 190 192.5 195 197.5 200 Previous Close $184.47 Key Data Bid Price and Ask Price The bid &... Discover historical prices for TSLA stock on Yahoo Finance. View daily, weekly or monthly format back to when Tesla, Inc. stock was issued. 1y 3y 5y max Mountain-Chart Date Compare with Compare with up to 5 Stocks On Friday morning 06/02/2023 the Tesla share started trading at the price of $210.00. Compared to the closing price... Tesla's $212 share price is its highest since mid-February—a massive boon for Musk and his fortune: The 51-year-old's $204 billion net worth is 19% higher than it was just a month ago,...
```

Unfortunately, it is not part of the pre-built tool. We need to create a custom tool:

```Python
from langchain.tools import Tool

duckduckgo_tool = Tool(
    name = 'DuckDuckGo Search',
    func = search.run,
    description = "Useful for when you need to do a search on the internet to find information that another tool can't find. be specific with your input."
)
```

We now can create an agent, with an access to our `duckduckgo_tool`:

```Python
from langchain.agents import AgentType
from langchain.agents import load_tools, initialize_agent

tools = [duckduckgo_tool]

agent = initialize_agent(
    tools,
    chat,
    agent = AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors = True,
    verbose = True
)
```

And let's test it:

```Python
agent.run("What are Tesla's revenue in 2022?")
```

That returns:
```
> Entering new AgentExecutor chain...
Thought: I need to search for Tesla's revenue for the year 2022, but it is not possible to know the revenue for a future year. I will search for Tesla's revenue for the latest year available and check if there are any predictions for 2022.

Action:
{
  "action": "DuckDuckGo Search",
  "action_input": "Tesla revenue latest year and predictions for 2022"
}


Observation: Antuan Goodwin Jan. 25, 2023 4:52 p.m. PT 3 min read Enlarge Image The Model 3 and Model Y make up around 95% of the 1.31 million Teslas sold in 2022. Tesla finished 2022 on a tear, bolstered... Mar 17, 2023 Tesla's revenue grew to nearly 81.5 billion U.S. dollars in the 2022 fiscal year, a 51 percent increase from the previous year. The United States is Tesla's largest sales... For Q4 2022, the Wall Street consensus is a gain of $1.13 per share, while Estimize's prediction is higher with a profit of $1.19 per share. The estimates have a wide range this quarter because... That represents a 59 percent increase year over year compared to $2.8 billion in revenue in Q4 2021. It was also Tesla's third year ending in the black, with $14.1 billion in net income for 2022 ... Tesla ended 2021 with a net income of $5.51 billion (a 665% increase from 2020). Aside from the constant swirl of buzz that surrounds Tesla's founder, the recent stock split and Inflation...
Thought:According to the search results, Tesla's revenue grew to nearly 81.5 billion U.S. dollars in the 2022 fiscal year, a 51 percent increase from the previous year. This is the latest information available and there are no predictions for 2022 revenue. 

Final Answer: Tesla's revenue in 2022 was nearly 81.5 billion U.S. dollars.

> Finished chain.
Tesla's revenue in 2022 was nearly 81.5 billion U.S. dollars.
```

Cool! We now have access to recent data!


## Reasoning and Acting

At this stage, we need to take a step back regarding the output from the agent. We want to underline the fact that `ChatGPT` processed the web search by different steps:

1. Thought
```
Thought: I need to search for Tesla's revenue for the year 2022, but it is not possible to know the revenue for a future year. I will search for Tesla's revenue for the latest year available and check if there are any predictions for 2022.
```

2. Action
```
Action:
{
  "action": "DuckDuckGo Search",
  "action_input": "Tesla revenue latest year and predictions for 2022"
}
```

3. Observation
```
Observation: Antuan Goodwin Jan. 25, 2023 4:52 p.m. PT 3 min read Enlarge Image The Model 3 and Model Y make up around 95% of the 1.31 million Teslas sold in 2022. Tesla finished 2022 on a tear, bolstered... Mar 17, 2023 Tesla's revenue grew to nearly 81.5 billion U.S. dollars in the 2022 fiscal year, a 51 percent increase from the previous year. The United States is Tesla's largest sales... For Q4 2022, the Wall Street consensus is a gain of $1.13 per share, while Estimize's prediction is higher with a profit of $1.19 per share. The estimates have a wide range this quarter because... That represents a 59 percent increase year over year compared to $2.8 billion in revenue in Q4 2021. It was also Tesla's third year ending in the black, with $14.1 billion in net income for 2022 ... Tesla ended 2021 with a net income of $5.51 billion (a 665% increase from 2020). Aside from the constant swirl of buzz that surrounds Tesla's founder, the recent stock split and Inflation...
```

4. New Thought
```
Thought:According to the search results, Tesla's revenue grew to nearly 81.5 billion U.S. dollars in the 2022 fiscal year, a 51 percent increase from the previous year. This is the latest information available and there are no predictions for 2022 revenue. 
```

5. Finished Chain
```
Final Answer: Tesla's revenue in 2022 was nearly 81.5 billion U.S. dollars.
```

What seems to be quite trivial is in fact impressive: the agent was able to reason about:
- what tool to use depending on the user input (determining the action)
- formulating the research query (formulating the `action_input`)
- reasoning about the result of the search query, and if the result answers correctly the initial question from the user (Thought)

To do so, it makes use of the ReAct (for Reasoning and Acting) framework developed by Yao et al. (2022) {cite:p}`yao2022react`, using specific prompt template under the hood.

It makes information search particularly efficient, as `ChatGPT` is able to reason about the usefulness of a first search result and continue further if needed. It can also reason about looking for complementary information.

## ChatGPT as a Financial Information Extractor

In the previous project, we've found that `ChatGPT` can be a useful tool as a zero-shot information extractor (Wei et al., 2023 and Shi et al., 2023). 
In fact, building on this finding, Yue et al. (2023) {cite:p}`yue2023leveraging`  found that one can leverage on these zero-shot IE capacity for financial information extraction. 

To do so, we can make an adaptation of the numerical value extraction prompt proposed by Yue et al. (2023), such as:

```Python
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

extraction_template = """Your task:\n\
Find the value of revenue in the given content.\n\
If you can't find the value, please output "None".\n\

Example 1:\n\
The amount of Apple's annual revenue in 2021 was $365.817B.
Result: 365.817

Given content: {text}
Result:
"""
extraction_prompt = ChatPromptTemplate.from_template(extraction_template)

extraction_chain = LLMChain(
    prompt = extraction_prompt,
    llm = chat
)
```

As before, we can make use of the `SimpleSequentialChain`:

```Python
from langchain.chains import SimpleSequentialChain

overall_chain = SimpleSequentialChain(chains = [agent, extraction_chain],
                                      verbose = True)

overall_chain.run("What are Tesla's revenue in 2022?")                                    
```

And we get:
```
 Entering new SimpleSequentialChain chain...


> Entering new AgentExecutor chain...
Thought: I need to search for Tesla's revenue for the year 2022, but it is not possible to know the revenue for a future year. I will search for Tesla's revenue for the latest year available and check if there are any predictions for 2022.

Action:
{
  "action": "DuckDuckGo Search",
  "action_input": "Tesla revenue latest year and predictions for 2022"
}

Observation: Antuan Goodwin Jan. 25, 2023 4:52 p.m. PT 3 min read Enlarge Image The Model 3 and Model Y make up around 95% of the 1.31 million Teslas sold in 2022. Tesla finished 2022 on a tear, bolstered... That represents a 59 percent increase year over year compared to $2.8 billion in revenue in Q4 2021. It was also Tesla's third year ending in the black, with $14.1 billion in net income for 2022 ... Mar 17, 2023 Tesla's revenue grew to nearly 81.5 billion U.S. dollars in the 2022 fiscal year, a 51 percent increase from the previous year. The United States is Tesla's largest sales... For Q4 2022, the Wall Street consensus is a gain of $1.13 per share, while Estimize's prediction is higher with a profit of $1.19 per share. The estimates have a wide range this quarter because... Tesla is expected to report adjusted EPS of $1.19 for the fourth quarter of 2022, compared with $0.85 for the prior-year quarter. Revenue likely climbed about 38% to $24.4 billion. Tesla...
Thought:Based on the search results, Tesla's revenue for the 2022 fiscal year was nearly 81.5 billion U.S. dollars, a 51 percent increase from the previous year. Additionally, the fourth quarter of 2022 saw a revenue of $24.4 billion and an adjusted EPS of $1.19. 

Action:

{
  "action": "None",
  "action_input": ""
}


Observation: None is not a valid tool, try another one.
Thought:I don't need to take any further action as I have already found the answer to the question.

Final Answer: Tesla's revenue for the 2022 fiscal year was nearly 81.5 billion U.S. dollars, a 51 percent increase from the previous year.

> Finished chain.
Tesla's revenue for the 2022 fiscal year was nearly 81.5 billion U.S. dollars, a 51 percent increase from the previous year.
81.5

> Finished chain.
81.5
```
The numerical information was successfully extracted!


## Exercise

We now are going to test if `ChatGPT` can be of any use for emissions data retrieval.

In this exercise, you need to:
1. Adapt the previous prompt template for Scope 1 Emissions.
2. Try your entire chain (search engine and extraction prompt) for a company of your choice
3. Apply this process to the following companies (think about a Python function):
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
 4. Did you encountered any issue applying this process to a list of companies? Please provide ideas to make the process working for multiple companies.

## Solution

The main idea here was to adapt the extraction prompt for your use case:

```Python
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

template = """Your task:\n\
Find the value of Scope 1 emissions in the given content.\n\
If you can't find the value, please output "None".\n\

Example 1:\n\
TotalEnergies' latest Scope 1 emissions were 32 million metric tons\
 of carbon dioxide in 2021.
Result: 32.0

Given content: {text}
Result:
"""
prompt = ChatPromptTemplate.from_template(template)

llm_chain = LLMChain(
    prompt = prompt,
    llm = chat
)
```

And to built the following `SimpleSequentialChain`:

```Python
from langchain.chains import SimpleSequentialChain

overall_chain = SimpleSequentialChain(
    chains = [agent, llm_chain],
    verbose = True
)
```

As an example with TotalEnergies, we have:

```Python
Observation: In early 2019, TotalEnergies made public our aim to reduce our net Scope 1+2 emissions from our operated activities by at least 40% from 2015 levels. In 2022, GHG emissions from our operated assets were 13% lower than in 2015, stand¬ing at close to 40 million tons of CO 2 e. Our objectives include emissions generated by the growth strategy in ... Scope 1 GHG emissions: direct emissions of greenhouse gases from sites or activities that are included in the scope of reporting for climate change-related indicators. ... TotalEnergies reports Scope 3 GHG emissions, category 11, which correspond to indirect GHG emissions related to the use of energy products by customers, i.e. from their ... Scope 1 emissions are direct emissions generated by TotalEnergies' activities. Scope 2 emissions are indirect emissions associated with the purchase of energy (electricity, heat and steam), i.e. emissions associated with the production by a third party of the energy purchased by TotalEnergies. TotalEnergies SE's operated greenhouse gas emissions were 37 million metric tons of carbon dioxide equivalent (MtCO2e) in 2021 - a reduction of roughly 10 percent compared to the previous year.... Greenpeace France also found Scope 1 greenhouse gas emissions - or the company's direct emissions - of about 160 million tonnes, which TotalEnergies described as "fanciful and false" as...
Thought:There are a few different numbers mentioned in the search results, so I'll need to clarify which year's emissions I'm looking for. 

Action:

{
  "action": "DuckDuckGo Search",
  "action_input": "TotalEnergies Scope 1 Emissions 2021"
}



Observation: We are moving aggressively to curtail emissions at our operated sites. In early 2019, TotalEnergies made public our aim to reduce our net Scope 1+2 emissions from our operated activities by at least 40% from 2015 levels. In 2022, GHG emissions from our operated assets were 13% lower than in 2015, stand¬ing at close to 40 million tons of CO 2 e. In 2021, TotalEnergies' Scope 1+2 operated emissions amounted to 37 million tons of GHGs (excluding Covid 19 effect), down 20% from 2015. TotalEnergies' Scope 1 + 2 equity share emissions amounted to 54 million tons in 2021 (49 million tons for Scope 1 alone). TotalEnergies SE's operated greenhouse gas emissions were 37 million metric tons of carbon dioxide equivalent (MtCO2e) in 2021 - a reduction of roughly 10 percent compared to the previous... This accounted for 54 percent of TotalEnergies total Scope 1 emissions in 2021. TotalEnergies SE changed their name from Total S.A. in 2021. Direct greenhouse gas emissions released... TotalEnergies SE's direct carbon dioxide emissions were 32 million metric tons (MtCO2) in 2021. This accounted for roughly 95 percent of the company's Scope 1 emissions that year....
Thought:Based on the search results, it looks like TotalEnergies' Scope 1 emissions were 49 million tons in 2021.

Final Answer: TotalEnergies' Scope 1 emissions were 49 million tons in 2021.

> Finished chain.
TotalEnergies' Scope 1 emissions were 49 million tons in 2021.
49.0

> Finished chain.
49.0
```

Then, you can use a simple loop with exception:

```Python
from tqdm.notebook import tqdm

list_companies = ['AT&T',
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
 'Wells Fargo']

list_results = []

for i in tqdm(range(len(list_companies))):
  try:
    response = overall_chain.run(f"What is the amount of {list_companies[i]} Scope 1 emissions?")
  except:
    response = "None"
  list_results.append(response)
```

However, you will find that most results are `None`. That is, it seems that Scope 1 emissions amount is not readily available through interest research.

## Sustainability Report as a Knowledge Base

A beginning of an extended solution is to use the Sustainability report as a knowledge base for `ChatGPT`.

Let's first download the supplementary libraries needed for parsing the report pdf and convert it to our knowledge base:

```Python
!pip install unstructured
!pip install pypdf
!pip install pdf2image
```

We now can load the online pdf for Tesla:

```Python
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.document_loaders import OnlinePDFLoader

url = "https://www.tesla.com/ns_videos/2021-tesla-impact-report.pdf"
loader = OnlinePDFLoader(url)
data = loader.load()
```
The report was chunked into smaller elements.

We can now install libraries for knowledge base creation:

```Python
!pip install docarray
!pip install tiktoken
```

Let's create our knowledge base:
```Python
from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import DocArrayInMemorySearch

index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch
).from_loaders([loader])
```

We can now interact with the pdf report. Let's ask a question about Scope 1:
```Python
index.query("What is the Scope 1 Emissions?")
```

And we get:
```
 185,000 tCO2e
```

Let's check into the report itself:
```{figure} emissions_from_report.png
---
name: emissions_from_report
---
Figure: Emissions From Tesla Impact Report
```