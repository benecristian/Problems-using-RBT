import heapq
from collections import defaultdict

class DynamicMedian:
    def __init__(self):
        # Max-Heap for the lower half of the numbers (store inverted values)
        self.low = []  
        # Min-Heap for the upper half of the numbers
        self.high = [] 
        
        # Lazy deletion tracker: Maps number -> count of pending deletions
        self.delayed = defaultdict(int)
        
        # Track the actual number of *valid* elements in each heap
        self.low_size = 0
        self.high_size = 0

    def _prune(self, heap, is_max_heap: bool):
        """Clears out any deleted elements that have floated to the root."""
        while heap:
            # Peek at the root value (invert it back if it's the Max-Heap)
            val = -heap[0] if is_max_heap else heap[0]
            
            if self.delayed[val] > 0:
                self.delayed[val] -= 1
                heapq.heappop(heap)
            else:
                break # The root is a valid element

    def _balance(self):
        """Maintains the size invariant between the two heaps."""
        if self.low_size > self.high_size + 1:
            self._prune(self.low, is_max_heap=True)
            val = -heapq.heappop(self.low)
            heapq.heappush(self.high, val)
            self.low_size -= 1
            self.high_size += 1
            
        elif self.high_size > self.low_size:
            self._prune(self.high, is_max_heap=False)
            val = heapq.heappop(self.high)
            heapq.heappush(self.low, -val)
            self.high_size -= 1
            self.low_size += 1

    def add(self, x: int):
        # Route the new number to the appropriate heap
        if not self.low or x <= -self.low[0]:
            heapq.heappush(self.low, -x)
            self.low_size += 1
        else:
            heapq.heappush(self.high, x)
            self.high_size += 1
        
        self._balance()

    def remove(self, x: int):
        self.delayed[x] += 1
        
        # Determine which heap's valid size counter needs to be decremented
        if self.low and x <= -self.low[0]:
            self.low_size -= 1
        else:
            self.high_size -= 1
            
        self._balance()

    def median(self):
        # Clean the root of the lower half before accessing it
        self._prune(self.low, is_max_heap=True)
        
        # The median is always the max of the lower half 
        # (This satisfies the "lower median" rule for even counts)
        if self.low:
            print(-self.low[0])
            return -self.low[0]
        return None

# --- Execution Example ---
if __name__ == "__main__":
    dm = DynamicMedian()
    dm.add(5)
    dm.add(2)
    dm.add(10)
    dm.median()   # Expected: 5
    dm.add(7)
    dm.median()   # Expected: 5
    dm.remove(5)
    dm.median()   # Expected: 7
