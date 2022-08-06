import argparse

from tokenizer import Tokenizer
from source_file import SourceFile
from parser import Parser
from tokenstream import TokenStream
from astnode import ASTNode
from display import Diagnostics
from sym_resolver import SymbolResolver
from driver import Driver

import pprint

driver = Driver()
driver.loadArgs()
driver.loadMainFile()
driver.startPipeline()
