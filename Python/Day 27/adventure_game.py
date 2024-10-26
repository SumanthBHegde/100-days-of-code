import os
import json
import random

class Room:
    def __init__(self, name, description, items=None, enemies=None):
        self.name = name
        self.description = description
        self.items = items if items else []
        self.enemies = enemies if enemies else []
        
    def __str__(self):
        return f"{self.name}: {self.description}"
    
    def get_items(self):
        return self.items
    
    def get_enemies(self):
        return self.enemies
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
    
    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)
            
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []
        self.location = None
        
    def move_to(self, room):
        self.location = room
        print(f"{self.name} moved to {room.name}. {room.description}")
        
    def pick_up(self, item):
        if item:
            self.inventory.append(item)
            print(f"Picked up: {item}")
    
    def attack(self, enemy):
        damage = random.randint(50, 100)  # Higher range for a possible one-hit kill
        print(f"Attacked {enemy} for {damage} damage!")
        return damage
    
    def show_inventory(self):
        print(f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")
        
    def save_game(self):
        data = {
            'name': self.name,
            'health': self.health,
            'inventory': self.inventory,
            'location': self.location.name if self.location else None
        }
        with open('save_game.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("Game saved successfully!")
    
    def load_game(self, rooms):
        if os.path.exists('save_game.json'):
            with open('save_game.json', 'r') as f:
                data = json.load(f)
            self.name = data['name']
            self.health = data['health']
            self.inventory = data['inventory']
            self.location = next((room for room in rooms if room.name == data['location']), None)
            print("Game loaded successfully!")
        else:
            print("No saved game found.")

class Game:
    def __init__(self, player):
        self.player = player
        self.rooms = self.create_rooms()
        
    def create_rooms(self):
        room1 = Room("Dungeon Entrance", "A dark, cold entrance to the dungeon.", ["torch"], ["goblin"])
        room2 = Room("Hall of Statues", "A room filled with eerie statues.", ["sword"], [])
        room3 = Room("Treasure Room", "A room full of glittering treasures.", ["gold"], ["dragon"])
        return [room1, room2, room3]
    
    def play(self):
        print("Welcome to the adventure game!")
        
        while True:
            self.show_actions()
            action = input("> ").lower().strip()

            if action == "move":
                self.move()
            elif action == "inventory":
                self.player.show_inventory()
            elif action == "attack":
                self.attack()
            elif action == "pick up":
                self.pick_up()
            elif action == "save":
                self.player.save_game()
            elif action == "load":
                self.player.load_game(self.rooms)
            elif action == "exit":
                print("Exiting game...")
                break
            else:
                print("Invalid action!")
                
    def show_actions(self):
        print("\nChoose an action: move, pick up, attack, inventory, save, load, exit")
    
    def move(self):
        print("Available rooms:")
        for idx, room in enumerate(self.rooms):
            print(f"{idx + 1}. {room}")
        choice = int(input("Choose a room number to move to: ")) - 1
        self.player.move_to(self.rooms[choice])
        
    def pick_up(self):
        room = self.player.location
        items = room.get_items()
        if items:
            print(f"Items in room: {', '.join(items)}")
            choice = input("Pick up an item: ").strip().lower()
            if choice in items:
                room.remove_item(choice)
                self.player.pick_up(choice)
            else:
                print("Item not found.")
        else:
            print("No items to pick up.")
            
    def attack(self):
        room = self.player.location
        enemies = room.get_enemies()
        if enemies:
            print(f"Enemies in room: {', '.join(enemies)}")
            choice = input("Choose an enemy to attack: ").strip().lower()
            if choice in enemies:
                damage = self.player.attack(choice)
                if damage >= 50:  # Assuming 50+ damage defeats the enemy
                    room.remove_enemy(choice)
                    print(f"Defeated {choice}!")
                else:
                    print(f"{choice} still lives!")
            else:
                print("Enemy not found.")
        else:
            print("No enemies to attack.")

if __name__ == '__main__':
    player_name = input("Enter your character's name: ")
    player = Player(player_name)
    game = Game(player)
    game.play()
