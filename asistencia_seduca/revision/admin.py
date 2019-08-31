# -*- coding: utf-8 -*-
'''
Created on 20/04/2011

@author: roque
'''
from asistencia_seduca.asistencia.models import *
from asistencia_seduca.revision.models import *
from django.contrib import admin

class ItemAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'lb_categoria',)

class CriterioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'lb_item',)

class IndicadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'lb_criterio',)

class ValoracionInline(admin.TabularInline):
    model = Valoracion
    max_num = 10
    fields = ('indicador', 'criterio_evaluacion',)
    readonly_fields = ('indicador',)
    can_delete = False

class LineadebaseAdmin(admin.ModelAdmin):
    inlines = [ValoracionInline]
    readonly_fields = ('institucion_educativa',)
    fields = ('institucion_educativa', 'causas_analisis_contextual', 'causas_analisis_institucional', 'causas_practicas_aula',)

     #--------- def formfield_for_foreignkey(self, db_field, request, **kwargs):
        #------------------------------------- if not request.user.is_superuser:
            #---------------------- if db_field.name == 'institucion_educativa':
                # kwargs['queryset'] = Institucioneducativa.objects.filter(tutor__usuario__username__exact=request.user)
        #----------------------------------------------------------------- else:
            #---------------------- if db_field.name == 'institucion_educativa':
                #------- kwargs['queryset'] = Institucioneducativa.objects.all()
        # return super(LineadebaseAdmin, self).formfield_for_foreignkey(db_field, **kwargs)

    def queryset(self, request):
        qs = super(LineadebaseAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(institucion_educativa__tutor__usuario__username__exact=request.user)

admin.site.register(Categoria)
admin.site.register(Item, ItemAdmin)
admin.site.register(Criterio, CriterioAdmin)
admin.site.register(Indicador, IndicadorAdmin)
admin.site.register(Criteriovaloracion)
admin.site.register(Lineadebase, LineadebaseAdmin)
