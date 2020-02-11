import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE = 'sqlite:////' + ROOT_DIR + '/assetmanagement.db'