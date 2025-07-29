"""
Booktrack - A reading time tracking application
Main module for launching the app.
"""

from .app import main

if __name__ == '__main__':
    app = main()
    app.main_loop()
