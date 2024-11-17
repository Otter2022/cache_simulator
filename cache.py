import math

class cache:
    def __init__(self, cache_size_kb, block_size, associativity):
        # Convert cache size from KB to Bytes
        self.cache_size = cache_size_kb * 1024 
        
        # Total number of blocks and rows
        self.total_blocks = self.cache_size // block_size 
        self.total_rows = self.total_blocks // associativity 
        
        # Calculate index and offset sizes in bits
        self.index_size = int(math.log2(self.total_rows)) if self.total_rows > 0 else 0  
        self.offset_size = int(math.log2(block_size)) if block_size > 0 else 0 
        self.address_size = 32  # Assuming 32-bit address space
        self.tag_size = self.address_size - self.index_size - self.offset_size 

        # Calculate overhead size 
        self.overhead_size = (self.total_rows * self.tag_size * associativity + self.total_blocks) / 8 
        
        # Implementation Memory Size (in KB)
        self.implementation_memory_size = (self.cache_size + self.overhead_size) / 1024  
        
        # Calculate costs
        self.cost_per_kb = 0.15  
        self.cost = self.implementation_memory_size * self.cost_per_kb 
