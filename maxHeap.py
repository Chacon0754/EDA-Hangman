class Node:
    def __init__(self, score, word):
        self.score = score
        self.word = word
    
    # Return a string representation of the Node
    def __repr__(self) -> str:
        return f"({self.score}, '{self.word}')"


class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, score, word):
        """
        Insert a new node with score and word into the heap
        """
        node = Node(score, word)
        self.heap.append(node)
        self._heapify_up(len(self.heap) - 1)

    def get_max(self):
        """
        Return the maximum node from the heap (the root)
        """
        if self.heap:
            return self.heap[0]
        return None
    
    def delete_max(self):
        """
        Remove and return the maximum node from the heap.
        """
        if len(self.heap) == 1:
            return self.heap.pop()
        elif self.heap:
            max_node = self.heap[0]
            self.heap[0] = self.heap.pop()
            self._heapify_down(0)
            print(f"Deleted: {max_node.word} {max_node.score}")
            return max_node
        return None
    
    def _heapify_up(self, index):
        """
        Ensure the heap property is mantained after insertion
        """
        parent = (index - 1) // 2
        while index > 0 and self.heap[index].score > self.heap[parent].score:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def _heapify_down(self, index):
        """
        Ensure the heap property is mantained after deletion
        """

        largest = index
        left = 2 * index + 1 # Left child
        right = 2 * index + 2 # Right child

        # Check if the left child exists and has a greater score
        if left < len(self.heap) and self.heap[left].score > self.heap[largest].score:
            largest = left
        
        # Check if the right child exists and has a greater score
        if right < len(self.heap) and self.heap[right].score > self.heap[largest].score:
            largest = right
        
        # If the largest is not the currrent index, swap and continue heapifying down
        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._heapify_down(largest)

    def is_empty(self):
        return len(self.heap) == 0
