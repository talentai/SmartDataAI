import logging
logger = logging.getLogger('Memory')

class Memory:
    def __init__(self):
        self.memory_store = {}

    def is_not_empty(self):
        """Checks if the memory store is not empty."""
        return bool(self.memory_store)
        
    def remember(self, key, role, value):
        """Stores a value in memory with the specified key."""
        if key not in self.memory_store:
            self.memory_store[key] = {'Human': '', 'AI': '', 'Plot Code Generate By AI':[]}
        self.memory_store[key][role] = value
        logger.info(f"Stored {role} message for key {key} in memory.")

    def recall(self, key):
        """Retrieves a value from memory by its key."""
        return self.memory_store.get(key, "Key not found in memory")
    
    def recall_all(self):
        return str(self.memory_store)

    def clear_all_conversation(self):
        self.memory_store.clear()

    def recall_last_conversation(self, number_last_conversation):
        if len(self.memory_store)>0:
            max_key = max(self.memory_store.keys())  # Get the largest key
            total_conversations = len(self.memory_store)  # Get the total number of conversations
        
            if number_last_conversation >= total_conversations:
                min_key = min(self.memory_store.keys())  # If size exceeds, start from the smallest key
            else:
                min_key = max_key - number_last_conversation + 1  # Calculate the starting key
            return {k: self.memory_store[k] for k in range(min_key, max_key + 1)}
        else:
            return {}
    
    def forget(self, key):
        """Removes a value from memory by its key."""
        if key in self.memory_store:
            del self.memory_store[key]
            logger.info(f"Forgot {key} from memory.")
        else:
            logger.warning(f"Key {key} not found in memory.")

    def clear_memory(self):
        """Clears all stored memory."""
        self.memory_store.clear()
        logger.info("Cleared all memory.")