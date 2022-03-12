from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_count = 0
        for form in self.forms:
            if is_main_count > 1:
                break
            data = form.cleaned_data
            if not data:
                continue
            if data['is_main']:
                is_main_count += 1
        if is_main_count == 0:
            raise ValidationError('Выберите основной раздел')
        elif is_main_count > 1:
            raise ValidationError('Основной раздел может быть только один')
        return super().clean()






class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'published_at', 'image']
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ['article', 'tag', 'is_main']
