import numpy as np
import time

_KEY_CHOICE = 'choice'

# Create a private variable to store the default values of player
_PLAYER_DEFAULT_VALUES = {
    _KEY_CHOICE: None
}

_CHOICE_ROCK = 'ROCK'
_CHOICE_PAPER = 'PAPER'
_CHOICE_SCISSOR = 'SCISSOR'


def getRock():
    return _CHOICE_ROCK


def getPaper():
    return _CHOICE_PAPER


def getScissors():
    return _CHOICE_SCISSOR


class RockPaperScissor:
    def __init__(self):
        self._players = {}
        self._number_of_players = 0

    # ******************* #
    # ***** SETTERS ***** #
    # ******************* #
    def setPlayers(self, how_many: int = 2):
        if how_many < 2:
            print('Acceptable value >= 2. Can\'t have a game with 1 or less players!')
            return False
        else:
            self._number_of_players = how_many
            for _p_index_ in range(how_many):
                self._players['player_' + str(_p_index_)] = _PLAYER_DEFAULT_VALUES.copy()

    def setChoiceForPlayerIndex(self, index: int, choice: str):
        playerName = 'player_' + str(index)
        if playerName in self._players.keys():
            if choice in [_CHOICE_ROCK, _CHOICE_PAPER, _CHOICE_SCISSOR]:
                self._players[playerName][_KEY_CHOICE] = choice
            else:
                print('Not Defined value a randomized value will be set')
                self._players[playerName][_KEY_CHOICE] = self.getRandomChoice()

    def setRandomChoiceForPLayerIndex(self, index):
        playerName = 'player_' + str(index)
        if playerName in self._players.keys():
            self._players[playerName][_KEY_CHOICE] = self.getRandomChoice()

    # ******************* #
    # ***** GETTERS ***** #
    # ******************* #
    @staticmethod
    def getRandomChoice():
        choiceList = [_CHOICE_ROCK, _CHOICE_PAPER, _CHOICE_SCISSOR]
        index = np.random.randint(301) % 3
        time.sleep(np.random.randint(11) * 0.2)
        return choiceList[index]

    @staticmethod
    def getScore(choice_1, choice_2):
        if choice_1 == _CHOICE_ROCK:  # ROCK
            if choice_2 == _CHOICE_PAPER:  # PAPER = L
                return -1
            elif choice_2 == _CHOICE_SCISSOR:  # SCISSOR = W
                return 1
        elif choice_1 == _CHOICE_PAPER:  # PAPER
            if choice_2 == _CHOICE_SCISSOR:  # SCISSOR = L
                return -1
            elif choice_2 == _CHOICE_ROCK:  # ROCK = W
                return 1
        elif choice_1 == _CHOICE_SCISSOR:  # SCISSOR
            if choice_2 == _CHOICE_ROCK:  # ROCK = L
                return -1
            elif choice_2 == _CHOICE_PAPER:  # PAPER = W
                return 1
        return 0  # SAME OPTION

    def getResults(self):
        playerNameList = []
        # Error checking
        for _playerName_ in self._players.keys():
            if self._players[_playerName_][_KEY_CHOICE] is None:
                print(_playerName_ + ' is not ready!')
                return False
            playerNameList.append(_playerName_)

        # Create score board and score list
        score_board = np.zeros((self._number_of_players, self._number_of_players))
        scoreList = []
        for _p_index1_ in range(self._number_of_players):
            for _p_index2_ in range(_p_index1_ + 1, self._number_of_players):
                player_1 = playerNameList[_p_index1_]
                player_2 = playerNameList[_p_index2_]
                score = self.getScore(self._players[player_1][_KEY_CHOICE],
                                      self._players[player_2][_KEY_CHOICE])
                score_board[_p_index1_][_p_index2_] = score
                score_board[_p_index2_][_p_index1_] = -score
            tmp_app = [playerNameList[_p_index1_],
                       self._players[playerNameList[_p_index1_]][_KEY_CHOICE],
                       _p_index1_,
                       sum(score_board[_p_index1_])]
            scoreList.append(tmp_app)
        scoreList = sorted(scoreList, key=lambda x: x[3])
        scoreList.reverse()
        # print(score_board)
        # print(score_list)
        return scoreList

    def getChoiceOfPlayerIndex(self, index):
        playerName = 'player_' + str(index)
        if playerName in self._players.keys():
            return self._players[playerName][_KEY_CHOICE]
        return None


if __name__ == '__main__':
    rps = RockPaperScissor()
    rps.setPlayers(how_many=5)
    for _index_ in range(5):
        rps.setRandomChoiceForPLayerIndex(_index_)
    score_list = rps.getResults()
    for _score_ in score_list:
        print(_score_)
