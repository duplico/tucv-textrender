from plasTeX import Command, Environment

class resentry(Command):
    args = '[indent] left right'

class ressubentry(Command):
    args = 'lefttext righttext'

class resentrysinglecol(Command):
    args = '[indent] text'

class ressubentrysinglecol(Command):
    args = 'text'

class resheading(Command):
    args = 'heading:str'

class resschool(Command):
    args = '[description] name location'

class resdegree(Command):
    args = '[description] degree major date'

class resemployer(Command):
    args = '[description] name'

class resjob(Command):
    args = '[description] title startdate enddate'

class resconference(Command):
    args = '[description] name role'

class ressubconference(Command):
    args = '[description] name role'

class resdesc(Command):
    args = 'item description'

class resbib(Command):
    args = 'title'