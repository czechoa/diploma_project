import spacy

nlp = spacy.load("pl_core_news_sm")


def tokenizing_text(text):
    doc = nlp(text)
    token_text = [token.lemma_.lower() for token in doc if
                  not token.is_stop and not token.is_punct and not token.is_space]
    return token_text


def get_adj_adv_from_text(token_text):
    doc = nlp(token_text)
    token_text = [token.lemma_.lower()  for token in doc if token.pos_ == 'ADV' or token.pos_ == 'ADJ']
    return token_text

# print(tokenizing_text('Ala ma mały pokój oraz ma małą łazienkę'))

#  token.pos_
# print(tokenizing_text('źle zła'))
