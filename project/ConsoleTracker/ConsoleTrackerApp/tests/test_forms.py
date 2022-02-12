from django.test import SimpleTestCase
from ..forms import NameForm

'''
    Testing NameForm Variations
    uname - [forms.CharField], Max Length = 50
    pword - [forms.CharField], Max Length = 50

    +--------+----------+----------+
    |        | uname    | pword    |
    +--------+----------+----------+
    | Case 1 | valid    | valid    |
    +--------+----------+----------+
    | Case 2 | invalid  | invalid  |
    +--------+----------+----------+
    | Case 3 | invalid  | valid    |
    +--------+----------+----------+
    | Case 4 | valid    | invalid  |
    +--------+----------+----------+
    | Case 5 | len > 50 |  valid   |
    +--------+----------+----------+
    | Case 6 | valid    | len > 50 |
    +--------+----------+----------+
'''


class TestForms(SimpleTestCase):

    def test_name_form_valid_data(self):
        form = NameForm(data={
            'uname': 'chris',
            'pword': 'dhden38&&'
        })

        self.assertTrue(form.is_valid())

    def test_name_form_no_data(self):
        form = NameForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_name_form_some_data(self):
        form = NameForm(data={'uname': 'chris'})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = NameForm(data={'pword': 'dhden38&&'})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_name_form_constraints(self):
        form = NameForm(data={
            'uname': 'chrischrischrischrischrischrischrischrischrischrisa',
            'pword': 'dhden38&&'
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = NameForm(data={
            'uname': 'chris',
            'pword': 'chrischrischrischrischrischrischrischrischrischrisa'
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = NameForm(data={
            'uname': 'chrischrischrischrischrischrischrischrischrischris',
            'pword': 'chrischrischrischrischrischrischrischrischrischris'
        })

        self.assertTrue(form.is_valid())
