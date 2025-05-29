# 🧠 Data Science AI Agent

**Data Science AI Agent** - an AI-powered agent that automates data science tasks — from data cleaning and visualization to model training and insights generation. Built to think and work like a real data scientist. Just tell it what you want to accomplish in natural language — whether it's data analysis, model building, or running a full experiment — and it takes care of the rest.


## 🚀 Key Features

- **1. Task Understanding**  
  Accepts high-level instructions (e.g., "Build a classifier for this dataset") and translates them into executable data science workflows.

- **2. Data-Aware**  
  Reads and understands datasets in your environment to tailor its analysis and model-building approach.

- **3. Subtask Decomposition**  
  Breaks down complex tasks into manageable subtasks, executed sequentially.

- **4. Auto Analysis & Modeling**  
  Performs EDA, feature engineering, model selection, training, and evaluation — all autonomously.

- **5. Notebook Control**  
  Dynamically creates, edits, and executes code and markdown cells in the notebook to document and perform tasks.

- **6. Error Resilience**  
  Detects, analyzes, and recovers from errors during execution. Automatically retries failed subtasks with intelligent debugging.

---

## 🔧 Use Cases

- Rapid prototyping and experimentation  
- Teaching and learning data science through auto-documented notebooks  
- Automating repetitive analysis tasks  
- Enhancing productivity for data scientists and ML engineers

---

## 📦 Getting Started

> Just open your Jupyter Notebook, load the agent, and start with a prompt like:

```python
"Analyze the dataset and build a regression model to predict housing prices."
```
<br><br>
> ⚠️ **Note:** The output quality heavily depends on the LLM you are using.  
---

## 📁 Project Structure

- `tools/`: Contains tools to control python notebook utilized by the AI agent.
- `nb_agent_backend.py`: This file is the backend for our notebook AI agent.
- `nb_agent_ui.py`: This file is the streamlit UI for our notebook AI agent.
- `prompts/`: Contains the prompt templates for the AI agents.
---


## 📌 Requirements

* Python 3.8+
* Jupyter
* Streamlit

