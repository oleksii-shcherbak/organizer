from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Note:
    title: str
    content: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        if tag in self.tags:
            self.tags.remove(tag)
