from ollama import Ollama

def main():
    client = Ollama()
    models = client.list()
    print("Available Ollama models:")
    for model in models:
        print(f"- {model}")

if __name__ == "__main__":
    main()

