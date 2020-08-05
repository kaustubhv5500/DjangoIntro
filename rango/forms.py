from django import forms
from rango.models import Page,Category,UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,help_text="Enter the category name")
    views = forms.IntegerField(widget = forms.HiddenInput(),initial = 0)
    likes = forms.IntegerField(widget = forms.HiddenInput(),initial = 0)
    slug = forms.CharField(widget= forms.HiddenInput(),required=False)

    class Meta:
        model = Category
        fields = ('name',)  #inline class to provide an association between model form and an already existing model


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,help_text="Enter the title")
    url = forms.URLField(max_length = 200,help_text="Enter the URL of the page")
    views = forms.IntegerField(widget = forms.HiddenInput(),initial = 0)

    def clean(self):
        cleaned_data = self.cleaned_data  # ModelForm has the attribute cleaned_data which is being manipulated : Dict
        url = cleaned_data.get('url')    # .get() of a dict to get values

        if url and not url.startswith('http://'):
            url = "http://" + url
            cleaned_data['url'] = url

        return cleaned_data   
        # basically getting the cleaned input from the site and furthur cleaning it to change it to the proper format

    class Meta:
        exclude = ('category',)
        model = Page
        #to specify the fields which need to be included use the tuple(fields(...))


class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password',)

class UserProfileForm(forms.ModelForm):
        class Meta:
            model = UserProfile
            fields = ('website','picture',)