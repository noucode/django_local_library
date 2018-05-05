from django.views import generic
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

def index(request):
    """
    View function for home page of site.
    """
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'catalog/index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/bookdetail.html'  		

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'booklist25'   		# your own name for the list as a template variable
    template_name = 'catalog/booklist.html'  		# Specify your own template name/location
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.order_by('-title')[:25] 	# Get first 25 books

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/authordetail.html'  		

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'authorlist'   		# your own name for the list as a template variable
    template_name = 'catalog/authorlist.html'  		# Specify your own template name/location
    paginate_by = 10

    def get_queryset(self):
        return Author.objects.all() 			# Get all books




