# import language_tool_python
import spacy

# from autocorrect import Speller

nlp = spacy.load("pl_core_news_sm")


# spell = Speller(lang='pl')
# tool = language_tool_python.LanguageTool('pl-PL')


def tokenizing_text(text):
    doc = nlp(text)

    to_delete_words = ['m', 'em', 'śmy', 'im', 'in']
    token_text = [token.lemma_.lower() for token in doc if token.dep_ == 'advmod:neg' or (
            not token.is_stop and not token.is_punct and not token.is_space and token.text not in to_delete_words
        # and token.pos_ != 'NOUN'
    )]

    return token_text


def get_adj_adv_verb_from_text(token_text):
    doc = nlp(token_text)
    token_text = [token.lemma_.lower() for token in doc if
                  (token.pos_ == 'ADV' or token.pos_ == 'ADJ')
                  # or token.pos_ == 'VERB'
                  and
                  (
                          not token.is_stop and not token.is_punct and not token.is_space and token.text
                      # and token.pos_ != 'NOUN'
                  )
                  ]
    return token_text


def tokenizing_text_with_pos(text):
    doc = nlp(text)

    for word in doc:
        # if word.pos_ != 'NOUN':
        print(word.text, word.pos_, word.dep_, word.is_stop, word.is_punct, word.is_space)

# def autocorrect(text):
#     to_delete_words = ['m', 'em', 'śmy', 'im', 'in']
#
#     return " ".join([tool.correct(spell(x)) for x in text.split(" ") if x not in to_delete_words])

# print(get_adj_adv_verb_from_text('Ala ma nie mały pokój'))

#  token.pos_
# print(tokenizing_text('źle, zły, zła'))
