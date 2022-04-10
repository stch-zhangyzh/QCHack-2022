import numpy as np

from qiskit import QuantumCircuit, QuantumRegister
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

class Table:
    """Grid-based model that is built when user interacts with circuit"""
    def __init__(self, max_wires, max_columns):
        self.max_wires = max_wires
        self.max_columns = max_columns
        self.nodes = np.empty((max_wires, max_columns), dtype=CircuitGridNode)

    def set_node(self, wire_num, column_num, circuit_grid_node):
        self.nodes[wire_num][column_num] = \
            CircuitGridNode(circuit_grid_node.node_type,
                            circuit_grid_node.radians,
                            circuit_grid_node.ctrl_a,
                            circuit_grid_node.ctrl_b,
                            circuit_grid_node.swap)

    def get_node(self, wire_num, column_num):
        return self.nodes[wire_num][column_num]

    def get_gate(self, wire_num, column_num):
        requested_node = self.nodes[wire_num][column_num]
        if requested_node and requested_node.node_type !=  EMPTY:
            # Node is occupied so return its gate
            return requested_node.node_type
        else:
            # Check for control nodes from gates in other nodes in this column
            nodes_in_column = self.nodes[:, column_num]
            for idx in range(self.max_wires):
                if idx != wire_num:
                    other_node = nodes_in_column[idx]
                    if other_node:
                        if other_node.ctrl_a == wire_num or other_node.ctrl_b == wire_num:
                            return  CTRL
                        elif other_node.swap == wire_num:
                            return  SWAP

        return  EMPTY

    def get_gate_wire_for_control_node(self, control_wire_num, column_num):
        """Get wire for gate that belongs to a control node on the given wire"""
        gate_wire_num = -1
        nodes_in_column = self.nodes[:, column_num]
        for wire_idx in range(self.max_wires):
            if wire_idx != control_wire_num:
                other_node = nodes_in_column[wire_idx]
                if other_node:
                    if other_node.ctrl_a == control_wire_num or \
                            other_node.ctrl_b == control_wire_num:
                        gate_wire_num =  wire_idx
                        print("Found gate: ",
                              self.get_gate(gate_wire_num, column_num),
                              " on wire: " , gate_wire_num)
        return gate_wire_num

    def compute_circuit(self):
        qr = QuantumRegister(self.max_wires, 'q')
        qc = QuantumCircuit(qr)

        for column_num in range(self.max_columns):
            for wire_num in range(self.max_wires):
                node = self.nodes[wire_num][column_num]
                if node:
                    if node.node_type ==  IDEN:
                        # Identity gate
                        qc.i(qr[wire_num])
                    elif node.node_type ==  X:
                        if node.radians == 0:
                            if node.ctrl_a != -1:
                                if node.ctrl_b != -1:
                                    # Toffoli gate
                                    qc.ccx(qr[node.ctrl_a], qr[node.ctrl_b], qr[wire_num])
                                else:
                                    # Controlled X gate
                                    qc.cx(qr[node.ctrl_a], qr[wire_num])
                            else:
                                # Pauli-X gate
                                qc.x(qr[wire_num])
                        else:
                            # Rotation around X axis
                            qc.rx(node.radians, qr[wire_num])
                    elif node.node_type ==  Y:
                        if node.radians == 0:
                            if node.ctrl_a != -1:
                                # Controlled Y gate
                                qc.cy(qr[node.ctrl_a], qr[wire_num])
                            else:
                                # Pauli-Y gate
                                qc.y(qr[wire_num])
                        else:
                            # Rotation around Y axis
                            qc.ry(node.radians, qr[wire_num])
                    elif node.node_type ==  Z:
                        if node.radians == 0:
                            if node.ctrl_a != -1:
                                # Controlled Z gate
                                qc.cz(qr[node.ctrl_a], qr[wire_num])
                            else:
                                # Pauli-Z gate
                                qc.z(qr[wire_num])
                        else:
                            if node.ctrl_a != -1:
                                # Controlled rotation around the Z axis
                                qc.crz(node.radians, qr[node.ctrl_a], qr[wire_num])
                            else:
                                # Rotation around Z axis
                                qc.rz(node.radians, qr[wire_num])
                    elif node.node_type ==  S:
                        # S gate
                        qc.s(qr[wire_num])
                    elif node.node_type ==  SDG:
                        # S dagger gate
                        qc.sdg(qr[wire_num])
                    elif node.node_type ==  T:
                        # T gate
                        qc.t(qr[wire_num])
                    elif node.node_type ==  TDG:
                        # T dagger gate
                        qc.tdg(qr[wire_num])
                    elif node.node_type ==  H:
                        if node.ctrl_a != -1:
                            # Controlled Hadamard
                            qc.ch(qr[node.ctrl_a], qr[wire_num])
                        else:
                            # Hadamard gate
                            qc.h(qr[wire_num])
                    elif node.node_type ==  SWAP:
                        if node.ctrl_a != -1:
                            # Controlled Swap
                            qc.cswap(qr[node.ctrl_a], qr[wire_num], qr[node.swap])
                        else:
                            # Swap gate
                            qc.swap(qr[wire_num], qr[node.swap])

        return qc


class CircuitGridNode:
    """Represents a node in the circuit grid"""
    def __init__(self, node_type, radians=0.0, ctrl_a=-1, ctrl_b=-1, swap=-1):
        self.node_type = node_type
        self.radians = radians
        self.ctrl_a = ctrl_a
        self.ctrl_b = ctrl_b
        self.swap = swap