# Building Systems

## Chat Format: System, User and Assistant Messages

The system sets the tone/behavior of the assistant.
The assistant corresponds to the LLM response. It can be used such that the LLM remembers what he told in the previous session (gives context to the LLM).
The user corresponds to the prompts.

```Python
def get_completion_from_messages(messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0, 
                                 max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
        max_tokens=max_tokens, # the maximum number of tokens the model can ouptut 
    )
    return response.choices[0].message["content"]
```

## Classification

```Python
# Make examples with classification OECM (12 sectors) with zero shot learning
```

## Chain of Thought Reasoning 

```Python
# Make a chain of thought example with:
# 1. Classification (based on the OECM sector)
# 2. Extract Revenues
# 3. Find emissions factors on the revenues among a list of emissions factors per OECM sector
#4. apply to get the footprint
# Print the intermediate steps of reasonning 
```

## Chaining Prompts

Complex tasks with multiples prompts. Trying to do all at once can be challenging. 
Chaining allows the model to focus on each component -> breaks down a complex task, easier to test.

```Python
# Make the same previous example but with chaining prompts
```

Another benefits that we will use later: we can use external tools (web search or databases).

## Evaluation

The way to evaluate the LLM differs from what you're used to with self-supervised learning model: rather than starting with a test set of labeled data, you will gradually build you dataset.

- tune prompt on handful of examples
- add additional tricky examples 
- develop metrics to measure performance on examples

```Python
# retrive GICS and map to OECM sectors 
# compute accuracy on some examples
```

Maybe the use of few-shot prompting could helps increase the accuracy!

