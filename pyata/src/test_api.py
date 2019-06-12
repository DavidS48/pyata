
import unittest

from api import Obj

class TestConnections(unittest.TestCase):
    def test_connect(self):
        obj1 = Obj("obj1")
        obj2 = Obj("obj2")
        obj1.i1 << obj2.o1
        self.assertEqual(obj1.ins.total_connections, 1)
        self.assertEqual(obj1.outs.total_connections, 0)
        self.assertEqual(obj2.ins.total_connections, 0)
        self.assertEqual(obj2.outs.total_connections, 1)

    def test_double_in(self):
        obj1 = Obj("obj1")
        obj2 = Obj("obj2")
        obj1.i1 << obj2.o1
        obj1.i1 << obj2.o2
        self.assertEqual(obj1.ins.total_connections, 2)
        self.assertEqual(obj1.outs.total_connections, 0)
        self.assertEqual(obj2.ins.total_connections, 0)
        self.assertEqual(obj2.outs.total_connections, 2)

    def test_replace_in(self):
        obj1 = Obj("obj1")
        obj2 = Obj("obj2")
        obj1.i1 << obj2.o1
        obj1.i1 <<= obj2.o2
        self.assertEqual(obj1.ins.total_connections, 1)
        self.assertEqual(obj1.outs.total_connections, 0)
        self.assertEqual(obj2.ins.total_connections, 0)
        self.assertEqual(obj2.outs.total_connections, 1)

    def test_disconnect(self):
        obj1 = Obj("obj1")
        obj2 = Obj("obj2")
        obj1.i1 << obj2.o1
        obj1.i1 << obj2.o2
        obj1.i1 | obj2.o2
        self.assertEqual(obj1.ins.total_connections, 1)
        self.assertEqual(obj1.outs.total_connections, 0)
        self.assertEqual(obj2.ins.total_connections, 0)
        self.assertEqual(obj2.outs.total_connections, 1)

    def test_reverse_disconnect(self):
        obj1 = Obj("obj1")
        obj2 = Obj("obj2")
        obj1.i1 << obj2.o1
        obj1.i1 << obj2.o2
        obj1.i2 << obj2.o1
        obj2.o1 | obj1.i1
        self.assertEqual(obj1.ins.total_connections, 2)
        self.assertEqual(obj1.outs.total_connections, 0)
        self.assertEqual(obj2.ins.total_connections, 0)
        self.assertEqual(obj2.outs.total_connections, 2)

class TestConnectionArithmetic(unittest.TestCase):

    def test_add_connections(self):
        obj1 = Obj("obj1")
        obj2 = Obj("obj2")
        obj1.i1 << obj2.o1 + obj2.o2
        self.assertEqual(obj1.ins.total_connections, 1)
        self.assertEqual(obj1.outs.total_connections, 0)
        self.assertEqual(obj2.ins.total_connections, 0)
        self.assertEqual(obj2.outs.total_connections, 2)

    def test_disconnect_added_connections(self):
        obj1 = Obj("obj1")
        obj2 = Obj("obj2")
        obj1.i1 << obj2.o1 + obj2.o2
        obj1.i1 | obj2.o1
        self.assertEqual(obj1.ins.total_connections, 1)
        self.assertEqual(obj1.outs.total_connections, 0)
        self.assertEqual(obj2.ins.total_connections, 0)
        self.assertEqual(obj2.outs.total_connections, 1)

    def test_add_constant(self):
        obj1 = Obj("obj1")
        obj2 = Obj("obj2")
        obj1.i1 << obj2.o1 + 3
        self.assertEqual(obj1.ins.total_connections, 1)
        self.assertEqual(obj1.outs.total_connections, 0)
        self.assertEqual(obj2.ins.total_connections, 0)
        self.assertEqual(obj2.outs.total_connections, 1)

    def test_disconnect_added_constant(self):
        obj1 = Obj("obj1")
        obj2 = Obj("obj2")
        obj1.i1 << obj2.o1 + 2
        obj1.i1 | obj2.o1
        self.assertEqual(obj1.ins.total_connections, 0)
        self.assertEqual(obj1.outs.total_connections, 0)
        self.assertEqual(obj2.ins.total_connections, 0)
        self.assertEqual(obj2.outs.total_connections, 0)

      
    
if __name__ == "__main__":
    unittest.main()


