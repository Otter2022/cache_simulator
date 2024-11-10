import math

def calculate_cache_parameters(cache_size_kb, block_size, associativity):
    
    # Convert cache size from KB to Bytes
    cache_size = cache_size_kb * 1024 
    
    # Total number of blocks and rows
    total_blocks = cache_size // block_size 
    total_rows = total_blocks // associativity 
    
    # Calculate index and offset sizes in bits
    index_size = int(math.log2(total_rows)) if total_rows > 0 else 0  
    offset_size = int(math.log2(block_size)) if block_size > 0 else 0 
    address_size = 32  # Assuming 32-bit address space
    tag_size = address_size - index_size - offset_size 

    # Calculate overhead size 
    overhead_size = (total_rows * tag_size) / 8 
    
    # Implementation Memory Size (in KB)
    implementation_memory_size = (cache_size + overhead_size) / 1024  
    
    # Calculate costs
    cost_per_kb = 0.15  
    cost = implementation_memory_size * cost_per_kb 
