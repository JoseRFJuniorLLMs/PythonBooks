
# script for test semantic generation

import sqlgen
import sqlbind

def go():
    global sql
    sql = sqlgen.BuildSQL()
    sql = sqlbind.BindRules(sql)
    db()
    return sql
    
from sqlsem import Database0, Relation0, File_Storage0, Parse_Context, tp

def ll(d, b):
    return tp(DRINKER=d, BEER=b)
def ff(d, b):
    return tp(DRINKER=d, BAR=b)
def ss(ba, be):
    return tp(BAR=ba, BEER=be)
    
def db():
    global database
    likes = Relation0( ["DRINKER", "BEER"],
      [  ll("john", "bud"),
         ll("jane", "mickies"),
      ]
    )
    serves = Relation0( ["BAR", "BEER"],
      [  ss("cheers", "bud"),
         ss("joes", "samaddams"),
      ]
    )
    frequents = Relation0( ["DRINKER", "BAR"],
      [  ff("john", "cheers"),
         ff("jane", "cheers"),
         ff("john", "joes"),
         ff("joe", "joes"),
      ]
    )
    print likes; print
    print serves; print
    print frequents; print
    database = Database0()
    database["FREQUENTS"]=frequents
    database["LIKES"] = likes
    database["SERVES"] = serves
    print database
    fs = File_Storage0("fls", "dbtest")
    fs.dump(database)
    return database
    
def dbreload():
    global database
    fs = File_Storage0("fls", "dbtest")
    database = fs.load()
    return database
    
def parse(str, dyn=None):
    print str
    context = Parse_Context()
    [ss] = sql.DoParse1(str, context)
    print "parsed"
    print ss
    ss = ss.relbind(database)
    print "bound"
    print ss
    try:
        print ss.__class__
    except:
        pass
    else:
        print "evaluated"
        return ss.eval(dyn)    
    
def parsetests():
    print parse("select drinker from likes where beer='bud'")
    print parse("select distinct * from likes where drinker='jane'")
    print parse("select distinct * from likes where not drinker='jane'")
    print parse(
     "select drinker from frequents where drinker='john' or drinker='jane'")
    print parse("""
     select l.drinker, f.bar, s.beer
     from likes l, serves s, frequents f
     where l.drinker=f.drinker and s.beer=l.beer and f.bar=s.bar""")

    print parse("""
      select *
      from frequents as f, likes as l
      where f.drinker=l.drinker""")
    print parse("""
      select *
      from frequents as f, likes as l
      where not f.drinker=l.drinker""")
    print parse(
      "select * from frequents, likes where likes.drinker=frequents.drinker")
    print parse(
      "select * from frequents where drinker=?", ("john",))
    print parse("create table xx (yy varchar, zz varchar)")
    print parse("insert into xx (zz, yy) select beer, drinker from likes")
    print parse("insert into xx (yy, zz) values ('samaddams', 'bar')")
    print parse("""select * from xx where not exists
                    (select * from likes where zz=beer and yy=drinker)""")
    print parse("""delete from xx
                   where zz='cheers' """)
    print parse("""update xx set zz='sams' where zz='samaddams' """)
    print parse("select * from xx")
    print parse("drop table xx")
    print parse("""select *
      			from frequents as f, serves as s
   				where f.bar = s.bar and
     				not exists(
       				select l.drinker
       				from likes l
       				where l.drinker=f.drinker and f.beer=l.beer)""")

    
                    