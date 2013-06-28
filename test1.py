import unittest
from Bricks_game import *


class BricksTest(unittest.TestCase):
  
    def test_brick(self):
        brick1 = brick()
        self.assertEqual(brick1.crush, False, "Noooo")
    
    def test_player_attributes(self):
        player1 = player()
        self.assertIn('name', dir(player1))
    
    def test_hard_brick(self):
        hard_brick1 = hard_brick()
        self.assertEqual(hard_brick1.fragile, 2, "Noooo")

    def test_player_lifes(self):
        player2 = player()
        self.assertEqual(player2.lifes, 3)

    def test_load_brick(self):
        bricks = load_brick()
        f = open('1_level.txt', 'r+').read()
        file = []
        bricks1 = []
        for char in range(0, len(f)):
            if not f[char] == ',' and not f[char] == '\n':
                file.append(int(f[char]))
        for brick in bricks:
            bricks1.append(brick.fragile)
        self.assertEqual(bricks1, file, "Nooooo")


if __name__ == '__main__':
    unittest.main()
