import pygame, random, math

# Queue to store snake nodes
class Queue:
    def __init__(self, head: any = None) -> None:
        self.head = head
    
    def append_start(self, value: any) -> None:
        currNode = self.Node(value)
        currNode.next = self.head
        self.head = currNode

    def append_end(self, value: any) -> None:
        if self.head:
            currNode = self.head
            while currNode.next:
                currNode = currNode.next
            currNode.next = self.Node(value)
        else:
            self.head = self.Node(value)
    
    def remove_start(self) -> None:
        self.head = self.head.next

    def remove_end(self) -> None:
        if self.head and self.head.next:
            currNode = self.head
            while currNode.next and currNode.next.next:
                currNode = currNode.next
            currNode.next = None
        else:
            self.head = None

    def get_head(self):
        return self.head

    def __iter__(self):
        self.current = self.Node(None, self.head)
        return self
    
    def __next__(self):
        if self.current.next:
            self.current = self.current.next
            return self.current
        raise StopIteration

    def __len__(self) -> int:
        index = 1
        currNode = self.head
        while currNode.next:
            currNode = currNode.next
            index += 1
        return index

    def __repr__(self) -> str:
        return self.head.__repr__()

    class Node:
        def __init__(self, value: any, next = None) -> None:
            self.value = value
            self.next = next
        
        def __repr__(self) -> str:
            return f"value: {self.value}, next: {self.next}"


class Snake:
    def __init__(self, display: pygame.Surface) -> None:
        # Init params
        self.display = display
        self.display_width = display.get_width()
        self.display_height = display.get_height()
        self.nodes: Queue = Queue()
        self.node_radius = 15
        self.node_color = pygame.Color(0, 255, 0)

        # In-game params
        self.direction = None
        self.apple_radius = 10
        self.apple_coords = self.clip_coords(self.display_width/1.5, self.display_height//2)
        self.apple_rect = None
        self.is_eating = False

        # Generate the 3 starting nodes
        for i in range(3): self.nodes.append_end(self.Node(self.clip_coords(self.display_width/4) - 2 * self.node_radius * i, self.clip_coords(self.display_height//2)))
    
    def move(self) -> None:
        if not self.is_eating:
            self.nodes.remove_end()
        else:
            self.set_is_eating(False)
            self.set_apple_coords(self.clip_coords(random.randint(0, self.display_width-1)), self.clip_coords(random.randint(0, self.display_height-1)))

        head = self.nodes.get_head()
        
        if self.direction == "up":
            self.nodes.append_start(self.Node(head.value.get_coords()[0], head.value.get_coords()[1] - 2 * self.node_radius))
        elif self.direction == "down":
            self.nodes.append_start(self.Node(head.value.get_coords()[0], head.value.get_coords()[1] + 2 * self.node_radius))
        elif self.direction == "left":
            self.nodes.append_start(self.Node(head.value.get_coords()[0] - 2 * self.node_radius, head.value.get_coords()[1]))
        elif self.direction == "right":
            self.nodes.append_start(self.Node(head.value.get_coords()[0] + 2 * self.node_radius, head.value.get_coords()[1]))

    def draw(self) -> None:
        self.draw_snake()
        self.draw_apple()

    def draw_snake(self) -> None:
        for node in self.nodes:
            rect = pygame.draw.circle(self.display, self.node_color, node.value.get_coords(), self.node_radius)
            node.value.set_rect(rect)
    
    def draw_apple(self) -> None:
        self.apple_rect = pygame.draw.circle(self.display, pygame.Color(255, 0, 0), self.apple_coords, self.apple_radius)

    def check_loop_collision(self) -> bool:
        head_coords = self.nodes.get_head().value.get_coords()
        for node in self.nodes:
            if node != self.nodes.get_head() and node.value.get_coords() == head_coords:
                return True
        return False
    
    def clip_coords(self, *args) -> tuple[int, int]:
        node_diameter = 2 * self.node_radius
        clipped = []
        for arg in args:
            clipped.append(math.floor(arg/node_diameter) * node_diameter + self.node_radius)
        if len(clipped) == 1: return clipped[0]
        return tuple(clipped)
    
    # Getters and setters
    def set_direction(self, direction: str) -> None:
        self.direction = direction

    def get_nodes(self):
        return self.nodes

    def get_node_color(self) -> pygame.Color:
        return self.node_color
    
    def get_node_radius(self) -> float:
        return self.node_radius
    
    def get_direction(self) -> str | None:
        return self.direction
    
    def get_coords(self) -> tuple[float, float]:
        return self.nodes.get_head().value.get_coords()
    
    def get_apple_rect(self) -> pygame.Rect | None:
        return self.apple_rect
    
    def set_is_eating(self, value: bool) -> None:
        self.is_eating = value
    
    def set_apple_coords(self, x: int, y: int) -> None:
        self.apple_coords = (x, y)

    class Node:
        def __init__(self, x: int, y: int) -> None:
            self.x, self.y = x, y
            self.rect = None

        def get_coords(self) -> tuple[float, float]:
            return (self.x, self.y)
        
        def set_rect(self, rect: pygame.Rect) -> None:
            self.rect = rect

        def get_rect(self) -> pygame.Rect:
            return self.rect