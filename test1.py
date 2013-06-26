import unittest
#from Bricks_game import *

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
        self.assertEqual(player2.lifes,3)


    def test_draw_bricks(self):
        #risuvam nqkakvi neshta
        print("draw")

    def test_load_brick(self):
        print("load")
                            #zarejdam si tuhlichki

if __name__ == '__main__':
    from Bricks_game import *
    unittest.main()
else:
    from Bricks_game import *
