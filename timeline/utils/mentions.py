import re
from django.urls import reverse
from core.models import User
from timeline.models import TimelineEntry
from timeline.utils.notifications.helpers import push_notification

MENTION_REGEX = '\@([a-zA-z0-9]+)'


def process_mentions(comment):
    """
    Processes any @ mentions into valid markdown to become urls

    Arguments:
        comment     String comment from user

    Return:
        original comment with url markdown
    """
    if comment is None:
        raise ValueError("comment cannot be None")

    # enusre only strings are processed
    if not isinstance(comment, str):
        raise ValueError("comment must be of type string")

    if len(comment) < 1:
        return comment

    pattern = re.compile(MENTION_REGEX)

    # turn comment into space seperated array
    comment = re.findall(r'\S+|\n', comment)

    # loop through each word, if it is a mention
    # then get the user and create the url
    for index, value in enumerate(comment):
        if pattern.match(value) is not None:
            try:
                user = User.objects.get(username=value[1:])
                url = reverse('user_profile', kwargs={'pk': user.pk})

                # replace current value with the url
                comment[index] = "[{}]({})".format(value, url)
            except User.DoesNotExist:
                pass

    # assemble the mesage back together
    return ' '.join(map(str, comment))


def extract_mentions(comment, author_username=''):
    """
    Extracts all of the usernames that are mention from a comment.

    Arguments:
        comment             users comment that could include mentions.
        author_username     username of the author of the comment.

    Return:
        list of usernames that were mentioned. Removes author's
        username if that was mentioned.
    """
    if not isinstance(comment, str):
        raise ValueError("comment is expected to be a string")

    if not isinstance(author_username, str):
        raise ValueError("author username is expected to be a string")

    # extract all of the mentions from the comment
    pattern = re.compile(MENTION_REGEX)
    mentions = pattern.findall(comment)

    # remove any trace of the user who wrote the comment
    # from being mentioned in their own comment
    return [u for u in mentions if u != author_username]


def push_mention_notifications(mentions, comment_author, entry):
    """
    Wrapper function that will handle mentions and notifications
    in one operation.

    Arguments:
        mentions            list of usernames, such as ['ryan', 'test']
                            or is a string, such as "@ryan hello world".

        comment_author      author that created the comment that will
                            trigger the notifications.

        entry               timeline entry for this comment

    Return:
        number of mentions it has seen
    """
    # only allow strings and lists to be processed
    if not isinstance(mentions, str) and not isinstance(mentions, list):
        raise ValueError(
            "Expected a list or string for mentions"
        )

    # ensure only users are processed
    if not isinstance(comment_author, User):
        raise ValueError("comment author expects a core:User type")

    # ensure only timeline entires are processed
    if not isinstance(entry, TimelineEntry):
        raise ValueError("entry expects TimelineEntry type")

    # if empty, automatically return o
    if len(mentions) < 1:
        return 0

    username = comment_author.username

    # if mentions is a string, then process to extract usernames
    if isinstance(mentions, str):
        # extract mentions from comment
        mentions = extract_mentions(mentions, username)

    # loop through each mention username and push
    # a notification to them.
    for m in mentions:
        try:
            user = User.objects.get(username=m)
            push_notification(
                'mention',
                author=comment_author,
                entry=entry,
                mention=user
            )
        except User.DoesNotExist:
            pass
    return len(mentions)
