from django import forms
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django.core.exceptions import ValidationError

from tiles.models import BLOCK_MODE_CHOICES
from tiles.models import BLOCK_SECTOR_CHOICES
from tiles.models import Tile
from tiles.rand import get_random_questions

class writeRequestDataForm(forms.Form):
    block_mode = forms.ChoiceField(choices=BLOCK_MODE_CHOICES)
    block_total_questions = forms.IntegerField(initial=40)
    sector = forms.ChoiceField(choices=BLOCK_SECTOR_CHOICES)
    timed = forms.BooleanField(required=False)

    def __init__ (self, *args, **kwargs):
        self.questions_queryset = kwargs.pop('questions_queryset', None)
        super().__init__(*args, **kwargs)

    def clean_block_total_questions(self):  
        print(self.questions_queryset)    
        self.random_questions = get_random_questions(self.questions_queryset, 
                                   self.cleaned_data['block_total_questions'])
        if self.random_questions is None:
            raise ValidationError('Not Enough Questions in Database', code='invalid')
        else:
            return self.cleaned_data['block_total_questions']
        
class SubTileBooleanForm(forms.ModelForm):
    is_selected = forms.BooleanField(required=False, label='')

    class Meta:
        model = Tile
        exclude = '__all__'
    
InlineSubTilesListFormSet = inlineformset_factory(Tile, Tile,
                                                  form=SubTileBooleanForm,
                                                #   fk_name='to_tile',
                                                  fields = [],
                                                  can_delete=False,
                                                  extra=0)

class PersonalQueryQuestionsForm(forms.Form):

    personal_filter_choices = (
        ('unseen', 'unseen'),
        ('mistakes', 'mistakes'),
        ('omitted', 'omitted'),
        ('correct', 'correct')
    )

    personal_filter = forms.MultipleChoiceField(choices=personal_filter_choices,
                                                  required=False)

PersonalFormset = formset_factory(PersonalQueryQuestionsForm)

#### Tile Create Form #####

class TileCreateForm(forms.ModelForm):
    class Meta:
        model = Tile
        fields = ['tile_headline', 'type_of_tile_char', 'parent']
