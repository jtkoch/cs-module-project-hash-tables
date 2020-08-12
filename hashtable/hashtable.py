class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key=None, value=None, next=None):
        self.key = key
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self, head=None):
        self.head = head
        self.length = 0

    def add_to_head(self, key, value):
        self.length += 1
        new_node = HashTableEntry(key, value)
        prev_head = self.head
        self.head = new_node
        self.head.set_next(prev_head)

    def delete(self, key):
        current = self.head
        if current.key == key:
            self.head = self.head.next_node
            self.length -= 1
            return current.value

        prev = current
        current = current.next_node
        # search linked list
        while current is not None:
            # if found, delete it from the linked list,
            if current.key == key:
                prev.set_next(current.next_node)
                # then return the deleted value
                self.length -= 1
                return current
            prev = prev.next_node
            current = current.next_node
        raise Exception

    def contains(self, key):
        for i in self:
            if i.key == key:
                return i.value
        return None

    def __len__(self):
        return self.length

    def get_max(self):
        if not self.head:
            return None
        if len(self) is 0:
            return None
        sorted_ll = sorted([i.value for i in self])
        return sorted_ll[-1]

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current
            current = current.next_node


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8
MIN_LOAD_FACTOR = 0.2
MAX_LOAD_FACTOR = 0.7
RESIZE_FACTOR = 2


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.counter = 0
        self.table = [LinkedList()] * self.capacity


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return self.capacity


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        if self.counter is 0:
            return 0
        return self.counter / self.capacity


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # Your code here
        pass


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        hash = 5381
        for x in key:
            hash = (( hash << 5) + hash) + ord(x)

        return hash & 0xFFFFFFFF


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        i = self.hash_index(key)

        if not self.table[i]:
            self.table[i] = HashTableEntry(key, value)
            self.counter += 1

        else:
            currNode = self.table[i]

            while currNode.key != key and currNode.next:
                currNode = currNode.next

            if currNode.key == key:
                currNode.value = value

            else:
                currNode.next = HashTableEntry(key, value)
                self.counter += 1

        load_factor = self.get_load_factor()
        if load_factor > MAX_LOAD_FACTOR:
            self.resize(self.capacity * RESIZE_FACTOR)


    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        i = self.hash_index(key)
        currNode = self.table[i]

        if not currNode:
            print("Key not found.")

        elif not currNode.next:
            self.table[i] = None
            self.counter -= 1

        else:
            prevNode = None

            while currNode.key != key and currNode.next:
                prevNode = currNode
                currNode = currNode.next

            if not currNode.next:
                prevNode.next = None
                self.counter -= 1
            else:
                prevNode.next = currNode.next
                self.counter -= 1

        load_factor = self.get_load_factor()
        if load_factor < MIN_LOAD_FACTOR:
            if self.capacity/RESIZE_FACTOR < MIN_CAPACITY:
                self.resize(MIN_CAPACITY)
            else:
                self.resize(self.capacity // RESIZE_FACTOR)


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.
        
        Implement this.
        """
        i = self.hash_index(key)

        if self.table[i]:
            currNode = self.table[i]

            while currNode.key != key and currNode.next:
                currNode = currNode.next

            if not currNode.next:
                return currNode.value
            else:
                return currNode.value

        else:
            return None


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.
        Implement this.
        """
        old_storage = self.table

        self.capacity = new_capacity
        self.table = [LinkedList()] * new_capacity

        for item in old_storage:
            if item:
                currNode = item
                while currNode:
                    self.put(currNode.key, currNode.value)
                    currNode = currNode.next


if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")