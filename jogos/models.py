from django.db import models

class Base(models.Model):
    """
    Base class for others Models
    """
    created_in = models.DateTimeField(auto_now_add=True)
    updated_in = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        """
        Abstract Class
        """
        abstract = True


class Modality(Base):
    """
    Class to game modes
    """
    name = models.CharField(max_length=255, blank=False, unique=True)

    class Meta:
        verbose_name = "Modality"
        verbose_name_plural = "Modalities"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Athlete(Base):
    """
    Class for creation of athletes
    """
    modality = models.ForeignKey(Modality, related_name="athletes", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    age = models.IntegerField(blank=False)

    class Meta:
        verbose_name = "Athlete"
        verbose_name_plural = "Athletes"
        unique_together = ["first_name", "last_name"]
        ordering = ["id"]  

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Stage(Base):
    """
    Class for Stage of Competitions
    """
    modality = models.ForeignKey(Modality, related_name="stages_modality", on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Stage"
        unique_together = ["modality", "name"]
        ordering = ["id"]

    def __str__(self):
        return f'{self.modality} - {self.name}'


class Results(Base):
    """
    Results of athletes in competitions
    """
    modality = models.ForeignKey(Modality, related_name="results_modality", on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, related_name="results_athletes", on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, related_name="results_stage", on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=8, decimal_places=3, blank=False)
    unity = models.CharField(max_length=1, blank=False)

    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "Results"

    def __str__(self):
        return f'{self.modality.name} {self.athlete.first_name} {self.athlete.last_name}'
