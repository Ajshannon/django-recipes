from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import reverse

from djangoforms.models import Recipe, Author
from djangoforms.forms import AddRecipe, AddAuthor, SignupForm, LoginForm


def all_recipes(request):
    html = 'all_recipes.html'
    recipes = Recipe.objects.all()
    user = request.user
    return render(request, html, {'data': {
        'recipes': recipes,
        'user': user,
    }})


def recipe(request, recipe_id):
    results = Recipe.objects.filter(id=recipe_id).first()
    return render(request, 'recipe.html', {'data': results})


def author(request, author_id):
    author = Author.objects.filter(id=author_id).first()
    recipes = Recipe.objects.filter(author=author)
    return render(request, 'author.html', {'data': {
        'author': author,
        'recipes': recipes,
    }})


@login_required()
def add_recipe(request):
    html = 'add_recipe.html'
    form = None
    if request.method == 'POST':
        form = AddRecipe(request.user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data['title'],
                body=data['body'],
                author=Author.objects.filter(id=data['author']).first(),
            )
            return render(request, 'thanks.html')
    else:
        form = AddRecipe(user=request.user)
    return render(request, html, {'form': form})


def add_author(request):
    html = 'add_author.html'
    form = None

    if request.method == 'POST':
        form = AddAuthor(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data['name'],
            )
            return render(request, 'thanks.html')
    else:
        form = AddAuthor()

    return render(request, html, {'form': form})


def signup_view(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('homepage'))

    html = 'signup.html'
    form = SignupForm(None or request.POST)

    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'], data['email'], data['password'])
        login(request, user)
        return HttpResponseRedirect(reverse('homepage'))

    return render(request, html, {'form': form})


def login_view(request):
    html = 'login.html'
    form = LoginForm(None or request.POST)
    if form.is_valid():
        next = request.POST.get('next')
        data = form.cleaned_data
        user = authenticate(
            username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('homepage'))

    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
