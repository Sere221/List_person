from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserOurRegistraion, ProfileImage, UserUpdateForm, ProfileImageDis
from django.views.generic import DetailView, UpdateView, DeleteView
from django.db import transaction
from django.urls import reverse_lazy
from .models import Profile


def register(request):
    if request.method == "POST":
        form = UserOurRegistraion(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} был создан, введите имя пользователя и пароль для авторизации')
            return redirect('user')
    else:
        form = UserOurRegistraion()
    return render(request, 'users/registraion.html', {'form': form, 'title':'Регистрация пользователя'})


@login_required
def profile(request):
    if request.method == "POST":
        img_profile_dis = ProfileImageDis(request.POST, request.FILES, instance=request.user.profile)
        img_profile = ProfileImage(request.POST, request.FILES, instance=request.user.profile)
        update_user = UserUpdateForm(request.POST, instance=request.user)

        if update_user.is_valid() and img_profile.is_valid():
            update_user.save()
            img_profile.save()
            messages.success(request, f'Ваш аккаунт был успешно обновлен')
            return redirect('profile')
    else:
        img_profile = ProfileImage(instance=request.user.profile)
        img_profile_dis = ProfileImageDis(instance=request.user.profile)
        update_user = UserUpdateForm(instance=request.user)

    data = {
        'title': request.user.username,
        'img_profile': img_profile,
        'update_user': update_user,
        'img_profile_dis': img_profile_dis
    }

    return render(request, 'users/profile.html', data)


class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'users/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.user.username}'
        return context


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileImage
    template_name = 'users/profile_edit.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.get_object().user.username}'
        if self.request.POST:
            context['user_form'] = ProfileImage(self.request.POST, instance=self.get_object().user)
        else:
            context['user_form'] = ProfileImage(instance=self.get_object().user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})


class ProfileDeleteView(DeleteView):
    model = Profile
    template_name = 'users/profile_del.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(ProfileDeleteView, self).get_context_data(**kwargs)
        context['title'] = f'Удаление профиля пользователя: {self.get_object().user.username}'
        return context

