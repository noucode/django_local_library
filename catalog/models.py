from django.db import models
from django.urls import reverse 	#Used to generate URLs by reversing the URL patterns
import uuid 				# Required for unique book instances

class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id       = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book     = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    imprint  = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]
        
    def __str__(self):
        """
        String for representing the Model object
        """
        return f'{self.id} ({self.book.title})'
	       

class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title   = models.CharField(max_length=200)
    genre   = models.ManyToManyField(Genre, help_text='Select a genre for this book')   # Genre specified as object because it is defined in this file before it is referenced.
    author  = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)         # Author as a string rather than object because not defined yet in the file.
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn    = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title
    
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this book.
        """
        return reverse('book-detail', args=[str(self.id)])


class Author(models.Model):
    """
    Model representing an author.
    """
    first_name 	  = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ["last_name","first_name"]
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0}, {1}'.format(self.last_name,self.first_name)