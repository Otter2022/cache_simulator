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

