import argparse
import cache as csh
import physical_memory as pm

def parse_replacement_policy(value):
    if value not in ["RR", "RND", "rr", "rnd"]:
        raise argparse.ArgumentTypeError("Replacement policy must be 'RR' or 'RND'")
    return value.upper()

def parse_commands():
    parser = argparse.ArgumentParser(description='Simulate cache settings and memory parameters.')

    parser.add_argument('-s', '--cache_size', type=int, choices=range(8, 8199),
                        help="Cache size in KB (8 to 8198 KB)", required=True)
    parser.add_argument('-b', '--block_size', type=int, choices=[8, 16, 32, 64],
                        help="Block size in bytes (8, 16, 32, 64 bytes)", required=True)
    parser.add_argument('-a', '--associativity', type=int, choices=[1, 2, 4, 8, 16],
                        help="Cache associativity (1, 2, 4, 8, 16)", required=True)
    parser.add_argument('-r', '--replacement_policy', type=parse_replacement_policy,
                        help="Replacement policy (RR or RND)", required=True)
    parser.add_argument('-p', '--physical_memory', type=int, choices=range(1, 4096 + 1),
                        help="Physical memory in MB (1 MB to 4096 MB / 4 GB)", required=True)
    parser.add_argument('-u', '--phys_mem_used', type=int, choices=range(0, 101),
                        help="Percentage of physical memory used (0% to 100%)", required=True)
    parser.add_argument('-n', '--time_slice', type=int,
                        help="Instructions per time slice (0 to -1, where -1 = max)", required=True)

    parser.add_argument('-f', '--trace_file', action='append', required=True,
                        help="Specify trace file(s). Accepts up to 3 files.")

    args = parser.parse_args()

    if args.time_slice is not None and args.time_slice < -1:
        parser.error("Time slice (-n) must be -1 or a non-negative integer.")

    if len(args.trace_file) < 1 or len(args.trace_file) > 3:
        parser.error("You must specify between 1 and 3 trace files using '-f'.")

    # Define page size
    page_size = 4096  # 4 KB page size

    my_cache = csh.cache(args.cache_size, args.block_size, args.associativity)
    my_physical_memory = pm.PhysicalMemory(args.physical_memory, args.phys_mem_used, len(args.trace_file), page_size)

    print_input_parameters(args, my_cache, my_physical_memory)

    return args, my_cache, my_physical_memory, page_size  # Ensure this line returns four values


def print_input_parameters(args, my_cache, my_physical_memory):

    print("Trace File(s):")
    for i in args.trace_file:
        print(f"\t{i}")

    print("\n***** Cache Input Parameters *****\n")

    print(f"{'Cache Size (KB):':<30} {args.cache_size:>10}")
    print(f"{'Block Size (Bytes):':<30} {args.block_size:>10}")
    print(f"{'Associativity:':<30} {args.associativity:>10}")
    print(f"{'Replacement Policy:':<30} {args.replacement_policy:>10}")
    print(f"{'Physical Memory (MB):':<30} {args.physical_memory:>10}")
    print(f"{'Percent Memory Used by System:':<30} {args.phys_mem_used:>10}%")
    print(f"{'Instructions / Time Slice:':<30} {args.time_slice:>10}")

    print("\n***** Cache Calculated Values *****\n")

    cost = "$" + f"{my_cache.cost:.2f}"
    
    print(f"{'Total # Blocks:':<30} {my_cache.total_blocks:>10}")
    print(f"{'Tag Size:':<30} {my_cache.tag_size:>10} bits")
    print(f"{'Index Size:':<30} {my_cache.index_size:>10} bits")
    print(f"{'Total # Rows:':<30} {my_cache.total_rows:>10}")
    print(f"{'Overhead Size:':<30} {my_cache.overhead_size:>10.2f} bytes")
    print(f"{'Implementation Memory Size:':<30} {my_cache.implementation_memory_size:>10.2f} KB")
    print(f"{'Cost:':<30} {cost} @ $0.15 per KB")

    print("\n***** Physical Memory Calculated Values *****\n")

    print(f"{'Number of Physical Pages:':<30} {my_physical_memory.num_physical_pages:>10}")
    print(f"{'Number of Pages for System:':<30} {my_physical_memory.num_pages_for_system:>10}")
    print(f"{'Size of Page Table Entry:':<30} {my_physical_memory.size_page_table_entry_bits:>10} bits")
    print(f"{'Total RAM for Page Table(s):':<30} {my_physical_memory.total_ram_page_table_bytes:>10.2f} bytes")
