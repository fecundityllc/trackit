# Color codes
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def print_success(msg: str = "Success") -> None:
    print(OKGREEN + msg + ENDC)


def print_error(msg: str) -> None:
    print(FAIL + msg + ENDC)


def print_info(msg: str) -> None:
    print(OKBLUE + msg + ENDC)


def print_warning(msg: str) -> None:
    print(WARNING + msg + ENDC)
