import aiml
from aiml_processing_functions import *
from qa_processing import QAProcessingUtil


def main():

    aiml_kernel = aiml.Kernel()
    aiml_kernel.setTextEncoding(None)
    aiml_kernel.bootstrap(learnFiles='data/my-bot.xml')

    print("Hi! I am your investing assistant. Ask me things related to investing and I shall answer.")

    user_input = get_user_input()

    qa_processing_util = QAProcessingUtil()

    while user_input is not None:

        answer = qa_processing_util.get_closest_matching_answer(text_to_compare=user_input)
        # if there was no close match, pass it to AIML
        if answer is None:
            answer = aiml_kernel.respond(user_input)

        if answer != '' and answer[0] == '#':
            post_process_answer(answer)
        else:
            print(answer)

        user_input = get_user_input()


if __name__ == "__main__":
    main()
