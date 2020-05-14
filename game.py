from deck import Deck
from card import Card, Suits, Ranks
from agents import Agent, QLearningAgent
from statetuple import State
import sys

class BlackjackPlayer:
    id = 0
    def __init__(self, intelligence=None):

        self.hand = list()
        self.score = 0
        self.gameState = {"busted": False, "won": False, "standing": False}
        self.ai = intelligence
        self._softScore = False
        self.id = BlackjackPlayer.id
        BlackjackPlayer.id += 1

    def getScore(self):
        return self.score

    def hit(self, card):
        """
        Takes a Card object into the Player's hand.

        Returns the Player's score for bookkeeping, else -1 if the Player
        is not eligible to take cards.

        Should check value immediately because any subsequent check of a Player
        will return -1 even if the Player had 'won' the game.
        """
        if any( list(self.gameState.values()) ):
            return -1

        assert isinstance(card, card.__class__)
        if card.getRank() == Ranks.ACE:
            self._softScore = True

        self.hand.append(card)
        self.score += card.getScore()

        if self.score > 21:
            if self._softScore:
                self.score -= 10
                self._softScore = False
            else:
                self.gameState["busted"] = True
        elif self.score is 21:
            self.gameState["won"] = True

        if self.id == 0:
            print("Dealer has a score of %d\n" % self.score)
        else:
            print("Player %d has a score of %d\n" % (self.id, self.score))
        return self.score

    def stand(self):
        self.gameState["standing"] = True
        if self.id == 0:
            print("Dealer is standing with a score of %d\n" % self.score)
        else:
            print("Player %d is standing with a score of %d\n" % (self.id, self.score))

    def isSoftScore(self):
        return self._softScore

    def isStanding(self):
        return self.gameState["standing"]

    def hasBusted(self):
        return self.gameState["busted"]

    def hasWon(self):
        return self.gameState["won"]

    def useAI(self, game):
        agent = self.ai
        move = agent.getMove(game)
        return move

    def reset(self):
        self.score = 0
        self.hand.clear()
        self.gameState = { k: 0 for k in self.gameState.keys() }

class BlackjackGame:
    def __init__(self, deck = Deck()):
        self.table = [BlackjackPlayer()]
        self.tableState = [False] #State checks if player is Out of game
        self.deck = deck
        self.gameStarted = False
        self.postGame = False
        self.playerCount = 0

    def beginNewGame(self):
        if self.postGame:
            for player in self.table:
                player.reset()
            for i in range( len(self.tableState) ):
                self.tableState[i] = False

        self.deck.restartDeck()

        self.postGame = False
        return self.game()

    def turnOrderGenerator(self):
        players = [player for player in self.table if not any( list( player.gameState.values() ) )]
        for player in players:
            yield player

    def playersStillPlaying(self):
        count = 0
        for state in self.tableState:
            if state is False:
                count += 1
        print(count, " players playing")
        return count

    def game(self):
        """
        Handles the behavior for the game. Returns an integer, the id number of
        the player that won this game.
        """
        self.gameStarted = True

        playing = True
        while playing:
            playing = False

            turnOrder = self.turnOrderGenerator()
            for player in turnOrder:
                playing = True #dead-man's switch that breaks with no players
                score = None
                if player.id is 0:
                    card = self.deck.draw()
                    score = player.hit(card)
                else:
                    inp = ""
                    if player.ai is not None:
                        inp = player.useAI(self).lower()
                    else:
                        trying_again = True
                        query = "Player "+str(player.id)+": hit (h) or Stand (s)? "
                        while trying_again:
                            inp = input(query)
                            inp = inp.lower()
                            if (inp == "h" or inp == "hit" or inp == "s" or inp == "stand"):
                                trying_again = False
                    print(inp, inp == "hit")
                    if inp == "h" or inp == "hit":
                        card = self.deck.draw()
                        score = player.hit(card)
                    elif inp == "s" or inp == "stand":
                        player.stand()
                        score = -1
                if score == 21:
                    print("Player %d has hit Blackjack!" % player.id)
                    player.gameState["won"] = True
                    return player.id
                elif score > 21:
                    print("Player %d has busted!" % player.id)
                    self.tableState[player.id] = True
                elif score == -1:
                    self.tableState[player.id] = True

        self.postGame = True
        return self.confirmWinner()

    def confirmWinner(self):
        """
        Calculates and returns the ID of the winning player or else
        returns `-1` if the game ended in a draw.
        """

        isDraw = False
        max = (-2, -2)
        for i, player in enumerate(self.table):
            if player.hasBusted():
                continue
            if player.getScore() > max[1]:
                max = (i, player.getScore())
                isDraw = False
            elif player.getScore() == max[1]:
                isDraw = True
        if isDraw:
            print("It was a draw at a score of %d." % max[1])
            return -1
        elif max[1] == -2:
            print("It was a draw because all players busted.")
            return -2
        else:
            print("Player %d has won! They had a score of %d" % (max[0], max[1]))
            self.table[max[0]].gameState["won"] = True
            return max[0]

    def addPlayers(self, numOfPlayers=1):
        if self.gameStarted:
            return

        self.playerCount += numOfPlayers
        for i in range(numOfPlayers):
            self.table.append( BlackjackPlayer() )
            self.tableState.append(False)

        return self

    def addAgent(self, agent):
        new_player = BlackjackPlayer(agent)
        print(str(agent.__class__).upper())
        if isinstance(new_player.ai, QLearningAgent):
            trainer = LearningEnv(new_player.ai)
            trainer.teach()
            print(str(new_player.ai.isTrained()).upper())
        self.table.append(new_player)
        self.tableState.append(False)
        self.playerCount += 1
        return self

    def getDeckRemaining(self):
        """
        Returns a copy of the current state of the Deck
        """
        return self.deck.copyDeck()

    def getPlayer(id):
        """
        Returns Player with given 'id'
        """
        return this.table[id]

    def pullState(self, player):
        tup = (self.table[player].getScore(), self.table[player]._softScore, self.table[player].isStanding(), self.table[player].hasBusted(), self.table[player].hasWon())
        #print(tup)
        state = State._make(tup)
        return state

class LearningEnv(BlackjackGame):
    def __init__(self, agent=QLearningAgent(id=1)):
        super().__init__()
        self.learning_agent = agent
        self.addPlayers()

    def prepEpisode(self):
        """
        Preps a new episode and returns the inital state observation
        """
        for player in self.table:
            player.reset()
        for i in range( len(self.tableState) ):
            self.tableState[i] = False

        self.gameStarted = True
        agent_state = self.pullState(1)
        #other_state = self.pullState(0)
        return (agent_state, True)

    def endEpisode(self):
        self.deck.restartDeck()
        self.gameStarted = False

    def step(self, action):
        assert self.gameStarted

        agent_state = self.pullState(1)
        #other_state = self.pullState(0)
        turnOrder = self.turnOrderGenerator()
        id = 0
        for i in range(len(self.tableState)):
            if self.tableState[i] is False:
                id = i
                break

        for player in turnOrder:
            score = None
            if id is 0:
                inp = ""
                deck = self.getDeckRemaining()
                sum = 0
                for card in deck.cards:
                    sum += card.getScore()

                expected = sum / deck.getNumberOfCardsLeft()
                if player.getScore() + round(expected) > 21:
                    inp = "Stand"
                else:
                    inp = "Hit"
                inp = inp.lower()
                if inp == "h" or inp == "hit":
                    card = self.deck.draw()
                    score = player.hit(card)
                elif inp == "s" or inp == "stand":
                    player.stand()
                    score = -1
                #other_state = self.pullState(0)
            else:
                inp = str(action)
                inp = inp.lower()
                if inp == "h" or inp == "hit":
                    card = self.deck.draw()
                    score = player.hit(card)
                elif inp == "s" or inp == "stand":
                    player.stand()
                    score = -1
                agent_state = self.pullState(1)
            if score == 21:
                #print("Player %d has hit Blackjack!" % player.id)
                agent_state = self.pullState(1)
                #other_state = self.pullState(0)
                return (agent_state, False)
            elif score > 21:
                #print("Player %d has busted!" % id)
                self.tableState[id] = True
            elif score == -1:
                self.tableState[id] = True
            id += 1

        stillPlaying = self.playersStillPlaying() > 0
        if not stillPlaying:
            self.confirmWinner()

        return (agent_state, stillPlaying)

    def teach(self):
        reward_normalBustLoss = -5
        reward_normalStayLoss = -2
        reward_normalWin = 5

        for i in range(self.learning_agent.training_iterations):
            #print("Iteration %d" % i)
            env_state = self.prepEpisode()
            inEpisode = env_state[1]
            while inEpisode:
                #print("\tin episode")
                new_action = self.learning_agent.pickAction(env_state)
                new_state = self.step(new_action)
                deltaReward = 0

                if new_state[0].score == 21:
                    deltaReward += 20
                if new_state[0].hasBusted and not new_state[0].hasWon:
                    deltaReward += reward_normalBustLoss
                elif new_state[0].isStanding and not new_state[0].hasWon:
                    deltaReward += reward_normalStayLoss
                elif new_state[0].isStanding and new_state[0].hasWon:
                    deltaReward += reward_normalWin

                self.learning_agent.update(env_state, new_action, new_state, deltaReward)
                inEpisode = new_state[1]
            self.endEpisode()
        self.learning_agent.finishTraining()

def main():
    gam = BlackjackGame()

    playerNumber = input("How many players?")
    result = gam.addPlayers(int(playerNumber)).beginNewGame()

if __name__ == "__main__":
    main()
