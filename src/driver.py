from display import Diagnostics
from source_file import SourceFile
from sym_resolver import SymbolResolver
from tokenizer import Tokenizer
from parser import Parser
from symtab import SymbolTable

from dataclasses import dataclass
import argparse

@dataclass
class Option:
    name: str
    value: str

class Driver:
    def __init__(self):
        self.__diagnostics = Diagnostics()
        self.__files: list[SourceFile] = []
        self.__symbol_table = SymbolTable()
        self.__sym_resolver = SymbolResolver(self.__symbol_table)
        self.__tokenizer = Tokenizer()
        self.__parser = Parser()
        self.__options = []

    def loadArgs(self):
        argparser = argparse.ArgumentParser()
        argparser.add_argument('main', 
                type=str, 
                help="The main source file to start the compiler")
        argparser.add_argument(
            'debug',
            type=int,
            help="Whether to run this in debug mode with a given mode: 1=tokenizer, 2=parser, 3=symbol resolution, 4=type checker")  # noqa
        argparser.add_argument(
                'dump',
                type=int,
                help="Whether to dump the result of a given pass (int argument): 1=tokens, 2=ast, 3=symbol table, 4=type map")  # noqa
        args = argparser.parse_args()
        if args.main:
            self.__options.append(Option('main', args.main))
        if args.debug:
            self.__options.append(Option('debug', args.debug))
        if args.dump:
            self.__options.append(Option("dump", args.dump))

    def getOption(self, name: str):
        for option in self.options:
            if option.name == name:
                return option.value
        return None

    def loadMainFile(self):
        file_option = self.getOption('main')
        self.loadSourceFile(file_option)

    def loadSourceFile(self, pth):
        file = open(pth, 'r')
        contents = file.read()
        file.close()
        source_file = SourceFile(contents, pth)
        self.__files.append(source_file)
        self.__sym_resolver.enter_file(pth)
        return source_file

    def getFile(self, path):
        for file in self.__files:
            if file.path == path:
                return file
        return None

    def startMainFile(self):
        main_file_path = self.getOption('main')
        main_file = self.getFile(main_file_path)
        self.startPipeline(main_file)

    def startPipeline(self, file):
        tokens = self.__tokenizer.tokenize(file)
        parse_result = self.__parser.parse(file, tokens)
        if parse_result.is_error():
            return
        if parse_result.unwrap().accept(self.__sym_resolver.visitor) is False:
            return
