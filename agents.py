import random
from collections import defaultdict
from statetuple import State

class Agent:
    def getMove(self, game):
        pass


class ExpectimaxAgent(Agent):
    def __init__(self, id):
        self.id = id

    def max(self):
        pass

    def remove_card(self, card, deck):
        deck.cards.remove(card)
        deck.discard.append(card)

    def expectimax_move(self, mover_score, mover_stood, other_score, other_stood, deck, player_turn, stand, level):
        """
        :param player_turn:
        :param mover_score:
        :param other_score:
        :param score: Player/agents score so far
        :param deck: Is the actual deck, not the list-version of the deck, and
        :return: An array deciding if player should hit or stand based on expectimax principles
        """
        if mover_score < 0:
            #  print('mover_score is {} (less than 0), return with (False, -1)'.format(mover_score))
            return False, -1

        if other_score < 0:
            #  print('other_score is {} (less than 0), return with (False, mover_score = {})'.format(other_score, other_score))
            return False, mover_score

        if stand >= 2:
            #  print('stand >= 2, returning')
            return None, (mover_score - other_score) * (1 if player_turn else 0)

        if mover_score > 20:
            return False, mover_score

        if level >= 2:
            #  if mover_score < 14:
            return False, (mover_score - other_score) * (1 if player_turn else 0)

        mover_score = mover_score
        # if we draw\/\/...line 40->48

        weight = 1 / len(deck.cards)
        final_score_draw = 0  # this is the score expected from the draw by averaging the cards left in the deck
        i = 0
        print('level {}: entering expectimax mover {}, other score {}, player {}, num cards {}'.format(level, mover_score, other_score,
                                                                                  player_turn, len(list(deck.cards))))
        if not mover_stood:
            for card in deck.cards:
                copy_deck_draw = deck.copyDeck()
                self.remove_card(card, copy_deck_draw)
                # opponent_score is for
                new_player_score = mover_score + card.getScore()
                #  print('level {}: new_player_score is {}, the {}th card, player {}'.format(level, new_player_score, i, player_turn))
                if new_player_score > 21:
                    new_player_score = -1
                score = self.expectimax_move(other_score, other_stood, new_player_score, False, copy_deck_draw, not player_turn, stand =  0, level = level+1)[1]
                final_score_draw += weight * score
                #  print('level {}: score of expectimax is weight ({}) * score ({})'.format(level, weight, score))
                i += 1
        else:
            final_score_draw = -1
        # if we stand
        # final_score_draw = round(final_score_draw)
        opponent_score_if_stand = self.expectimax_move(other_score, other_stood, mover_score, True, deck, not player_turn, stand = stand + 1, level = level+1)[1]
        final_score_stand = opponent_score_if_stand

        # \/\/max of if draw and if stand
        if player_turn:  # if player is maxing
            if final_score_draw > final_score_stand:
                print('{} decides to draw for an expected score of {}'.format(player_turn, final_score_draw))
                return True, final_score_draw
            else:
                print('{} decides to stand at score of {}'.format(player_turn, final_score_stand))
                return False, final_score_stand
        else:  # if person stands
            print('Dealer score from {} to {}'.format(mover_score, final_score_draw / 2 + final_score_stand / 2))
            return None, final_score_draw / 2 + final_score_stand / 2

    def expectimax(self, game_deck, game_dealer, game_player):
        """
        Returns an action String either "Hit" or "Stand" corresponding to legal
        moves in Blackjack.
        """
        decky = game_deck # returns a deck version of the deck
        print('type of decky is.........', type(decky))
        me = game_player
        dealer = game_dealer
        print('score at beginning of expectimax layer', me.getScore())
        # print('getscore type', me.getScore().typeOf())

        if False:  # this will be the new dealer heuristic, so that its not brain dead
            summy = me.getScore()
            for card in decky.getCards():  # have deck be an iterable list
                summy += card.getScore()
            expected = summy / len(decky.getCards())
            newRank = round(expected)

            newScore = me.getScore() + newRank
            # me.setScore(newScore)
            print('What expectimax expected to get if it draws now...', newScore)
            if newScore > 21:
                return "Stand"
            else:
                return "Hit"
        else:
            print('expectimax_move first time')
            if self.expectimax_move(me.getScore(), False, dealer.getScore(), False, decky, True, stand = 0, level = 0)[0]:
                return "Hit"
            else:
                return "Stand"

        # if newScore > 21:
        #     return "Stand"
        # else:
        #     return "Hit"

        # newDeck = drawXorClosest(round(expected), deck)

    def draw(self, x, deck):
        """
        Checks 'deck' for a card with rank matching 'x' and returns the first one
        found.
        Returns `None` if there is no card with rank matching 'x'
        """
        for c in deck:
            if c.getRank() is x:
                deck.remove(c)
                return deck
        return None

    def drawXorClosest(self, x, deck):
        """
        Returns a deck with a card removed of rank equal to `x` or
        the closest integer rank
        """
        deckValues = set()
        drawn = list()
        for c in deck:
            if c.getRank() is x:
                deck.remove(c)
                return deck
            deckValues.append(c.getRank())

        # iteratively expands the scope of "nearest rank" and searches the deck
        hi = x
        lo = x
        drawValue = set()
        while drawValue.isEmpty():
            hi = t = (hi + 1) if t < 11 else 11
            lo = t = (lo - 1) if t > 2 else 2
            if hi in deckValues:
                drawValue.append(hi)
            if lo in deckValues:
                drawValue.append(lo)

        xNew = random.choice(drawValue)
        return self.draw(xNew, deck)

    def getMove(self, game):
        game_dealer = game.table[0]
        game_player = game.table[self.id]
        game_deck = game.getDeckRemaining()
        return self.expectimax(game_deck, game_dealer, game_player)

class QLearningAgent(Agent):
    last_state = None
    last_action = None

    def __init__(self, id, iterations=5000, epsilon=0.5, alpha=0.5, gamma=1):
        self.id = id
        self.qValues = defaultdict(float)
        self.training_iterations = int(iterations)
        self.epsilon = float(epsilon)
        self.learningRate = float(alpha)
        self.discount = float(gamma)
        self.trained = False
    """
    def update(self, state, action, nextState, reward):
        #
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here
        #
        qValue = self.getQValue(state, action)
        if not nextState:
            self.qValues[(state, action)] = qValue + (self.learningRate * reward)
        else:
            insideAlpha = reward + (self.discount * self.getUtility(nextState)) - qValue
            self.qValues[(state, action)] = qValue + ( self.learningRate * insideAlpha)
    """

    def computeUtilityFromQValues(self, state):
        qValueList = list()
        legalActionsList = self.getPossibleActions(state)
        if not legalActionsList:
            return -10
        for action in legalActionsList:
            qValueList.append(self.getQValue(state, action))
        return max(qValueList)

    def computeActionFromQValues(self, state):
        print("cafqv")
        qValueList = list()
        legalActionsList = self.getPossibleActions(state)
        if not legalActionsList:
            return None
        for action in legalActionsList:
            qValueList.append((action, self.getQValue(state, action)))
        maxPair = max(qValueList, key= lambda i: i[1])
        return maxPair[0]

    def pickAction(self, state):
        legalActions = self.getPossibleActions(state)
        action = None
        if not legalActions:
            return action

        doRandom = random.random() < self.epsilon
        if doRandom:
            action = random.choice(legalActions)
        else:
            action = self.getPolicy(state)

        return action

    def getQValue(self, state, action):
        return self.qValues[(state, action)]

    def getPossibleActions(self, state):
        print("gpa")
        print(state)
        #state = State._make(state)
        if state[0].score < 21:
            return ["hit", "stand"]
        else:
            return None #I'm saying 'stand' here as a quick fix but TODO: doesn't seem right

    def getMove(self, game):
        print("gm")
        #print(self.id, " ", len(game.table))
        own_state = game.pullState(self.id)
        """
        others = list()
        print(len(others), " ", len(others) == 0)
        for i,v in enumerate(game.table):
            if i == self.id:
                continue
            if v.hasBusted():
                continue
            others.append((v.getScore(), v))

        other_state = None

        if len(others) is not 0:
            max_other = max(others, key= lambda i: i[0])
            other_state = game.pullState(max_other[1].id)
        """
        stillPlaying = game.playersStillPlaying() > 0
        new_state = (own_state, stillPlaying)
        return self.pickAction(new_state)

    def getPolicy(self, state):
        print("gp")
        return self.computeActionFromQValues(state)

    def getUtility(self, state):
        return self.computeUtilityFromQValues(state)

    ## Training methods ##
    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        self.last_state = state
        self.last_action = action
        qValue = self.getQValue(state, action)
        if not nextState:
            self.qValues[(state, action)] = qValue + (self.learningRate * reward)
        else:
            insideAlpha = reward + (self.discount * self.getUtility(nextState)) - qValue
            self.qValues[(state, action)] = qValue + ( self.learningRate * insideAlpha)

    def observeTransition(self, state, action, nextState):
        if state is not None:
            reward = nextState[0].score - state[0].score
            self.update(state, action, nextState, reward)

    def finishTraining(self):
        self.trained = True
        self.epsilon = 0.0
        self.learningRate = 0.0
        return self.trained

    def isTrained(self):
        return self.trained
# dealer heuristic

#         deck = game.getDeckRemaining()
#         me = game.getPlayer(self.id)
#         print('score at beginning of expectimax layer', me.getScore())
#         # print('getscore type', me.getScore().typeOf())
#
#         sum = me.getScore()
#
#         for card in deck:
#             sum += card.getScore()
#
#         if True:
#             expected = sum / len(deck)
#             newRank = round(expected)
#
#             newScore = me.getScore() + newRank
#             # me.setScore(newScore)
#             print('What expectimax expected to get if it draws now...', newScore)
#             if newScore > 21:
#                 return "Stand"
#             else:
#                 return "Hit"
#         else:
#             if self.expectimax_player_move(me.getScore(), deck):
#                 return "Hit"
#             else:
#                 return "Stand"
