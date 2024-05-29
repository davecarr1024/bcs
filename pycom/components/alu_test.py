import unittest

import pycom


class ALUTest(unittest.TestCase):
    def test_set_status(self) -> None:
        alu = pycom.ALU(pycom.Bus())
        alu.status = 1
        self.assertEqual(alu.status, 1)

    def test_set_carry(self) -> None:
        alu = pycom.ALU(pycom.Bus())
        alu.carry = True
        self.assertTrue(alu.carry)
        self.assertEqual(
            alu.status & pycom.ALU.CARRY,
            pycom.ALU.CARRY,
        )
        alu.carry = False
        self.assertFalse(alu.carry)
        self.assertEqual(
            alu.status & pycom.ALU.CARRY,
            0,
        )

    def test_carry_set(self) -> None:
        alu = pycom.ALU(pycom.Bus())
        alu.carry = False
        alu.set_controls("carry_set")
        alu.update()
        self.assertTrue(alu.carry)

    def test_carry_clear(self) -> None:
        alu = pycom.ALU(pycom.Bus())
        alu.carry = True
        alu.set_controls("carry_clear")
        alu.update()
        self.assertFalse(alu.carry)

    def test_idle(self) -> None:
        alu = pycom.ALU(pycom.Bus())
        alu.lhs = 1
        alu.rhs = 2
        alu.result = 0
        alu.add = False
        alu.update()
        self.assertEqual(alu.result, 0)
        self.assertTrue(alu.zero)

    def test_add(self) -> None:
        alu = pycom.ALU(pycom.Bus())
        alu.lhs = 1
        alu.rhs = 2
        alu.result = 0
        alu.add = True
        alu.update()
        self.assertEqual(alu.result, 3)
        self.assertFalse(alu.carry)
        self.assertFalse(alu.zero)

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
        self.assertFalse(alu.zero)

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
        self.assertTrue(alu.zero)

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
        self.assertFalse(alu.zero)

    def test_inc(self) -> None:
        alu = pycom.ALU(pycom.Bus())
        alu.lhs = 1
        alu.inc = True
        alu.update()
        self.assertEqual(alu.result, 2)
        self.assertFalse(alu.zero)

    def test_dec(self) -> None:
        alu = pycom.ALU(pycom.Bus())
        alu.lhs = 1
        alu.dec = True
        alu.update()
        self.assertEqual(alu.result, 0)
        self.assertTrue(alu.zero)
