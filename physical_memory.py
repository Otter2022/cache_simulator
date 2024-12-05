import math

class PhysicalMemory:
    def __init__(self, physical_memory_mb, percent_memory_used, amount_of_trace_files, page_size):
        # Calculate physical memory in bytes
        self.physical_memory_bytes = physical_memory_mb * 1024 * 1024  # Convert MB to bytes
        
        # Use the provided page size to calculate number of physical pages
        self.page_size_bytes = page_size  # Page size in bytes
        self.num_physical_pages = self.physical_memory_bytes // self.page_size_bytes  # Calculate number of physical pages
        
        # Calculate number of pages reserved for the system
        self.num_pages_for_system = int((percent_memory_used / 100) * self.num_physical_pages)
        
        # Page table entry size in bits
        self.size_page_table_entry_bits = 19  # Assuming fixed size of 19 bits per entry
        
        # Calculate total RAM for page tables
        entries_per_page_table = 2 ** (32 - int(math.log2(self.page_size_bytes)))  # Number of entries per page table
        total_entries = entries_per_page_table * amount_of_trace_files  # Total entries for all trace files
        self.total_ram_page_table_bytes = (total_entries * self.size_page_table_entry_bits) / 8  # Convert bits to bytes
