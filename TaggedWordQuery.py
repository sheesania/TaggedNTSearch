from typing import Dict, Optional
from TaggedWord import TaggedWord


class TaggedWordQuery:
    def __init__(self, word: Optional[str], tags: Dict[str, str]) -> None:
        self.word = word
        self.tags = tags

    def matches(self, word: TaggedWord) -> bool:
        if self.word and word.word != self.word:
            return False
        mutual_tags = self.tags.items() & word.tags.items()
        return len(mutual_tags) == len(self.tags)
