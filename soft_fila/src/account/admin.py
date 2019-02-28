from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import FilaUser,Profile,Events
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .forms import RegistrationForm,EditProfileForm,CustomProfileForm

class EventAdmin(admin.ModelAdmin):

    model = Events
    can_delete = False
    fk_name = 'filauser'
    verbose_name_plural = 'Event'

    fieldsets = (
        (None, {'fields': ('UserEvent',)}),

        (_('Event'), {'fields': ('day',)}),
        (_('Event Details'), {'fields': ('concert_type','vocal_type','city','location','room',)}),
        (_('Event Time'), {'fields': ('start_time','final_time',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('UserEvent','day','concert_type','vocal_type','city','location','room','start_time','final_time',),
        }),
    )

    list_display = ['UserEvent','day']
    search_fields = ('UserEvent',)

admin.site.register(Events, EventAdmin)

class FilaCustomUserAdmin(UserAdmin):

    add_form = RegistrationForm
    form = EditProfileForm
    model = FilaUser
    """inlines =(ProfileFilaUserAdmin, )

    def get_inline_instances(self, request, obj=None):

        if not obj:
            return list()

        return super(FilaCustomUserAdmin,self).get_inline_instances(request,obj)"""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'),
         {'fields': ('first_name',
                     'last_name',
                     )}
         ),
        #(_('Details'),{'fields' : ('photo','phone_number','instagram','facebook','caption')}),
        (_('Permissions'), {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'email2', 'first_name', 'last_name', 'password1', 'password2','photo','phone_number','instagram','facebook','caption','day',),
        }),
    )
    list_display = ['email', 'first_name', 'last_name']
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)


admin.site.register(FilaUser,FilaCustomUserAdmin)

class ProfileFilaUserAdmin(admin.ModelAdmin):
    add_form = CustomProfileForm
    form = EditProfileForm
    model = Profile

    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'filauser'

    # list_display = ('first_name','last_name','photo','phone','instagram','facebook','caption')

    fieldsets = (
        (None, {'fields': ('filauser',)}),

        (_('Name'), {'fields': ('first_name', 'last_name',)}),

        (_('Contact'), {'fields': ('phone', 'caption',)}),
        (_('Social-Media'), {'fields': ('photo', 'instagram', 'facebook',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'photo', 'phone_number',
                       'instagram', 'facebook', 'caption',),
        }),
    )
    list_display = ['filauser', 'first_name', 'last_name']
    search_fields = ('filauser', 'first_name', 'last_name')

    def photo(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.photo.url,
            width=obj.photo.width,
            height=obj.photo.height,
        ))

admin.site.register(Profile, ProfileFilaUserAdmin)



