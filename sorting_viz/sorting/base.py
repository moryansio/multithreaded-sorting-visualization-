from abc import ABC, abstractmethod
from typing import Callable, Optional
import threading

VisualizeCallback = Callable[[list[int], Optional[tuple[int, int]]], None]


class SorterBase(ABC):
    def __init__(self, arr: list[int]):
        self.arr = arr

    def fill(self, arr: list[int]) -> None:
        self.arr = arr[:]

    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def sort(
        self,
        visualize: VisualizeCallback,
        stop_event: threading.Event,
        sleep_factor: float
    ) -> None:
        ...