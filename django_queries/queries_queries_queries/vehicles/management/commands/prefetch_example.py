#!/usr/bin/python

import logging

from django.core.management.base import BaseCommand, CommandError
from vehicles import models

LOG = logging.getLogger('console')


class Command(BaseCommand):
    help = 'Simple tests of queries'

    def handle(self, *args, **options):

        owners = models.Owner.objects.all().prefetch_related('car', 'car__trailer')

        LOG.info("Looping through owners") 
        for owner in owners:
            cars = owner.car.all()
            LOG.info("Looping through cars") 
            for car in cars:
                LOG.info("list all trailers") 
                print car.trailer.all()
    
        # without prefetch related
        LOG.info('NOT using prefetch')
        owners = models.Owner.objects.all()

        LOG.info("Looping through owners") 
        for owner in owners:
            cars = owner.car.all()
            LOG.info("Looping through cars") 
            for car in cars:
                LOG.info("list all trailers") 
                print car.trailer.all()

