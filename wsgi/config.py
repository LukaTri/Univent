import sys

# The following line will insert the given directory at the beginning of
# Python's module search path.  The idea is to keep sensitive information
# out of GitHub and outside Apache's namespace.
sys.path.insert(0, '/home/univent/.secrets')

# Open .secrets/cs417secrets.py for editing.  It should contain lines of
# the form
#
#     VAR = value
#
# for example:
#
#     FOO = 'bar'
#
# Variable names should be uppercase.
#
# Notice that it contains a line setting the variable SECRET_KEY to a
# secret key value.  This is required for sessions.
#
# cs417secrets.py should be used to set other 'secret' values such as the
# PostgreSQL user and password used for database connections.  It can also
# be used for configuration settings that shouldn't be propagated through
# git.

from cs417secrets import *

# Place shared, non-sensitive configuration values after this line.
