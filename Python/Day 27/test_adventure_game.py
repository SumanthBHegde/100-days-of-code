import unittest
from io import StringIO
from unittest.mock import patch
from adventure_game import Room, Player, Game

class TestAdventureGame(unittest.TestCase):

    def setUp(self):
        """Set up the game environment for testing."""
        # Initialize rooms
        self.room1 = Room("Dungeon Entrance", "A dark, cold entrance.", ["torch"], ["goblin"])
        self.room2 = Room("Hall of Statues", "A room filled with eerie statues.", ["sword"], [])
        self.room3 = Room("Treasure Room", "A room full of treasures.", ["gold"], ["dragon"])
        
        # Create a player and set initial room
        self.player = Player("Sumanth")
        self.game = Game(self.player)
        self.game.rooms = [self.room1, self.room2, self.room3]

    def test_room_creation(self):
        """Test that rooms are created with the correct attributes."""
        self.assertEqual(self.room1.name, "Dungeon Entrance")
        self.assertEqual(self.room1.description, "A dark, cold entrance.")
        self.assertIn("torch", self.room1.items)
        self.assertIn("goblin", self.room1.enemies)

    def test_player_move_to_room(self):
        """Test that player moves to the specified room."""
        self.player.move_to(self.room2)
        self.assertEqual(self.player.location, self.room2)

    def test_pick_up_item(self):
        """Test that player can pick up items from a room."""
        self.player.move_to(self.room1)
        item = "torch"
        self.player.pick_up(item)
        self.assertIn(item, self.player.inventory)
        self.assertNotIn(item, self.room1.items)

    def test_attack_enemy(self):
        """Test that attacking an enemy affects the enemy status."""
        with patch('random.randint', return_value=15):  # Mock damage value
            self.player.move_to(self.room1)
            self.player.attack("goblin")
            self.assertNotIn("goblin", self.room1.enemies)  # Goblin should be removed

    @patch("builtins.input", side_effect=["move", "1", "pick up", "torch", "inventory", "exit"])
    def test_game_play(self, mock_input):
        """Simulate gameplay and check if the sequence works as expected."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.game.play()
            output = fake_out.getvalue()
            self.assertIn("Welcome to the game", output)
            self.assertIn("Picked up: torch", output)
            self.assertIn("Inventory: torch", output)

    def test_save_load_game(self):
        """Test saving and loading the game state."""
        self.player.move_to(self.room1)
        self.player.pick_up("torch")
        self.player.save_game()

        # Reset player and load game
        new_player = Player("Sumanth")
        new_game = Game(new_player)
        new_game.rooms = [self.room1, self.room2, self.room3]
        new_player.load_game(self.game.rooms)

        # Check that player has correct loaded state
        self.assertEqual(new_player.location, self.room1)
        self.assertIn("torch", new_player.inventory)


if __name__ == "__main__":
    unittest.main()
