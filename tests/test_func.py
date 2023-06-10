"""test bot functions"""

import unittest
import praw
from helpers.func import (
    already_replied_submission,
    already_replied_comment,
    comment_is_user,
    keyword_in_comment,
    keyword_in_submission,
    comment_logic,
    submission_logic,
)
from bot import reddit, USERNAME
import helpers.general as general


class TestFunc(unittest.TestCase):
    """test bot functions"""

    def test_already_replied_submission(self):
        """test already replied submission with actual submissions"""
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
        """test already replied comment with actual comments"""
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
        """test comment is user with actual comments"""
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
        """test keyword in comment with actual comments"""
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
        """test keyword in submission with actual submissions"""
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

    def test_comment_logic(self):
        """test comment logic, using fake comments"""
        comment = praw.models.Comment
        custom_logic = general.try_load_config("tests/fixtures/custom.yaml")
        username = "suipiss"
        keyword = "suipiss"
        # test comment is self
        self.assertEqual(
            comment_logic(
                comment(reddit, "hywwf45"),
                username,
                keyword,
                custom_logic=custom_logic,
                debug=True,
            ),
            "comment is self",
        )
        # test comment already replied
        self.assertEqual(
            comment_logic(
                comment(reddit, "hz208fy"),
                username,
                keyword,
                custom_logic=custom_logic,
                debug=True,
            ),
            "already replied",
        )
        # test parent is user
        parent_comment = FakeComment(
            author=FakeRedditor(username),
        )
        fake_comment = FakeComment(
            author=FakeRedditor("not self"),
            parent_comment=parent_comment,
            replies=FakeCommentForest([]),
        )
        self.assertEqual(
            comment_logic(
                fake_comment,
                username,
                keyword,
                custom_logic=custom_logic,
                debug=True,
            ),
            "parent is self",
        )
        # test reply gratitude
        fake_comment.body = "thanks"
        self.assertEqual(
            comment_logic(
                fake_comment,
                username,
                keyword,
                custom_logic=custom_logic,
                debug=True,
            ),
            "replied",
        )
        # test custom
        parent_parent_comment = FakeComment(author=FakeRedditor(username))
        parent_comment.parent_comment = parent_parent_comment
        parent_comment.author = FakeRedditor("not self")
        # test B0tRank
        fake_comment.author = FakeRedditor("B0tRank")
        self.assertEqual(
            comment_logic(
                fake_comment,
                username,
                keyword,
                custom_logic=custom_logic,
                debug=True,
            ),
            "bot??? not bot",
        )
        # test pekofy_bot
        fake_comment.author = FakeRedditor("pekofy_bot")
        self.assertEqual(
            comment_logic(
                fake_comment,
                username,
                keyword,
                custom_logic=custom_logic,
                debug=True,
            ),
            "ok thanks pekofy_bot",
        )
        # test mentioned keyword
        parent_parent_comment.author = FakeRedditor("not self")
        fake_comment.body = keyword

        # test pekofy_bot reply mention
        self.assertEqual(
            comment_logic(
                fake_comment,
                username,
                keyword,
                custom_logic=custom_logic,
                debug=True,
            ),
            "suipiss peko",
        )
        # test reply
        fake_comment.author = FakeRedditor("not self")
        self.assertEqual(
            comment_logic(
                fake_comment,
                username,
                keyword,
                custom_logic=custom_logic,
                debug=True,
            ),
            "replied",
        )

    def test_submission_logic(self):
        """test submission logic, using fake submissions"""
        submission = praw.models.Submission
        username = "suipiss"
        keyword = "suipiss"
        # test already replied
        self.assertEqual(
            submission_logic(
                submission(reddit, "t48wjd"), username, keyword, debug=True
            ),
            "already replied",
        )
        # test reply submission from title
        fake_submission = FakeSubmission(title=keyword)
        self.assertEqual(
            submission_logic(fake_submission, username, keyword, debug=True),
            "replied",
        )
        # test reply submission from selftext
        fake_submission = FakeSubmission(selftext=keyword)
        self.assertEqual(
            submission_logic(fake_submission, username, keyword, debug=True),
            "replied",
        )


class FakeRedditor:
    """fake redditor class"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, string: str):
        return self.name == string


class FakeCommentForest:
    """fake comment forest class"""

    def __init__(self, comments):
        self.comments = comments

    def list(self):
        """return list of comments"""
        return self.comments

    def replace_more(self):
        """placeholder function"""
        return


class FakeComment:
    """fake comment class"""

    def __init__(
        self,
        author=None,
        body="",
        id=None,
        parent_comment=None,
        replies=[],
    ):
        self.author = author
        self.body = body
        self.id = id
        self.parent_comment = parent_comment
        self.replies = replies
        self.permalink = ""

    def parent(self):
        """return parent comment"""
        return self.parent_comment

    def refresh(self):
        """placeholder function"""
        return


class FakeSubmission:
    """fake submission class"""

    def __init__(
        self,
        author=None,
        comments=[],
        id=None,
        selftext="",
        title="",
    ):
        self.author = author
        self.comments = comments
        self.id = id
        self.selftext = selftext
        self.title = title
        self.permalink = ""


if __name__ == "__main__":
    unittest.main()
