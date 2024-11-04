from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.models import Blog


class BlogCreateView(CreateView):
    """
    Создает новую публикацию блога
    """

    model = Blog
    fields = (
        "title",
        "content",
        "preview",
        "is_published",
    )
    success_url = reverse_lazy("blog:blog_list")

    def form_valid(self, form):
        """
        Проверяет данные на валидность и генерирует slug
        """
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    """
    Обновляет публикацию блога
    """

    model = Blog
    fields = (
        "title",
        "content",
        "preview",
        "is_published",
    )
    success_url = reverse_lazy("blog:blog_list")

    def get_success_url(self):
        return reverse_lazy("blog:blog_view", args=[self.object.pk])


class BlogListView(ListView):
    """
    Получает все публикации блога
    """

    model = Blog

    def get_queryset(self, *args, **kwargs):
        """
        Получает все публикации блога, которые опубликованы
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        """
        Получает публикацию блога с увеличением числа просмотров
        """
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogDeleteView(DeleteView):
    """
    Удаляет публикацию блога
    """

    model = Blog
    success_url = reverse_lazy("blog:blog_list")
