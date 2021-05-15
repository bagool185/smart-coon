from lib.aiml_processing_util import *
from lib.language_result_item import LanguageResultItem
from lib.qa_processing import QAProcessingUtil
from lib.translation_util import TranslationUtil


def get_user_input() -> str or None:
    try:
        return input("> ")
    except (KeyboardInterrupt, EOFError):
        print("Quitting")
        return None


def main():

    translation_util = TranslationUtil()
    aiml_processing_util = AIMLProcessingUtil(aiml_file='data/my-bot.xml',
                                              knowledge_base_doc='data/knowledge-base.csv',
                                              translation_util=translation_util)

    print("Hi! I am your investing assistant. Ask me things related to investing and I shall answer.")

    user_input = get_user_input()

    qa_processing_util = QAProcessingUtil(data_file='data/qa.csv')

    while user_input is not None:

        detected_language: LanguageResultItem = translation_util.detect_language(source_text=user_input)
        # If not English
        if detected_language.iso6391_name != 'en':
            user_input = translation_util.translate_text(source_text=user_input,
                                                         to_lang='en',
                                                         from_lang=detected_language.iso6391_name)

            aiml_processing_util.set_language(detected_language.iso6391_name)

        answer = qa_processing_util.get_closest_matching_answer(text_to_compare=user_input)
        # if there was no close match, pass it to AIML
        if answer is None:
            answer = aiml_processing_util.aiml_kernel.respond(user_input)

        if answer != '' and answer[0] == '#':
            aiml_processing_util.post_process_answer(answer)
        else:

            if detected_language.iso6391_name != 'en':
                translated_answer = translation_util.translate_text(source_text=answer,
                                                                    to_lang='en',
                                                                    from_lang=detected_language.iso6391_name)
                print(translated_answer)
            else:
                print(answer)

        user_input = get_user_input()


if __name__ == "__main__":
    main()


