from .pkg.application import *
from .pkg.configuration import *
from .pkg.controller.grpcservice import *
from .pkg.model.datastream import *
from .pkg.service import *

import os

APP_RESOURCE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                 '../../resource'))