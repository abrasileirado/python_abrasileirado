"""
The MIT License (MIT)

Copyright 2015 Umbrella Tech.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


import re
from .exceptions import MaskException, EmptyMaskException, DVException, MaskWithoutDigitsException, MaskWithoutSpecialCharsException, MaskNotStringException, TooManyDigitsException
from abrasileirado import only_digits


PROCESSO_MASK = '9999999-99.9999.9.99.9999'
PROCESSO_RE = re.compile('^(\d{7})-?(\d{2})\.?(\d{4})\.?(\d)\.?(\d{2})\.?(\d{4})$')


def apply_mask(value, mask):
    unmask = only_digits(mask)
    zfill_value = only_digits(value).zfill(len(unmask))
    if len(unmask) != len(zfill_value):
        raise MaskException()

    result = ''
    i = 0
    for m in mask:
        if m.isdigit():
            result += zfill_value[i]
            i += 1
        else:
            result += m
    return result


def validate_masked_value(value, mask, force=True):
    masked_value = apply_mask(only_digits(value), mask) if force else value
    if len(mask) != len(masked_value):
        raise MaskException()

    for i in range(0, len(mask)):
        m = mask[i]
        v = masked_value[i]
        if (not m.isdigit() and m != v) or m.isdigit() != v.isdigit():
            raise MaskException()
    return masked_value


def validate_mask(mask):
    if not isinstance(mask, str):
        raise MaskNotStringException()

    if mask is None or mask.strip() == '':
        raise EmptyMaskException()

    unmask = only_digits(mask)

    if unmask.find('9') < 0:
        raise MaskWithoutDigitsException()

    if len(unmask) == len(mask):
        raise MaskWithoutSpecialCharsException()


def validate_mod11(unmasked_value, num_len, dvs_len):
    if num_len > 11:
        raise TooManyDigitsException()
    for v in range(dvs_len, 0, -1):
        num_dvs = num_len - v + 1
        dv = sum([i * int(unmasked_value[idx]) for idx, i in enumerate(range(num_dvs, 1, -1))]) % 11
        calculated_dv = '%d' % (11 - dv if dv >= 2 else 0,)
        if calculated_dv != unmasked_value[-v]:
            raise DVException()


def validate_dv_by_mask(value, mask, force=True, validate_dv=validate_mod11):
    if not isinstance(value, str):
        raise ValueError('O valor deve ser uma string')

    if value is None or value.strip() == '':
        raise ValueError('O valor não poder ser nulo ou uma string vazia')
    validate_mask(mask)
    unmask = only_digits(mask)
    masked_value = validate_masked_value(value, mask, force)
    unmasked_value = only_digits(masked_value)
    num_dvs = len([x for x in unmask if x == '0'])
    num_digits = len(unmask)
    validate_dv(unmasked_value, num_digits, num_dvs)
    return masked_value
