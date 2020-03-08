# -*- coding: utf-8 -*-
import sys
import os
import time
import codecs

pwd_path = os.path.abspath(os.path.dirname(__file__))
parent_path =  os.path.join(pwd_path, '../')
sys.path.append(parent_path)

from codebase.utils import math_utils
from codebase.corrector import Corrector
from codebase.config import *


cn_char_set = Corrector.load_char_set(common_char_path)

print(len(math_utils.edit_distance_word("做喜欢做的",cn_char_set)))
