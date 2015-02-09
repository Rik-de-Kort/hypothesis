# coding=utf-8

# Copyright (C) 2013-2015 David R. MacIver (david@drmaciver.com)

# This file is part of Hypothesis (https://github.com/DRMacIver/hypothesis)

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function, unicode_literals, division

# END HEADER

from hypothesis.internal.classmap import ClassMap
import pytest


class A(object):
    pass


class B(A):
    pass


class C(A):
    pass


class D(C):
    pass


class BC(B, C):
    pass


def test_can_set_and_lookup_class():
    x = ClassMap()
    x[A] = 1
    assert x[A] == 1


def test_parent_values_will_be_used_if_child_is_not_set():
    x = ClassMap()
    x[A] = 1
    assert x[D] == 1


def test_child_values_will_be_used_if_set():
    x = ClassMap()
    x[A] = 1
    x[B] = 2
    assert x[B] == 2


def test_grand_parent_values_will_be_used_if_child_is_not_set():
    x = ClassMap()
    x[A] = 1
    assert x[B] == 1


def test_setting_child_does_not_set_parent():
    x = ClassMap()
    x[B] = 1
    with pytest.raises(KeyError):
        x[A]


def test_prefers_first_parent_in_mro():
    x = ClassMap()
    x[C] = 3
    x[B] = 2
    assert x[BC] == 2


def test_all_mappings_yields_all_mappings():
    x = ClassMap()
    x[object] = 1
    x[BC] = 2
    x[B] = 3
    x[C] = 4
    x[A] = 5
    assert list(x.all_mappings(BC)) == [2, 3, 4, 5, 1]
