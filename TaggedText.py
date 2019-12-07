from TaggedWord import TaggedWord
from TaggedWordQuery import TaggedWordQuery
from TextStructure import TextStructure
from collections import defaultdict
from typing import DefaultDict, List, Optional, Set, Tuple


class TaggedText:
    def __init__(self, words: Optional[List[TaggedWord]] = None,
                 structure_level_names: Optional[List[str]] = None) -> None:
        if words is None:
            words: List[TaggedWord] = []
        self.words = words
        if structure_level_names is None:
            self.structure_level_names: List[str] = []
        self.structure_level_names = structure_level_names
        self.structure = TextStructure(0, 0)

    def __len__(self) -> int:
        return len(self.words)

    def add_word(self, word: TaggedWord, taxonomy: Optional[List[str]] = None) -> None:
        self.words.append(word)
        self.structure.to_index += 1

        if not taxonomy:
            return
        structure = self.structure
        for level in taxonomy:
            if level in structure.children:
                structure.children[level].to_index += 1
            if level not in structure.children:
                current_word_index = len(self.words) - 1
                structure.children[level] = TextStructure(current_word_index, current_word_index + 1)
            structure = structure.children[level]

    def get_text(self, from_index: int, to_index: int) -> str:
        if from_index < 0:
            from_index = 0
        if to_index >= len(self.words):
            to_index = len(self.words) - 1
        strings = [self.words[i].word for i in range(from_index, to_index)]
        return ' '.join(strings)

    def get_all_tags(self) -> DefaultDict[str, Set[str]]:
        tags = defaultdict(set)
        for word in self.words:
            for tag_key, tag_value in word.tags.items():
                tags[tag_key].add(tag_value)
        return tags

    def words_match(self, start_index: int, queries: List[TaggedWordQuery]) -> bool:
        words = self.words[start_index:start_index + len(queries)]
        for x in range(len(queries)):
            if not queries[x].matches(words[x]):
                return False
        return True

    def search(self, queries: List[TaggedWordQuery]) -> List[int]:
        matches = []
        for word_index in range(len(self) - len(queries) + 1):
            if self.words_match(word_index, queries):
                matches.append(word_index)
        return matches

    def get_taxonomy_for_index(self, index: int) -> Optional[List[Tuple[str, str]]]:
        taxonomy: List[tuple] = []
        level = self.structure
        current_level = 0
        while level.children:
            new_level = None
            for child_name, child in level.children.items():
                if (child.from_index <= index) and (child.to_index > index):
                    taxonomy.append((self.get_level_name(current_level), child_name))
                    new_level = child
                    break
            if not new_level:
                return None  # this is not a valid index in the taxonomy
            else:
                level = new_level
                current_level += 1
        return taxonomy

    def get_level_name(self, level_index: int) -> str:
        if level_index < len(self.structure_level_names):
            return self.structure_level_names[level_index]
        else:
            return ''

    def get_text_for_taxonomy(self, taxonomy: List[str]) -> Optional[str]:
        structure = self.structure
        for level in taxonomy:
            if level not in structure.children:
                return None  # this is not a valid taxonomy
            structure = structure.children[level]
        return self.get_text(structure.from_index, structure.to_index)
