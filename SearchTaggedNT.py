from TaggedText import TaggedText
from TaggedWordQuery import TaggedWordQuery
from typing import Dict, List, Tuple
import pickle

#######################
####    EDIT ME    ####
#######################
query = [
    TaggedWordQuery(None, {'Stem': 'πορεύομαι', 'Tense': 'Aorist', 'Mood': 'Participle'}),
    TaggedWordQuery(None, {}),
    TaggedWordQuery(None, {'Mood': 'Imperative'}),
]
#######################
####    EDIT ME    ####
#######################


def print_result(book: str, taxonomy: List[Tuple[str, str]], verse: str) -> None:
    cv_string = ' '.join([f'{level_name} {level_value}' for level_name, level_value in taxonomy])
    print(f'{book} {cv_string}')
    print(f'\t{verse}')


file = open('tagged_books.pickle', 'rb')
books: Dict[str, TaggedText] = pickle.load(file)
for book_name, book in books.items():
    matches = book.search(query)
    for match in matches:
        taxonomy = book.get_taxonomy_for_index(match)
        norm_taxonomy = [level_value for level_name, level_value in taxonomy]
        verse = book.get_text_for_taxonomy(norm_taxonomy)
        print_result(book_name, taxonomy, verse)
file.close()
