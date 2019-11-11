#!/usr/bin/python

# [Icarus] units.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2018 Gramercy Park Studios
#
# Look-up table for Maya's discrete unit preset values.


time = [('film',      'Film',                24), 
        ('pal',       'PAL',                 25), 
        ('ntsc',      'NTSC',                30), 
        ('show',      'Film HFR',            48), 
        ('palf',      'PAL Field',           50), 
        ('ntscf',     'NTSC Field',          60), 
        ('23.976fps', '24p',             23.976), 
        ('29.97fps',  'NTSC',             29.97), 
        ('29.97df',   'NTSC Drop-Frame',  29.97), 
        ('47.952fps', '48p',             47.952), 
        ('59.94fps',  'NTSC Field',       59.94), 
        ('sec',       'Second',               1), 
        ('2fps',      '',                     2), 
        ('3fps',      '',                     3), 
        ('4fps',      '',                     4), 
        ('5fps',      '',                     5), 
        ('6fps',      '',                     6), 
        ('8fps',      '',                     8), 
        ('10fps',     '',                    10), 
        ('12fps',     '',                    12), 
        ('game',      '',                    15), 
        ('16fps',     '',                    16), 
        ('20fps',     '',                    20), 
        ('40fps',     '',                    40), 
        ('75fps',     '',                    75), 
        ('80fps',     '',                    80), 
        ('100fps',    '',                   100), 
        ('120fps',    '',                   120), 
        ('125fps',    '',                   125), 
        ('150fps',    '',                   150), 
        ('200fps',    '',                   200), 
        ('240fps',    '',                   240), 
        ('250fps',    '',                   250), 
        ('300fps',    '',                   300), 
        ('375fps',    '',                   375), 
        ('400fps',    '',                   400), 
        ('500fps',    '',                   500), 
        ('600fps',    '',                   600), 
        ('750fps',    '',                   750), 
        ('millisec',  'Millisecond',       1000), 
        ('1200fps',   '',                  1200), 
        ('1500fps',   '',                  1500), 
        ('2000fps',   '',                  2000), 
        ('3000fps',   '',                  3000), 
        ('6000fps',   '',                  6000), 
        ('44100fps',  '44,100 Hz',        44100), 
        ('48000fps',  '48,000 Hz',        48000)]

linear = [('mm', 'millimeter'), 
          ('cm', 'centimeter'), 
          ('m',  'meter'), 
          ('km', 'kilometer'), 
          ('in', 'inch'), 
          ('ft', 'foot'), 
          ('yd', 'yard'), 
          ('mi', 'mile')]

angular = [('deg', 'degree'), 
           ('rad', 'radian')]

