from django.shortcuts import render, redirect, get_object_or_404
from .forms import SupportRequestForm
from .models import SupportRequest

def index(request):
    # Show form + existing requests
    if request.method == "POST":
        form = SupportRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("support_success")
    else:
        form = SupportRequestForm()

    requests = SupportRequest.objects.all().order_by("-created_at")  # latest first
    return render(request, "user_support/index.html", {"form": form, "requests": requests})


def support_success(request):
    return render(request, "user_support/success.html")



def ticket_detail(request, pk):
    ticket = get_object_or_404(SupportRequest, pk=pk)
    return render(request, 'user_support/ticket_detail.html', {'ticket': ticket})
