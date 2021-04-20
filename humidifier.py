#!/usr/bin/env python3
# coding: utf-8

from zencad import *
DISK_R = 75
DISK_THICK = 1
DISK_CLEARANCE = 5
DISKS_COUNT = 10

AXIS_R = 4
SHAFT_R = AXIS_R + 4
SHAFT_CLEARANCE = 0.5
SHAFT_EXTRA_LEN = 20

ALL_CONES_EXTRA_R = 7
ALL_CONES_THICK = 5
CONES_R = DISK_R
SECOND_CONES_R = 7
SECOND_CONES_BOLT_R = 2

FIX_BEAR_R = 22
FIX_BEAR_THICK = 7
FIX_BOLT_R = 2

print(f'Gears relation {CONES_R/SECOND_CONES_R}')
def disk():
	cyl = cylinder(DISK_R, DISK_THICK)
	cyl2 = cylinder(SHAFT_R + 5, DISK_CLEARANCE)
	hole = ngon(r=SHAFT_R, n=8).extrude(DISK_CLEARANCE)
	return cyl + cyl2 - hole


def disks():
	return [disk().translate(z=i * DISK_CLEARANCE) for i in range(DISKS_COUNT)]


def shaft():
	length = DISKS_COUNT * DISK_CLEARANCE + SHAFT_EXTRA_LEN
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
	return c.translate(z=DISKS_COUNT * DISK_CLEARANCE + SHAFT_EXTRA_LEN/2)

def second_cones():
	c = _cones(SECOND_CONES_R, ALL_CONES_THICK, 1)
	return c.translate(z=DISKS_COUNT * DISK_CLEARANCE + SHAFT_EXTRA_LEN/2, x=CONES_R*2)

def fix():
	b = box(FIX_BEAR_R*2+FIX_BEAR_R, FIX_BEAR_R*2+FIX_BEAR_R*0.8, FIX_BEAR_THICK*1.3, center=True).fillet(r=2).translate(z=(FIX_BEAR_THICK+3)/-2)
	bearing = cylinder(FIX_BEAR_R, FIX_BEAR_THICK*1.1).translate(z=-FIX_BEAR_THICK*1.1)
	axis = cylinder(AXIS_R*1.1, 1000).translate(z=-500)
	bolt1 = cylinder(FIX_BOLT_R, 1000).translate(z=-500, x=FIX_BEAR_R+5, y=FIX_BEAR_R+1)
	bolt2 = cylinder(FIX_BOLT_R, 1000).translate(z=-500, x=-FIX_BEAR_R-5, y=FIX_BEAR_R+1)
	bolt3 = cylinder(FIX_BOLT_R, 1000).translate(z=-500, x=FIX_BEAR_R+5, y=-FIX_BEAR_R-1)
	bolt4 = cylinder(FIX_BOLT_R, 1000).translate(z=-500, x=-FIX_BEAR_R-5, y=-FIX_BEAR_R-1)
	return b - bearing - axis - bolt1 - bolt2 - bolt3 - bolt4

to_stl(disk(), './disk.stl', delta=0.5)
to_stl(shaft(), './shaft.stl', delta=0.5)
to_stl(cones(), './cones.stl', delta=0.5)
to_stl(second_cones(), './second_cones.stl', delta=0.5)
to_stl(stopper(), './stopper.stl', delta=0.5)
to_stl(fix(), './fix.stl', delta=0.5)

disp(disks())
disp(shaft())
disp(stopper().translate(z=shaft().bbox().zmax))
disp(cones())
disp(second_cones())
disp(fix().translate(z=shaft().bbox().zmin-50))
disp(fix().rotateX(3.1415).translate(z=shaft().bbox().zmax+50))
#disp(fix())

show()

