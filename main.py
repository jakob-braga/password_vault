import tkinter as tk
from application import Application


def main():
    # initialize the window
    application = Application()

    application.login()

    application.loop()


if __name__ == '__main__':
    main()
