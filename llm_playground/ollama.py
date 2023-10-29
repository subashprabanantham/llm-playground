from langchain.llms import Ollama


if __name__ == "__main__":
    """
    # To pull new model
    ollama pull codellama:7b

    # To see locally running models
    ollama list
    """

    llm = Ollama(model="codellama:7b")
    print(llm("Has India won any world cups ?"))
