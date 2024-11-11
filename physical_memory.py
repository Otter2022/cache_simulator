def calculate_physical_memory_parameters(physical_memory_mb, percent_memory_used):

    physical_memory_bytes = physical_memory_mb * 1024 * 1024  
    page_size_kb = 4
    num_physical_pages = physical_memory_bytes // (page_size_kb * 1024) 
    num_pages_for_system = int((percent_memory_used / 100) * num_physical_pages)
    size_page_table_entry_bits = 19  
    total_ram_page_table_bytes = num_physical_pages * (size_page_table_entry_bits / 8)
    
