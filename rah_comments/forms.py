from django import forms

from threadedcomments.forms import ThreadedCommentForm

COMMENT_TYPES = (
    ('T', 'Tip/Idea',),
    ('Q', 'Question',),
    ('C', 'Comment',),
)

class RahCommentForm(ThreadedCommentForm):
    def __init__(self, target_object, parent=None, data=None, initial=None):
        self.base_fields.insert(
                self.base_fields.keyOrder.index('comment'), 'message_type',
                forms.ChoiceField(choices=COMMENT_TYPES, widget=forms.RadioSelect)
            )
        self.parent = parent
        if initial is None:
            initial = {}
        initial.update({'parent': self.parent})
        super(RahCommentForm, self).__init__(target_object, data=data, initial=initial)

    def get_comment_create_data(self):
        d = super(RahCommentForm, self).get_comment_create_data()
        d['parent_id'] = self.cleaned_data['parent']
        d['title'] = self.cleaned_data['message_type']
        return d
