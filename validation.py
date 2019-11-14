from rasa_nlu.model import Metadata, Interpreter
import matplotlib.pyplot as plt
from utils import conversension_car
if __name__ == "__main__":    
    # where `model_directory points to the folder the model is persisted in
    interpreter = Interpreter.load('C:\\Users\\DrStetterITQ\\Desktop\\sylvia\\models\\nlu')
    x1 = []
    y1 = []
    
    for conv in conversension_car.keys(): 
        anwser = interpreter.parse(conversension_car[conv][0])
        x1.append(anwser['intent']['name'])
        y1.append(anwser['intent']['confidence'])
    plt.plot(x1,y1,marker='o', linestyle='--')
    plt.ylim(0,1)
    plt.xticks(rotation=90)
    plt.show()