import markdown
from django import template
from timeline.models import Discussion
from timeline.utils.mentions import process_mentions

register = template.Library()


@register.filter(is_safe=False)
def covert_markdown(md):
    """
    Filter method that will convert a markdown
    string into html.
    """
    md = process_mentions(md)
    return markdown.markdown(md)


@register.filter(is_safe=True)
def entry_comments(entry_id):
    """
    Filter that returns the number of root
    comments that the entry has.
    """
    discussion = Discussion.objects.filter(entry=entry_id)
    return discussion.count()
