#!/usr/bin/python

import logging

from django.db.models import Q, Max
from django.core.management.base import BaseCommand, CommandError
from vehicles import models

LOG = logging.getLogger('console')


class Command(BaseCommand):
    help = 'Simple example of select_related queries'

    def handle(self, *args, **options):

        cars = models.Car.objects.all().select_related('owner')
        LOG.info("Looping through all cars") 
        for car in cars:
            LOG.info("Car: %s owner:  %s", car.license_plate, car.owner.name)
       
        LOG.info('Without select related')
        cars = models.Car.objects.all()
        LOG.info("Looping through all cars") 
        for car in cars:
            LOG.info("Car: %s owner:  %s", car.license_plate, car.owner.name)
