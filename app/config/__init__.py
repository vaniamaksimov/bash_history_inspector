from argparse import ArgumentParser
from dataclasses import dataclass

from lexicon import lexicon


@dataclass
class Config:
    argument_parser = ArgumentParser()

    def __post_init__(self):
        self.configuration_argument_parser()

    def configuration_argument_parser(self):
        self.argument_parser.prog = lexicon.argument_parser.program_name
