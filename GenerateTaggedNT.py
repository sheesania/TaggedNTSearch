from collections import OrderedDict
from pysblgnt import morphgnt_rows
from TaggedText import TaggedText
from TaggedWord import TaggedWord
from typing import Dict
import pickle

ccat_part_of_speech_codes = {
    'A-': 'Adjective',
    'C-': 'Conjunction',
    'D-': 'Adverb',
    'I-': 'Interjection',
    'N-': 'Noun',
    'P-': 'Preposition',
    'RA': 'Definite article',
    'RD': 'Demonstrative pronoun',
    'RI': 'Interrogative/indefinite pronoun',
    'RP': 'Personal pronoun',
    'RR': 'Relative pronoun',
    'V-': 'Verb',
    'X-': 'Particle',
}

ccat_parsing_codes = list(OrderedDict([
    (
        'Person',
        {
            '1': '1st',
            '2': '2nd',
            '3': '3rd',
        }
    ),
    (
        'Tense',
        {
            'P': 'Present',
            'I': 'Imperfect',
            'F': 'Future',
            'A': 'Aorist',
            'X': 'Perfect',
            'Y': 'Pluperfect',
        }
    ),
    (
        'Voice',
        {
            'A': 'Active',
            'M': 'Middle',
            'P': 'Passive',
        }
    ),
    (
        'Mood',
        {
            'I': 'Indicative',
            'D': 'Imperative',
            'S': 'Subjunctive',
            'O': 'Optative',
            'N': 'Infinitive',
            'P': 'Participle',
        }
    ),
    (
        'Case',
        {
            'N': 'Nominative',
            'G': 'Genitive',
            'D': 'Dative',
            'A': 'Accusative',
            'V': 'Vocative',
        }
    ),
    (
        'Number',
        {
            'S': 'Singular',
            'P': 'Plural',
        }
    ),
    (
        'Gender',
        {
            'M': 'Masculine',
            'F': 'Feminine',
            'N': 'Neuter',
        }
    ),
    (
        'Degree',
        {
            'C': 'Comparative',
            'S': 'Superlative',
        }
    )
]).items())

book_names = [
    'Matthew',
    'Mark',
    'Luke',
    'John',
    'Acts',
    'Romans',
    '1 Corinthians',
    '2 Corinthians',
    'Galatians',
    'Ephesians',
    'Philippians',
    'Colossians',
    '1 Thessalonians',
    '2 Thessalonians',
    '1 Timothy',
    '2 Timothy',
    'Titus',
    'Philemon',
    'Hebrews',
    'James',
    '1 Peter',
    '2 Peter',
    '1 John',
    '2 John',
    '3 John',
    'Jude',
    'Revelation',
]


def get_tags(ccat_parse: str) -> Dict[str, str]:
    tag_dict = {}
    tags = list(ccat_parse)
    for x in range(len(tags)):
        if tags[x] != '-':
            tag_name, tag_codes = ccat_parsing_codes[x]
            tag_dict[tag_name] = tag_codes[tags[x]]
    return tag_dict


books: Dict[str, TaggedText] = {}
for book_num in range(1, 28):
    book_name = book_names[book_num - 1]
    print(f'Processing {book_name}...')
    book = TaggedText(structure_level_names=['Chapter', 'Verse'])
    for row in morphgnt_rows(book_num):
        word = row['word']
        tags = {
            'POS': ccat_part_of_speech_codes[row['ccat-pos']],
            'Stem': row['lemma'],
            **get_tags(row['ccat-parse'])
        }
        taxonomy = [
            row['bcv'][2:4],  # chapter
            row['bcv'][4:6],  # verse
        ]
        book.add_word(TaggedWord(word, tags), taxonomy)
    books[book_name] = book

file = open('tagged_books.pickle', 'wb')
pickle.dump(books, file)
file.close()
