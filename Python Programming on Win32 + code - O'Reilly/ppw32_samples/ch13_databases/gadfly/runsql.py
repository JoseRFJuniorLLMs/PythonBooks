
"""Simple script to run sql (query) commands.

usage
   runsql [dbname] [dbdirectory] < commandfile

If dbname and dbdirectory are absent, they are
taken from environment variables DBNAME and DBDIRECTORY.

if GADFLYPATH env. var. is present it is added to the Python Path.

commands are split on semicolons (not intelligently)
-- thus comments and string literals cannot contain
semicolons.

Updates are not committed -- not stored permanently.
"""
    
def runfile(file, dbname, dbdir):
    print "running sql commands ", dbname, dbdir
    from string import split, join
    from gadfly import gadfly
    connect = gadfly(dbname, dbdir)
    cursor = connect.cursor()
    data = file.read()
    from string import split, strip
    commands = split(data, ";")
    for c in commands:
        if not strip(c): continue
        print "COMMAND:"
        data = str(c)
        pdata = "  "+join(split(c, "\n"), "\n  ")
        print pdata
        print
        cursor.execute(data)
        print cursor.pp()
        print
    #connect.commit()
    connect.close()

# c:\python\python relalg.py ratest.txt

if __name__=="__main__":
    import sys, os
    argv = sys.argv
    env = os.environ
    done = 0
    try:
        commandfile = sys.stdin
        largv = len(argv)
        if largv>1:
            dbname = argv[1]
        else:
            dbname = env["DBNAME"]
        if largv>2:
            dbdir = argv[2]
        else:
            dbdir = env["DBDIRECTORY"]
        if env.has_key("GADFLYPATH"):
            sys.path.append(env["GADFLYPATH"])
        runfile(commandfile, dbname, dbdir)
        done = 1
    finally:
        if not done:
           print "abnormal termination"; print
           print __doc__


