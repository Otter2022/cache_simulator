# -s <cache size - KB> [ 8 to 8198 KB]
# -b <block size> [ 8 bytes to 64 bytes ]
# -a <associativity> [ 1, 2, 4, 8, 16 ]
# -r <replacement policy> [ RR or RND ]  Implement one of these
# -p <physical memory - MB> [ 1 MB to 4 GB ]
# -u <% phys mem used> [ 0% to 100% ]
# -n <Instr / Time Slice [ 0 to -1 ] -1 = max
# -f <trace file name> [ name of text file with the trace ]
# o You must accept 1, 2, or 3 trace files as input
# o Each file will use a “-f “ to specify it 

import argparse

def parse_replacement_policy(value):
    if value not in ["RR", "RND", "rr", "rnd"]:
        raise argparse.ArgumentTypeError("Replacement policy must be 'RR' or 'RND'")
    return value

def parse_trace_files(value):
    return value

def parse_commands():
    parser = argparse.ArgumentParser(description='Simulate cache settings and memory parameters.')

    parser.add_argument('-s', '--cache_size', type=int, choices=range(8, 8199),
                        help="Cache size in KB (8 to 8198 KB)", required=False)
    parser.add_argument('-b', '--block_size', type=int, choices=[8, 16, 32, 64],
                        help="Block size in bytes (8, 16, 32, 64 bytes)", required=False)
    parser.add_argument('-a', '--associativity', type=int, choices=[1, 2, 4, 8, 16],
                        help="Cache associativity (1, 2, 4, 8, 16)", required=False)
    parser.add_argument('-r', '--replacement_policy', type=parse_replacement_policy,
                        help="Replacement policy (RR or RND)", required=False)
    parser.add_argument('-p', '--physical_memory', type=int, choices=range(1, 4096 + 1),
                        help="Physical memory in MB (1 MB to 4096 MB / 4 GB)", required=False)
    parser.add_argument('-u', '--phys_mem_used', type=int, choices=range(0, 101),
                        help="Percentage of physical memory used (0% to 100%)", required=False)
    parser.add_argument('-n', '--time_slice', type=int,
                        help="Instructions per time slice (0 to -1, where -1 = max)", required=False)

    parser.add_argument('-f', '--trace_file', action='append', required=True,
                        help="Specify trace file(s). Accepts up to 3 files.")

    args = parser.parse_args()

    if args.time_slice is not None and args.time_slice < -1:
        parser.error("Time slice (-n) must be -1 or a non-negative integer.")

    if len(args.trace_file) < 1 or len(args.trace_file) > 3:
        parser.error("You must specify between 1 and 3 trace files using '-f'.")

    print(f"Cache Size: {args.cache_size} KB")
    print(f"Block Size: {args.block_size} bytes")
    print(f"Associativity: {args.associativity}")
    print(f"Replacement Policy: {args.replacement_policy}")
    print(f"Physical Memory: {args.physical_memory} MB")
    print(f"Physical Memory Used: {args.phys_mem_used} %")
    print(f"Time Slice: {args.time_slice}")
    print(f"Trace Files: {args.trace_file}")
    print_input_parameters(args)
    return args


def print_input_parameters(args):

    print("Trace File(s):")
    for i in args.trace_file:
        print(f"\t{i}")

    print("\n***** Cache Input Parameters *****\n")

    print(f"{'Cache Size:':<30} {args.cache_size:>10}")
    print(f"{'Block Size:':<30} {args.block_size:>10}")
    print(f"{'Associativity:':<30} {args.associativity:>10}")
    print(f"{'Replacement Policy:':<30} {args.replacement_policy:>10}")
    print(f"{'Physical Memory:':<30} {args.physical_memory:>10}")
    print(f"{'Percent Memory Used by System:':<30} {args.phys_mem_used:>10}")
    print(f"{'Instructions / Time Slice:':<30} {args.time_slice:>10}")

    print()
    print("\n***** Cache Calculated Values *****")
    
    print(f"{'Total # Blocks:':<30} {total_blocks:>10}")
    print(f"{'Tag Size:':<30} {tag_size:>10} bits")
    print(f"{'Index Size:':<30} {index_size:>10} bits")
    print(f"{'Total # Rows:':<30} {total_rows:>10}")
    print(f"{'Overhead Size:':<30} {overhead_size:>10} bytes")
    print(f"{'Implementation Memory Size:':<30} {implementation_memory_size_kb:>10.2f} KB")
    print(f"{'Cost:':<30} ${cost:>10.2f} @ $0.15 per KB")

    print("\n***** Physical Memory Calculated Values *****")

    print(f"{'Number of Physical Pages:':<30} {num_physical_pages:>10}")
    print(f"{'Number of Pages for System:':<30} {num_pages_for_system:>10}")
    print(f"{'Size of Page Table Entry:':<30} {size_page_table_entry_bits:>10} bits")
    print(f"{'Total RAM for Page Table(s):':<30} {total_ram_page_table_bytes:>10.2f} bytes")
