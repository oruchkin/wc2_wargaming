from django.contrib import admin
from . models import User, Word, Query_name, Query_name_Words, Document

# Register your models here.

admin.site.register(User)
admin.site.register(Word)
admin.site.register(Query_name)
admin.site.register(Query_name_Words)
admin.site.register(Document)
