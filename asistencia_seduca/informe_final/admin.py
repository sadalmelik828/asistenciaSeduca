# -*- coding: utf-8 -*-
'''
Created on 28/03/2011

@author: roque
'''
from django.contrib import admin
from asistencia_seduca.asistencia.models import *
from asistencia_seduca.informe_final.models import Categoria, Criterioevaluacionproceso, Proceso, Evaluacionproceso, Criterioinformefinal, Informefinal, Evaluacioninformefinal, Informedesarrolloproceso

class EvaluacionprocesoInline(admin.StackedInline):
    model = Evaluacionproceso
    extra = 5
    max_num = 5
    #readonly_fields = ('criterio',)
    fields = ('criterio', 'si', 'observaciones',)
    can_delete = False

class ProcesoAdmin(admin.ModelAdmin):
    inlines = [EvaluacionprocesoInline]
    list_display = ('establecimiento_educativo', 'evento_asistido',)
    exclude = ('tutor',)

    def establecimiento_educativo(self, obj):
        ins = Institucioneducativa.objects.get(proceso=obj)
        return '%s' % (ins.nombre)
    establecimiento_educativo.short_descripcion = "Establecimiento Educativo"

    def evento_asistido(self, obj):
        e = Evento.objects.get(proceso=obj)
        return '%s - %s - %s' % (e.lugar, e.municipio, e.fecha_1)
    evento_asistido.short_description = "Evento al que asistio"

    def save_model(self, request, obj, form, change):
        tutor = Tutor.objects.get(usuario__username__exact=request.user)
        obj.tutor = tutor
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'evento':
                kwargs['queryset'] = Evento.objects.filter(tutor__usuario__username__exact=request.user)
            if db_field.name == 'institucion_educativa':
                kwargs['queryset'] = Institucioneducativa.objects.filter(tutor__usuario__username__exact=request.user)
        else:
            if db_field.name == 'evento':
                kwargs['queryset'] = Evento.objects.all()
            if db_field.name == 'institucion_educativa':
                kwargs['queryset'] = Institucioneducativa.objects.all()
        return super(ProcesoAdmin, self).formfield_for_foreignkey(db_field, **kwargs)

    def queryset(self, request):
        qs = super(ProcesoAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(institucion_educativa__tutor__usuario__username__exact=request.user)

class EvaluacioninformefinalInline(admin.StackedInline):
    model = Evaluacioninformefinal
    extra = 8
    max_num = 8
    #readonly_fields = ('criterio',)
    fields = ('criterio', 'si', 'observaciones',)
    can_delete = False

class InformefinalAdmin(admin.ModelAdmin):
    list_display = ('establecimiento_educativo', 'evento_asistido',)
    inlines = [EvaluacioninformefinalInline]
    exclude = ('tutor',)

    def establecimiento_educativo(self, obj):
        ins = Institucioneducativa.objects.get(informefinal=obj)
        return '%s' % (ins.nombre)
    establecimiento_educativo.short_descripcion = "Establecimiento Educativo"

    def evento_asistido(self, obj):
        e = Evento.objects.get(informefinal=obj)
        return '%s - %s - %s' % (e.lugar, e.municipio, e.fecha_1)
    evento_asistido.short_description = "Evento al que asistio"

    def save_model(self, request, obj, form, change):
        tutor = Tutor.objects.get(usuario__username__exact=request.user)
        obj.tutor = tutor
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'evento':
                kwargs['queryset'] = Evento.objects.filter(tutor__usuario__username__exact=request.user)
            if db_field.name == 'institucion_educativa':
                kwargs['queryset'] = Institucioneducativa.objects.filter(tutor__usuario__username__exact=request.user)
        else:
            if db_field.name == 'evento':
                kwargs['queryset'] = Evento.objects.all()
            if db_field.name == 'institucion_educativa':
                kwargs['queryset'] = Institucioneducativa.objects.all()
        return super(InformefinalAdmin, self).formfield_for_foreignkey(db_field, **kwargs)

    def queryset(self, request):
        qs = super(InformefinalAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(institucion_educativa__tutor__usuario__username__exact=request.user)

class InformedesarrolloprocesoAdmin(admin.ModelAdmin):
    change_form_template = "admin/informe_final/informedesarrolloproceso/informe_desarrollo_cap.html"
    exclude = ('tutor',)

    def change_view(self, request, object_id, extra_context=None):
        if request.user.is_superuser:
            tutor = Tutor.objects.get(informedesarrolloproceso=object_id)
        else:
            tutor = Tutor.objects.get(usuario__username__exact=request.user)
        contenido = {
                     'tutor': tutor,
                     'cant_eventos': Evento.objects.filter(tutor=tutor).count(),
                     'cant_ie': Institucioneducativa.objects.filter(tutor=tutor).exclude(pk=450).count(),
                     'cant_participantes': Asistente.objects.filter(evento__tutor=tutor).count(),
                     'subregiones': Subregion.objects.filter(municipio__institucioneducativa__tutor=tutor).distinct(),
                     'agregados': Criterioevaluacionproceso.objects.select_related(depth=1).extra(select={"si": "select count(*) from evaluacion_proceso ep join proceso p where ep.criterio_id = criterio_evaluacion_proceso.id and ep.proceso_id = p.id and p.tutor_id = " + str(tutor.id) + " and ep.si = 1", "no": "select count(*) from evaluacion_proceso ep join proceso p where ep.criterio_id = criterio_evaluacion_proceso.id and ep.proceso_id = p.id and p.tutor_id = " + str(tutor.id) + " and ep.si = 0"}),
                     'asistencias': Municipio.objects.filter(evento__tutor=tutor).distinct().extra(select={"asistentes": "select count(a.id) from asistente a join asistente_evento ae, evento e, evento_tutor et, tutor t where a.id = ae.asistente_id and e.id = ae.evento_id and e.id = et.evento_id and t.id = et.tutor_id and e.municipio_id = municipio.id and t.id = " + str(tutor.id)}),
                     'consolidado': Institucioneducativa.objects.filter(tutor=tutor).exclude(pk=450).extra(select={"compromiso": "select case 1 when sum(ep.si)=2 then 'si' when sum(ep.si)=0 then 'no' else 'diferente' end as tipo from evaluacion_proceso ep join criterio_evaluacion_proceso cep, proceso p where cep.id = ep.criterio_id and p.id = ep.proceso_id and p.institucion_educativa_id = institucion_educativa.id and cep.categoria_id = 1", "desarrollo": "select case 1 when sum(ep.si)=3 then 'si' when sum(ep.si)=0 then 'no' else 'diferente' end as tipo from evaluacion_proceso ep join criterio_evaluacion_proceso cep, proceso p where cep.id = ep.criterio_id and p.id = ep.proceso_id and p.institucion_educativa_id = institucion_educativa.id and cep.categoria_id = 2"})
                     }
        return super(InformedesarrolloprocesoAdmin, self).change_view(request, object_id, extra_context=contenido)

    def save_model(self, request, obj, form, change):
        tutor = Tutor.objects.get(usuario__username__exact=request.user)
        obj.tutor = tutor
        obj.save()

    def queryset(self, request):
        qs = super(InformedesarrolloprocesoAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tutor__usuario__username__exact=request.user)

admin.site.register(Categoria)
admin.site.register(Criterioevaluacionproceso)
admin.site.register(Criterioinformefinal)
admin.site.register(Proceso, ProcesoAdmin)
admin.site.register(Informefinal, InformefinalAdmin)
admin.site.register(Informedesarrolloproceso, InformedesarrolloprocesoAdmin)
