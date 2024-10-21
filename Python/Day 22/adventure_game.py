import sys

# Room class
class Room:
    def __init__(self, name, description, items=None):
        self.name = name
        self.description = description
        self.items = items if items else []
        self.connected_rooms = {}
    
    def connect_room(self, direction, room):
        self.connected_rooms[direction] = room
    
    def describe(self):
        print(f"\n{self.name}")
        print(self.description)
        if self.items:
            print(f"You see: {', '.join(self.items)}")
        if self.connected_rooms:
            directions = ', '.join(self.connected_rooms.keys())
            print(f"Exits: {directions}")
        
    def get_room_in_direction(self, direction):
        return self.connected_rooms.get(direction)

# Player Class
class Player:
    def __init__(self, starting_room):
        """Initialize the player with a starting room"""
        self.inventory = []
        self.current_room = starting_room
    
    def move(self, direction):
        """Move the player in the given direction"""
        next_room = self.current_room.get_room_in_direction(direction)
        if next_room:
            self.current_room = next_room
            self.current_room.describe()
        else:
            print("You can't go that way.")
            
    def pick_item(self, item):
        """Pick an item from the current room and add it to the inventory"""
        if item in self.current_room.items:
            self.inventory.append(item)
            self.current_room.items.remove(item)
            print(f"You picked up: {item}")
        else:
            print(f"No {item} here!")
    
    def show_inventory(self):
        """Display the player's inventory"""
        print(f"Inventory: {','.join(self.inventory) if self.inventory else 'empty'}")


# Helper Function to Display Help
def display_help():
    print("\nAvailable commands:")
    print("  move <direction>  - Move to a room in a specific direction (e.g., 'move north')")
    print("  pick <item>       - Pick up an item from the current room (e.g., 'pick key')")
    print("  inventory         - Check what items you're carrying")
    print("  look              - Look around the current room")
    print("  quit              - Quit the game")
    print("  help              - Show this help message")    
 
    
# Main Game function
def start_game():
    # Creating rooms
    living_room = Room("Living Room", "A cozy room with a sofa and a TV.")
    kitchen = Room("Kitchen", "A messy kitchen with dirty dishes.", ["knife"])
    garden = Room("Garden", "A lush garden with beautiful flowers.", ["key"])
    
    # Connecting rooms
    living_room.connect_room('north', kitchen)
    kitchen.connect_room('south', living_room)
    living_room.connect_room('east', garden)
    garden.connect_room('west', living_room)
    
    # Creating player, setting their starting room to 'living_room'
    player = Player(living_room)
    player.current_room.describe()
    
    # Game loop
    while True:
        command = input("\nWhat would you like to do? (type 'help' for options) ").lower().split()

        if len(command) == 0:
            print("Please enter a valid command.")
            continue

        action = command[0]

        if action == "move":
            if len(command) > 1:
                direction = command[1]
                player.move(direction)
            else:
                print("Move where? Please specify a direction.")
        
        elif action == "pick":
            if len(command) > 1:
                item = command[1]
                player.pick_item(item)
            else:
                print("Pick what? Please specify an item to pick up.")
        
        elif action == "inventory":
            player.show_inventory()

        elif action == "look":
            player.current_room.describe()
        
        elif action == "help":
            display_help()

        elif action == "quit":
            print("Thanks for playing!")
            sys.exit()

        else:
            print("Invalid command. Type 'help' to see available options.")


if __name__ == "__main__":
    start_game()