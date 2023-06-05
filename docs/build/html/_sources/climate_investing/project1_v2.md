# Project 1: Emissions Data Search with ChatGPT


Gathering data needed for portfolio decarbonization can be challenging for three reasons:
- Emissions reporting is not well-standardized yet, and not freely available in a centralized platform
- Data disclosed by companies can be misleading (especially for Scope 3)
- A majority of companies still doesn't disclose any data about carbon emissions, or only disclose partial data (especially without Scope 3 reporting)


Let's test if we can use `ChatGPT` to find data about corporate emissions on internet.

In the first part, we are going to introduce the concept of agents that can be useful to give `ChatGPT` access to latest news and external knowledge.

## Agents

If LLMs are powerful, they lack some particular abilities that a simple computer program can handle, such as logic, calculation or search.

For example, `ChatGPT` can fails with math question such as $4.1^{2.1}$:

```Python
from langchain.prompts import ChatPromptTemplate


template = """Question: {question}
Answer: """

prompt = ChatPromptTemplate.from_template(template)

from langchain.prompts import ChatPromptTemplate


template = """Question: {question}
Answer: """

prompt = ChatPromptTemplate.from_template(template)

from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(temperature = 0.0,
                  )

from langchain import LLMChain

llm_chain = LLMChain(
    prompt = prompt,
    llm = chat
)

print(llm_chain.run("what is the answer to 4.1^2.1?"))
```
```
Approximately 10.08.
```

While the answer should be approximately 19.357.

Another issue with LLMs is that they don't have access to external information and need to rely on knowledge that was captured from its training data, which cuts off at a certain data.

For example:

```Python
print(llm_chain.run("What are Tesla's revenue in 2022?"))
```

```
As an AI language model, I do not have access to future information or predictions. Therefore, I cannot provide an accurate answer to this question.
```

A potential solution for these ploblems comes from agents. 

Agents are enabling tools for LLMs. It can be a calculator or a search engine for example. 

Using agents, an LLM can write and execute Python code, or search for information or query a SQL database.
### Agents and Tools

To use agents with `ChatGPT`, we need:

- a tool to interact with
- an agent to control the interaction

Let's test it with the prebuilt `llm_math` tool to gives `ChatGPT` better math capabilities: 

```Python
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType

tools = load_tools(["llm-math"], llm=chat)

agent= initialize_agent(
    tools, 
    chat, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = True)
```

```Python
agent("What is the 25% of 300?")
```

```
Question: What is the 25% of 300?
Thought: I need to use a calculator to find the answer.
Action:
{
  "action": "Calculator",
  "action_input": "0.25*300"
}

Observation: Answer: 75.0
Thought:The final answer is 75.0
Final Answer: 75.0

> Finished chain.
{'input': 'What is the 25% of 300?', 'output': '75.0'}
```

But what if we decide to ask a non-math question?

```Python
agent("what is the capital of Norway?")
```

We run into an error. The reason is that even if he knows the answer, the agent keeps trying to use a tool. However, our agent contains only one tool: the calculator.

We can fix this problem by giving our agent more tools! 
## Custom Tools

To fix the previous issue, we need to learn how to create custom tools.
### Adding a General Purpose LLM Tool

We can add a plain and simple `ChatGPT` tool:

```Python
from langchain.prompts import ChatPromptTemplate
from langchain import LLMChain

prompt = ChatPromptTemplate.from_template("{query}")

llm_chain = LLMChain(
    prompt = prompt,
    llm = chat
)

chat_gpt_tool = Tool(
    name='Language Model',
    func= llm_chain.run,
    description="use this tool for general purpose queries and logic"
)
tools.append(chat_gpt_tool)
```

Let's reinitialize our agent and ask again the same question:

```Python

agent= initialize_agent(
    tools, 
    chat, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = True)

agent("what is the capital of Norway?")
```
We obtain:

```
> Entering new AgentExecutor chain...
Thought: I'm not sure about the answer, I'll use the Language Model tool to find out.
Action:

{
  "action": "Language Model",
  "action_input": "What is the capital of Norway?"
}

Observation: The capital of Norway is Oslo.
Thought:I have found the answer to the question.
Final Answer: The capital of Norway is Oslo.

> Finished chain.
{'input': 'what is the capital of Norway?',
 'output': 'The capital of Norway is Oslo.'}
```
### Adding a Research Engine Tool

To fix the issue regarding access to more recent data, we can give `ChatGPT` access to a web search engine tool!

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

We can build a new tool and add it to our list:

```Python
duckduckgo_tool = Tool(
    name='DuckDuckGo Search',
    func= search.run,
    description="Useful for when you need to do a search on the internet to find information that another tool can't find. be specific with your input."
)

tools.append(duckduckgo_tool)
```

We can reinitialize our agent and to finally obtain last revenue figures for Tesla!

```Python
agent= initialize_agent(
    tools, 
    chat, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = True)

agent("What are Tesla's revenue in 2022?")
```

It gives:

```
> Entering new AgentExecutor chain...
Thought: I don't have this information readily available, I will need to search for it.
Action:
{
  "action": "DuckDuckGo Search",
  "action_input": "Tesla revenue 2022"
}

Observation: The automaker's full-year 2022 earnings statement, released at the close of market Wednesday, revealed it delivered 405,278 electric cars in the fourth quarter -- up from 343,830 deliveries in... AUSTIN, Texas, January 25, 2023 - Tesla has released its financial results for the fourth quarter and full year ended December 31, 2022 by posting an update on its Investor Relations website. Please visit https://ir.tesla.com to view the update. Tesla's revenue grew to nearly 81.5 billion U.S. dollars in the 2022 fiscal year, a 51 percent increase from the previous year. The United States is Tesla's largest sales market. Revenue... 540 Tesla published its financial results for the fourth quarter of 2022 on Wednesday afternoon. The company brought in $24.3 billion in revenue, a 37 percent increase on Q4 2021. Automotive... Sep 8, 2022,07:30am EDT Listen to article Share to Facebook Share to Twitter Share to Linkedin An aerial view of Tesla Shanghai Gigafactory. Getty Images Key takeaways: There's more to Tesla...
Thought:The revenue for Tesla in 2022 was nearly 81.5 billion U.S. dollars, a 51 percent increase from the previous year. 
Final Answer: Tesla's revenue in 2022 was nearly 81.5 billion U.S. dollars.

> Finished chain.
{'input': "What are Tesla's revenue in 2022?",
 'output': "Tesla's revenue in 2022 was nearly 81.5 billion U.S. dollars."}
```

## Exercise


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

