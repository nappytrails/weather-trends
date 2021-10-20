# Dependencies
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.parser import *
import json
import requests
from pprint import pprint
from config import driver, username, password, host, port, database
from sqlalchemy import create_engine

connection_string = f"{driver}://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string)
connection = engine.connect()

contentChoiceDF = pd.read_sql_table('contentChoice', connection)
print(contentChoiceDF)