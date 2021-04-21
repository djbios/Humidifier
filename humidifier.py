#!/usr/bin/env python3
# coding: utf-8

# https://101bt.ru/vozduh/xiaomi-smartmi-zhimi-air-humidifier-2/
import decimal

from zencad import *

DISK_R = 90
DISK_THICK = 1
DISK_CLEARANCE = 3
DISKS_COUNT = 36
DISK_STICK_HEIGHT = 0.8
DISK_STEP_COUNT = 8

AXIS_R = 4
SHAFT_R = AXIS_R + 4
SHAFT_CLEARANCE = 0.5
SHAFT_EXTRA_LEN = 20

ALL_CONES_EXTRA_R = 7
ALL_CONES_THICK = 5
CONES_R = DISK_R
SECOND_CONES_R = 7
SECOND_CONES_BOLT_R = 2

FIX_BEAR_R = 11
FIX_BEAR_THICK = 7
FIX_BOLT_R = 2

INFINITY = 10000
HALF_INFINITY = 500
PI = 3.14159265359

print(f'Gears relation {CONES_R / SECOND_CONES_R}')


def disk():
    cyl = cylinder(DISK_R, DISK_THICK)
    cyl2 = cylinder(SHAFT_R + 5, DISK_CLEARANCE).translate(z=DISK_THICK)
    hole = ngon(r=SHAFT_R, n=8).extrude(DISK_CLEARANCE+DISK_THICK)
    b = union(
        [box(
            1,
            DISK_R - SHAFT_R - 5,
            DISK_STICK_HEIGHT
        )
             .translate(y=SHAFT_R + 5, z=DISK_STICK_HEIGHT)
             .rotateZ(PI * x) for x in drange(0, 2, 2 / DISK_STEP_COUNT)]
    )
    b2 = union(
        [
            box(
                2,
                5,
                DISK_CLEARANCE
            )
                .rotateZ(PI / 2)
                .translate(y=DISK_R / 2, z=DISK_STICK_HEIGHT)
                .rotateZ(PI * x) for x in drange(2 / DISK_STEP_COUNT / 2, 2, 2 / DISK_STEP_COUNT)]
    )
    return cyl + cyl2 - hole + b + b2


def disks():
    return [disk().translate(z=i * (DISK_CLEARANCE+DISK_THICK)) for i in range(DISKS_COUNT)]


def shaft():
    length = DISKS_COUNT * (DISK_CLEARANCE+DISK_THICK) + SHAFT_EXTRA_LEN
    shaft = ngon(
        r=SHAFT_R - SHAFT_CLEARANCE, n=8).extrude(length - SHAFT_EXTRA_LEN / 2)
    hole = cylinder(AXIS_R, length)
    stopper = cylinder(SHAFT_R + 5, SHAFT_EXTRA_LEN / 2)
    return (shaft + stopper - hole).translate(z=-(SHAFT_EXTRA_LEN / 2))


def stopper():
    stop = cylinder(SHAFT_R + 5, SHAFT_EXTRA_LEN / 4)
    hole = cylinder(AXIS_R, SHAFT_EXTRA_LEN / 2)
    return stop - hole


def _cones(r, thick, axis_d):
    con1 = cone(r + ALL_CONES_EXTRA_R, r, thick / 2)
    con2 = cone(r, r + ALL_CONES_EXTRA_R, thick / 2).translate(z=thick / 2)
    hole = cylinder(axis_d, thick)
    return con1 + con2 - hole


def cones():
    c = _cones(CONES_R, ALL_CONES_THICK, AXIS_R)
    return c


def second_cones():
    c = _cones(SECOND_CONES_R, ALL_CONES_THICK, 1)
    return c.translate(z=DISKS_COUNT * DISK_CLEARANCE + SHAFT_EXTRA_LEN / 2, x=CONES_R * 2)


def fix():
    b = box(
        FIX_BEAR_R * 2 + FIX_BEAR_R,
        FIX_BEAR_R * 2 + FIX_BEAR_R * 0.8,
        FIX_BEAR_THICK * 1.3, center=True
    ).fillet(r=2).translate(z=(FIX_BEAR_THICK + 3) / -2)
    bearing = cylinder(FIX_BEAR_R, FIX_BEAR_THICK).translate(z=-FIX_BEAR_THICK)
    axis = cylinder(AXIS_R * 1.1, INFINITY).translate(z=-HALF_INFINITY)
    bc = 2
    bolt1 = cylinder(FIX_BOLT_R, INFINITY).translate(z=-HALF_INFINITY, x=b.bbox().xmax-FIX_BOLT_R-bc, y=b.bbox().ymax-FIX_BOLT_R-bc)
    bolt2 = cylinder(FIX_BOLT_R, INFINITY).translate(z=-HALF_INFINITY, x=b.bbox().xmin+FIX_BOLT_R+bc, y=b.bbox().ymax-FIX_BOLT_R-bc)
    bolt3 = cylinder(FIX_BOLT_R, INFINITY).translate(z=-HALF_INFINITY, x=b.bbox().xmax-FIX_BOLT_R-bc, y=b.bbox().ymin+FIX_BOLT_R+bc)
    bolt4 = cylinder(FIX_BOLT_R, INFINITY).translate(z=-HALF_INFINITY, x=b.bbox().xmin+FIX_BOLT_R+bc, y=b.bbox().ymin+FIX_BOLT_R+bc)
    return b - bearing - axis - bolt1 - bolt2 - bolt3 - bolt4


def drange(x, y, jump):
    while x < y:
        yield float(x)
        x += jump


def assembled_drum():
    return union(disks() + [
        shaft(),
        stopper().translate(z=shaft().bbox().zmax)
    ])


to_stl(assembled_drum(), './drum.stl', delta=0.5)
to_stl(cones(), './cones.stl', delta=0.5)
to_stl(second_cones(), './second_cones.stl', delta=0.5)
to_stl(fix(), './fix.stl', delta=0.5)

disp(assembled_drum())
disp(cones().translate(z=DISKS_COUNT * (DISK_CLEARANCE+DISK_THICK) + SHAFT_EXTRA_LEN / 2))
disp(second_cones())
disp(fix().translate(z=shaft().bbox().zmin-50))
disp(fix().rotateX(PI).translate(z=shaft().bbox().zmax+50))

#disp(fix())
#disp(disk())
show()
