import numpy as np
import pygame

MOVE_LEFT = 1
MOVE_RIGHT = 2
MOVE_UP = 3
MOVE_DOWN = 4

EMPTY = -1
IDEN = 0
X = 1
Y = 2
Z = 3
S = 4
SDG = 5
T = 6
TDG = 7
H = 8
SWAP = 9
# B = 10
CTRL = 11  # "control" part of multi-qubit gate
TRACE = 12  # In the path between a gate part and a "control" or "swap" part

class Controller(pygame.sprite.RenderPlain):
    def __init__(self, table):
        self.table = table
        self.selected_wire = 0
        self.selected_column = 0
        self.circuit_grid_cursor = CircuitGridCursor()
        self.gate_tiles = np.empty((3, 13),
                                   dtype=Grid)

        for i in range(3):
            for j in range(13):
                self.gate_tiles[i][j] = Grid(table, i, j)

        pygame.sprite.RenderPlain.__init__(self.gate_tiles,
                                           self.circuit_grid_cursor)
        self.update()

    def update(self):

        sprite_list = self.sprites()
        for sprite in sprite_list:
            sprite.update()

        for i in range(3):
            for j in range(13):
                self.gate_tiles[i][j].rect.centerx = 120 + 80*j
                self.gate_tiles[i][j].rect.centery = 640 + 70*i

        self.highlight_selected_node(self.selected_wire, self.selected_column)

    def highlight_selected_node(self, wire_num, column_num):
        self.selected_wire = wire_num
        self.selected_column = column_num
        self.circuit_grid_cursor.rect.centerx = 120 + 80*wire_num
        self.circuit_grid_cursor.rect.centery = 640 + 70*column_num

    def reset_cursor(self):
        self.highlight_selected_node(0, 0)

    def display_exceptional_condition(self):
        # TODO: Make cursor appearance indicate condition such as unable to place a gate
        return

    def move_to_adjacent_node(self, direction):
        if direction == MOVE_LEFT and self.selected_column > 0:
            self.selected_column -= 1
        elif direction == MOVE_RIGHT and self.selected_column < 13 - 1:
            self.selected_column += 1
        elif direction == MOVE_UP and self.selected_wire > 0:
            self.selected_wire -= 1
        elif direction == MOVE_DOWN and self.selected_wire < 3 - 1:
            self.selected_wire += 1

        self.highlight_selected_node(self.selected_wire, self.selected_column)

    def get_selected_node_gate_part(self):
        return self.table.get_gate(self.selected_wire, self.selected_column)

    def handle_input_x(self):
        # Add X gate regardless of whether there is an existing gate
        # circuit_grid_node = CircuitGridNode( X)
        # self.table.set_node(self.selected_wire, self.selected_column, circuit_grid_node)

        # Allow deleting using the same key only
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part ==  EMPTY:
            circuit_grid_node = CircuitGridNode( X)
            self.table.set_node(self.selected_wire, self.selected_column, circuit_grid_node)
        elif selected_node_gate_part ==  X:
            self.handle_input_delete()
        self.update()

    def handle_input_y(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part ==  EMPTY:
            circuit_grid_node = CircuitGridNode( Y)
            self.table.set_node(self.selected_wire, self.selected_column, circuit_grid_node)
        elif selected_node_gate_part ==  Y:
            self.handle_input_delete()
        self.update()

    def handle_input_z(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part ==  EMPTY:
            circuit_grid_node = CircuitGridNode( Z)
            self.table.set_node(self.selected_wire, self.selected_column, circuit_grid_node)
        elif selected_node_gate_part ==  Z:
            self.handle_input_delete()
        self.update()

    def handle_input_h(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part ==  EMPTY:
            circuit_grid_node = CircuitGridNode( H)
            self.table.set_node(self.selected_wire, self.selected_column, circuit_grid_node)
        elif selected_node_gate_part ==  H:
            self.handle_input_delete()
        self.update()

    def handle_input_delete(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part ==  X or \
                selected_node_gate_part ==  Y or \
                selected_node_gate_part ==  Z or \
                selected_node_gate_part ==  H:
            self.delete_controls_for_gate(self.selected_wire, self.selected_column)

        if selected_node_gate_part ==  CTRL:
            gate_wire_num = \
                self.table.get_gate_wire_for_control_node(self.selected_wire,
                                                                       self.selected_column)
            if gate_wire_num >= 0:
                self.delete_controls_for_gate(gate_wire_num,
                                              self.selected_column)
        elif selected_node_gate_part !=  SWAP and \
                selected_node_gate_part !=  CTRL and \
                selected_node_gate_part !=  TRACE:
            circuit_grid_node = CircuitGridNode( EMPTY)
            self.table.set_node(self.selected_wire, self.selected_column, circuit_grid_node)

        self.update()

    def handle_input_ctrl(self):
        # TODO: Handle Toffoli   For now, control qubit is assumed to be in ctrl_a variable
        #       with ctrl_b variable reserved for Toffoli gates
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part ==  X or \
                selected_node_gate_part ==  Y or \
                selected_node_gate_part ==  Z or \
                selected_node_gate_part ==  H:
            circuit_grid_node = self.table.get_node(self.selected_wire, self.selected_column)
            if circuit_grid_node.ctrl_a >= 0:
                # Gate already has a control qubit so remove it
                orig_ctrl_a = circuit_grid_node.ctrl_a
                circuit_grid_node.ctrl_a = -1
                self.table.set_node(self.selected_wire, self.selected_column, circuit_grid_node)

                # Remove TRACE nodes
                for wire_num in range(min(self.selected_wire, orig_ctrl_a) + 1,
                                      max(self.selected_wire, orig_ctrl_a)):
                    if self.table.get_gate(wire_num,
                                                                  self.selected_column) ==  TRACE:
                        self.table.set_node(wire_num, self.selected_column,
                                                         CircuitGridNode( EMPTY))
                self.update()
            else:
                # Attempt to place a control qubit beginning with the wire above
                if self.selected_wire >= 0:
                    if self.place_ctrl_qubit(self.selected_wire, self.selected_wire - 1) == -1:
                        if self.selected_wire < self.table.max_wires:
                            if self.place_ctrl_qubit(self.selected_wire, self.selected_wire + 1) == -1:
                                print("Can't place control qubit")
                                self.display_exceptional_condition()

    def handle_input_move_ctrl(self, direction):
        # TODO: Handle Toffoli   For now, control qubit is assumed to be in ctrl_a variable
        #       with ctrl_b variable reserved for Toffoli gates
        # TODO: Simplify the logic in this method, including considering not actually ever
        #       placing a TRACE, but rather always dynamically calculating if a TRACE s/b displayed
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part ==  X or \
                selected_node_gate_part ==  Y or \
                selected_node_gate_part ==  Z or \
                selected_node_gate_part ==  H:
            circuit_grid_node = self.table.get_node(self.selected_wire, self.selected_column)
            if 0 <= circuit_grid_node.ctrl_a < self.table.max_wires:
                # Gate already has a control qubit so try to move it
                if direction == MOVE_UP:
                    candidate_wire_num = circuit_grid_node.ctrl_a - 1
                    if candidate_wire_num == self.selected_wire:
                        candidate_wire_num -= 1
                else:
                    candidate_wire_num = circuit_grid_node.ctrl_a + 1
                    if candidate_wire_num == self.selected_wire:
                        candidate_wire_num += 1
                if 0 <= candidate_wire_num < self.table.max_wires:
                    if self.place_ctrl_qubit(self.selected_wire, candidate_wire_num) == candidate_wire_num:
                        print("control qubit successfully placed on wire ", candidate_wire_num)
                        if direction == MOVE_UP and candidate_wire_num < self.selected_wire:
                            if self.table.get_gate(candidate_wire_num + 1,
                                                                          self.selected_column) ==  EMPTY:
                                self.table.set_node(candidate_wire_num + 1, self.selected_column,
                                                                 CircuitGridNode( TRACE))
                        elif direction == MOVE_DOWN and candidate_wire_num > self.selected_wire:
                            if self.table.get_gate(candidate_wire_num - 1,
                                                                          self.selected_column) ==  EMPTY:
                                self.table.set_node(candidate_wire_num - 1, self.selected_column,
                                                                 CircuitGridNode( TRACE))
                        self.update()
                    else:
                        print("control qubit could not be placed on wire ", candidate_wire_num)

    def handle_input_rotate(self, radians):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part ==  X or \
                selected_node_gate_part ==  Y or \
                selected_node_gate_part ==  Z:
            circuit_grid_node = self.table.get_node(self.selected_wire, self.selected_column)
            circuit_grid_node.radians = (circuit_grid_node.radians + radians) % (2 * np.pi)
            self.table.set_node(self.selected_wire, self.selected_column, circuit_grid_node)

        self.update()

    def place_ctrl_qubit(self, gate_wire_num, candidate_ctrl_wire_num):
        """Attempt to place a control qubit on a wire.
        If successful, return the wire number. If not, return -1
        """
        if candidate_ctrl_wire_num < 0 or candidate_ctrl_wire_num >= self.table.max_wires:
            return -1
        candidate_wire_gate_part = \
            self.table.get_gate(candidate_ctrl_wire_num,
                                                       self.selected_column)
        if candidate_wire_gate_part ==  EMPTY or \
                candidate_wire_gate_part ==  TRACE:
            circuit_grid_node = self.table.get_node(gate_wire_num, self.selected_column)
            circuit_grid_node.ctrl_a = candidate_ctrl_wire_num
            self.table.set_node(gate_wire_num, self.selected_column, circuit_grid_node)
            self.table.set_node(candidate_ctrl_wire_num, self.selected_column,
                                             CircuitGridNode( EMPTY))
            self.update()
            return candidate_ctrl_wire_num
        else:
            print("Can't place control qubit on wire: ", candidate_ctrl_wire_num)
            return -1

    def delete_controls_for_gate(self, gate_wire_num, column_num):
        control_a_wire_num = self.table.get_node(gate_wire_num, column_num).ctrl_a
        control_b_wire_num = self.table.get_node(gate_wire_num, column_num).ctrl_b

        # Choose the control wire (if any exist) furthest away from the gate wire
        control_a_wire_distance = 0
        control_b_wire_distance = 0
        if control_a_wire_num >= 0:
            control_a_wire_distance = abs(control_a_wire_num - gate_wire_num)
        if control_b_wire_num >= 0:
            control_b_wire_distance = abs(control_b_wire_num - gate_wire_num)

        control_wire_num = -1
        if control_a_wire_distance > control_b_wire_distance:
            control_wire_num = control_a_wire_num
        elif control_a_wire_distance < control_b_wire_distance:
            control_wire_num = control_b_wire_num

        if control_wire_num >= 0:
            # TODO: If this is a controlled gate, remove the connecting TRACE parts between the gate and the control
            # ALSO: Refactor with similar code in this method
            for wire_idx in range(min(gate_wire_num, control_wire_num),
                                  max(gate_wire_num, control_wire_num) + 1):
                print("Replacing wire ", wire_idx, " in column ", column_num)
                circuit_grid_node = CircuitGridNode( EMPTY)
                self.table.set_node(wire_idx, column_num, circuit_grid_node)

class CircuitGridNode:
    """Represents a node in the circuit grid"""
    def __init__(self, node_type, radians=0.0, ctrl_a=-1, ctrl_b=-1, swap=-1):
        self.node_type = node_type
        self.radians = radians
        self.ctrl_a = ctrl_a
        self.ctrl_b = ctrl_b
        self.swap = swap

    def __str__(self):
        string = 'type: ' + str(self.node_type)
        string += ', radians: ' + str(self.radians) if self.radians != 0 else ''
        string += ', ctrl_a: ' + str(self.ctrl_a) if self.ctrl_a != -1 else ''
        string += ', ctrl_b: ' + str(self.ctrl_b) if self.ctrl_b != -1 else ''
        return string

class CircuitGridCursor(pygame.sprite.Sprite):
    """Cursor to highlight current grid node"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('utils/Assets/consor.png')
        self.rect = self.image.get_rect()
        self.image.convert_alpha()



class Grid(pygame.sprite.Sprite):
    """Images for nodes"""

    def __init__(self, table, wire_num, column_num):
        pygame.sprite.Sprite.__init__(self)
        self.table = table
        self.wire_num = wire_num
        self.column_num = column_num

        self.update()

    def update(self):
        node_type = self.table.get_gate(self.wire_num, self.column_num)

        if node_type ==  H:
            self.image = pygame.image.load('utils/Assets/H.png')
        # elif node_type ==  X:
        #     node = self.table.get_node(self.wire_num, self.column_num)
        #     if node.ctrl_a >= 0 or node.ctrl_b >= 0:
        #         # This is a control-X gate or Toffoli gate
        #         # TODO: Handle Toffoli gates more completely
        #         if self.wire_num > max(node.ctrl_a, node.ctrl_b):
        #             self.image, self.rect = pygame.image.load('gate_images/not_gate_below_ctrl.png', -1)
        #         else:
        #             self.image, self.rect = pygame.image.load('gate_images/not_gate_above_ctrl.png', -1)
        #     elif node.radians != 0:
        #         self.image, self.rect = pygame.image.load('gate_images/rx_gate.png', -1)
        #         self.rect = self.image.get_rect()
        #         pygame.draw.arc(self.image, MAGENTA, self.rect, 0, node.radians % (2 * np.pi), 6)
        #         pygame.draw.arc(self.image, MAGENTA, self.rect, node.radians % (2 * np.pi), 2 * np.pi, 1)
        #     else:
        #         self.image, self.rect = pygame.image.load('gate_images/x_gate.png', -1)
        # elif node_type ==  Y:
        #     node = self.table.get_node(self.wire_num, self.column_num)
        #     if node.radians != 0:
        #         self.image, self.rect = pygame.image.load('gate_images/ry_gate.png', -1)
        #         self.rect = self.image.get_rect()
        #         pygame.draw.arc(self.image, MAGENTA, self.rect, 0, node.radians % (2 * np.pi), 6)
        #         pygame.draw.arc(self.image, MAGENTA, self.rect, node.radians % (2 * np.pi), 2 * np.pi, 1)
        #     else:
        #         self.image, self.rect = pygame.image.load('gate_images/y_gate.png', -1)
        # elif node_type ==  Z:
        #     node = self.table.get_node(self.wire_num, self.column_num)
        #     if node.radians != 0:
        #         self.image, self.rect = pygame.image.load('gate_images/rz_gate.png', -1)
        #         self.rect = self.image.get_rect()
        #         pygame.draw.arc(self.image, MAGENTA, self.rect, 0, node.radians % (2 * np.pi), 6)
        #         pygame.draw.arc(self.image, MAGENTA, self.rect, node.radians % (2 * np.pi), 2 * np.pi, 1)
        #     else:
        #         self.image, self.rect = pygame.image.load('gate_images/z_gate.png', -1)
        # elif node_type ==  S:
        #     self.image, self.rect = pygame.image.load('gate_images/s_gate.png', -1)
        # elif node_type ==  SDG:
        #     self.image, self.rect = pygame.image.load('gate_images/sdg_gate.png', -1)
        # elif node_type ==  T:
        #     self.image, self.rect = pygame.image.load('gate_images/t_gate.png', -1)
        # elif node_type ==  TDG:
        #     self.image, self.rect = pygame.image.load('gate_images/tdg_gate.png', -1)
        # elif node_type ==  IDEN:
        #     # a completely transparent PNG is used to place at the end of the circuit to prevent crash
        #     # the game crashes if the circuit is empty
        #     self.image, self.rect = pygame.image.load('gate_images/transparent.png', -1)
        # elif node_type ==  CTRL:
        #     # TODO: Handle Toffoli gates correctly
        #     if self.wire_num > \
        #             self.table.get_gate_wire_for_control_node(self.wire_num, self.column_num):
        #         self.image, self.rect = pygame.image.load('gate_images/ctrl_gate_bottom_wire.png', -1)
        #     else:
        #         self.image, self.rect = pygame.image.load('gate_images/ctrl_gate_top_wire.png', -1)
        # elif node_type ==  TRACE:
        #     self.image, self.rect = pygame.image.load('gate_images/trace_gate.png', -1)
        # elif node_type ==  SWAP:
        #     self.image, self.rect = pygame.image.load('gate_images/swap_gate.png', -1)
        else:
            self.image = pygame.Surface([60, 60])
            self.image.set_alpha(0)
            
        self.rect = self.image.get_rect()
        self.image.convert()