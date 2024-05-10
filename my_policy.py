from policy import CribbagePolicy, CompositePolicy, GreedyThrower, GreedyPegger, PegPolicy, ThrowPolicy
from scoring import score
from deck import Card
import random
# import itertools as it

class CustomThrower(ThrowPolicy):
    """ A greedy policy for keep/throw in cribbage.  The greedy decision is
        based only on the score obtained by the cards kept and thrown, without
        consideration for how they might interact with the turned card or
        cards thrown by the opponent.
    """
    
    def __init__(self, game):
        """ Creates a greedy keep/throw policy for the given game.

            game -- a cribbage Game
        """
        super().__init__(game)
        

    def throw(self, game, deal, crib):
        """ Returns a greedy choice of which cards to throw.  The greedy choice
            is determined by the score of the four cards kept and the two cards
            thrown in isolation, without considering what the turned card
            might be or what the opponent might throw to the crib.  If multiple
            choices result in the same net score, then one is chosen randomly.

            game -- a Cribbage game
            deal -- a list of the cards dealt
            crib -- 1 for owning the crib, -1 for opponent owning the crib
        """
        def score_split(indices):
            keep = []
            throw = []
            for i in range(len(deal)):
                if i in indices:
                    throw.append(deal[i])
                else:
                    keep.append(deal[i])

            crib_score = 0
            hand_score = 0

            for i in range(1, 14):
                turn = Card(i, "H")
                count = 0
                for card in deal:
                    if card.rank == i: 
                        count += 1

                crib_score += score(game, throw, turn, crib)[0] * ((4-count)/46) 
                hand_score += score(game, keep, turn, crib)[0] * ((4-count)/46)



            return keep, throw, hand_score + crib * crib_score

            # return keep, throw, score(game, keep, None, False)[0] + crib * crib_score

        throw_indices = game.throw_indices()
        
        # to randomize the order in which throws are considered to have the effect
        # of breaking ties randomly
        random.shuffle(throw_indices)

        # pick the (keep, throw, score) triple with the highest score
        return max(map(lambda i: score_split(i), throw_indices), key=lambda t: t[2])
        





    def keep(self, hand, scores, am_dealer):
        """ Selects the cards to keep to maximize the net score for those cards
            and the cards in the crib.  Points in the crib count toward the
            total if this policy is the dealer and against the total otherwise.

            hand -- a list of cards
            scores -- the current scores, with this policy's score first
            am_dealer -- a boolean flag indicating whether the crib
                         belongs to this policy
        """
        keep, throw, net_score = self.throw(self._game, hand, 1 if am_dealer else -1)
        return keep, throw
    
    

class SecondaryPegger(PegPolicy):
    """ A cribbage pegging policy that plays the card that maximizes the
        points earned on the current play.
    """

    def __init__(self, game):
        """ Creates a greedy pegging policy for the given game.

            game -- a cribbage Game
        """
        super().__init__(game)


    def peg(self, cards, history, turn, scores, am_dealer):
        """ Returns the card that maximizes the points earned on the next
            play.  Ties are broken uniformly randomly.

            cards -- a list of cards
            history -- the pegging history up to the point to decide what to play
            turn -- the cut card
            scores -- the current scores, with this policy's score first
            am_dealer -- a boolean flag indicating whether the crib
                         belongs to this policy
        """
        # shuffle cards to effectively break ties randomly
        # random.shuffle(cards)


        best_card = None
        best_score = None
        pairs = {}
        # deck = cards.copy()

        # sorted(deck, key = lambda card: card._rank)
        sorted(cards, key = lambda card: card._rank)


        # separating game into three stages

        # for each, hard code options of what you could do depending on the stage. 

        # previous = history._total
        for card in cards:
            
            score = history.score(self._game, card, 0 if am_dealer else 1)

            if score != None:
                weight = score
            else:
                weight = 0
                
            #     # weighs bigger cards better
            index = cards.index(card)
            weight += ((1 + index) * 0.05)

            points = history._total
            
            if card._rank < 10:
                rank = card._rank
            else:
                rank = 10

            tally = points + rank


            # if score < 15, 
            if points == 0:
                if rank == 5:
                    weight -=.5
                elif rank == 4:
                    weight += .75
                elif rank < 4:
                    weight += .5
            
            elif points < 5:
                if tally == 5:
                    weight -= .5

            elif 5 <= points < 15:
                if tally == 15:
                    weight += .5
                elif tally < 15:
                    weight -= .5
                else:
                    weight += .2
            
            elif 15 <= points < 21:
                if tally == 21:
                    weight -= .75

            elif points == 21: 
                if rank == 4:
                    weight += .5
                elif rank >= 10: 
                    weight += .5
                else:
                    weight += ((1 + index) * 0.05)


            # if score > 15, race to 31
            
            # encourage pairs
            if card._rank in pairs:
                pairs[card._rank] += 1
                if (rank * 3 + points <= 31):
                    weight += .5
            else:
                pairs[rank] = 1

        # encourage runs
            runs = 0
            hand = len(cards)
            end = cards.index(card)
            if (end + 1 < hand):
                if cards[end + 1]._rank == (card._rank + 1):
                    if ((end + 2) < hand) :
                        if (cards[end + 2]._rank == (card._rank + 2)):
                            if rank * 3 + points <= 31:
                                weight += .5

            # try to get last hand


            if score is not None and (best_score is None or weight > best_score):
                best_score = weight
                best_card = card
        return best_card        




class MyPolicy(CribbagePolicy):
    def __init__(self, game):
        self._policy = CompositePolicy(game, CustomThrower(game), SecondaryPegger(game))
        super().__init__(game)

        
    def keep(self, hand, scores, am_dealer):
        return self._policy.keep(hand, scores, am_dealer)


    def peg(self, cards, history, turn, scores, am_dealer):
        return self._policy.peg(cards, history, turn, scores, am_dealer)



    

                                    
