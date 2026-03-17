from sortedcontainers import SortedSet

class DynamicLeaderboard:
    def __init__(self):
        # Hash Map: Provides O(1) lookup for a player's current score
        self.scores = {}
        
        # Balanced Tree (SortedSet): Maintains the leaderboard in O(log N)
        # We store tuples of (-score, player) so the highest scores naturally 
        # sort to the beginning of the set (ascending order of negative numbers).
        self.tree = SortedSet()

    def add(self, player: str, score: int):
        self.scores[player] = score
        self.tree.add((-score, player))

    def update(self, player: str, delta: int):
        if player in self.scores:
            old_score = self.scores[player]
            
            # 1. Remove the old entry from the sorted set
            self.tree.remove((-old_score, player))
            
            # 2. Calculate the new score
            new_score = old_score + delta
            
            # 3. Update the hash map and re-insert into the sorted set
            self.scores[player] = new_score
            self.tree.add((-new_score, player))

    def remove(self, player: str):
        if player in self.scores:
            score = self.scores[player]
            # Remove from both data structures
            self.tree.remove((-score, player))
            del self.scores[player]

    def top(self, k: int):
        # Retrieve the first 'k' elements. O(K) time complexity.
        results = []
        for i in range(min(k, len(self.tree))):
            neg_score, player = self.tree[i]
            # Convert the score back to a positive integer
            print(f"{player} {-neg_score}")
            results.append((player, -neg_score))
        return results


# --- Execution Example ---
if __name__ == "__main__":
    lb = DynamicLeaderboard()
    lb.add("Alice", 120)
    lb.add("Bob", 90)
    lb.add("Carol", 150)
    lb.update("Bob", 50)
    lb.top(2)        # Expected: Carol 150, Bob 140
    lb.remove("Carol")
    lb.top(2)        # Expected: Bob 140, Alice 120
