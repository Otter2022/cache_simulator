import math

class cache:
    def __init__(self, cache_size_kb, block_size, associativity):
        # Convert cache size from KB to Bytes
        self.cache_size = cache_size_kb * 1024 
        self.block_size = block_size
        self.associativity = associativity
        
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

        self.cache = [{} for _ in range(self.total_rows)]  # Each row is a dictionary for associativity
        self.access_count = 0
        self.hit_count = 0
        self.miss_count = 0
        self.compulsory_misses = 0
        self.conflict_misses = 0
        self.used_blocks = set()  # For tracking compulsory misses

    def access(self, address):
        self.access_count += 1
        index, tag = self.get_index_and_tag(address)
        cache_set = self.cache[index]

        # Check for hit
        if tag in cache_set:
            self.hit_count += 1
            # Update cache replacement policy if needed
        else:
            # Miss occurred
            self.miss_count += 1
            # Check for compulsory miss
            block_address = address // self.block_size
            if block_address not in self.used_blocks:
                self.compulsory_misses += 1
                self.used_blocks.add(block_address)
            else:
                self.conflict_misses += 1

            # Handle cache replacement
            if len(cache_set) < self.associativity:
                cache_set[tag] = {'valid': True}
            else:
                # Implement replacement policy (e.g., random replacement)
                evicted_tag = next(iter(cache_set))
                del cache_set[evicted_tag]
                cache_set[tag] = {'valid': True}

    def get_index_and_tag(self, address):
        offset_bits = self.offset_size
        index_bits = self.index_size
        offset = address & ((1 << offset_bits) - 1)
        index = (address >> offset_bits) & ((1 << index_bits) - 1)
        tag = address >> (offset_bits + index_bits)
        return index, tag
    