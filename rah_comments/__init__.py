from threadedcomments.models import ThreadedComment

from forms import RahCommentForm

def get_model():
    return ThreadedComment

def get_form():
    return RahCommentForm
