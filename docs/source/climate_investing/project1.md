# Project 1: Emissions Data Retrieval with ChatGPT

Gathering data needed for portfolio decarbonization can be challenging for three reasons:
- Emissions reporting is not well-standardized yet, and not freely available in a centralized platform
- Data disclosed by companies can be misleading (especially for Scope 3)
- A majority of companies still doesn't disclose any data about carbon emissions, or only disclose partial data (especially without Scope 3 reporting)

In this part, we will test how ChatGPT can help in gathering emissions data.


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

## Information Retrieval with the ReAct Framework

Language models have demonstrated impressive capabilities across tasks in language understanding and abilities for reasoning (e.g. chain-of-thought prompting).

In a seminal paper, Yao et al. (2022) {cite:p}`yao2022react` proposed a new paradigm combining reasoning and acting paradigms, on which large language models capabilities have been previously applied.

In this framework, actions lead to observation feedback from an external environment. Reasoning traces affect the internal state of the model by reasoning over the context and updating it with information to support future reasoning and acting.

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

## Emissions Extraction with ChatGPT

With the Information Retrieval with the ReAct tool, you know have a toolkit you to test to retrieve emisions with ChatGPT.

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


