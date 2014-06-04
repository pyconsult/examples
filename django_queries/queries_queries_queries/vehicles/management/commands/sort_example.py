#!/usr/bin/python

import logging

from django.db.models import Q, Max
from django.core.management.base import BaseCommand, CommandError
from vehicles import models

LOG = logging.getLogger('console')


class Command(BaseCommand):
    help = 'Simple tests of queries'

    def handle(self, *args, **options):
        owners = models.Owner.objects.all().\
                annotate(Max('car__trailer__weight')).order_by('-car__trailer__weight__max').\
                prefetch_related('car').prefetch_related('car__trailer')

        LOG.info("Looping through owners") 
        for owner in owners:
            LOG.info('max weight %s', owner.car__trailer__weight__max)
            cars = owner.car.all()
            for car in cars:
                trailers = car.trailer.all()
                for trailer in trailers:
                    LOG.info("Trailer weight %s" % trailer.weight)


