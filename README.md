\# 🤖 AI Agent with Tools \& Memory



A practical AI Agent application built with \*\*Python, Streamlit, and Groq\*\*.



The project demonstrates how an AI agent can understand a user's request, decide whether a tool is required, execute the appropriate tool, process the result, maintain conversation memory, and return a final response.



\---



\## 🚀 Features



\* 🤖 LLM-powered AI agent

\* 🔧 Function/tool calling

\* 🧮 Calculator tool

\* 🔤 Text-length tool

\* 🧠 Conversation memory

\* 🔄 Multi-tool execution

\* 🛡️ Tool safety validation

\* 📊 Agent activity tracking

\* ⚠️ Error handling

\* 💬 Interactive Streamlit chat interface

\* 🔐 Secure API-key management using Streamlit Secrets



\---



\## 🧠 Agent Workflow



The application follows this workflow:



```text

User Request

&#x20;    ↓

Understand Task

&#x20;    ↓

LLM Decides Action

&#x20;    ↓

Select Tool

&#x20;    ↓

Safety Validation

&#x20;    ↓

Execute Tool

&#x20;    ↓

Process Tool Result

&#x20;    ↓

LLM Generates Final Response

&#x20;    ↓

Save Conversation to Memory

```



\---



\## 🔧 Available Tools



\### 1. Calculator



The calculator can perform:



\* Addition

\* Subtraction

\* Multiplication

\* Division



Example:



```text

Calculate 45 multiplied by 12

```



Result:



```text

540

```



\---



\### 2. Text Length



The text-length tool counts the number of characters in a given string.



Example:



```text

How many characters are in "Generative AI"?

```



Result:



```text

13

```



\---



\## 🧠 Conversation Memory



The application stores the conversation inside Streamlit session state.



This allows the agent to use previous interactions as context.



Example:



```text

User:

Calculate 45 multiplied by 12



Agent:

45 × 12 = 540



User:

What did we calculate earlier?



Agent:

You previously calculated 45 × 12, which resulted in 540.

```



\---



\## 🛡️ Safety Validation



Before executing a tool, the application validates:



\* Whether the requested tool is allowed

\* Required arguments

\* Argument data types

\* Valid calculator operations

\* Division by zero



Example:



```text

Division by zero

```



is blocked by the safety validation layer.



\---



\## 📊 Agent Activity



The application records tool actions including:



\* Tool name

\* Execution status

\* Arguments

\* Tool result



This makes the agent's decision-making process easier to inspect and debug.



\---



\## 🛠️ Technologies Used



\* Python

\* Streamlit

\* Groq API

\* `openai/gpt-oss-20b`

\* JSON

\* Function calling

\* Session state



\---



\## 📁 Project Structure



```text

AI-Agent-Tools-Automation/

│

├── app.py

├── requirements.txt

├── README.md

│

├── .gitignore

│

└── .streamlit/

&#x20;   └── secrets.toml

```



> `.streamlit/secrets.toml` contains the API key and is excluded from Git using `.gitignore`.



\---



\## ⚙️ Installation



Clone the repository:



```bash

git clone <YOUR-GITHUB-REPOSITORY-URL>

```



Move into the project directory:



```bash

cd AI-Agent-Tools-Automation

```



Install dependencies:



```bash

pip install -r requirements.txt

```



\---



\## 🔐 API Key Setup



Create the following file:



```text

.streamlit/secrets.toml

```



Add:



```toml

GROQ\_API\_KEY = "YOUR\_GROQ\_API\_KEY"

```



Never commit your API key to GitHub.



\---



\## ▶️ Run the Application



Run:



```bash

python -m streamlit run app.py

```



The Streamlit application will open in your browser.



\---



\## 🧪 Example Queries



Try the following:



```text

Calculate 125 multiplied by 12

```



```text

How many characters are in "Artificial Intelligence"?

```



```text

Calculate 25 multiplied by 16 and tell me how many characters are in "Generative AI".

```



```text

What did we calculate earlier?

```



\---



\## 🎯 Learning Outcomes



Through this project, I learned:



\* What AI agents are

\* Difference between chatbots and agents

\* Agent decision-making

\* Function/tool calling

\* Tool execution

\* Multi-tool workflows

\* Conversation memory

\* Agent state management

\* Safety validation and guardrails

\* Error handling

\* Building AI applications with Streamlit

\* Connecting LLMs with external tools



\---



\## 🔮 Future Improvements



Possible future improvements include:



\* 🌐 Web search tool

\* 🕒 Date and time tool

\* 📁 Document analysis

\* 🗄️ Database tools

\* 🔌 External API integrations

\* 🧠 Persistent long-term memory

\* 🔐 More advanced security controls

\* 🔄 More complex autonomous workflows



\---



\## 👨‍💻 Author



\*\*Rajeet Pratap Mall\*\*



B.Tech CSE-AIML

Raj Kumar Goel Institute of Technology



GitHub:

https://github.com/Rajeet495



LinkedIn:

https://www.linkedin.com/in/rajeet-pratap-mall-9257ba338/



