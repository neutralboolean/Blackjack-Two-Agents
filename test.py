from game import BlackjackGame, BlackjackPlayer
from agents import QLearningAgent, ExpectimaxAgent
import pprint

class TestGame:
    def __init__(self, game = BlackjackGame(), numberTests=100):
        super().__init__()
        self.game = game
        self.number_of_tests = numberTests
        self.result_table = dict()
        for i in range(-2,1):
            self.result_table[i] = 0
            i += 1

    def fullTest(self):
        self.game.addAgent( ExpectimaxAgent(BlackjackPlayer.id) )
        self.result_table[1] = 0
        self.game.addAgent( QLearningAgent(BlackjackPlayer.id) )
        self.result_table[2] = 0
        self.doTests()

    def testExpectimax(self):
        self.game.addAgent( ExpectimaxAgent(BlackjackPlayer.id) )
        self.result_table[1] = 0
        self.doTests()

    def testQLearn(self):
        self.game.addAgent( QLearningAgent(BlackjackPlayer.id) )
        self.result_table[1] = 0
        self.doTests()
        #pprint.pprint(self.game.table[1].ai.qValues)

    def doTests(self):
        for i in range(self.number_of_tests):
            result = self.game.beginNewGame()
            self.result_table[result] += 1

        print(self.result_table.keys())
        for player in self.result_table.keys():
            self.readPercentage(player)

    def readPercentage(self, player):
        wins = self.result_table[player]
        decimal = wins / self.number_of_tests
        ai = self.game.table[player].ai
        if player == 0:
            print("Dealer won %d%% of games." % (decimal*100))
        elif player == -2:
            print("Players busted, reaching a draw in %0.4f%% of games." % (decimal*100))
        elif player == -1:
            print("Players reached a draw in %0.4f%% of games." % (decimal*100))
        elif player == None:
            print("Error?3!223## Test won %0.4f%% of games.\n" % (decimal*100))
        elif isinstance(ai, ExpectimaxAgent):
            print("Player %d (Expectimax) won %0.4f%% of games." % (player, decimal*100))
        elif isinstance(ai, QLearningAgent):
            print("Player %d (Q-Learner) won %0.4f%% of games." % (player, decimal*100))

def main():
    test = TestGame(numberTests=1000)
    inp = input("Perform which test?\n\t1. Full test\n\t2. Test Expectimax agent\n\t3. Test Q-Learning agent\nTest: ")

    if inp is "1":
        test.fullTest()
    elif inp is "2":
        test.testExpectimax()
    elif inp is "3":
        test.testQLearn()

if __name__ == "__main__":
    main()
