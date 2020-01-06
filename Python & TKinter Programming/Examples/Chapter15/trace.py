#!/usr/bin/env python

# $Id: trace.py,v 1.9 1999/08/20 20:44:24 skip Exp $
#
# Copyright 1995-1997, Automatrix, Inc., all rights reserved.
# Author: Skip Montanaro
#
# Copyright 1991-1995, Stichting Mathematisch Centrum, all rights reserved.
#
# Permission to use, copy, modify, and distribute this Python software and
# its associated documentation for any purpose without fee is hereby
# granted, provided that the above copyright notice appears in all copies,
# and that both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Automatrix not be used in
# advertising or publicity pertaining to distribution of the software
# without specific, written prior permission.
#
# Summary of recent changes:
#   Added run-time display of statements being executed
#   Incorporated portability and performance fixes from Greg Stein
#   Incorporated main program from Michael Scharf

# Sample use:
#    # create a StatementCoverage object, telling it where you want output
#    t = trace.StatementCoverage('/usr/local/Automatrix/concerts/coverage')
#    # run the application or function
#    t.run('main()')
#    # generate annotated listings, excluding several system modules
#    t.list(exclude_list=['regsub.py', 'string.py', 'copy.py',
#			  'traceback.py'])

import sys, time
from string import split, rstrip

class StatementCoverage:
    # by default, any coverage files are written in the current
    # directory
    def __init__(self, dir = '.', verbose=0, dotimes=0):
	import marshal, os, stat
	self.tracedir = dir
	self.docounts = (not verbose)
	self.files = {'<string>': None}
	status = os.stat(self.tracedir)
	if not stat.S_ISDIR(status[stat.ST_MODE]):
	    import tempfile
	    d = tempfile.gettempdir()
	    sys.stderr.write('%s: %s is not a directory - using %s instead...\n' %
			     (__name__, self.tracedir, d))
	    self.tracedir = d
	    self.counts = {}

	self.counts_file = os.path.join(self.tracedir, 'counts')
	try:
	    self.counts = marshal.load(open(self.counts_file, 'rb'))
	except IOError:
	    self.counts = {}
	self.dotimes = dotimes
	self.time = time.clock()
	self.last_key = None

    # straight from profile.py
    def run(self, cmd):
	import __main__
	dict = __main__.__dict__
	self.runctx(cmd, dict, dict)

    # from profile.py, with obvious changes
    def runctx(self, cmd, globals=None, locals=None):
	if globals is None: globals = {}
	if locals is None: locals = {}
	sys.settrace(self.trace)
	try:
	    exec cmd in globals, locals
	finally:
	    sys.settrace(None)

    def runfunc(self, func, *args, **kw):
	result = None
	sys.settrace(self.trace)
	try:
	    result = apply(func, args, kw)
	finally:
	    sys.settrace(None)
	return result

    # thanks to Greg Stein for speeding this up somewhat...
    def trace(self, frame, why, arg):
	if why == 'line':
	    if self.docounts:
		if self.dotimes and self.last_key is not None:
		    # time increment is for the previous line
		    newt = time.clock()
		    count, t = self.counts[self.last_key]
		    t = t + newt - self.time
		    self.counts[self.last_key] = count, t
		    self.time = time.clock()

		# counter is for this line
		key = self.last_key = \
		      (frame.f_code.co_filename, frame.f_lineno)
		try:
		    count, t = self.counts[key]
		except KeyError:
		    count, t = (0, 0.0)
		count = count+1
		self.counts[key] = (count, t)

	    else:
		# display the current line being executed...
		fname = frame.f_code.co_filename
		line = frame.f_lineno
		files = self.files
		if fname != '<string>' and not files.has_key(fname):
		    try:
			files[fname] = map(rstrip, open(fname).readlines())
		    except IOError:
			files[fname] = None
		if files[fname] != None:
		    print '%s(%d): %s' % (split(fname, '/')[-1], line,
					 files[fname][line-1])
		else:
		    print '%s(%d): ??' % (split(fname, '/')[-1], line)
	return self.trace

    # create an annotated listing file for each Python module.
    # note that statements like
    #	 for i in range(len(foo)): foo[i] = foo[i] + 1
    # count both the for statement and the assignment statement.
    # this is only a small nit for my purposes.	 if you are
    # so inclined, feel free to correct things
    #
    # use exclude_list to exclude modules from being listed
    #
    def list(self, exclude_list=[]):
	from string import split, join, expandtabs
	import stat, sys, marshal, os, regex

	marshal.dump(self.counts, open(self.counts_file, 'wb'))

	per_file = { }
	for fname, lineno in self.counts.keys():
	    try:
		lines_hit = per_file[fname]
	    except KeyError:
		lines_hit = per_file[fname] = { }
	    lines_hit[lineno] = self.counts[(fname, lineno)]

	blank = regex.compile('[ \t\r\n]*\(\|#.*\)$')
	for fname in per_file.keys():
	    if fname == '<string>' or os.path.basename(fname) in exclude_list:
		continue

	    try:
		lines = open(fname, 'r').readlines()
	    except IOError:
		sys.stderr.write('%s: Could not open %s for reading - skipping\n' %
			     (__name__, fname))
		continue

	    lines_hit = per_file[fname]

	    # build list file name by appending 'l' to filename component of
	    # input and tacking it onto the trace directory
	    file = os.path.join(self.tracedir, os.path.basename(fname) + 'l')
	    try:
		out = open(file, 'w')
	    except IOError:
		sys.stderr.write('%s: Could not open %s for writing - skipping\n' %
					 (__name__, file))
		continue

	    for i in range(len(lines)):
		line = lines[i]

		# do the blank/comment match to try to mark more lines
		# (help the reader find stuff that hasn't been covered)
		if lines_hit.has_key(i+1):
		    count, t = lines_hit[i+1]
		    # count precedes the lines that we captured
		    if self.dotimes:
			out.write('%5d(%7.3fs): ' % (count, t))
		    else:
			out.write('%5d: ' % count)
		elif blank.match(line) != -1:
		    # blank lines and comments are preceded by dots
		    out.write('    .          ')
		else:
		    # lines preceded by no marks weren't hit
		    out.write('#'*16)
		out.write(expandtabs(lines[i], 8))

	    out.close()

def main():
    import os
    # split the args into two parts
    dir='.'
    verbose=0
    dotimes=0

    n=len(sys.argv)
    if n==1:
	sys.stderr.write("%s [-v] [-d directory] program {arg}\n"%sys.argv[0])
	sys.exit(-1)
    i=1
    while i<n:
	arg=sys.argv[i]
	if arg=='-d':
	    i=i+1
	    dir=arg=sys.argv[i]
	elif arg=='-v':
	    verbose=1
	elif arg=='-t':
	    dotimes=1
	else:
	    break
	i=i+1

    prog_argv=sys.argv[i:]
    # set the sys.argv
    sys.argv=prog_argv
    # set the first entry of path to the path of the
    # main program
    progname=prog_argv[0]
    if eval(sys.version[:3])>1.3:
	sys.path[0]=os.path.split(progname)[0]

    tracer=StatementCoverage(dir,verbose,dotimes)
    tracer.run('execfile(' + `progname` + ')')

if __name__=='__main__':
    main()

