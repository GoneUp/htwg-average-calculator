
import argparse

cmd_args = None

def main():
    print("HTWG QIS Average calculator")
    #

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', action='store',
                        dest='course',
                        default='ain',
                        help='Set the course, defaults to ain')

    parser.add_argument('-t', action='store_true',
                        dest='debug')

    #parser.add_help

    cmd_args = parser.parse_args()

    print(cmd_args)
    print(cmd_args.course)
    print(cmd_args.debug)


if __name__ == '__main__':
    main()