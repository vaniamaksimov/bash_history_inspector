import argparse
from argparse import ArgumentParser, Namespace
from collections.abc import Sequence
from typing import Any


class CronTime(argparse.Action):
    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        return super().__call__(parser, namespace, values, option_string)
