# Part 1: ChatGPT

What are Large Language Models?
Trained as supervised learning method to predict next word.

Two types of large language models (LLM)s:
1. Base LLM
Predicts next word based on text training data
2. Instruction Tuned LLM
Tries to follow instruction

From Base LLM to an instruction tuned LLM:
1. Trained a Base LLM on a lot of data
2. Further train the model:
Fine-tune on examples where the output follows an input instruction 
3. Human ratings of the quality of LLM outputs
4. Tune LLM to increase probability that it generates more highly rated output, using Reinforcement Learning from Human Feedback (RLHF)

Prompting is revolutionizing AI application development:

Supervised learning: 
    - Get labeled data (months)
    - Train model on data (months)
    - Deploy and call the model (months)

And, honestly, you will never achieve the same level of accuracy on your own.

Prompt-based AI:
    - Specify prompt (hours)
    - Call model (hours)

## Get Your OpenAI API Key

## Installation

```Python
!pip install openai
```

Do not hard-copy your API key into your script.

```Python
# read a text file 
```

