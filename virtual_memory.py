import re

class TraceParser:
    def __init__(self, trace_file_path):
        self.trace_file_path = trace_file_path

    def parse_trace_file(self):
        memory_accesses = []
        with open(self.trace_file_path, 'r') as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                # Process instruction fetch line
                instruction_line = lines[i].strip()
                i += 1
                # Process data access line
                data_line = lines[i].strip()
                i += 1

                # Extract instruction fetch details
                instr_fetch = self.parse_instruction_line(instruction_line)
                if instr_fetch:
                    memory_accesses.append(instr_fetch)

                # Extract data access details
                data_accesses = self.parse_data_line(data_line)
                memory_accesses.extend(data_accesses)

        return memory_accesses

    def parse_instruction_line(self, line):
        # Example line: EIP (07): 7c80976b ...
        match = re.match(r'EIP \((\d+)\): ([0-9a-fA-F]{8})', line)
        if match:
            length = int(match.group(1))
            address = int(match.group(2), 16)
            return {'type': 'instruction', 'address': address, 'length': length}
        return None

    def parse_data_line(self, line):
        # Example line: dstM: 7ffdf034 00000000 srcM: 7ffdfe2c 901e8b00
        data_accesses = []
        dst_match = re.search(r'dstM: ([0-9a-fA-F]{8})', line)
        src_match = re.search(r'srcM: ([0-9a-fA-F]{8})', line)

        # Process dstM (write)
        if dst_match:
            dst_address = int(dst_match.group(1), 16)
            if dst_address != 0:
                data_accesses.append({'type': 'data_write', 'address': dst_address, 'length': 4})

        # Process srcM (read)
        if src_match:
            src_address = int(src_match.group(1), 16)
            if src_address != 0:
                data_accesses.append({'type': 'data_read', 'address': src_address, 'length': 4})

        return data_accesses 
