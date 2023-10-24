from argparse import ArgumentParser
from dataclasses import dataclass

from lexicon import Lexicon

lexicon = Lexicon.get_lexicon()


@dataclass
class Config:
    argument_parser = ArgumentParser()

    def __post_init__(self):
        self.configurate_argument_parser()

    def configurate_argument_parser(self):
        self.argument_parser.prog = lexicon.argument_parser.program_name
