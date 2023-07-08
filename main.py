from parser import parse_page
from config import URL
from bot import run_bot


def main():
    parse_page(URL)
    run_bot()


if __name__ == '__main__':
    main()
