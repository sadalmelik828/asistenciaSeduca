# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Departamento(models.Model):
    nombre = models.CharField(max_length=80)
    codigo = models.IntegerField(max_length=2)

    class Meta:
        db_table = "departamento"
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ["nombre"]

    def __unicode__(self):
        return self.nombre

class Subregion(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'subregion'
        verbose_name = 'Sub-región'
        verbose_name_plural = 'Sub-regiones'

    def __unicode__(self):
        return '%s' % (self.nombre)

class Municipio(models.Model):
    nombre = models.CharField(max_length=80)
    codigo = models.IntegerField(max_length=3)
    departamento = models.ForeignKey(Departamento)
    subregion = models.ForeignKey(Subregion)

    class Meta:
        db_table = "municipio"
        verbose_name = "Municipio"
        verbose_name_plural = 'Municipios'
        ordering = ['departamento', 'nombre']

    def __unicode__(self):
        return u'%s (%s)' % (self.nombre, self.departamento.nombre)

class Cargo(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'cargo'
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __unicode__(self):
        return '%s' % (self.nombre)

class Tutor(models.Model):
    nombre = models.CharField(max_length=70)
    usuario = models.ForeignKey(User)

    class Meta:
        db_table = "tutor"
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"

    def __unicode__(self):
        return self.nombre

class Personallamada(models.Model):
    nombre = models.CharField(max_length=150)

    class Meta:
        db_table = "persona_llamada"
        verbose_name = "Persona que llama la institución"
        verbose_name_plural = "Personas que llaman las instituciones"

    def __unicode__(self):
        return '%s' % (self.nombre)

class Institucioneducativa(models.Model):
    dane = models.BigIntegerField(unique=True)
    nombre = models.CharField(max_length=200)
    municipio = models.ForeignKey(Municipio)
    direccion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Dirección de la Institución")
    telefono = models.CharField(max_length=100, blank=True, null=True, verbose_name="Teléfono(s)")
    fax = models.CharField(max_length=100, blank=True, null=True)
    correo_electronico_1 = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico principal")
    correo_electronico_2 = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico opcional")
    correo_electronico_3 = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico opcional")
    rector = models.CharField(max_length=120, blank=True, null=True, verbose_name="Nombre del rector")
    linea_base_diligenciada = models.BooleanField()
    cantidad_docentes = models.IntegerField(blank=True, null=True, verbose_name="Cupo de docentes")
    cantidad_alumnos_media = models.IntegerField(blank=True, null=True, verbose_name="Cantidad de alumnos de media")
    tutor = models.ManyToManyField(Tutor)
    persona_llamada = models.ManyToManyField(Personallamada, through="Llamada")

    class Meta:
        db_table = 'institucion_educativa'
        verbose_name = 'Institución educativa'
        verbose_name_plural = 'Instituciones educativas'

    def __unicode__(self):
        return '%s' % (self.nombre)

class Llamada(models.Model):
    institucion_educativa = models.ForeignKey(Institucioneducativa)
    persona_llamada = models.ForeignKey(Personallamada, verbose_name="Persona que hace la llamada")
    fecha_hora_llamada = models.DateTimeField(blank=True, null=True, verbose_name="Fecha y hora de la llamada")
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "institucion_educativa_persona_llamada"
        verbose_name = "Llamada Institución Educativa"
        verbose_name_plural = "Llamadas Instituciones Educativas"

    def __unicode__(self):
        return '%s -- %s' % (self.institucion_educativa.nombre, self.persona_llamada.nombre)

class Registrovisita(models.Model):
    institucion_educativa = models.ForeignKey(Institucioneducativa)
    fecha_visita = models.DateField(verbose_name="Fecha de la visita")
    cantidad_docentes_participantes = models.IntegerField(blank=True, null=True, verbose_name="Cantidad de docentes a participar")
    valor_unitario_persona = models.IntegerField(blank=True, null=True, verbose_name="Costo de transporte por persona")

    class Meta:
        db_table = "registro_visita"
        verbose_name = "Registro de visita institución"
        verbose_name_plural = "Registros de visitas institución"

    def __unicode__(self):
        return '%s - %s docentes participantes' % (self.fecha_visita, self.cantidad_docentes_participantes)

OPCIONES_VISITA = (
                 (1, '1'),
                 (2, '2'),
                 (3, '3'),
                 (4, '4'),
                 (5, '5'),
                 )

class Evento(models.Model):
    visita_numero = models.PositiveIntegerField(max_length=1, choices=OPCIONES_VISITA, verbose_name="Visita No")
    lugar = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio)
    tutor = models.ManyToManyField(Tutor, blank=False)
    fecha_1 = models.DateField(verbose_name="Fecha de realización 1")
    fecha_2 = models.DateField(blank=True, verbose_name="Fecha de realización 2")

    class Meta:
        db_table = "evento"
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __unicode__(self):
        return u"%s - %s - %s" % (self.lugar, self.municipio.nombre, self.fecha_1)

OPCIONES_SEXO = (
                 ('F', 'Femenino'),
                 ('M', 'Masculino'),
                 ('S', 'Sin diligenciar'),
                 )

class Asistente(models.Model):
    nombre = models.CharField(max_length=70)
    cargo = models.ForeignKey(Cargo)
    sexo = models.CharField(max_length='1', choices=OPCIONES_SEXO)
    nro_identificacion = models.BigIntegerField(max_length=25, blank=True, null=True)
    institucion_educativa = models.ForeignKey(Institucioneducativa)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    celular = models.CharField(max_length=25, blank=True, null=True)
    telefono_fijo = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    evento = models.ManyToManyField(Evento, blank=False)

    class Meta:
        db_table = "asistente"
        verbose_name = "Asistente"
        verbose_name_plural = "Asistentes"

    def __unicode__(self):
        return self.nombre
