class Room:

    def __init__(self, room_name, room_description):
        self.name = room_name
        self.description = room_description
        self.linked_rooms = {}
        self.character = None
        self.item = None

    def get_name(self):
        return self.name

    def set_description(self, room_description):
        self.description = room_description

    def link_room(self, room_to_link, direction):
        self.linked_rooms[direction] = room_to_link

    def get_character(self):
        return self.character

    def set_character(self, character):
        self.character = character

    def get_item(self):
        return self.item

    def set_item(self, item):
        self.item = item

    def get_details(self):
        print(self.name)
        print("-----")
        if self.description != None:
            print(self.description)
        print("\nLinked Rooms:")
        for direction in self.linked_rooms:
            room = self.linked_rooms[direction]
            print("The " + room.get_name() + " is " + direction)

    def move(self, direction):
        if direction in self.linked_rooms:
            return self.linked_rooms[direction]