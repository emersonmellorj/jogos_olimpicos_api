from django.contrib import admin

from .models import Athlete, Modality, Stage, Results

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'modality', 'age', 'created_in', 'active')


@admin.register(Modality)
class ModalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_in', 'active')


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('modality', 'name', 'status', 'created_in', 'active')


@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    list_display = ('modality', 'athlete', 'stage', 'value', 'unity')