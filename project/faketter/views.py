from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    FeekForm,
    ProfilePicForm,
    RegisterUserForm,
    UpdateUserForm,
    UserConfirmationForm,
)
from .models import Feek, Profile


def home(request: HttpRequest):
    if request.user.is_authenticated:
        form = FeekForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                feek: Feek = form.save(commit=False)
                feek.user = request.user
                feek.save()
                messages.success(request, "Se agrego tu fake!")
                return redirect("home")

        feeks = Feek.objects.all().order_by("-created_at")
        return render(request, "home.html", {"feeks": feeks, "form": form})

    else:
        feeks = Feek.objects.all().order_by("-created_at")
    return render(request, "home.html", {"feeks": feeks})


def profile_list(request: HttpRequest):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, "profile_list.html", {"profiles": profiles})

    messages.success(request, "Tenes que estar logueado para ver esta pagina.")
    return redirect("home")


def followers(request: HttpRequest, pk: int):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profile = Profile.objects.get(user_id=pk)
            return render(request, "followers.html", {"profile_user": profile})
        else:
            messages.success(request, "Esa no es tu pagina de seguidores")
            return redirect("home")

    messages.success(request, "Tenes que estar logueado para ver esta pagina.")
    return redirect("home")


def following(request: HttpRequest, pk: int):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profile = Profile.objects.get(user_id=pk)
            return render(request, "following.html", {"profile_user": profile})
        else:
            messages.success(request, "Esa no es tu pagina de seguidores")
            return redirect("home")

    messages.success(request, "Tenes que estar logueado para ver esta pagina.")
    return redirect("home")


def profile(request: HttpRequest, pk: int):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        feeks = Feek.objects.filter(user_id=pk).order_by("-created_at")

        # post form logic follow button
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST["follow"]
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            else:
                current_user_profile.follows.add(profile)

            current_user_profile.save()

        return render(request, "profile.html", {"profile": profile, "feeks": feeks})

    messages.success(request, "Tenes que estar logueado para ver esta pagina.")
    return redirect("home")


def login_user(request: HttpRequest):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logueado.")
            return redirect("home")
        else:
            messages.success(request, "Algo salio mal. Intenta devuelta.")
            return redirect("login")

    else:
        return render(request, "login.html", {})


def logout_user(request: HttpRequest):
    logout(request)
    messages.success(request, "Sesion cerrada!.")
    return redirect("home")


def register_user(request: HttpRequest):
    form = RegisterUserForm()
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            # login user
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "User created successfully! Welcome!")
            return redirect("home")
    return render(request, "register.html", {"form": form})


# ----------- Update profile made for me -----------------------------------------
# tuve que hacer un formulario para la data del usuario y otra para la imagen
# porque en realidad la info del "perfil" es del usuario y la imagen solo esta en
# el perfil. Al instanciar UpdateUserForm se llama a la instancia del usuario y
# al llamar al ProfilePicForm se llama a la instancia del perfil
def update_user(request: HttpRequest):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user_id=request.user.id)

        if request.method == "POST":
            profile_form = UpdateUserForm(
                request.POST or None, request.FILES or None, instance=profile_user.user
            )
            profile_pic = ProfilePicForm(
                request.POST or None, request.FILES or None, instance=profile_user
            )
            confirmation_form = UserConfirmationForm(request.POST or None)

            if (
                confirmation_form.is_valid()
                and profile_form.is_valid()
                and profile_pic.is_valid()
            ):
                passw = confirmation_form.cleaned_data["password"]
                user = authenticate(
                    request, username=current_user.username, password=passw
                )
                if user:
                    profile_form.save()
                    profile_pic.save()
                    messages.success(request, "Your info has been updated!")
                    return redirect("profile", profile_user.user.id)

                else:
                    messages.success(request, "wrong passowrd. Try again!")
                    return redirect("update_user")

        else:
            profile_form = UpdateUserForm(instance=profile_user.user)
            profile_pic = ProfilePicForm(instance=profile_user)
            confirmation_form = UserConfirmationForm()

        return render(
            request,
            "update_user.html",
            {
                "profile_form": profile_form,
                "profile": profile_user,
                "conf": confirmation_form,
                "profile_pic_form": profile_pic,
            },
        )
    else:
        messages.success(request, "You must be logged in to view that page.")
        return redirect("home")


# --------------------------------------------------------------------------------


def feek_like(request: HttpRequest, pk: int):
    if request.user.is_authenticated:
        meep = get_object_or_404(Feek, id=pk)
        if meep.likes.filter(id=request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)

        # HTTP_REFERER hace referencia a la ruta actual
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, "You must be logged in to view that page.")
        return redirect("home")


def feek_show(request: HttpRequest, pk: int):
    feek = get_object_or_404(Feek, id=pk)
    if feek:
        return render(request, "feek_show.html", {"feek": feek})
    else:
        messages.success(request, "that feek does not exist any more.")
        return redirect("home")


def unfollow(request: HttpRequest, pk: int):
    if request.user.is_authenticated:
        # get profile to unfollow
        profile = Profile.objects.get(id=pk)
        # unfollow the profile
        request.user.profile.follows.remove(profile)
        # save our profile
        request.user.profile.save()
        messages.success(
            request, f"You have successfully unfollowed {profile.user.username}"
        )
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, "You must be logged in to view that page.")
        return redirect("home")


def follow(request: HttpRequest, pk: int):
    if request.user.is_authenticated:
        profile = Profile.objects.get(id=pk)
        # follow the profile
        request.user.profile.follows.add(profile)
        # save our profile
        request.user.profile.save()
        messages.success(
            request, f"You have successfully followed {profile.user.username}"
        )
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, "You must be logged in to view that page.")
        return redirect("home")


# -------------------------------------------------------------------------------


def delete_feek(request: HttpRequest, pk: int):
    if request.user.is_authenticated:
        feek = get_object_or_404(Feek, id=pk)
        if request.user.username == feek.user.username:
            feek.delete()
            messages.success(request, "El post fue eliminado!")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, "no es tu post")
            return redirect("home")
    else:
        messages.success(request, "You must be logged in to view that page.")
        return redirect("home")


@login_required("", login_url="login")
def edit_feek(request: HttpRequest, pk: int):
    feek = get_object_or_404(Feek, id=pk)
    if request.user.username == feek.user.username:
        form = FeekForm(request.POST or None, instance=feek)
        if request.method == "POST":
            if form.is_valid():
                feek = form.save(commit=False)
                feek.user = request.user
                feek.save()
                messages.success(request, "Your feek was updated!")
                return redirect("profile", request.user.id)
        else:
            return render(request, "edit_feek.html", {"feek": feek, "form": form})
    else:
        messages.success(request, "no es tu post")
        return redirect("home")
