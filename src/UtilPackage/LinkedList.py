from typing import Generic, TypeVar

from .Node import Node

T = TypeVar("T")


class LinkedList(Generic[T]):
    def __init__(self):
        self.head: Node[T] | None = None
        self.current: Node[T] | None = None
        self.previous: Node[T] | None = None

    def __str__(self):
        current_node = self.head
        result = ""

        while current_node is not None:
            result += str(current_node.data) + " "
            current_node = current_node.next

        return result

    def append(self, data) -> None:
        new_node = Node[T](data)

        if self.head is None:
            self.head = new_node
            self.current = new_node
            return

        current_node = self.head

        while current_node.next is not None:
            current_node = current_node.next

        current_node.next = new_node

    def next(self) -> None:
        if self.current.next is None:
            self.previous = self.current
            self.current = None
            return

        self.previous = self.current
        self.current = self.current.next

    def peak_previous(self) -> T | None:
        return self.previous.data

    def peak_next(self) -> T | None:
        return self.current.next.data

    def reverse(self) -> None:
        prev = None
        current = self.head

        while current is not None:
            next_node = current.next
            current.next = prev

            prev = current
            current = next_node

        self.head = prev

    def has_to_reset(self) -> bool:
        return self.current is None

    def reset(self) -> None:
        self.current = self.head
