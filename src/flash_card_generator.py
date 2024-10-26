import os

import google.generativeai as genai


class FlashCardGenerator:
    """
    This class is used to generate flashcard for a given data using
    Gemini API.
    """
    def __init__(self, gemini_api_key: str, generation_config: dict, model_name) -> None:
        self.gemini_api_key = gemini_api_key
        self.generation_configuration = generation_config
        self.model_name = model_name
        self.model = None
        self.chat_session = None
        self.initialize_model()
        self.initialize_chat_session()

    
    def initialize_model(self) -> None:
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_configuration,
        )
    
    def initialize_chat_session(self) -> None:
        self.chat_session = self.model.start_chat(
            history=[
            {
                "role": "user",
                "parts": [
                    "You are an helpful assistant. Create anki flashcards with the following text using a format like question;answer next line question;answer etc...",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Please provide me with the text you want me to use to create Anki flashcards. I need the text to be able to format it into question;answer pairs. \n\nFor example, you could give me:\n\n\"The capital of France is Paris. The capital of Germany is Berlin. The capital of Spain is Madrid.\"\n\nAnd I would create flashcards like this:\n\nWhat is the capital of France?;Paris\nWhat is the capital of Germany?;Berlin\nWhat is the capital of Spain?;Madrid \n",
                ],
            },
        ]
        )
    
    def get_flash_cards(self, study_material: str) -> str:
        response = self.chat_session.send_message(study_material)

        return response.text


if __name__ == "__main__":
    GEMINI_API_KEY =  os.environ['GEMINI_API_KEY']
    GEMINI_CONFIGURATION = {
        "temperature": 0.1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    GEMINI_MODEL_NAME = "gemini-1.5-flash"

    flash_card_gen_obj = FlashCardGenerator(
        GEMINI_API_KEY,
        GEMINI_CONFIGURATION,
        GEMINI_MODEL_NAME,
    )
    study_material = """"Here is a list of text",
        - Artificial Intelligence\n    - AI is a superset of ML which is a superset of DL.\n    - AI encompasses all solutions that imitates human intelligence to perform a task.\n    - This incudes algorithms that both learn and do not learn.\n    - In the early days, programmers created a detailed rule-based algorithms that could even beat a human in chess.\n    - But this approach worked well defined and logical problems, it was not suited for more complex and fuzzy problems.\n- Machine Learning\n    - Machine Learning came from the thought that, “could computers come up with the rules by themselves by looking at the data provided to them?”.\n    - This lead to programs that would take in `Data` and `Answers` and come up with `Rules` as of to traditional programs that took in `Rules` and `Data` to come up with `Answers`.\n    - Machine Learning programs are trained as of to programmed. It is presented with many examples relevant to the task and comes up with statistical structure in these examples and allows the system to come up with rules to automate that task.\n    - Machine Learning and Deep Learning tends to deal with large and complex data (images), as supposed to statistical analysis.\n    - Thus for a machine learning program to work, we need 4 main things\n        - Input Data\n        - Answers for the Input Data\n        - A metric to measure how close the output is to the expected answers\n- Learning Representations from data\n    - We can consider machine learning to transform the input into output, and its working is that it needs to learn useful representations in order to transform the input into output.\n    - Representations are like one way of looking at the data, like encoding. For example, for images, RGB, HSV (Hue-Saturation-Value) and other format, which can make it easier to perform the task at hand.\n    - Learning can be considered as an automatic search process in order to find better representation.\n    - The operations to arrive at the relevant representation can be coordinate change, linear projections, translations, nonlinear operations and so on.\n    - Machine Learning is technically searching for useful representations of some input data, within a predefined space of possibilities, using guidance from a feedback signal.\n- Deep Learning\n    - Deep learning is a subset of machine learning that is all about learning meaningful representation in each successive layer.\n    - Deep does not stand for higher level of understanding but rather the idea of successive representation learning. Thus it is also called *hierarchical learning* or *layered representation learning*.\n    - Since traditional machine learning focuses on one or two representations, they can be referred to as *shallow learning*.\n- How Deep Learning works\n    - Normally deep learning is done using neural networks which are literal representations stacked on top of each other.\n    - Even though neural networks were inspired from our brain, that is not how brain functions. We can consider it to be a mathematical framework to learn representations.\n    - We can consider deep networks as a multistage information distillation operation where information goes through successive filters and comes out increasingly purified.\n    - The effects of each layer is determined by its weights or parameters. Thus learning in deep learning context is essentially getting the value for these weights. This is not a simple task as there can be thousands of weights which are interdependent on each other.\n    - To identify this, first we need to measure the distance between the prediction and actual target data. This is computed by the *objective function* or the *loss function*.\n    - The next step is to adjust the weights, little by using the loss function as a feedback, such that the loss decreases. The adjustment is performed by the *optimizer*, which implements an algorithm called *back propagation*.\n    - Initially the weights of the neural network is assigned randomly and naturally the loss would be high. But with adjustments and weight corrections, the loss would start to decrease. This training loop (Iteration) which repeated a sufficient number of times, until the performance is satisfactory (Minimal loss, where the prediction is close to the target).\n        \n        ```mermaid\n        %%{init: {\"flowchart\": {\"htmlLabels\": false}} }%%\n        flowchart TB\n        \tA[[Input X]]\n          B[\"Weights\"]\n          C[\"Layer <br>(Data Transformation)\"]\n        \tD[\"Layer <br>(Data Transformation)\"]\n        \tB2[\"Weights\"]\n        \tE[[\"Predictions Y'\"]]\n        \tF[[\"True Targets Y\"]]\n        \tG([\"Loss Function\"]) \n        \tH[[\"Loss Score\"]]\n        \tI([\"Optimizer\"])\n        \n        B2 --> D\n        A --> C --> D\n        B --> C\n        I --\"Update Weights\" --> B2\n        D --> E --> G --> H --> I\n        F --> G\n        \n        ```\n\nCreate flashcards on this"""
    print(flash_card_gen_obj.get_flash_cards(study_material))
        


