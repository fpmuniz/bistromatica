from django.contrib import admin

from blog.models import Post, Thread, ThreadItem

# Register your models here.


class ThreadItemInLine(admin.TabularInline):
	model = ThreadItem


class PostAdmin(admin.ModelAdmin):
	inlines = (ThreadItemInLine,)


class ThreadAdmin(admin.ModelAdmin):
	inlines = (ThreadItemInLine,)


admin.site.register(Post, PostAdmin)
admin.site.register(Thread, ThreadAdmin)
