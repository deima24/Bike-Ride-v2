from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Entry


class EntryList(generic.ListView):
    model = Entry
    queryset = Entry.objects.filter(status=1).order_by('-created_on')
    template_name = 'ride.html'
    paginate_by = 3


class EntryDetail(View):

    def get(self, request, slug, *args, **kwargs):

        queryset = Entry.objects.filter(status=1)
        entry = get_object_or_404(queryset, slug=slug)
        comments = entry.comments.filter(approved=True).order_by('created_on')  

        return render (
            request,
            "post_detail.html",
            {
                "entry": entry,
                "comments": comments,
            },
        )