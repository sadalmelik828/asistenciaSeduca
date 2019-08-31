# -*- encoding: utf-8 -*-

DATE_FORMAT = r'j \de F \de Y'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = r'j \de F \de Y \a \l\a\s H:i'
YEAR_MONTH_FORMAT = r'F \de Y'
MONTH_DAY_FORMAT = r'j \de F'
SHORT_DATE_FORMAT = 'Y-m-d'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i'
FIRST_DAY_OF_WEEK = 1 # Lunes
DATE_INPUT_FORMATS = (
    # '2009-12-31', '09-12-31'
    '%Y-%m-%d', '%y-%m-%d'
)
TIME_INPUT_FORMATS = (
    # '14:30:59', '14:30'
    '%H:%M:%S', '%H:%M'
)
DATETIME_INPUT_FORMATS = (
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M',
    '%y-%m-%d %H:%M:%S',
    '%y-%m-%d %H:%M',
)
DECIMAL_SEPARATOR = ','
THOUSAND_SEPARATOR = '.'
NUMBER_GROUPING = 3