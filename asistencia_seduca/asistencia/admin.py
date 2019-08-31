'''
Created on 11/01/2011

@author: roque sosa
'''
from asistencia_seduca.asistencia.models import *
from django import forms
from django.contrib import admin
import locale

class EventoAdmin(admin.ModelAdmin):
    list_display = ("lugar", "municipio", "visita_numero", "fecha_1", "cantidad_asistentes")
    raw_id_fields = ("municipio",)
    exclude = ("tutor",)

    def cantidad_asistentes(self, obj):
        c = Asistente.objects.filter(evento=obj).count()
        return c
    cantidad_asistentes.short_descripcion = "Cantidad Asistentes"

    def save_model(self, request, obj, form, change):
        tutor = Tutor.objects.get(usuario__username__exact=request.user)
        obj.save()
        obj.tutor.add(tutor)

    def queryset(self, request):
        qs = super(EventoAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tutor__usuario__username__exact=request.user)

class MunicipioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "departamento", "subregion",)
    search_fields = ("nombre", "departamento__nombre",)

#    def queryset(self, request):
#        qs = super(MunicipioAdmin, self).queryset(request)
#        return qs.filter(departamento__nombre__exact="Antioquia")

class LlamadaInline(admin.TabularInline):
    model = Llamada
    extra = 1

class RegistrovisitaInline(admin.TabularInline):
    model = Registrovisita
    extra = 1
    can_delete = False

class InstitucioneducativaAdmin(admin.ModelAdmin):
    inlines = [RegistrovisitaInline, LlamadaInline]
    list_display = ('dane', 'nombre', 'municipio', 'direccion', 'fechas_visita', 'telefono', 'correo_electronico_1', 'rector', 'linea_base_diligenciada',)
    search_fields = ('dane', 'nombre', 'municipio__nombre', 'direccion', 'telefono', 'correo_electronico_1', 'rector',)
    filter_horizontal = ("tutor",)
    readonly_fields = ('linea_base_diligenciada',)
    formfield_overrides = {
                           models.CharField: { 'widget': forms.TextInput(attrs={'size': '80'}) },
                           models.IntegerField: { 'widget': forms.TextInput(attrs={'size': '80'}) },
                           models.BigIntegerField: { 'widget': forms.TextInput(attrs={'size': '80'}) },
                           }

    def fechas_visita(self, obj):
        v = Registrovisita.objects.filter(institucion_educativa=obj)
        fechas = []
        loc = locale.getlocale()
        if v.count() > 0:
            locale.setlocale(locale.LC_ALL, ('es_CO', 'UTF8'))
            for f in v:
                fechas.append(str(f.fecha_visita.strftime("%d de %B de %Y")))
            fv = ', '.join(fechas)
            locale.setlocale(locale.LC_ALL, loc)
        else:
            fv = ""
        return fv
    fechas_visita.short_description = "Fechas de visita"

class AsistenteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "nro_identificacion", "cargo", "celular", "email", "institucion_educativa", "municipio_evento", "lugar_evento",)
    filter_horizontal = ("evento",)
    search_fields = ("nombre", "nro_identificacion", "cargo__nombre", "celular", "email", "institucion_educativa__nombre", "evento__lugar", "evento__municipio__nombre",)

    def municipio_evento(self, obj):
        m = Municipio.objects.filter(evento__asistente=obj)
        municipios = []
        for i in m:
            municipios.append('%s (%s)' % (i.nombre, i.departamento.nombre))
        r = ', '.join(municipios)
        return r
    municipio_evento.short_description = "Municipio del Evento"

    def lugar_evento(self, obj):
        e = Evento.objects.filter(asistente=obj)
        lugar = []
        for i in e:
            lugar.append('%s' % (i.lugar))
        l = ', '.join(lugar)
        return l
    lugar_evento.short_description = "Lugar del Evento"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'cargo':
                kwargs['queryset'] = Cargo.objects.all()
            if db_field.name == 'institucion_educativa':
                kwargs['queryset'] = Institucioneducativa.objects.filter(tutor__usuario__username__exact=request.user)
        else:
            if db_field.name == 'cargo':
                kwargs['queryset'] = Cargo.objects.all()
            if db_field.name == 'institucion_educativa':
                kwargs['queryset'] = Institucioneducativa.objects.all()
        return super(AsistenteAdmin, self).formfield_for_foreignkey(db_field, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'evento':
                kwargs['queryset'] = Evento.objects.filter(tutor__usuario__username__exact=request.user)
        else:
            kwargs['queryset'] = Evento.objects.all()
        return super(AsistenteAdmin, self).formfield_for_manytomany(db_field, **kwargs)

    #def queryset(self, request):
        #qs = super(AsistenteAdmin, self).queryset(request)
        #if request.user.is_superuser:
            #return qs
        #return qs.filter(evento__tutor__usuario__username__exact=request.user).distinct()

admin.site.register(Departamento)
admin.site.register(Subregion)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Cargo)
admin.site.register(Tutor)
admin.site.register(Personallamada)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Institucioneducativa, InstitucioneducativaAdmin)
admin.site.register(Asistente, AsistenteAdmin)
