from argparse import ArgumentParser
from dataclasses import dataclass


@dataclass
class Config:
    parser = ArgumentParser()
