import pygame
import os
import gates

class Grid(pygame.sprite.Sprite):
    """Images for nodes"""

    def __init__(self, table, wire_num, column_num):
        pygame.sprite.Sprite.__init__(self)
        self.table = table
        self.wire_num = wire_num
        self.column_num = column_num

        self.update()

    def update(self):
        node_type = self.table.get_node_gate_part(self.wire_num, self.column_num)

        if node_type == gates.H:
            self.image, self.rect = pygame.image.load('Asserts/H.png')
        # elif node_type == gates.X:
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
        # elif node_type == gates.Y:
        #     node = self.table.get_node(self.wire_num, self.column_num)
        #     if node.radians != 0:
        #         self.image, self.rect = pygame.image.load('gate_images/ry_gate.png', -1)
        #         self.rect = self.image.get_rect()
        #         pygame.draw.arc(self.image, MAGENTA, self.rect, 0, node.radians % (2 * np.pi), 6)
        #         pygame.draw.arc(self.image, MAGENTA, self.rect, node.radians % (2 * np.pi), 2 * np.pi, 1)
        #     else:
        #         self.image, self.rect = pygame.image.load('gate_images/y_gate.png', -1)
        # elif node_type == gates.Z:
        #     node = self.table.get_node(self.wire_num, self.column_num)
        #     if node.radians != 0:
        #         self.image, self.rect = pygame.image.load('gate_images/rz_gate.png', -1)
        #         self.rect = self.image.get_rect()
        #         pygame.draw.arc(self.image, MAGENTA, self.rect, 0, node.radians % (2 * np.pi), 6)
        #         pygame.draw.arc(self.image, MAGENTA, self.rect, node.radians % (2 * np.pi), 2 * np.pi, 1)
        #     else:
        #         self.image, self.rect = pygame.image.load('gate_images/z_gate.png', -1)
        # elif node_type == gates.S:
        #     self.image, self.rect = pygame.image.load('gate_images/s_gate.png', -1)
        # elif node_type == gates.SDG:
        #     self.image, self.rect = pygame.image.load('gate_images/sdg_gate.png', -1)
        # elif node_type == gates.T:
        #     self.image, self.rect = pygame.image.load('gate_images/t_gate.png', -1)
        # elif node_type == gates.TDG:
        #     self.image, self.rect = pygame.image.load('gate_images/tdg_gate.png', -1)
        # elif node_type == gates.IDEN:
        #     # a completely transparent PNG is used to place at the end of the circuit to prevent crash
        #     # the game crashes if the circuit is empty
        #     self.image, self.rect = pygame.image.load('gate_images/transparent.png', -1)
        # elif node_type == gates.CTRL:
        #     # TODO: Handle Toffoli gates correctly
        #     if self.wire_num > \
        #             self.table.get_gate_wire_for_control_node(self.wire_num, self.column_num):
        #         self.image, self.rect = pygame.image.load('gate_images/ctrl_gate_bottom_wire.png', -1)
        #     else:
        #         self.image, self.rect = pygame.image.load('gate_images/ctrl_gate_top_wire.png', -1)
        # elif node_type == gates.TRACE:
        #     self.image, self.rect = pygame.image.load('gate_images/trace_gate.png', -1)
        # elif node_type == gates.SWAP:
        #     self.image, self.rect = pygame.image.load('gate_images/swap_gate.png', -1)
        # else:
        #     self.image = pygame.Surface([GATE_TILE_WIDTH, GATE_TILE_HEIGHT])
        #     self.image.set_alpha(0)
        #     self.rect = self.image.get_rect()

        self.image.convert()