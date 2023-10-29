import pandas as pd
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.retrievers import WikipediaRetriever
from langchain.schema.output_parser import StrOutputParser
from langchain.utilities.python import PythonREPL
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent


class PythonCodeLLM:
    @staticmethod
    def sanitize_output(text: str):
        _, after = text.split("```python")
        return after.split("```")[0]

    def run(self):
        # Expects `OPENAI_API_KEY` as environment variable
        template = """Write some python code to solve the user's problem. 
                    Return only python code in Markdown format, e.g.:
                    ```python
                    ....
                    ```"""

        chat_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", template),
                ("human", "{input}"),
            ]
        )
        chain = (
            chat_prompt
            | ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
            | StrOutputParser()
            | PythonCodeLLM.sanitize_output
            | PythonREPL().run
        )
        print(
            chain.invoke(
                {
                    "input": "Write a code to sort list of numbers and fetch top one. Use the input [2,3,4,5]"
                }
            )
        )


class RAGWithWikipedia:
    def run(self):
        retriever = WikipediaRetriever()
        model = ChatOpenAI(model_name="gpt-3.5-turbo")
        qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)
        result = qa({"question": "What does hakuna matata means ?", "chat_history": []})
        print(result["answer"])


class AgentsWithPandasDF:
    def run(self):
        df = pd.read_csv("titanic.csv")
        agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True)
        print(agent.run("Whats the average ticket fare of people who survived?"))


if __name__ == "__main__":
    AgentsWithPandasDF().run()
