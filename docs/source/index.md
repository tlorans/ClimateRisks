% Climate Risks Modelling documentation master file, created by
% sphinx-quickstart on Thu Dec 29 10:41:45 2022.
% You can adapt this file completely to your liking, but it should at least
% contain the root `toctree` directive.

# Net Zero Investing with ChatGPT


```{warning}
This course is under heavy development
```

In this course, I propose a step-by-step implementation of a net zero strategy with Python, following the methodology proposed by Barahhou et al. (2022) {cite:p}`barahhou2022net`.

In the projects, we investigate the use of `ChatGPT` with the development framework `LangChain`.

This course is calibrated as an introductory course (one-week duration).

The portfolio construction methodology presented here is a direct adaption from Thierry Roncalli's (2023)  {cite:p}`2023:Roncalli` course and publications. If you want to get a deeper knowledge of some notions in this course, please refer to Thierry Roncalli's course and / or publications.
Any error in this course is mine. 

Unless it is sourced, any opinion expressed in this course is my personnal opinion only. 

We investigate the use of `ChatGPT` for carbon emissions retrieval from the internet, carbon emissions and green revenues estimates. Those tasks involve Natural Language Processing (NLP) technics. 

Before transfer learning and Transformers models introduction, solving a specific NLP task required training a specific model dedicated to it.

```{figure} specific_task.png
---
name: specific_task
---
Figure: Specific NLP Task Required Specific Model Training, from LangChain AI Handbook, Pinecone
```

The introduction of Transformers models and transfer learning already simplified this process, as adapting a language model for different tasks only required to add small layers at the head of the model and fine-tuning.

```{figure} transfer_learning.png
---
name: transfer_learning
---
Figure: Transfer Learning with Fine-Tuning Transformer Model, from LangChain AI Handbook, Pinecone
```

`ChatGPT` (and other LLMs) made possible to forget about adding model layers and fine-tuning, with multi-modality. With `ChatGPT`, performing a specific task only requires to adapt the prompt sent to the model.

```{figure} multi_modality.png
---
name: multi_modality
---
Figure: Multi-modality with ChatGPT, from LangChain AI Handbook, Pinecone
```

This multi-modality property gives us the possibility to solve NLP tasks in a few days rather than months.

```{toctree}
:caption: 'Contents:'
:maxdepth: 2

intro/lowcarbon
intro/net_zero
intro/intro_langchain_v2
climate_investing/net_zero_investing
climate_investing/portfolio_decarbonization_pathway
climate_investing/portfolio_alignment
climate_investing/project1
climate_investing/project_2
climate_investing/self_decarbonization
climate_investing/integratingtransition
references
```
