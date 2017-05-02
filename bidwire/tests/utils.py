import os


def get_abs_filename(filename):
    """Given a filename relative to the current file, returns the absolute filename"""
    absolute_current_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(absolute_current_dir, filename)
