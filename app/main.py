from pathlib import Path


def main():
    homedir = Path.home()
    with open(homedir / '.bash_history') as bash_history:
        for command in bash_history:
            yield command


if __name__ == '__main__':
    for i in main():
        print(i)
