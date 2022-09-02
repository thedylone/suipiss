import unittest
from bot import (
    praw,
    try_import_messages,
    assign_random_weights,
    already_replied_submission,
    already_replied_comment,
    comment_is_self,
    keyword_in_comment,
    keyword_in_submission,
)
import bot


class TestBot(unittest.TestCase):
    def test_try_import_messages(self):
        # test multiple lines
        self.assertEqual(
            try_import_messages("tests/fixtures/multiple.txt"),
            ["a", "b", "c", "d", "e"],
        )
        # test single line
        self.assertEqual(
            try_import_messages("tests/fixtures/single.txt"),
            ["a"],
        )
        # test empty
        self.assertEqual(
            try_import_messages("tests/fixtures/empty.txt"),
            ["suipiss"],
        )
        # test invalid path
        self.assertEqual(
            try_import_messages(""),
            ["suipiss"],
        )
        # test default message
        self.assertEqual(
            try_import_messages("tests/fixtures/empty.txt", "test"),
            ["test"],
        )

    def test_assign_random_weights(self):
        # test multiple items
        self.assertEqual(
            assign_random_weights(["a", "b", "c", "d", "e"]),
            [
                0.5,
                0.125,
                0.125,
                0.125,
                0.125,
            ],
        )
        # test single item
        self.assertEqual(
            assign_random_weights(["a"]),
            [1],
        )
        # test empty
        self.assertEqual(
            assign_random_weights([]),
            [],
        )

    def test_already_replied_submission(self):
        submission = praw.models.Submission
        # test already replied
        self.assertTrue(
            already_replied_submission(submission(bot.reddit, "t48wjd"))
        )
        # test already replied (deleted submission)
        self.assertTrue(
            already_replied_submission(submission(bot.reddit, "x0pc6n"))
        )
        # test not replied (many replied comments)
        self.assertFalse(
            already_replied_submission(submission(bot.reddit, "x25v00"))
        )

    def test_already_replied_comment(self):
        comment = praw.models.Comment
        # test already replied
        self.assertTrue(
            already_replied_comment(comment(bot.reddit, "hz208fy"))
        )
        # test already replied (deleted comment)
        self.assertTrue(
            already_replied_comment(comment(bot.reddit, "i307ztm"))
        )
        # test not replied (top level)
        self.assertFalse(
            already_replied_comment(comment(bot.reddit, "hywwnfq"))
        )

    def test_comment_is_self(self):
        comment = praw.models.Comment
        # test comment is self
        self.assertTrue(comment_is_self(comment(bot.reddit, "hywwf45")))
        # test comment parent is self
        self.assertTrue(comment_is_self(comment(bot.reddit, "icgxdy9"), 1))
        # test comment parent parent is self
        self.assertTrue(comment_is_self(comment(bot.reddit, "ilzt04v"), 2))
        # test comment not self
        self.assertFalse(comment_is_self(comment(bot.reddit, "icgxdy9")))
        # test comment parent not self
        self.assertFalse(comment_is_self(comment(bot.reddit, "ilzt04v"), 1))
        # test top comment parent
        self.assertFalse(comment_is_self(comment(bot.reddit, "icgx9xu"), 1))
        # test top comment parent parent
        self.assertFalse(comment_is_self(comment(bot.reddit, "icgx9xu"), 2))

    def test_keyword_in_comment(self):
        comment = praw.models.Comment
        # test keyword in comment
        self.assertTrue(
            keyword_in_comment(comment(bot.reddit, "hywy79s"), "suipiss")
        )
        # test one of keywords in comment
        self.assertTrue(
            keyword_in_comment(
                comment(bot.reddit, "icgxdy9"), *["thank", "good", "love"]
            )
        )
        # test keyword not in comment
        self.assertFalse(
            keyword_in_comment(comment(bot.reddit, "hywwnfq"), "suipiss")
        )
        # test none of keywords in comment
        self.assertFalse(
            keyword_in_comment(
                comment(bot.reddit, "hywwnfq"), *["thank", "good", "love"]
            )
        )

    def test_keyword_in_submission(self):
        submission = praw.models.Submission
        # test keyword in title
        self.assertTrue(
            keyword_in_submission(submission(bot.reddit, "t48wjd"), "suipiss")
        )
        # test keyword in body
        self.assertTrue(
            keyword_in_submission(submission(bot.reddit, "to9vpu"), "suipiss")
        )
        # test no keyword
        self.assertFalse(
            keyword_in_submission(submission(bot.reddit, "tzry2q"), "suipiss")
        )


if __name__ == "__main__":
    unittest.main()
