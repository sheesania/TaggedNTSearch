from typing import Dict, Optional


class TaggedWord:
    def __init__(self, word: str, tags: Dict[str, str], attributes: Optional[Dict[str, str]] = None) -> None:
        self.word = word
        self.tags = tags
        self.attributes = attributes

    def __repr__(self) -> str:
        return f'{self.word}\n\ttags: {str(self.tags)}\n\tattributes: {str(self.attributes)}'
