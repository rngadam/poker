import unittest
import poker

class TestHandOrder(unittest.TestCase):
    def testRoyalFlush(self):
        h0 = poker.OnePair(['2, S', '2, C', 'A, S', 'Q, D', 'J, H'])
        h1 = poker.Straight(['A, S', '5, D', '3, S', '2, C', '4, D'])
        h2 = poker.Flush(['5, S', 'J, S', '6, S', '10, S', 'Q, S'])
        h3 = poker.FullHouse(['5, S', 'J, C', '5, D', 'J, S', '5, H'])
        h4 = poker.FourOfAKind(['5, S', '5, C', '5, D', 'J, S', '5, H'])
        h5 = poker.StraightFlush(['5, S', '8, S', '6, S', '9, S', '7, S'])
        h6 = poker.RoyalFlush(['J, S', 'A, S', 'K, S', '10, S', 'Q, S'])
        l = [h0, h1, h2, h3, h4, h5, h6]
        l.sort(cmp=poker.HandCompare, reverse=True)
        self.assertEqual(h6, l[0], '%s != %s' % (h6, l[0]))
        self.assertEqual(h5, l[1])
        self.assertEqual(h4, l[2])
        self.assertEqual(h3, l[3])
        self.assertEqual(h2, l[4])
        self.assertEqual(h1, l[5])
        self.assertEqual(h0, l[6])
        
    def testStraightFlush(self):
        h0 = poker.OnePair(['2, S', '2, C', 'A, S', 'Q, D', 'J, H'])
        h1 = poker.Straight(['A, S', '5, D', '3, S', '2, C', '4, D'])
        h2 = poker.Flush(['5, S', 'J, S', '6, S', '10, S', 'Q, S'])
        h3 = poker.FullHouse(['5, S', 'J, C', '5, D', 'J, S', '5, H'])
        h4 = poker.FourOfAKind(['5, S', '5, C', '5, D', 'J, S', '5, H'])
        h5 = poker.StraightFlush(['5, S', '8, S', '6, S', '9, S', '7, S'])
        l = [h0, h1, h2, h3, h4, h5]
        l.sort(cmp=poker.HandCompare, reverse=True)
        self.assertEqual(h5, l[0], '%s != %s' % (h5, l[0]))
        self.assertEqual(h4, l[1])
        self.assertEqual(h3, l[2])
        self.assertEqual(h2, l[3])
        self.assertEqual(h1, l[4])
        self.assertEqual(h0, l[5])
        
    def testFourOfAKind(self):
        h0 = poker.OnePair(['2, S', '2, C', 'A, S', 'Q, D', 'J, H'])
        h1 = poker.Straight(['A, S', '5, D', '3, S', '2, C', '4, D'])
        h2 = poker.Flush(['5, S', 'J, S', '6, S', '10, S', 'Q, S'])
        h3 = poker.FullHouse(['5, S', 'J, C', '5, D', 'J, S', '5, H'])
        h4 = poker.FourOfAKind(['5, S', '5, C', '5, D', 'J, S', '5, H'])
        l = [h0, h1, h2, h3, h4]
        l.sort(cmp=poker.HandCompare, reverse=True)
        self.assertEqual(h4, l[0], '%s != %s' % (h4, l[0]))
        self.assertEqual(h3, l[1])
        self.assertEqual(h2, l[2])
        self.assertEqual(h1, l[3])
        self.assertEqual(h0, l[4])
        
    def testFullHouse(self):
        h0 = poker.OnePair(['2, S', '2, C', 'A, S', 'Q, D', 'J, H'])
        h1 = poker.Straight(['A, S', '5, D', '3, S', '2, C', '4, D'])
        h2 = poker.Flush(['5, S', 'J, S', '6, S', '10, S', 'Q, S'])
        h3 = poker.FullHouse(['5, S', 'J, C', '5, D', 'J, S', '5, H'])
        l = [h0, h1, h2, h3]
        l.sort(cmp=poker.HandCompare, reverse=True)
        self.assertEqual(h3, l[0], '%s != %s' % (h3, l[0]))
        self.assertEqual(h2, l[1])
        self.assertEqual(h1, l[2])
        self.assertEqual(h0, l[3])
        
    def testFlush(self):
        h0 = poker.OnePair(['2, S', '2, C', 'A, S', 'Q, D', 'J, H'])
        h1 = poker.Straight(['A, S', '5, D', '3, S', '2, C', '4, D'])
        h2 = poker.Flush(['5, S', 'J, S', '6, S', '10, S', 'Q, S'])
        l = [h0, h1, h2]
        l.sort(cmp=poker.HandCompare, reverse=True)
        self.assertEqual(h2, l[0], '%s != %s' % (h2, l[0]))
        self.assertEqual(h1, l[1])
        self.assertEqual(h0, l[2])
        
    def testStraight(self):
        h0 = poker.OnePair(['2, S', '2, C', 'A, S', 'Q, D', 'J, H'])
        h1 = poker.Straight(['A, S', '5, D', '3, S', '2, C', '4, D'])
        h2 = poker.Straight(['A, S', 'J, D', 'K, S', '10, C', 'Q, D'])
        l = [h0, h1, h2]
        l.sort(cmp=poker.HandCompare, reverse=True)
        self.assertEqual(h2, l[0], '%s != %s' % (h2, l[0]))
        self.assertEqual(h1, l[1])
        self.assertEqual(h0, l[2])
        
    def testThreeOfAKind(self):
        h0 = poker.OnePair(['2, S', '2, C', 'A, S', 'Q, D', 'J, H'])
        h1 = poker.TwoPairs(['Q, D', 'Q, H', '2, S', '2, C', 'A, S'])
        h2 = poker.ThreeOfAKind(['A, S', '2, D', '2, S', '2, C', 'Q, D'])
        h3 = poker.HighCard(['Q, 4', '10, 1', '9, 1', '8, 3', '7, 3'])
        l = [h0, h1, h2, h3]
        l.sort(cmp=poker.HandCompare, reverse=True)
        self.assertEqual(h2, l[0], '%s != %s' % (h2, l[0]))
        self.assertEqual(h1, l[1])
        self.assertEqual(h0, l[2])
        self.assertEqual(h3, l[3])
        
    def testTwoPairs(self):
        h0 = poker.OnePair(['2, S', '2, C', 'A, S', 'Q, D', 'J, H'])
        h1 = poker.TwoPairs(['Q, D', 'Q, H', '2, S', '2, C', 'A, S'])
        h2 = poker.TwoPairs(['A, S', 'A, D', '2, S', '2, C', 'Q, D'])
        l = [h0, h1, h2]
        l.sort(cmp=poker.HandCompare, reverse=True)
        self.assertEqual(h2, l[0], '%s != %s' % (h2, l[0]))
        self.assertEqual(h1, l[1])
        self.assertEqual(h0, l[2])

    def testHighCards(self):
        h1 = poker.HighCard(['Q, 4', '10, 1', '9, 1', '8, 3', '7, 3'])
        h2 = poker.HighCard(['Q, 4', 'J, 2', '10, 1', '8, 1', '7, 3'])
        l = [h1, h2]
        l.sort(cmp=poker.HandCompare)
        self.assertEqual(h2, l[1], '%s != %s' % (h2, l[0]))
        self.assertEqual(h1, l[0])

    def testReverseHighCards(self):
        h1 = poker.HighCard(['Q, 4', '10, 1', '9, 1', '8, 3', '7, 3'])
        h2 = poker.HighCard(['Q, 4', 'J, 2', '10, 1', '8, 1', '7, 3'])
        l = [h1, h2]
        l.sort(cmp=poker.HandCompare, reverse=True)
        self.assertEqual(h2, l[0], '%s != %s' % (h2, l[0]))
        self.assertEqual(h1, l[1])
        
if __name__ == '__main__':
    unittest.main()
