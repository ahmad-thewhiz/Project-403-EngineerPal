from langchain.llms import Ollama

def loadOllama(modelName: str, temp: float = 0.5):
    try:
        ollama = Ollama(model=modelName, verbose=True, temperature=temp)
        return ollama
    except Exception as e:
        return f"Error while loading the model: {e}."
    