from typing import Dict, Optional


class TextStructure:
    def __init__(self, from_index: int, to_index: int, children: Optional[Dict[str, 'TextStructure']] = None) -> None:
        self.from_index = from_index
        self.to_index = to_index
        if children is None:
            self.children = dict()
        else:
            self.children = children

    def __repr__(self) -> str:
        if not self.children:
            return f'[{self.from_index} to {self.to_index}]'
        else:
            children_str = ' '.join(
                [f'{child_key}: {child_value.__repr__()}' for child_key, child_value in self.children.items()])
            return f'[{self.from_index} to {self.to_index} -> {children_str}]'
