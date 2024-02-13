from src.tracker import MemSniff


@MemSniff()
def create_list():
    custom_list = [0] * 100000


if __name__ == "__main__":
    create_list()
