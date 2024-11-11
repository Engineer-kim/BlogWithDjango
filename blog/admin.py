from django.contrib import admin

from blog.models import Author ,Post ,Tag , Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_filter = ("author" , "date" , "tags")
    list_display = ("title" , "date" , "author" )
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    list_filter = ("user_name",  "post")



admin.site.register(Post , PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment ,CommentAdmin)
