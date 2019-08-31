# -*- coding: utf-8 -*-
from asistencia_seduca.asistencia.models import Institucioneducativa
from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = "lb_categoria"
        verbose_name = "Categoría linea base"
        verbose_name_plural = "Categorias linea base"

    def __unicode__(self):
        return '%s' % (self.nombre)

class Item(models.Model):
    nombre = models.CharField(max_length=120)
    lb_categoria = models.ForeignKey(Categoria)

    class Meta:
        db_table = "lb_item"
        verbose_name = "Item o Pregunta"
        verbose_name_plural = "Items o Preguntas"

    def __unicode__(self):
        return '%s' % (self.nombre)

class Criterio(models.Model):
    nombre = models.TextField()
    lb_item = models.ForeignKey(Item)

    class Meta:
        db_table = "lb_criterio"
        verbose_name = "Criterio"
        verbose_name_plural = "Criterios"

    def __unicode__(self):
        return '%s' % (self.nombre)

class Indicador(models.Model):
    nombre = models.TextField()
    lb_criterio = models.ForeignKey(Criterio)

    class Meta:
        db_table = "lb_indicador"
        verbose_name = "Indicador"
        verbose_name_plural = "Indicadores"

    def __unicode__(self):
        return '%s' % (self.nombre)

class Criteriovaloracion(models.Model):
    nombre = models.CharField(max_length=80)

    class Meta:
        db_table = "lb_criterio_valoracion"
        verbose_name = "Criterio de valoración"
        verbose_name_plural = "Criterios de valoración"

    def __unicode__(self):
        return '%s' % (self.nombre)

class Lineadebase(models.Model):
    institucion_educativa = models.ForeignKey(Institucioneducativa, unique=True, verbose_name="Institución educativa asesorada")
    causas_analisis_contextual = models.TextField(blank=True, null=True, verbose_name="Causas por las cuales no se alcanzaron los niveles esperados (Análisis Contextual)")
    causas_analisis_institucional = models.TextField(blank=True, null=True, verbose_name="Causas por las cuales no se alcanzaron los niveles esperados (Análisis Institucional)")
    causas_practicas_aula = models.TextField(blank=True, null=True, verbose_name="Causas por las cuales no se alcanzaron los niveles esperados (Prácticas de Aula)")
    lineadebase_indicador = models.ManyToManyField(Indicador, through="Valoracion")

    class Meta:
        db_table = "linea_base"
        verbose_name = "Linea de base"
        verbose_name_plural = "Linea de base"

    def __unicode__(self):
        return '%s' % (self.institucion_educativa.nombre)

class Valoracion(models.Model):
    linea_base = models.ForeignKey(Lineadebase)
    indicador = models.ForeignKey(Indicador)
    criterio_evaluacion = models.ForeignKey(Criteriovaloracion)

    class Meta:
        db_table = "linea_base_indicador"
        verbose_name = "Valoración linea de base"
        verbose_name_plural = "Valoraciones linea de base"
        unique_together = (('linea_base', 'indicador'),)

    def __unicode__(self):
        return '%s' % (self.criterio_evaluacion.nombre)
