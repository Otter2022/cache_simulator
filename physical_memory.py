import math
import re

class PhysicalMemory:
    def __init__(self, physical_memory_mb, percent_memory_used, amount_of_trace_files):
        # Calculate physical memory in bytes
        self.physical_memory_bytes = physical_memory_mb * 1024 * 1024
        
        # Page size in KB and calculate number of physical pages
        self.page_size_kb = 4  # Assuming 4 KB pages
        self.num_physical_pages = self.physical_memory_bytes // (self.page_size_kb * 1024)  # Convert page size to bytes
        
        # Calculate number of pages reserved for the system
        self.num_pages_for_system = int((percent_memory_used / 100) * self.num_physical_pages)
        
        # Page table entry size in bits and calculate total RAM for page tables
        self.size_page_table_entry_bits = 19  # Assuming fixed size of 19 bits per entry
        self.total_ram_page_table_bytes = 2**self.size_page_table_entry_bits * amount_of_trace_files * (self.size_page_table_entry_bits / 8)  # Convert bits to bytes

class MemoryAccessor:
    def __init__(self, address, length, access_type):
        self.address = address
        self.length = length
        self.access_type = access_type  # 'IF', 'DR', 'DW'

    def __repr__(self):
        return f"MemoryAccess(address=0x{self.address:X}, length={self.length}, type={self.access_type})"

def parse_instruction_line(line):
    match = re.match(r'EIP \(([\dA-Fa-f]{2})\): ([\dA-Fa-f]{8})', line)
    if match:
        inst_length_hex, inst_address_hex = match.groups()
        inst_length = int(inst_length_hex, 16)
        inst_address = int(inst_address_hex, 16)
        return inst_length, inst_address
    else:
        raise ValueError(f"Invalid instruction line format: {line}")

def parse_data_line(line):
    match = re.match(
        r'dstM: ([\dA-Fa-f]{8}) \S+ srcM: ([\dA-Fa-f]{8}) \S+',
        line
    )
    if match:
        dstM_hex, srcM_hex = match.groups()
        dstM_address = int(dstM_hex, 16)
        srcM_address = int(srcM_hex, 16)
        return dstM_address, srcM_address
    else:
        raise ValueError(f"Invalid data line format: {line}")

def process_memory_access(access):
    # Integrate this function with your cache simulator
    # For example, check if the address is in the cache, update hits/misses, etc.
    print(access)

def parse_trace_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        line1 = lines[i].strip()
        if i + 1 < len(lines):
            line2 = lines[i + 1].strip()
        else:
            print(f"Incomplete block at line {i + 1}")
            break
        i += 2

        # Parse instruction fetch line
        try:
            inst_length, inst_address = parse_instruction_line(line1)
            inst_access = MemoryAccessor(inst_address, inst_length, 'IF')
            process_memory_access(inst_access)
        except ValueError as ve:
            print(ve)
            continue

        # Parse data access line
        try:
            dstM_address, srcM_address = parse_data_line(line2)
            # Data Read Access
            if srcM_address != 0x00000000:
                data_read_access = MemoryAccessor(srcM_address, 4, 'DR')
                process_memory_access(data_read_access)
            # Data Write Access
            if dstM_address != 0x00000000:
                data_write_access = MemoryAccessor(dstM_address, 4, 'DW')
                process_memory_access(data_write_access)
        except ValueError as ve:
            print(ve)
            continue
