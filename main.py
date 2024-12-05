import sys
import command_parser
import re
import virtual_memory

class PageTable:
    def __init__(self, physical_page_count):
        """
        Initialize the PageTable.
        :param physical_page_count: Number of available physical pages.
        """
        self.physical_page_count = physical_page_count
        self.page_table = {}  # Maps virtual page numbers to physical page numbers
        self.lru_queue = []  # Tracks the order of access for LRU replacement
        self.stats = {
            "virtual_pages_mapped": 0,
            "page_table_hits": 0,
            "pages_from_free": 0,
            "total_page_faults": 0
        }

    def access_page(self, virtual_page):
        """
        Simulates accessing a virtual page.
        :param virtual_page: The virtual page number being accessed.
        """
        if virtual_page in self.page_table:
            # Page table hit
            self.stats["page_table_hits"] += 1
            self._update_lru(virtual_page)
        else:
            # Page table miss
            self.stats["virtual_pages_mapped"] += 1
            if len(self.page_table) < self.physical_page_count:
                # Map to a free physical page
                self.stats["pages_from_free"] += 1
                self._map_page(virtual_page)
            else:
                # Page fault (requires eviction)
                self.stats["total_page_faults"] += 1
                self._replace_page(virtual_page)

    def _update_lru(self, virtual_page):
        """
        Updates the LRU queue for a page access.
        :param virtual_page: The virtual page being accessed.
        """
        if virtual_page in self.lru_queue:
            self.lru_queue.remove(virtual_page)
        self.lru_queue.append(virtual_page)

    def _map_page(self, virtual_page):
        """
        Maps a virtual page to a free physical page.
        :param virtual_page: The virtual page to map.
        """
        physical_page = len(self.page_table)  # Assign the next free physical page
        self.page_table[virtual_page] = physical_page
        self.lru_queue.append(virtual_page)

    def _replace_page(self, virtual_page):
        """
        Handles a page replacement using LRU policy.
        :param virtual_page: The virtual page to map.
        """
        # Evict the least recently used page
        evicted_page = self.lru_queue.pop(0)
        del self.page_table[evicted_page]
        # Map the new virtual page to the evicted physical page
        self._map_page(virtual_page)

    def get_statistics(self):
        """
        Returns the statistics of the page table simulation.
        :return: Dictionary of statistics.
        """
        return self.stats

    def reset(self):
        """
        Resets the page table and statistics.
        """
        self.page_table.clear()
        self.lru_queue.clear()
        self.stats = {
            "virtual_pages_mapped": 0,
            "page_table_hits": 0,
            "pages_from_free": 0,
            "total_page_faults": 0
        }


def process_trace_file(trace_file_path, my_cache, page_table, page_size):
    """
    Processes a trace file to simulate memory and cache accesses while updating page table stats.
    """
    # Initialize Counters for this trace file
    instruction_bytes = 0
    srcdst_bytes = 0

    # Parse Trace File
    parser = virtual_memory.TraceParser(trace_file_path)
    memory_accesses = parser.parse_trace_file()

    # Simulate Memory Accesses
    for access in memory_accesses:
        address = access['address']
        virtual_page = address // page_size  # Use page_size for virtual page calculation
        page_table.access_page(virtual_page)  # Simulate page table access

        if access['type'] == 'instruction':
            instruction_bytes += access['length']
            start_address = address
            end_address = address + access['length']
            current_address = start_address
            while current_address < end_address:
                my_cache.access(current_address)
                current_address = ((current_address // my_cache.block_size) + 1) * my_cache.block_size
        elif access['type'] in ('data_read', 'data_write'):
            srcdst_bytes += access['length']
            my_cache.access(address)

    # Collect Statistics for the trace file
    stats = {
        'instruction_bytes': instruction_bytes,
        'srcdst_bytes': srcdst_bytes,
        'page_table_stats': page_table.get_statistics()
    }
    return stats


if __name__ == "__main__":
    args, my_cache, my_physical_memory, page_size = command_parser.parse_commands()

    # Correct physical_memory_size conversion
    physical_memory_size = args.physical_memory * 1024 * 1024  # Convert MB to bytes

    # Calculate physical page count using page size
    physical_page_count = physical_memory_size // page_size  # Calculate total physical pages

    # Initialize PageTable with correct physical page count
    page_table = PageTable(physical_page_count)

    # Overall counters
    total_instruction_bytes = 0
    total_srcdst_bytes = 0

    for trace_file in args.trace_file:
        # Process each trace file
        stats = process_trace_file(trace_file, my_cache, page_table, page_size)

        # Update overall counters
        total_instruction_bytes += stats['instruction_bytes']
        total_srcdst_bytes += stats['srcdst_bytes']

    # Page table statistics
    page_table_stats = page_table.get_statistics()

    # Print overall statistics
    print("\n***** Cache and Page Table Simulation Results *****\n")
    print(f"{'Virtual Pages Mapped:':<30} {page_table_stats['virtual_pages_mapped']}")
    print(f"{'Page Table Hits:':<30} {page_table_stats['page_table_hits']}")
    print(f"{'Pages from Free:':<30} {page_table_stats['pages_from_free']}")
    print(f"{'Total Page Faults:':<30} {page_table_stats['total_page_faults']}")
    print(f"{'Instruction Bytes:':<30} {total_instruction_bytes}")
    print(f"{'SrcDst Bytes:':<30} {total_srcdst_bytes}")
