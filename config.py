import os
from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__)) 


class Configuration (object):
    GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")