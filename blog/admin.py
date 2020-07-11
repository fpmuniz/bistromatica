from django.contrib import admin

from blog.models import Post, Thread

# Register your models here.
class PostAdmin(admin.ModelAdmin):
	pass


class ThreadAdmin(admin.ModelAdmin):
	pass


admin.site.register(Post, PostAdmin)
admin.site.register(Thread, ThreadAdmin)
