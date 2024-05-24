import unittest

import pycom


class ALUTest(unittest.TestCase):
    def test_idle(self) -> None:
        alu = pycom.ALU(pycom.Bus())
        alu.lhs = 1
        alu.rhs = 2
        alu.result = 0
        alu.add = False
        alu.update()
        self.assertEqual(alu.result, 0)

    def test_add(self) -> None:
        alu = pycom.ALU(pycom.Bus())
        alu.lhs = 1
        alu.rhs = 2
        alu.result = 0
        alu.add = True
        alu.update()
        self.assertEqual(alu.result, 3)
        self.assertFalse(alu.carry)

    def test_add_carry_in(self) -> None:
        alu = pycom.ALU(pycom.Bus())
        alu.lhs = 1
        alu.rhs = 2
        alu.result = 0
        alu.add = True
        alu.carry = True
        alu.update()
        self.assertEqual(alu.result, 4)
        self.assertFalse(alu.carry)

    def test_add_carry_out(self) -> None:
        alu = pycom.ALU(pycom.Bus())
        alu.lhs = pycom.Byte.max() - 1
        alu.rhs = 1
        alu.result = 0
        alu.add = True
        alu.carry = False
        alu.update()
        self.assertEqual(alu.result, 0)
        self.assertTrue(alu.carry)

    def test_add_carry_in_out(self) -> None:
        alu = pycom.ALU(pycom.Bus())
        alu.lhs = pycom.Byte.max() - 1
        alu.rhs = 1
        alu.result = 0
        alu.add = True
        alu.carry = True
        alu.update()
        self.assertEqual(alu.result, 1)
        self.assertTrue(alu.carry)
