from collections import deque
class PageTable:
    def __init__(self, physical_page_count):
        self.physical_page_count = physical_page_count
        self.page_table = {}  # Maps virtual page numbers to physical page numbers
        self.page_table_mapped = set()  # Track unique virtual pages mapped
        self.lru_queue = deque()  # Tracks the order of access for LRU replacement
        self.stats = {
            "virtual_pages_mapped": 0,
            "page_table_hits": 0,
            "pages_from_free": 0,
            "total_page_faults": 0,
        }
        self._next_physical_page = 0  # Track next available physical page

    def access_page(self, virtual_page):
        if virtual_page in self.page_table:
            # Page table hit
            self.stats["page_table_hits"] += 1
            self._update_lru(virtual_page)
        else:
            # Page table miss
            if virtual_page not in self.page_table_mapped:
                self.stats["virtual_pages_mapped"] += 1
                self.page_table_mapped.add(virtual_page)

            if len(self.page_table) < self.physical_page_count:
                # Map to a free physical page
                self.stats["pages_from_free"] += 1
                self._map_page(virtual_page)
            else:
                # Page fault requiring eviction
                self.stats["total_page_faults"] += 1
                self._replace_page(virtual_page)

    def _update_lru(self, virtual_page):
        if virtual_page in self.lru_queue:
            self.lru_queue.remove(virtual_page)
        self.lru_queue.append(virtual_page)

    def _map_page(self, virtual_page):
        if self._next_physical_page < self.physical_page_count:
            physical_page = self._next_physical_page
            self._next_physical_page += 1
        else:
            raise RuntimeError("Attempting to map page when all pages should be handled by replacement.")
        
        self.page_table[virtual_page] = physical_page
        self.lru_queue.append(virtual_page)

    def _replace_page(self, virtual_page):
        evicted_virtual_page = self.lru_queue.popleft()
        physical_page = self.page_table[evicted_virtual_page]
        del self.page_table[evicted_virtual_page]
        
        self.page_table[virtual_page] = physical_page
        self.lru_queue.append(virtual_page)

    def get_statistics(self):
        return self.stats

    def reset(self):
        self.page_table.clear()
        self.page_table_mapped.clear()
        self.lru_queue.clear()
        self._next_physical_page = 0
        self.stats = {
            "virtual_pages_mapped": 0,
            "page_table_hits": 0,
            "pages_from_free": 0,
            "total_page_faults": 0,
        }