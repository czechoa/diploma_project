import spacy

nlp = spacy.load("pl_core_news_sm")


def tokenizing_text(text):
    doc = nlp(text)

    to_delete_words = ['m', 'em', 'śmy', 'im', 'in']
    token_text = [token.lemma_.lower() for token in doc if
                  not token.is_stop and not token.is_punct and not token.is_space and token.text not in to_delete_words and token.pos_ != 'NOUN']

    return token_text


def get_adj_adv_from_text(token_text):
    doc = nlp(token_text)
    token_text = [token.lemma_.lower() for token in doc if token.pos_ == 'ADV' or token.pos_ == 'ADJ']
    return token_text


def tokenizing_text_with_pos(text):
    doc = nlp(text)

    for word in doc:
        if word.pos_ != 'NOUN':
            print(word.text, word.pos_, word.dep_)

# print(tokenizing_text_with_pos('Ala ma mały pokój oraz ma małą łazienkę! oraz wdziwc'))

#  token.pos_
# print(tokenizing_text('źle zła'))
