import unittest
import praw
from helpers.func import (
    already_replied_submission,
    already_replied_comment,
    comment_is_user,
    keyword_in_comment,
    keyword_in_submission,
)
from bot import reddit, USERNAME


class TestFunc(unittest.TestCase):
    def test_already_replied_submission(self):
        submission = praw.models.Submission
        # test already replied
        self.assertTrue(
            already_replied_submission(submission(reddit, "t48wjd"), USERNAME)
        )
        # test already replied (deleted submission)
        self.assertTrue(
            already_replied_submission(submission(reddit, "x0pc6n"), USERNAME)
        )
        # test not replied (many replied comments)
        self.assertFalse(
            already_replied_submission(submission(reddit, "x25v00"), USERNAME)
        )

    def test_already_replied_comment(self):
        comment = praw.models.Comment
        # test already replied
        self.assertTrue(
            already_replied_comment(comment(reddit, "hz208fy"), USERNAME)
        )
        # test already replied (deleted comment)
        self.assertTrue(
            already_replied_comment(comment(reddit, "i307ztm"), USERNAME)
        )
        # test not replied (top level)
        self.assertFalse(
            already_replied_comment(comment(reddit, "hywwnfq"), USERNAME)
        )

    def test_comment_is_user(self):
        comment = praw.models.Comment
        # test comment is self
        self.assertTrue(comment_is_user(comment(reddit, "hywwf45"), USERNAME))
        # test comment parent is self
        self.assertTrue(
            comment_is_user(comment(reddit, "icgxdy9"), USERNAME, 1)
        )
        # test comment parent parent is self
        self.assertTrue(
            comment_is_user(comment(reddit, "ilzt04v"), USERNAME, 2)
        )
        # test comment not self
        self.assertFalse(comment_is_user(comment(reddit, "icgxdy9"), USERNAME))
        # test comment parent not self
        self.assertFalse(
            comment_is_user(comment(reddit, "ilzt04v"), USERNAME, 1)
        )
        # test top comment parent
        self.assertFalse(
            comment_is_user(comment(reddit, "icgx9xu"), USERNAME, 1)
        )
        # test top comment parent parent
        self.assertFalse(
            comment_is_user(comment(reddit, "icgx9xu"), USERNAME, 2)
        )

    def test_keyword_in_comment(self):
        comment = praw.models.Comment
        # test keyword in comment
        self.assertTrue(
            keyword_in_comment(comment(reddit, "hywy79s"), "suipiss")
        )
        # test one of keywords in comment
        self.assertTrue(
            keyword_in_comment(
                comment(reddit, "icgxdy9"), *["thank", "good", "love"]
            )
        )
        # test keyword not in comment
        self.assertFalse(
            keyword_in_comment(comment(reddit, "hywwnfq"), "suipiss")
        )
        # test none of keywords in comment
        self.assertFalse(
            keyword_in_comment(
                comment(reddit, "hywwnfq"), *["thank", "good", "love"]
            )
        )

    def test_keyword_in_submission(self):
        submission = praw.models.Submission
        # test keyword in title
        self.assertTrue(
            keyword_in_submission(submission(reddit, "t48wjd"), "suipiss")
        )
        # test keyword in body
        self.assertTrue(
            keyword_in_submission(submission(reddit, "to9vpu"), "suipiss")
        )
        # test no keyword
        self.assertFalse(
            keyword_in_submission(submission(reddit, "tzry2q"), "suipiss")
        )


if __name__ == "__main__":
    unittest.main()
