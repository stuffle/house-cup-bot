import bot
import unittest

sample_user_data = {
    'name': 'aname',
    'mention': '<@111111111111111111>',
    'house': 'hufflepuff',
    'last_daily': 1555433597.4030607,
    'last_workshop': 0,
    'word_count': 0,
    'daily': 10,
    'post': 30,
    'beta': 0,
    'workshop': 0,
    'comment': 1,
    'excred': 0,
    'wc': 0,
    'mod_adjust': 0,
    'art': 0
}


class TestLogScore(unittest.TestCase):

    def setUp(self):
        bot.participants = {
            "123": sample_user_data
        }

    def test_valid(self):
        self.assertIsNotNone(bot.log_score("~log daily", "123"))
        self.assertIsNotNone(bot.log_score("~log post", "123"))
        self.assertIsNotNone(bot.log_score("~log beta", "123"))
        # TODO: Uncomment art in May
        # self.assertIsNotNone(bot.log_score("~log art 10", "123"))
        self.assertIsNotNone(bot.log_score("~log workshop", "123"))
        self.assertIsNotNone(bot.log_score("~log exercise", "123"))
        self.assertIsNotNone(bot.log_score("~log comment", "123"))
        self.assertIsNotNone(bot.log_score("~log comment extra", "123"))
        self.assertIsNotNone(bot.log_score("~log excred 10", "123"))
        self.assertIsNotNone(bot.log_score("~log wc 2000", "123"))
        self.assertIsNotNone(bot.log_score("~log wc add 2000", "123"))

    def test_invalid(self):
        with self.assertRaises(bot.HouseCupException):
            bot.log_score("~log wc", "123")
        with self.assertRaises(bot.HouseCupException):
            bot.log_score("~log excred", "123")


class TestRemoveScore(unittest.TestCase):

    def setUp(self):
        bot.participants = {
            "123": sample_user_data
        }

    def test_valid(self):
        self.assertIsNotNone(bot.remove_score("~remove daily", "123"))
        self.assertIsNotNone(bot.remove_score("~remove post", "123"))
        self.assertIsNotNone(bot.remove_score("~remove beta", "123"))
        # TODO: Uncomment art in May
        # self.assertIsNotNone(bot.remove_score("~remove art 10", "123"))
        self.assertIsNotNone(bot.remove_score("~remove workshop", "123"))
        self.assertIsNotNone(bot.remove_score("~remove exercise", "123"))
        self.assertIsNotNone(bot.remove_score("~remove comment", "123"))
        self.assertIsNotNone(bot.remove_score("~remove comment extra", "123"))
        self.assertIsNotNone(bot.remove_score("~remove excred 10", "123"))

    def test_invalid(self):
        with self.assertRaises(bot.HouseCupException):
            bot.remove_score("~remove wc 2000", "123")
        with self.assertRaises(bot.HouseCupException):
            bot.remove_score("~remove excred", "123")
        with self.assertRaises(bot.HouseCupException):
            bot.remove_score("~remove art", "123")


class TestStandings(unittest.TestCase):

    def setUp(self):
        bot.participants = {
            "111111111111111111": sample_user_data
        }

    def test_runs(self):
        self.assertIsNotNone(bot.standings())


class TestLeaderboard(unittest.TestCase):

    def setUp(self):
        bot.participants = {
            "111111111111111111": sample_user_data
        }

    def test_valid(self):
        self.assertIsNotNone(bot.leader_board("leaderboard"))
        self.assertIsNotNone(bot.leader_board("leaderboard post"))
        self.assertIsNotNone(bot.leader_board("leaderboard beta"))
        self.assertIsNotNone(bot.leader_board("leaderboard daily"))
        # TODO: self.assertIsNotNone(bot.leader_board("leaderboard art"))
        self.assertIsNotNone(bot.leader_board("leaderboard workshop"))
        self.assertIsNotNone(bot.leader_board("leaderboard comment"))
        self.assertIsNotNone(bot.leader_board("leaderboard excred"))
        self.assertIsNotNone(bot.leader_board("leaderboard wc"))
        self.assertIsNotNone(bot.leader_board("leaderboard word_count"))
        self.assertIsNotNone(bot.leader_board("leaderboard mod_adjust"))
        self.assertIsNotNone(bot.leader_board("leaderboard total"))

    def test_invalid(self):
        with self.assertRaises(bot.HouseCupException):
            bot.leader_board("leaderboard invalid")


class TestWinnings(unittest.TestCase):

    def setUp(self):
        bot.participants = {
            "111111111111111111": sample_user_data
        }

    def test_valid(self):
        msg1, msg2 = bot.winnings()
        self.assertIsNotNone(msg1)
        self.assertIsNotNone(msg2)


if __name__ == '__main__':
    unittest.main()
