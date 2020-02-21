import os
import sys

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

if os.name == 'nt':
    # Windows
    ENGINE = 'sqlite:///' + application_path + '/assetmanagement.db'
else:
    ENGINE = 'sqlite:////' + application_path + '/assetmanagement.db'
