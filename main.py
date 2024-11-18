import sys
import command_parser
import physical_memory
import virtual_memory
import re

def process_trace_file(trace_file_path, my_cache):
    # Initialize Counters for this trace file
    instruction_bytes = 0
    srcdst_bytes = 0

    # Parse Trace File
    parser = virtual_memory.TraceParser(trace_file_path)
    memory_accesses = parser.parse_trace_file()

    # Simulate Cache Accesses
    for access in memory_accesses:
        if access['type'] == 'instruction':
            instruction_bytes += access['length']
            address = access['address']
            length = access['length']
            # Simulate cache accesses for instruction fetch
            start_address = address
            end_address = address + length
            current_address = start_address
            while current_address < end_address:
                my_cache.access(current_address)
                # Move to the next block if instruction spans multiple blocks
                current_address = ((current_address // my_cache.block_size) + 1) * my_cache.block_size
        elif access['type'] in ('data_read', 'data_write'):
            srcdst_bytes += access['length']
            address = access['address']
            my_cache.access(address)

    # Collect Statistics for this trace file
    total_accesses = my_cache.access_count
    cache_hits = my_cache.hit_count
    cache_misses = my_cache.miss_count
    compulsory_misses = my_cache.compulsory_misses
    conflict_misses = my_cache.conflict_misses

    # Return per-trace file statistics
    return {
        'instruction_bytes': instruction_bytes,
        'srcdst_bytes': srcdst_bytes,
        'total_accesses': total_accesses,
        'cache_hits': cache_hits,
        'cache_misses': cache_misses,
        'compulsory_misses': compulsory_misses,
        'conflict_misses': conflict_misses,
    }

if __name__ == "__main__":

    args, my_cache, my_physical_memory = command_parser.parse_commands()

    # Initialize overall counters
    total_instruction_bytes = 0
    total_srcdst_bytes = 0
    total_accesses = 0
    total_cache_hits = 0
    total_cache_misses = 0
    total_compulsory_misses = 0
    total_conflict_misses = 0

    for trace_file in args.trace_file:

        # Do not reset cache or counts between trace files
        # Process the trace file
        stats = process_trace_file(trace_file, my_cache)

        # Update overall counters
        total_instruction_bytes += stats['instruction_bytes']
        total_srcdst_bytes += stats['srcdst_bytes']
        total_accesses += stats['total_accesses']
        total_cache_hits += stats['cache_hits']
        total_cache_misses += stats['cache_misses']
        total_compulsory_misses += stats['compulsory_misses']
        total_conflict_misses += stats['conflict_misses']

        # Calculate per-trace file hit and miss rates
        hit_rate = (stats['cache_hits'] / stats['total_accesses']) * 100
        miss_rate = 100 - hit_rate

        # Calculate CPI for this trace file
        average_instruction_size = 4  # Adjust based on actual average
        total_instructions = stats['instruction_bytes'] / average_instruction_size
        base_cpi = 1  # Base CPI for each instruction
        miss_penalty = 50  # Adjust based on system specifications
        total_cycles = (total_instructions * base_cpi) + (stats['cache_misses'] * miss_penalty)
        cpi = total_cycles / total_instructions if total_instructions > 0 else 0

    # After processing all trace files, compute overall statistics
    overall_hit_rate = (total_cache_hits / total_accesses) * 100
    overall_miss_rate = 100 - overall_hit_rate

    total_instructions = total_instruction_bytes / average_instruction_size
    total_cycles = (total_instructions * base_cpi) + (total_cache_misses * miss_penalty)
    overall_cpi = total_cycles / total_instructions if total_instructions > 0 else 0

    # Calculate the number of used cache blocks
    used_cache_blocks = my_cache.get_used_cache_blocks()
    unused_blocks = my_cache.total_blocks - used_cache_blocks

    # Ensure unused_blocks is not negative
    unused_blocks = max(unused_blocks, 0)

    # Overhead per block in bytes (assuming valid bit + tag bits)
    overhead_per_block_bytes = (my_cache.tag_size + 1) / 8  # Convert bits to bytes

    # Unused Cache Space in bytes
    unused_cache_space_bytes = unused_blocks * (my_cache.block_size + overhead_per_block_bytes)

    # Unused Cache Space in KB
    unused_cache_space_kb = unused_cache_space_bytes / 1024

    # Percentage waste
    percentage_waste = (unused_cache_space_kb / my_cache.implementation_memory_size) * 100

    # Waste Cost
    waste_cost = unused_cache_space_kb * my_cache.cost_per_kb

    # Print overall statistics
    print("\n***** Cache Simulation Results *****\n")
    print(f"{'Total Cache Accesses:':<30} {total_accesses:>10} ({len(my_cache.used_blocks)} addresses)")
    print(f"{'Instruction Bytes:':<30} {total_instruction_bytes:>10} {'SrcDst Bytes:':<10} {total_srcdst_bytes:>10}")
    print(f"{'Cache Hits:':<30} {total_cache_hits:>10}")
    print(f"{'Cache Misses:':<30} {total_cache_misses:>10}")
    print(f"{'--- Compulsory Misses:':<30} {total_compulsory_misses:>10}")
    print(f"{'--- Conflict Misses:':<30} {total_conflict_misses:>10}")

    print("\n***** Cache Hit and Miss Rate *****\n")
    print(f"{'Hit Rate:':<30} {overall_hit_rate:>10.4f}%")
    print(f"{'Miss Rate:':<30} {overall_miss_rate:>10.4f}%")
    print(f"{'CPI:':<30} {overall_cpi:>10.2f} Cycles/Instruction ({int(total_cycles)})")
    print(f"{'Unused Cache Space:':<30} {unused_cache_space_kb:.2f} KB / {my_cache.implementation_memory_size:.2f} KB = {percentage_waste:.2f}% Waste: ${waste_cost:.2f}")
    print(f"{'Unused Cache Blocks:':<30} {f'{unused_blocks} / {my_cache.total_blocks}':>10}")
