from rasa.__main__ import main
import os
import sys

# insert path of this script in syspath so actions.py will be found
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))

#
# Script for debugging action server
# This is exactly like issuing the command:
#  $ rasa run actions
#
sys.argv.append('run')
sys.argv.append('actions')
sys.argv.append('--port')
sys.argv.append('5055')
main()
