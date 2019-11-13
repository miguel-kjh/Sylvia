from rasa_nlu.model import Metadata, Interpreter
if __name__ == "__main__":    
    # where `model_directory points to the folder the model is persisted in
    interpreter = Interpreter.load('C:\\Users\\DrStetterITQ\\Desktop\\sylvia\\models\\nlu')

    print(interpreter.parse("get a quick quote"))