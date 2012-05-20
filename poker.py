# -*- coding: utf-8 -*-

import random


def GetCards():
    cards = []
    for f in range(2,15):
        for c in ['H', 'S', 'D', 'C']:
            cards.append(Card(f,c))
    assert len(cards) == 52
    return cards


class Card(object):
    face_cards_names = ['J', 'Q', 'K', 'A']
    face_cards_values = [11, 12, 13, 14]
    color_names = ['H', 'S', 'D', 'C']
    color_code = [1, 2, 3, 4]
    name_to_face_value = dict(zip(face_cards_names, face_cards_values))
    name_to_color_code = dict(zip(color_names, color_code))
    face_value_to_name = dict(zip(face_cards_values, face_cards_names))
    color_code_to_name = dict(zip(color_code, color_names))
    
    def __init__(self, v, c):
        if isinstance(v, str):
            try:
                v = int(v)
            except ValueError:
                v = self.name_to_face_value[v]
        if isinstance(c, str):
            try:
                c = int(c)
            except ValueError:
                c = self.name_to_color_code[c]
        self.v = v
        self.c = c

    def __str__(self):
        return self.ReadableName()
    
    def ReadableName(self):
        vs = self.face_value_to_name.setdefault(self.v, self.v)
        cs = self.color_code_to_name[self.c]
        return  '%s, %s' % (vs, self.c)
    
class Dealer(object):
    def __init__(self, cards):
        self.cards = cards
        self.Shuffle()

    def GetCard(self):
        c = self.cards[self.top]
        self.top = self.top + 1
        return c

    def Shuffle(self):
        random.shuffle(self.cards)
        self.top = 0

    def GetFlop(self):
        flop = []
        for i in range(0,3):
            flop.append(self.GetCard())
        return flop

    def GetTurn(self):
        return self.GetCard()

    def GetRiver(self):
        return self.GetCard()

    
class Decision(object):
    def __str__(self):
        return self.__class__.__name__

class Fold(Decision):
    pass

class Check(Decision):
    pass

class Call(Decision):
    pass

class AllIn(Decision):
    pass

class Raise(Decision):
    def __init__(self, amount):
        self.amount = amount


class Player(object):
    
    def __init__(self, name, cash):
        self.name = name
        self.cash = cash
        self.cards = []

    def __str__(self):
        return '%s [%s]' % (self.name, self.cash)
    
    def GiveCard(self, card):
        self.cards.append(card)

    def Decide(self,  table):
        current_min_bet = table.GetCurrentMinBet()
        my_bet = table.GetPlayerBet(self)
        if current_min_bet == my_bet:
            return Check()
        else:
            if current_min_bet > self.cash:
                return AllIn()
            return Call()
        
    def NextPlay(self):
        del self.cards[:]

    def GetCards(self):
        return self.cards

    def Take(self, amount):
        self.cash = self.cash - amount
        return amount

    def Give(self, amount):
        self.cash = self.cash + amount

        
class Table(object):
    def __init__(self, min_buyin, max_buyin, small_blind, big_blind):
        self.players = []
        self.min_buyin = min_buyin
        self.max_buyin = max_buyin
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.current_min_bet = big_blind

    def GetPlayerBet(self, player):
        if player not in self.recorded_bets:
            return 0
        return self.recorded_bets[player]
    
    def GetCurrentMinBet(self):
        return self.current_min_bet
    
    def AddPlayer(self, player):
        assert player.cash >= self.min_buyin
        self.players.append(player)

    def GetPlayers(self):
        return self.players

    def RecordDecision(self, player, decision):
        print '%s: %s' % (player, decision)
        if  isinstance(decision, Call):
            needed = self.current_min_bet - self.GetPlayerBet(player)
            self.GetFromPlayer(player, needed)
        if  isinstance(decision, AllIn):
            self.GetFromPlayer(player, player.cash)

    def FlopCards(self, cards):
        self.table_cards.extend(cards)

    def NextPlay(self):
        # kick out players who lost everything
        ruined_players = []
        for i in  range(0, len(self.players)):
            if self.players[i].cash  == 0:
                ruined_players.append(self.players[i])
        for p in ruined_players:
            self.players.remove(p)

        if len(self.players) == 1:
            raise 'Game finished with final player: %s' % self.players[0]
            
                
        self.recorded_bets = {}
        self.table_cards = []
        del self.table_cards[:]
        self.pot = 0

        # move dealer chip
        current_dealer = self.players[0]
        self.players = self.players[1:]
        self.players.append(current_dealer)

    def GetTableCards(self):        
        return self.table_cards

    def GetDealer(self):
        return self.players[0]

    def GetBlinds(self):
        if len(self.players) == 2:
            self.GetFromPlayer(self.players[0], self.small_blind)
            self.GetFromPlayer(self.players[1], self.big_blind)
        else:
            self.GetFromPlayer(self.players[1], self.small_blind)
            self.GetFromPlayer(self.players[2], self.big_blind)

    def GetFromPlayer(self, player, amount):
        player.Take(amount)
        self.recorded_bets[player] =  self.recorded_bets.setdefault(player, 0) + amount
        self.pot = self.pot + amount

    def GetPot(self):
        return self.pot

    def DetermineWinner(self):
        player_by_hand = {}
        for p in self.players:
            hand = GetTopHand(p.GetCards(), self.GetTableCards())
            player_by_hand[hand] = p
            print 'Player %s got %s.  Resulting hand is %s' % (p, hand, map(str, hand.cards))
        sorted_hands = sorted(player_by_hand.keys(), cmp=HandCompare, reverse=True)
        winner = player_by_hand[sorted_hands[0]]
        #TODO: split pot
        winner.Give(self.pot)
        print 'Winner: %s with pot of %s' % (winner, self.pot)
   
def CardCompare(c1, c2):
    return c1.v-c2.v

class Hand(object):
    def __init__(self, cards):
        assert len(cards) == 5, 'Got: %s of length %s which is not length 5' % (cards, len(cards))
        if not isinstance(cards[0], Card):
            parsed_cards = []
            for s in cards:
                v, c = s.split(',')
                v = v.strip()
                c = c.strip()
                parsed_cards.append(Card(v,c))
            cards = parsed_cards
        self.cards = cards

class RoyalFlush(Hand):
    def __str__(self):
        return 'Royal flush of %s' % self.cards[0].c

class StraightFlush(Hand):
    def __str__(self):
        return 'Straight flush %s high' % self.cards[0].v

class FourOfAKind(Hand):
    def __str__(self):
        return 'four of a kind - %s' % self.cards[0].v

class FullHouse(Hand):
    def __str__(self):
        return 'full house %s full of %s' % (self.cards[0].v, self.cards[3].v)

class Flush(Hand):
    def __str__(self):
        return 'Flush %s high' % self.cards[0].v

class Straight(Hand):
    def __str__(self):
        return 'Straight %s high' % self.cards[0].v

class ThreeOfAKind(Hand):
    def __str__(self):
        return 'Three of a kind %s' % self.cards[0].v

class TwoPairs(Hand):
    def __str__(self):
        return'Two pairs %s and %s with kicker %s' % (self.cards[0].v, self.cards[2].v, self.cards[4].v)

class OnePair(Hand):
    def __str__(self):
        return 'Pair of %s' % (self.cards[0].v)

class HighCard(Hand):
    def __str__(self):
        return 'High card %s (%s)' % (self.cards[0], map(str, self.cards))

HandOrder = [
    RoyalFlush,
    StraightFlush,
    FourOfAKind,
    FullHouse,
    Flush,
    Straight,
    ThreeOfAKind,
    TwoPairs,
    OnePair,
    HighCard
    ]

def HandCompare(h1, h2):
    rank_h1 = None
    rank_h2 = None
    for i in range(0, len(HandOrder)):
        if isinstance(h1, HandOrder[i]):
            rank_h1 = i
        if isinstance(h2, HandOrder[i]):
            rank_h2 = i
    assert rank_h1 is not None and rank_h2 is not None
    if rank_h2 == rank_h1:
        for i in range(0, 5):
            if h1.cards[i].v <> h2.cards[i].v:
                ret = h1.cards[i].v - h2.cards[i].v
                return ret
            # else we continue
        return 0
    return rank_h2 - rank_h1

def GetTopHand(player_cards, community_cards):
    cards = list(community_cards)
    cards.extend(player_cards)
    cards.sort(cmp=CardCompare, reverse=True)
    flush = GetFlush(cards)
    if flush:
        if GetStraight(flush):
            if cards[0].v == 1:
                return RoyalFlush(flush)
            return StraightFlush(flush)            

    sames = GetSame(cards)
    if sames:
        if len(sames[0]) == 4:
            four_of_a_kind = list(sames[0])
            four_of_a_kind.append(sames[0][0])
            return FourOfAKind(four_of_a_kind)

    straight = GetStraight(cards)
    if straight:
        Straight(straight)

    if sames:
        if len(sames[0]) == 3:
            if len(sames[1]) == 2 or len(sames[2] ) == 2:
                full_house = list(sames[0])
                if len(sames[1]) == 2:
                    full_house.extend(sames[1])
                else:
                    full_house.extend(sames[2])
                return FullHouse(full_house)            
            three_of_a_kind = list(sames[0])
            for s in sames[1:]:
                for c in s:
                    three_of_a_kind.append(c)
                    if len(three_of_a_kind) == 5:
                        return ThreeOfAKind(three_of_a_kind)                    
        if len(sames[0]) == 2:
            if len(sames[1]) == 2:
                two_pairs = list(sames[0])
                two_pairs.extend(sames[1])
                two_pairs.append(sames[2][0])
                return TwoPairs(two_pairs)
            pair = sames[0]
            for s in sames[1:4]:
                pair.extend(s)
            return OnePair(pair)
    return HighCard(cards[0:5])
                


def CompareSame(l1, l2):
    diff = len(l1) - len(l2)
    if diff == 0:
        return l1[0].v - l2[0].v
    return diff
    
def GetSame(cards):
    value_counts = {}
    for c in cards:
        value_counts[c.v] = value_counts.setdefault(c.v, 0) + 1
    sames = []
    for value in value_counts.keys():
        sames.append([c for c in cards if c.v == value])
    sames.sort(CompareSame, reverse=True)
    return sames

def GetStraight(cards):
    if IsStraightOutOfFive(cards[0:5]):
        return cards[0:5]
    if IsStraightOutOfFive(cards[1:6]):
        return cards[1:6]
    if IsStraightOutOfFive(cards[2:7]):
        return cards[2:7]
    return None
    
def IsStraightOutOfFive(cards):
    for i in range(0, len(cards)-1):
        if (cards[i].v - cards[i+1].v) <> 0:
            return False
    return True            
        
def GetFlush(cards):
    color_counts = {}
    for c in cards:
        color_counts[c.c] = color_counts.setdefault(c.c, 0) + 1
    for color,count in color_counts.iteritems():
        if count == 5:
            return [c for c in cards if c.c == color]
    return None

def PrintAll(table):
    print 'Table %s Dealer: %s Pot: %s' % (map(str, table.GetTableCards()), table.GetDealer(), table.GetPot())
    for p in table.GetPlayers():
        print '%s: %s' % (p, map(str, p.GetCards()))

def main():
    dealer = Dealer(GetCards())

    #players_count = raw_input("Number of players>")
    #buyin = raw_input("Buy in>")
    #buyin = raw_input("S>")

    table = Table(min_buyin=1000, max_buyin=5000, small_blind=25, big_blind=50)
    buyin = 1000
    names = ['Min', 'Ricky', 'Neil']

    for n in names:
        table.AddPlayer(Player(n, buyin))

    while True:
        for p in table.GetPlayers():
            p.NextPlay()
        table.NextPlay()

        dealer.Shuffle()

        table.GetBlinds()

        for i in range(2):
            for p in table.GetPlayers():
                 p.GiveCard(dealer.GetCard())
        PrintAll(table)

        for p in table.GetPlayers():
            table.RecordDecision(p, p.Decide(table))
            
        table.FlopCards(dealer.GetFlop())
        PrintAll(table)

        for p in table.GetPlayers():
            table.RecordDecision(p, p.Decide(table))

        table.FlopCards([dealer.GetTurn()])
        PrintAll(table)

        for p in table.GetPlayers():
            table.RecordDecision(p, p.Decide(table))

        table.FlopCards([dealer.GetRiver()])
        PrintAll(table)

        for p in table.GetPlayers():
            table.RecordDecision(p, p.Decide(table))

        table.DetermineWinner()
        raw_input("Next>")

if __name__ == '__main__':
    main()
