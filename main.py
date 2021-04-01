from aiml_processing_util import *
from qa_processing import QAProcessingUtil
from translation_util import TranslationUtil


def get_user_input() -> str or None:
    try:
        return input("> ")
    except (KeyboardInterrupt, EOFError):
        print("Quitting")
        return None


def main():

    aiml_processing_util = AIMLProcessingUtil(aiml_file='data/my-bot.xml', knowledge_base_doc='data/knowledge-base.csv')

    print("Hi! I am your investing assistant. Ask me things related to investing and I shall answer.")

    user_input = get_user_input()

    qa_processing_util = QAProcessingUtil(data_file='data/qa.csv')

    while user_input is not None:

        answer = qa_processing_util.get_closest_matching_answer(text_to_compare=user_input)
        # if there was no close match, pass it to AIML
        if answer is None:
            answer = aiml_processing_util.aiml_kernel.respond(user_input)

        if answer != '' and answer[0] == '#':
            aiml_processing_util.post_process_answer(answer)
        else:
            print(answer)

        user_input = get_user_input()


if __name__ == "__main__":
    # main()

    translation_util = TranslationUtil()
    detected_language_thingie = translation_util.detect_language('Idek what this is anymore')

    if detected_language_thingie is not None:
        print(detected_language_thingie.name)
        print(detected_language_thingie.score)
        print(detected_language_thingie.iso6391_name)

