from typing import Any


class Notion:
    def __init__(self, database_id: str) -> None:
        self.parent = {"database_id": database_id}
        self._approved = {"Approved": {"select": {"name": "Need Approve"}}}

    @property
    def title(self):
        return self._title

    def set_title(self, title: str):
        self._title = {"Title": {"title": [{"text": {"content": title}}]}}

    @property
    def author(self):
        return self._author

    def set_author(self, author):
        self._author = {"Author": {"text": [{"text": {"content": author}}]}}

    @property
    def tags(self):
        return self._tags

    def set_tags(self, bug_or_enhancement: bool):
        if bug_or_enhancement:
            self._tags = {"Tags": {"multi_select": [{"name": "bug"}]}}
        else:
            self._tags = {"Tags": {"multi_select": [{"name": "enhancement"}]}}

    @property
    def step_to_reproduce(self) -> Any:
        return self._step_to_reproduce

    def set_step_to_reproduce(self, step: str):
        self._step_to_reproduce = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "text": [{"type": "text", "text": {"content": "Step to reproduce"}}]
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"text": [{"type": "text", "text": {"content": step}}]},
            },
        ]

    @property
    def expected_result(self) -> Any:
        return self._expected_result

    def set_expected_result(self, result: str):
        self._expected_result = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "text": [{"type": "text", "text": {"content": "Expected Result"}}]
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"text": [{"type": "text", "text": {"content": result}}]},
            },
        ]

    @property
    def actual_result(self) -> Any:
        return self._actual_result

    def set_actual_result(self, result: str):
        self._actual_result = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "text": [{"type": "text", "text": {"content": "Actual Result"}}]
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"text": [{"type": "text", "text": {"content": result}}]},
            },
        ]

    @property
    def description(self) -> Any:
        return self._description

    def set_description(self, result: str):
        self._description = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "text": [{"type": "text", "text": {"content": "Description"}}]
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"text": [{"type": "text", "text": {"content": result}}]},
            },
        ]

    def to_dict(self):
        properties = ["title", "author", "approved", "tags"]
        children = [
            "step_to_reproduce",
            "expected_result",
            "actual_result",
            "description",
        ]
        properties_dict = {}
        children_dict = []

        for key in self.__dict__:
            if key[0] == "_" and hasattr(self, key):
                if key[1:] in properties:
                    properties_dict.update(getattr(self, key))
                elif key[1:] in children:
                    children_dict.extend(getattr(self, key))

        return {
            "parent": self.parent,
            "properties": properties_dict,
            "children": children_dict,
        }
