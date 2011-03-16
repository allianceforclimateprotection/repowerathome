from django import forms

from threadedcomments.forms import ThreadedCommentForm

COMMENT_TYPES = (
    ('T', 'Tip/Idea',),
    ('Q', 'Question',),
    ('C', 'Comment',),
)

class RahCommentForm(ThreadedCommentForm):
    def __init__(self, target_object, parent=None, data=None, initial=None):
        require_message_type = not bool(parent or (data and data['parent']))
        self.base_fields.insert(
                self.base_fields.keyOrder.index('comment'), 'message_type',
                forms.ChoiceField(choices=COMMENT_TYPES, widget=forms.RadioSelect,
                    required=require_message_type)
            )
        super(RahCommentForm, self).__init__(target_object, parent=parent, data=data, initial=initial)

    def clean(self):
        if self.cleaned_data['parent']:
            self.cleaned_data['message_type'] = u'C'
        return super(RahCommentForm, self).clean()

    def get_comment_create_data(self):
        d = super(RahCommentForm, self).get_comment_create_data()
        d['parent_id'] = self.cleaned_data['parent']
        d['title'] = self.cleaned_data['message_type']
        return d
