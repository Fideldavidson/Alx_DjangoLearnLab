from django.shortcuts import render

# Create your views here.

def post_list(request):
    """View to display the list of all blog posts."""
    # This will render the template we created
    return render(request, 'blog/post_list.html', {})
