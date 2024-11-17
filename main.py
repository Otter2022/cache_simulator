import sys
import command_parser
import physical_memory
import re

if __name__ == "__main__":

    args, my_cache, my_physical_memory = command_parser.parse_commands()

    physical_memory.parse_trace_file(args.trace_file[0])