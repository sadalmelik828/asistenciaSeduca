# -*- coding: utf-8 -*-
from django.db import models
from asistencia_seduca.asistencia.models import Institucioneducativa, Evento, Tutor
# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=150)

    class Meta:
        db_table = "categoria"
        verbose_name = "Categoría"
        verbose_name_plural = "Categorias"

    def __unicode__(self):
        return '%s' % (self.nombre)

class Criterioevaluacionproceso(models.Model):
    nombre = models.TextField()
    categoria = models.ForeignKey(Categoria)

    class Meta:
        db_table = "criterio_evaluacion_proceso"
        verbose_name = "Criterio de la evaluación del proceso"
        verbose_name_plural = "Criterios de la evaluación del proceso"

    def __unicode__(self):
        return "%s --- %s" % (self.categoria.nombre, self.nombre)

class Proceso(models.Model):
    fecha = models.DateField(blank=True, null=True)
    tutor = models.ForeignKey(Tutor)
    evento = models.ForeignKey(Evento)
    institucion_educativa = models.ForeignKey(Institucioneducativa)
    recomendaciones = models.TextField(blank=True, null=True, verbose_name="Recomendaciones para la institución")
    evaluacion = models.ManyToManyField(Criterioevaluacionproceso, through="Evaluacionproceso")

    class Meta:
        db_table = "proceso"
        verbose_name = "Evaluación del proceso"
        verbose_name_plural = "Evaluación del proceso"
        unique_together = (('tutor', 'evento', 'institucion_educativa',))

    def __unicode__(self):
        return "%s" % (self.institucion_educativa.nombre)

class Evaluacionproceso(models.Model):
    proceso = models.ForeignKey(Proceso)
    criterio = models.ForeignKey(Criterioevaluacionproceso, help_text="Seleccione un criterio; evite repetir los criterios ya que puede generar problemas al guardar.")
    si = models.BooleanField(blank=True, help_text="En caso de que su respuesta sea 'No' no marque en esta opción.")
    observaciones = models.TextField(blank=True)

    class Meta:
        db_table = "evaluacion_proceso"
        verbose_name = "Proceso"
        verbose_name_plural = "Procesos"
        unique_together = (('proceso', 'criterio',))

    def __unicode__(self):
        return "%s --- %s" % (self.proceso.institucion_educativa.nombre, self.criterio.nombre)

class Criterioinformefinal(models.Model):
    nombre = models.TextField()
    categoria = models.ForeignKey(Categoria)

    class Meta:
        db_table = "criterio_informe_final"
        verbose_name = "Criterio del informe final"
        verbose_name_plural = "Criterios del informe final"

    def __unicode__(self):
        return "%s --- %s" % (self.categoria.nombre, self.nombre)

class Informefinal(models.Model):
    fecha = models.DateField(blank=True, null=True)
    tutor = models.ForeignKey(Tutor)
    evento = models.ForeignKey(Evento)
    institucion_educativa = models.ForeignKey(Institucioneducativa)
    observaciones_generales = models.TextField(blank=True, null=True)
    evaluacion = models.ManyToManyField(Criterioinformefinal, through="Evaluacioninformefinal")

    class Meta:
        db_table = "informe_final"
        verbose_name = "Evaluación final del proceso"
        verbose_name_plural = "Evaluación final del proceso"
        unique_together = (('tutor', 'evento', 'institucion_educativa',))

    def __unicode__(self):
        return "%s" % (self.institucion_educativa.nombre)

class Evaluacioninformefinal(models.Model):
    informe_final = models.ForeignKey(Informefinal)
    criterio = models.ForeignKey(Criterioinformefinal, help_text="Seleccione un criterio; evite repetir los criterios ya que puede generar problemas al guardar.")
    si = models.BooleanField(blank=True, help_text="En caso de que su respuesta sea 'No' no marque en esta opción.")
    observaciones = models.TextField(blank=True)

    class Meta:
        db_table = "evaluacion_informe_final"
        verbose_name = "Informe final"
        verbose_name_plural = "Informes final"
        unique_together = (('informe_final', 'criterio',))

    def __unicode__(self):
        return "%s --- %s" % (self.informe_final.institucion_educativa.nombre, self.criterio.nombre)

class Informedesarrolloproceso(models.Model):
    tutor = models.ForeignKey(Tutor, unique=True)
    obs_tabla_agregados = models.TextField(blank=True, null=True, verbose_name="2.1.1 Observaciones del cuadro de resultados agregados", help_text="Haga sus observaciones con base en el cuadro que se encuentra abajo en el informe. Si las cifras aparecen en ceros debe diligenciar evaluaciones de proceso.")
    obs_tabla_asistencia = models.TextField(blank=True, null=True, verbose_name="2.1.2 Observaciones del cuadro de asistencias", help_text="Haga sus observaciones con base en el cuadro que se encuentra abajo en el informe.")
    obs_tabla_cat_compromiso = models.TextField(blank=True, null=True, verbose_name="2.2 Observaciones del cuadro consolidado de la evaluación del proceso categoría compromisos", help_text="Haga sus observaciones con base en el cuadro que se encuentra abajo en el informe.")
    obs_tabla_cat_desarrollo_proceso = models.TextField(blank=True, null=True, verbose_name="2.2 Observaciones del cuadro consolidado de la evaluación del proceso categoría desarrollo del proceso", help_text="Haga sus observaciones con base en el cuadro que se encuentra abajo en el informe.")

    class Meta:
        db_table = "informe_desarrollo_proceso"
        verbose_name = "Informe de desarrollo del proceso"
        verbose_name_plural = "Informe de desarrollo del proceso"

    def __unicode__(self):
        return '%s' % (self.tutor.nombre)
