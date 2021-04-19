#!/usr/bin/env python3
# coding: utf-8

from zencad import *
DISK_DIAM = 150
DISK_THICK = 1
DISK_CLEARANCE = 5
DISKS_COUNT = 10

AXIS_DIAM = 6
SHAFT_DIAM = AXIS_DIAM + 4
SHAFT_CLEARANCE = 0.5
SHAFT_EXTRA_LEN = 20

CONES_R = 50
CONES_BOTH_THICK = 10

SECOND_CONES_R = 20
SECOND_CONES_BOTH_THICK = 10


def disk():
	cyl = cylinder(DISK_DIAM, DISK_THICK)
	cyl2 = cylinder(SHAFT_DIAM + 5, DISK_CLEARANCE)
	hole = ngon(r=SHAFT_DIAM, n=8).extrude(DISK_CLEARANCE)
	return cyl + cyl2 - hole


def disks():
	return [disk().translate(z=i * DISK_CLEARANCE) for i in range(DISKS_COUNT)]


def shaft():
	length = DISKS_COUNT * DISK_CLEARANCE + SHAFT_EXTRA_LEN
	shaft = ngon(
		r=SHAFT_DIAM - SHAFT_CLEARANCE, n=8).extrude(length-SHAFT_EXTRA_LEN/2)
	hole = cylinder(AXIS_DIAM, length)
	stopper = cylinder(SHAFT_DIAM + 5, SHAFT_EXTRA_LEN / 2)
	return (shaft + stopper - hole).translate(z=-(SHAFT_EXTRA_LEN / 2))


def stopper():
	stop = cylinder(SHAFT_DIAM + 5, SHAFT_EXTRA_LEN / 4)
	hole = cylinder(AXIS_DIAM, SHAFT_EXTRA_LEN / 2)
	return stop - hole

def _cones(r, thick, axis_d):
	con1 = cone(r + 5, r, thick / 2)
	con2 = cone(r, r + 5, thick / 2).translate(z=thick / 2)
	hole = cylinder(axis_d, thick)
	return con1 + con2 - hole

def cones():
	c = _cones(CONES_R, CONES_BOTH_THICK, AXIS_DIAM)
	return c.translate(z=DISKS_COUNT * DISK_CLEARANCE + SHAFT_EXTRA_LEN/2)

def second_cones():
	c = _cones(SECOND_CONES_R, SECOND_CONES_BOTH_THICK, 1)
	return c.translate(z=DISKS_COUNT * DISK_CLEARANCE + SHAFT_EXTRA_LEN/2, x=CONES_R*2)

to_stl(disk(), './disk.stl', delta=0.5)
to_stl(shaft(), './shaft.stl', delta=0.5)
to_stl(cones(), './cones.stl', delta=0.5)
to_stl(second_cones(), './second_cones.stl', delta=0.5)
to_stl(stopper(), './stopper.stl', delta=0.5)

disp(disks())
disp(shaft())
disp(stopper().translate(z=shaft().bbox().zmax))
disp(cones())
disp(second_cones())
show()

