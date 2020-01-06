
""" sql semantics 

A simple tuple (in core) is a (kj)dictionary name->value

A bound tuple is a graph of equality constraints
    (relname, att) --> (relname, att)
    and a collection of assignments
    (relname, att) --> value
    in closed (x.close()) form should satisfy the constraints that
    two equated (r,a) pairs should have equal values.
    If inconsistent x.Clean() should return None else x,
       but is only accurate after x.close()
       
For now a database is a simple dictionary
    relname --> list of tuples
    
"""

# use kjbuckets builtin if available
try:
    import kjbucketsxxx # force an error for now
except ImportError:
    import kjbuckets0
    kjbuckets = kjbuckets0
    
Tuple = kjbuckets.kjDict
Graph = kjbuckets.kjGraph
Set = kjbuckets.kjSet
    
# operations on simple tuples, mostly from kjbuckets

def maketuple(thing):
    """try to make a tuple from thing.
       thing should be a dictionary or sequence of (name, value)
       or other tuple."""
    from types import DictType
    if type(thing)==DictType:
       return Tuple(thing.items() )
    else: return Tuple(thing)    

# stuff for bound tuples.

def hashjoin(btseq, relname, tuples):
    """attempt a hash-join over btseq with relname bound to tuples.
       No support for null values yet."""
    if not btseq: return []
    result = []
    witness = btseq[0]
    (batts, atts) = witness.known(relname)
    atts = tuple(atts)
    if not batts:
       # cross product
       for t in tuples:
           new = BoundTuple()
           new.bind(relname, t)
           for bt in btseq:
               result.append(bt + new)
    else:
       # hash join
       if len(btseq)<len(tuples):
          # hash the btseq
          btindex = kjbuckets.kjGraph()
          for i in xrange(len(btseq)):
              bt = btseq[i]
              its = bt.getitems(batts)
              #print "items", its
              # keep sequence number to preserve redundancies
              btindex[its] = (i, bt)
          for t in tuples:
              its = t.dump(atts)
              n = btindex.neighbors(its)
              if n:
                 new = BoundTuple()
                 new.bind(relname, t)
                 for (i, bt) in n:
                     result.append(bt + new)
       else:
          # hash the tuples
          tindex = kjbuckets.kjGraph()
          for i in xrange(len(tuples)):
              t = tuples[i]
              its = t.dump(atts)
              new = BoundTuple()
              new.bind(relname, t)
              # keep seq num...
              tindex[its] = (i, new)
          for bt in btseq:
              its = bt.getitems(batts)
              n = tindex.neighbors(its)
              for (i, new) in n:
                  result.append(bt + new)
    return filter(None, result)

class BoundTuple:

   clean = 1  # false if inconsistent
   closed = 0 # true if equality constraints inferred

   def __init__(self, **bindings):
       """bindings are name-->simpletuple associations."""
       self.eqs = Graph()
       self.assns = Tuple()
       for (name, simpletuple) in bindings.items():
           self.bind(name, simpletuple)
           
   def relbind(self, dict, db):
       """return bindings of self wrt dict rel-->att"""
       result = BoundTuple()
       e2 = result.eqs
       a2 = result.assns
       for ((a,b), (c,d)) in self.eqs.items():
           if a is None:
              try:
                 a = dict[b]
              except KeyError:
                 raise NameError, `b`+": ambiguous or unknown attribute"
           if c is None:
              try:
                 c = dict[d]
              except KeyError:
                 raise NameError, `d`+": ambiguous or unknown attribute"
           e2[(a,b)] = (c,d)
       for ((a,b), v) in self.assns.items():
           if a is None:
              try:
                 a = dict[b]
              except KeyError:
                 raise NameError, `b`+": ambiguous or unknown attribute"
           a2[(a,b)] = v
       result.closed = self.closed
       result.clean = self.clean
       return result
           
   def known(self, relname):
       """return ([(relname, a1), ...], [a1, ...])
          for attributes ai of relname known in self."""
       atts = []
       batts = []
       for x in self.assns.keys():
           (r,a) = x
           if r==relname:
              batts.append(x)
              atts.append(a)
       return (batts, atts)
                 
   def relorder(self, db, allrels):
       """based on known constraints, pick an
          ordering for materializing relations.
          db is database (ignored currently)
          allrels is all relations to include (list)."""
       order = []
       eqs = self.eqs
       assns = self.assns
       kjSet = kjbuckets.kjSet
       kjGraph = kjbuckets.kjGraph
       pinned = kjSet()
       needed = kjSet(allrels)
       for (r,a) in assns.keys():
           pinned[r]=r # pinned if some value known
       pinned = pinned & needed
       related = kjGraph()
       for ( (r1, a1), (r2, a2) ) in eqs.items():
           related[r1]=r2 # related if equated to other
           related[r2]=r1 # redundant if closed.
       related = needed * related * needed
       chosen = kjSet()
       pr = kjSet(related) & pinned
       # choose first victim
       if pr:
          choice = pr.choose_key()
       elif pinned:
          choice = pinned.choose_key()
       elif related:
          choice = related.choose_key()
       else:
          return allrels[:] # give up!
       while pinned or related:
          order.append(choice)
          chosen[choice] = 1
          if pinned.has_key(choice):
             del pinned[choice]
          if related.has_key(choice):
             del related[choice]
          nexts = related * chosen
          if nexts:
             # prefer a relation related to chosen
             choice = nexts.choose_key()
          elif pinned:
             # otherwise one that is pinned
             choice = pinned.choose_key()
          elif related:
             # otherwise one that relates to something...
             choice = related.choose_key()
       others = kjSet(allrels) - chosen
       if others: order = order + others.keys()
       return order
           
   def domain(self):
       kjSet = kjbuckets.kjSet
       return kjSet(self.eqs) + kjSet(self.assns)
           
   def bind(self, name, simpletuple):
       """bind name --> simpletuple in self."""
       a = self.assns
       for (att, value) in simpletuple.items():
           a[ (name, att) ] = value
           
   def __repr__(self):
       from string import join
       result = []
       for ( (name, att), value) in self.assns.items():
           result.append( "%s.%s=%s" % (name, att, `value`) )
       for ( (name, att), (name2, att2) ) in self.eqs.items():
           result.append( "%s.%s=%s.%s" % (name, att, name2, att2) )
       if self.clean:
          if not result: return "TRUE"
       else:
          result.insert(0, "FALSE")
       result.sort()
       return join(result, " & ")
           
   def equate(self, equalities):
       """add equalities to self, only if not closed.
          equalities should be seq of ( (name, att), (name, att) )
          """
       if self.closed: raise ValueError, "cannot add equalities! Closed!"
       e = self.eqs
       for (a, b) in equalities:
           e[a] = b
           
   def close(self):
       """infer equalities, if consistent.
          only recompute equality closure if not previously closed.
          return None on inconsistency.
       """
       neweqs = self.eqs
       if not self.closed:
          self.eqs = neweqs = (neweqs + ~neweqs).tclosure() # sym, trans closure
          self.closed = 1
       # add trivial equalities to self
       for x in self.assns.keys():
           if not neweqs.member(x,x):
              neweqs[x] = x
       newassns = self.assns.remap(neweqs)
       if newassns is not None and self.clean:
          self.assns = newassns
          #self.clean = 1
          return self
       else:
          self.clean = 0
          return None
          
   def share_eqs(self):
       """make clone of self that shares equalities, closure.
          note: will share future side effects to eqs too."""
       result = BoundTuple()
       result.eqs = self.eqs
       result.closed = self.closed
       return result
          
   def Clean(self):
       """return self if apparently consistent, else None"""
       if self.clean: return self
       return None
       
   def __add__(self, other):
       """combine self with other, return closure."""
       result = self.share_eqs()
       se = self.eqs
       oe = other.eqs
       if (se is not oe) and (se != oe):
          result.eqs = se + oe
          result.closed = 0
       ra= result.assns = self.assns + other.assns
       result.clean = result.clean and (ra.Clean() is not None)
       return result.close()
       
   def __and__(self, other):
      """return closed constraints common to self and other."""
      result = BoundTuple()
      se = self.eqs
      oe = other.eqs
      if (se is oe) or (se == oe):
         result.eqs = self.eqs
         result.closed = self.closed
      else:
         result.eqs = self.eqs & other.eqs
      result.assns = self.assns & other.assns
      result.clean = self.clean and other.clean
      return result.close()
      
   def __sub__(self, other):
      """return constraints in self, not in other.
         works best if self, other are closed."""
      # need to nuke trivial eqs
      result = BoundTuple()
      eqs = self.eqs - other.eqs
      k = eqs.keys()
      result.eqs = eqs - kjbuckets.kjGraph( map(None, k, k) )
      result.assns = self.assns - other.assns
      return result.close()
       
   def __getitem__(self, item):
      """retrieve value for item==(rname,att)
         note: this may be inlined for speed!"""
      return self.assns[item]
      
   def getitems(self, items):
      """retrieve values for items=[(rname, att),...]
         in conformance with kjDict.dump a list of
         length one returns just the map, not a list
         of length one, otherwise a tuple"""
      if len(items)==1:
         return self.assns[items[0]]
      result = []
      a = self.assns
      ap = result.append
      for item in items:
          ap(a[item])
      return tuple(result)
      
   def __hash__(self):
      # note: equalities don't enter into hash computation!
      # (some may be spurious)
      self.close()
      return hash(self.assns)# ^ hash(self.eqs)
      
   def __cmp__(self, other):
       sa = self.assns
       oa = other.assns
       test = cmp(sa, oa)
       if test: return test
       # check equalities, is there an equality fault?
       se = self.eqs
       oe = other.eqs
       for (a,b) in ( (se-oe) + (oe-se) ).items():
           try:
              if sa[a]!=oa[b]:
                 return cmp(se, oe)
           except KeyError:
              return cmp(se, oe)
       return 0
      
   def trivial(self):
      return not(self.assns or self.eqs)
      
class BoundExpression:
   """superclass for all bound expressions.
      except where overloaded expressions are binary
      with self.left and self.right
   """
   
   def __init__(self, left, right):
       self.left = left
       self.right = right
   
   # eventually add converters...
   def equate(self,other):
       """return predicate equating self and other.
          Overload for special cases, please!"""
       return NontrivialEqPred(self, other)
       
   def attribute(self):
       return (None, `self`)
       
   def le(self, other):
       """predicate self<=other"""
       return LessEqPred(self, other)
   
   # these should be overridden for 2 const case someday...
   def lt(self, other):
       """predicate self<other"""
       return LessPred(self, other)
       
   def __coerce__(self, other):
       return (self, other)
       
   def __add__(self, other):
       return BoundAddition(self, other)
       
   def __sub__(self, other):
       return BoundSubtraction(self, other)
       
   def __mul__(self, other):
       return BoundMultiplication(self, other)
       
   def __neg__(self):
       return BoundMinus(self)
       
   def __div__(self, other):
       return BoundDivision(self, other)
       
   def relbind(self, dict, db):
       Class = self.__class__
       return Class(self.left.relbind(dict, db), self.right.relbind(dict, db))
   
   def __repr__(self):
       return "(%s)%s(%s)" % (self.left, self.op, self.right)
       
   def domain(self):
       return self.left.domain() + self.right.domain()
   # always overload value
   
class BoundMinus(BoundExpression):
   def __init__(self, thing):
       self.thing = thing
   def __repr__(self):
       return "-(%s)" % (thing,)
   def value(self, context):
       return - self.thing.value(context)
   
class BoundAddition(BoundExpression):
   """promised addition."""
   op = "+"
   def value(self, context):
       return self.left.value(context) + self.right.value(context)
   
class BoundSubtraction(BoundExpression):
   """promised subtraction."""
   op = "-"
   def value(self, context):
       return self.left.value(context) - self.right.value(context)
   
class BoundMultiplication(BoundExpression):
   """promised multiplication."""
   op = "*"
   def value(self, context):
       return self.left.value(context) * self.right.value(context)
   
class BoundDivision(BoundExpression):
   """promised division."""
   op = "/"
   def value(self, context):
       return self.left.value(context) / self.right.value(context)
       
class BoundAttribute(BoundExpression):
   """bound attribute: initialize with relname=None if
      implicit."""
      
   def __init__(self, rel, name):
       self.rel = rel
       self.name = name
       
   def relbind(self, dict, db):
       if self.rel is not None: return self
       name = self.name
       try:
           rel = dict[name]
       except KeyError:
           raise NameError, `name` + ": unknown or ambiguous"
       return BoundAttribute(rel, name)
       
   def __repr__(self):
       return "%s.%s" % (self.rel, self.name)
       
   def attribute(self):
       """return (rename, attribute) for self."""
       return (self.rel, self.name)
       
   def domain(self):
       return [ (self.rel, self.name) ]
       
   def value(self, context):
       """return value of self in context (bound tuple)."""
       #print "value of ", self, "in", context
       return context[ (self.rel, self.name) ]
       
   def equate(self, other):
       oc = other.__class__
       if oc==BoundAttribute:
          result = BoundTuple()
          result.equate([(self.attribute(), other.attribute())])
          return BTPredicate(result)
       elif oc==Constant:
          result = BoundTuple()
          result.assns[ self.attribute() ] = other.value(None)
          return BTPredicate(result)
       else:
          return NontrivialEqPred(self, other)
          
class Constant(BoundExpression):
   def __init__(self, value):
       self.value0 = value
       
   def domain(self):
       return []
       
   def __add__(self, other):
       if other.__class__==Constant:
          return Constant(self.value0 + other.value0)
       return BoundAddition(self, other)
       
   def __sub__(self, other):
       if other.__class__==Constant:
          return Constant(self.value0 - other.value0)
       return BoundSubtraction(self, other)
       
   def __mul__(self, other):
       if other.__class__==Constant:
          return Constant(self.value0 * other.value0)
       return BoundMultiplication(self, other)
       
   def __neg__(self):
       return Constant(-self.value0)
       
   def __div__(self, other):
       if other.__class__==Constant:
          return Constant(self.value0 / other.value0)
       return BoundDivision(self, other)

   def relbind(self, dict, db):
       return self
       
   def value(self, context):
       """return the constant value associated with self."""
       return self.value0
       
   def equate(self,other):
       if other.__class__==Constant:
          if other.value0 == self.value0:
             return BTPredicate() #true
          else:
             return ~BTPredicate() #false
       else:
          return other.equate(self)
          
   def attribute(self):
       """invent a pair to identify a constant"""
       return ('unbound', `self`)
       
   def __repr__(self):
       return "<const %s at %s>" % (self.value0, id(self))
          
class TupleCollector:
   """Translate a sequence of BoundTuples to simple tuples.
      (for implementing the select list of a SELECT).
   """
   def __init__(self):
       self.final = None
       self.order = []
       self.attorder = []
       
   def __repr__(self):
       l = []
       for (att, exp) in self.order:
           l.append( "%s as %s" % (exp, att) )
       from string import join
       return join(l, ", ")
       
   def addbinding(self, attribute, expression):
       """bind att-->expression."""
       self.order.append((attribute, expression) )
       self.attorder.append(attribute )
       
   def map(self, btlist):
       """remap btlist by self. return (tuplelist, attorder)"""
       result = list(btlist)
       order = self.order
       for i in xrange(len(result)):
           trans = Tuple()
           this = result[i]
           for (att, exp) in order:
               trans[att] = exp.value(this)
           result[i] = trans
       return (result, self.attorder)
       
   def relbind(self, dict, db):
       """disambiguate missing rel names if possible.
          also choose output names appropriately."""
       # CURRENTLY THIS IS AN "IN PLACE" OPERATION
       order = self.order
       attorder = self.attorder
       known = {}
       for i in xrange(len(order)):
           (att, exp) = order[i]
           #print exp
           exp = exp.relbind(dict, db)
           if att is None:
              # choose a name for this column
              #print exp
              (rname, aname) = exp.attribute()
              if known.has_key(aname):
                 both = rname+"."+aname
                 att = both
                 count = 0
                 while known.has_key(att):
                    # crank away!
                    count = count+1
                    att = both+"."+`count`
              else:
                 att = aname
           else:
              if known.has_key(att):
                 raise NameError, `att`+" ambiguous in select list"
           order[i] = (att, exp)
           attorder[i] = att
           known[att] = att
       return self

class BTPredicate:
   """superclass for bound tuple predicates.
      Eventually should be modified to use "compile" for speed
      to generate an "inlined" evaluation function.
      self(bt) returns bt with additional equality constraints
      (possible) or None if predicate fails."""
      
   false = 0
   constraints = None
      
   def __init__(self, constraints=None):
       """default interpretation: True."""
       if constraints is not None:
          self.constraints = constraints.close()
          
   def relbind(self, dict, db):
       c = self.constraints
       if c is None: return self
       return BTPredicate( self.constraints.relbind(dict, db) )
          
   def evaluate(self, db, relnames):
       """evaluate the predicate over database bindings."""
       # pretty simple strategy right now...
       ### need to do something about all/distinct...
       c = self.constraints
       if c is None:
          c = BoundTuple()
       order = c.relorder(db, relnames)
       if not order:
          raise ValueError, "attempt to evaluate over no relations: "+`relnames`
       result = [c]
       for r in order:
           result = hashjoin(result, r, db[r])
       if self.__class__==BTPredicate:
          # if it's just equality conjunction, we're done
          return result
       else:
          # apply additional constraints
          return self(result)
          
   def domain(self):
       c = self.constraints
       kjSet = kjbuckets.kjSet
       if c is None: return kjSet()
       return c.domain()
       
   def __repr__(self):
       if self.false: return "FALSE"
       c = self.constraints
       if c is None: c = "true"
       return "[pred](%s)" % c
          
   def detrivialize(self):
       """hook added to allow elimination of trivialities
          return None if completely true, or simpler form
          or self, if no simplification is possible."""
       if self.false: return self
       if not self.constraints: return None
       return self
          
   def negated_constraints(self):
       """equality constraints always false of satisfactory tuple."""
       return BoundTuple() # there aren't any
       
   def __call__(self, boundtuples):
       """apply self to sequence of bound tuples.
          return copy of boundtuples with false results
          replaced by 0!  Input may have 0's!"""
       lbt = len(boundtuples)
       if self.false: return [0] * lbt
       c = self.constraints
       if c is None or not c:
          result = boundtuples[:] # no constraints
       else:
          result = boundtuples[:]
          for i in xrange(lbt):
              this = boundtuples[i]
              #print "comparing", self, "to", this
              if this==0: continue
              this = this + c
              if this is None or not this.clean:
                 result[i] = 0
       return result
          
   def __and__(self, other):
       """NOTE: all subclasses must define an __and__!!!"""
       #print "BTPredicate.__and__", (self, other)
       if self.__class__==BTPredicate and other.__class__==BTPredicate:
          c = self.constraints
          o = other.constraints
          if c is None: return other
          if o is None: return self
          if self.false: return self
          if other.false: return other
          # optimization for simple constraints
          all = (c+o)
          result = BTPredicate( all ) # all constraints
          if all is None: result.false = 1
       else:
          result = other & self
       return result
       
   def __or__(self, other):
       if self.__class__==BTPredicate and other.__class__==BTPredicate:
          c = self.constraints
          o = other.constraints
          if c is None: return self # true dominates
          if o is None: return other
          if other.false: return self
          if self.false: return other
          if self == other: return self
       result = BTor_pred([self, other])
       return result
       
   def __invert__(self):
       if self.false:
          return BTPredicate()
       if not self.constraints:
          result = BTPredicate()
          result.false = 1
          return result
       return BTnot_pred(self)
       
   def __cmp__(self, other):
       if other.__class__!=self.__class__:
          return __cmp__(self.__class__, other.__class__)
       if self.false and other.false: return 0
       return cmp(self.constraints, other.constraints)
       
   def __hash__(self):
       if self.false: return 11111
       return hash(self.constraints)
       
class BTor_pred(BTPredicate):

   def __init__(self, members):
       # replace any OR in members with its members
       for m in members[:]:
           if m.__class__==BTor_pred:
              members.remove(m)
              members = members + m.members
       members = self.members = kjbuckets.kjSet(members).items()
       for m in members[:]:
           if m.false: members.remove(m)
       self.constraints = None # common constraints
       if members:
          # common constraints are those in all members
          constraints = members[0].constraints
          for m in members[1:]:
              mc = m.constraints
              if not constraints or not mc:
                 constraints = None
                 break
              constraints = constraints & mc
          self.constraints = constraints
          
   def relbind(self, dict, db):
       ms = []
       for m in self.members:
           ms.append( m.relbind(dict, db) )
       return BTor_pred(ms)
          
   def domain(self):
       all = BTPredicate.domain(self).items()
       for x in self.members:
           all = all + x.domain().items()
       return kjbuckets.kjSet(all)
       
   def __repr__(self):
       c = self.constraints
       m = self.members
       mr = map(repr, m)
       from string import join
       mr.sort()
       mr = join(mr, " | ")
       if not mr: mr = "FALSE_OR"
       if c:
          mr = "[disj](%s and %s)" % (c, mr)
       return mr

   def detrivialize(self):
       """hook added to allow elimination of trivialities
          return None if completely true, or simpler form
          or self, if no simplification is possible."""
       ms = self.members
       for i in xrange(len(ms)):
           ms[i] = ms[i].detrivialize()
       # now suck out subordinate ors
       someor = None
       for m in ms:
           if m.__class__== BTor_pred:
              someor = m
              ms.remove(m)
              break
       if someor is not None:
           result = someor
           for m in ms:
               result = result + m
           return result.detrivialize()
       allfalse = 1
       for m in ms:
           if m is None: allfalse=0; break # true member
           allfalse = allfalse & m.false
       if allfalse: return ~BTPredicate() # boundary case
       ms[:] = filter(None, ms)
       if not ms: return None # all true.
       ms[:] = kjbuckets.kjSet(ms).items()
       if len(ms)==1: return ms[0] # or of 1
       return self           

   def __call__(self, boundtuples):
       # apply common constraints first
       lbt = len(boundtuples)
       # boundary case for or is false
       members = self.members
       if not members:
          return [0] * lbt
       current = BTPredicate.__call__(self, boundtuples)
       # now apply first alternative
       alt1 = members[0](current)
       # determine questionables
       questionables = current[:]
       rng = xrange(len(current))
       for i in rng:
           if alt1[i]!=0:
              questionables[i]=0
       # now test other alternatives
       #print "alt1", members[0]
       #for x in alt1: 
           #print x
       for m in self.members[1:]:
           #print "questionables", m
           #for x in questionables:
               #print x
           passm = m(questionables)
           for i in rng:
               test = passm[i]
               if test!=0:
                  questionables[i] = 0
                  alt1[i] = test
       return alt1

   def negated_constraints(self):
       """the negated constraints of an OR are
          the negated constraints of *all* members"""
       ms = self.members
       result = ms.negated_constraints()
       for m in ms[1:]:
           if not result: return result
           mc = m.negated_constraints()
           if not mc: return mc
           result = result & mc
       return result
       
   def __and__(self, other):
       """push "and" down"""
       newmembers = self.members[:]
       for i in xrange(len(newmembers)):
           newmembers[i] = newmembers[i] & other
       return BTor_pred(newmembers)
       
   def __or__(self, other):
       """collapse two ors, otherwise just add new member"""
       if self.__class__==BTor_pred and other.__class__==BTor_pred:
          return BTor_pred(self.members+other.members)
       return BTor_pred(self.members + [other])
       
   def __invert__(self):
       """translate to and-not"""
       ms = self.members
       if not ms: return BTPredicate() # boundary case
       result = ~ms[0]
       for m in ms[1:]:
           result = result & ~m
       return result
       
   def __cmp__(self, other):
       if other.__class__!=self.__class__:
          return __cmp__(self.__class__, other.__class__)
       kjSet = kjbuckets.kjSet
       return cmp(kjSet(self.members), kjSet(other.members))
       
   def __hash__(self):
       return hash(kjbuckets.kjSet(self.members))
       
class BTnot_pred(BTPredicate):

   def __init__(self, thing):
       self.negated = thing
       self.constraints = thing.negated_constraints()
       
   def relbind(self, dict, db):
       return BTnot_pred( self.negated.relbind(dict, db) )
       
   def domain(self):
       return BTPredicate.domain(self) + self.negated.domain()
       
   def __repr__(self):
       c = self.constraints
       n = self.negated
       r = "(NOT %s)" % n
       if c: r = "[neg](%s & %s)" % (c, r)
       return r

   def detrivialize(self):
       """hook added to allow elimination of trivialities
          return None if completely true, or simpler form
          or self, if no simplification is possible."""
       # first, fix or/and/not precedence
       thing = self.negated
       if thing.__class__ == BTnot_pred:
          return thing.negated.detrivialize()
       if thing.__class__ == BTor_pred:
          # translate to and_not
          members = thing.members[:]
          for i in xrange(len(members)):
              members[i] = ~members[i]
          result = BTand_pred(members)
          return result.detrivialize()
       if thing.__class__ == BTand_pred:
          # translate to or_not
          members = thing.members[:]
          c = thing.constraints # precondition
          if c is not None:
             members.append(BTPredicate(c))
          for i in xrange(len(members)):
              members[i] = ~members[i]
          result = BTor_pred(members)
          return result.detrivialize()
       self.negated = thing = self.negated.detrivialize()
       if thing is None: return ~BTPredicate() # uniquely false
       if thing.false: return None # uniquely true
       return self

   def __call__(self, boundtuples):
       current = BTPredicate.__call__(self, boundtuples)
       omit = self.negated(current)
       for i in xrange(len(current)):
           if omit[i]!=0:
              current[i]=0
       return current

   def negated_constraints(self):
       """the negated constraints of a NOT are the
          negated constraints of the thing negated."""
       return self.negated.constraints
       
   def __and__(self, other):
       """do the obvious thing."""
       return BTand_pred([self, other])
       
   def __or__(self, other):
       """do the obvious thing"""
       return BTor_pred([self, other])
       
   def __invert__(self):
       return self.negated
       
   def __cmp__(self, other):
       if other.__class__!=self.__class__:
          return __cmp__(self.__class__, other.__class__)
       kjSet = kjbuckets.kjSet
       return cmp(self.negated,other.negated)
       
   def __hash__(self):
       return hash(self.negated)^787876
       
class BTand_pred(BTPredicate):

   def __init__(self, members, precondition=None):
       #print "BTand_pred", (members, precondition)
       members = self.members = kjbuckets.kjSet(members).items()
       self.constraints = precondition # common constraints
       if members:
          # common constraints are those in any member
          if precondition is not None:
             constraints = precondition
          else:
             constraints = BoundTuple()
          for i in xrange(len(members)):
              m = members[i]
              mc = m.constraints
              if mc:
                 #print "constraints", constraints
                 constraints = constraints + mc
                 if constraints is None: break
              if m.__class__==BTPredicate:
                 members[i] = None # subsumed above
          self.members = filter(None, members)
          ### consider propagating constraints down?
          self.constraints = constraints
          if constraints is None: self.false = 1
          
   def relbind(self, dict, db):
       ms = []
       for m in self.members:
           ms.append( m.relbind(dict, db) )
       c = self.constraints.relbind(dict, db)
       return BTand_pred(ms, c)
          
   def domain(self):
       all = BTPredicate.domain(self).items()
       for x in self.members:
           all = all + x.domain().items()
       return kjbuckets.kjSet(all)
       
   def __repr__(self):
       m = self.members
       c = self.constraints
       r = map(repr, m)
       if self.false: r.insert(0, "FALSE")
       from string import join
       r = join(r, " AND ")
       r = "(%s)" % r
       if c: r = "[conj](%s and %s)" % (c, r)
       return r

   def detrivialize(self):
       """hook added to allow elimination of trivialities
          return None if completely true, or simpler form
          or self, if no simplification is possible."""
       # first apply demorgan's law to push ands down
       # (exponential in worst case).
       #print "detrivialize"
       #print self
       ms = self.members
       some_or = None
       c = self.constraints
       for m in ms:
           if m.__class__==BTor_pred:
              some_or = m
              ms.remove(m)
              break
       if some_or is not None:
          result = some_or
          if c is not None:
             some_or = some_or & BTPredicate(c)
          for m in ms:
              result = result & ms # preserves or/and precedence
          if result.__class__!=BTor_pred:
             raise "what the?"
          result = result.detrivialize()
          #print "or detected, returning"
          #print result
          return result
       for i in xrange(len(ms)):
           ms[i] = ms[i].detrivialize()
       ms[:] = filter(None, ms)
       if not ms:
          #print "returning boundary case of condition"
          if c is None:
             return None
          else: 
             return BTPredicate(c).detrivialize()
       ms[:] = kjbuckets.kjSet(ms).items()
       if len(ms)==1 and c is None: 
          #print "and of 1, returning"
          #print ms[0]
          return ms[0] # and of 1
       return self           

   def __call__(self, boundtuples):
       # apply common constraints first
       current = BTPredicate.__call__(self, boundtuples)
       for m in self.members:
           current = m(current)
       return current

   def negated_constraints(self):
       """the negated constraints of an AND are
          the negated constraints of *any* member"""
       ms = self.members
       result = BoundTuple()
       for m in ms:
           mc = m.negated_constraints()
           if mc: result = result + mc 
       return result
       
   def __and__(self, other):
       """push "and" down if other is an or"""
       if other.__class__==BTor_pred:
          return other & self
       c = self.constraints
       # merge in other and
       if other.__class__==BTand_pred:
          allmem = self.members+other.members
          oc = other.constraints
          if c is None:
             c = oc
          elif oc is not None:
             c = c+oc
          return BTand_pred(allmem, c)
       return BTand_pred(self.members + [other], c)
       
   def __or__(self, other):
       """do the obvious thing."""
       return BTor_pred([self, other])
       
   def __invert__(self):
       """translate to or-not"""
       ms = self.members
       if not ms: return ~BTPredicate() # boundary case
       result = ~ms[0]
       for m in ms[1:]:
           result = result | ~m
       return result
       
   def __cmp__(self, other):
       if other.__class__!=self.__class__:
          return __cmp__(self.__class__, other.__class__)
       kjSet = kjbuckets.kjSet
       return cmp(kjSet(self.members), kjSet(other.members))
       
   def __hash__(self):
       return hash(kjbuckets.kjSet(self.members))
       
class NontrivialEqPred(BTPredicate):
   """equation of nontrivial expressions."""
   
   def __init__(self, left, right):
       #print "making pred", self.__class__, left, right
       self.left = left
       self.right = right
       
   def relbind(self, dict, db):
       Class = self.__class__
       return Class(self.left.relbind(dict,db), self.right.relbind(dict,db) )
       
   def domain(self):
       return self.left.domain() + self.right.domain()
       
   op = "=="
       
   def __repr__(self):
       return "(%s)%s(%s)" % (self.left, self.op, self.right)
       
   def detrivialize(self):
       return self
       
   def __call__(self, btups):
       lv = self.left.value
       rv = self.right.value
       result = btups[:]
       for i in xrange(len(btups)):
           t = btups[i]
           if t!=0 and lv(t)!=rv(t):
              result[i] = 0
       return result
       
   def negated_constraints(self):
       return None
       
   def __and__(self, other):
       return BTand_pred( [self, other] )
       
   def __or__(self, other):
       return BTor_pred( [self, other] )
       
   def __invert__(self):
       return BTnot_pred(self)
       
class ExistsPred(NontrivialEqPred):
   """EXISTS subquery."""
   
   def __init__(self, subq):
       self.subq = subq
       
   def relbind(self, dict, db):
       self.subq = self.subq.relbind(db, dict)
       return self
       
   def __repr__(self):
       return "\nEXISTS\n%s\n" % (self.subq,)
       
   def __call__(self, btups):
       ### should optimize!!!
       eval = self.subq.eval
       result = btups[:]
       for i in range(len(btups)):
           testbtup = btups[i]
           if testbtup!=0:
              test = eval(outerboundtuple=testbtup).rows()
              if not test:
                 result[i] = 0
       return result
       
class LessPred(NontrivialEqPred):
   op = "<"
   def __call__(self, btups):
       lv = self.left.value
       rv = self.right.value
       result = btups[:]
       for i in xrange(len(btups)):
           t = btups[i]
           if t!=0 and lv(t)>=rv(t):
              result[i] = 0
       return result
       
   def __inv__(self):
       return LessEqPred(self.right, self.left)

       
class LessEqPred(NontrivialEqPred):
   op = "<="
   def __call__(self, btups):
       lv = self.left.value
       rv = self.right.value
       result = []
       for t in btups:
           if lv(t)<rv(t):
              result.append(t)
       return result
   def __inv__(self):
       return LessPred(self.right, self.left)

SELECT_TEMPLATE = """\
SELECT %s %s
FROM %s
WHERE %s
GROUP BY %s
HAVING %s
UNION %s %s
ORDER BY %s %s
"""

def dynamic_binding(ndynamic, dynamic):
    """create bindings from dynamic tuple for ndynamic parameters"""
    if not dynamic and ndynamic>0:
             raise ValueError, `ndynamic`+" dynamic parameters unbound"
    ldyn = len(dynamic)
    if ldyn!=ndynamic:
             raise ValueError, "%s,%s: wrong number of dynamics" % (ldyn,dynamic)
    dyn = BoundTuple()
    for i in xrange(ldyn):
              dyn.assns[ (0, i) ] = dynamic[i]
    #print "dynamic", dyn
    return dyn


class Selector:
   """For implementing, eg the SQL SELECT statement."""
   def __init__(self, alldistinct,
                      select_list,
                      table_reference_list,
                      where_pred,
                      group_list,
                      having_cond,
                      union_select =None,
                      order_by_spec =None,
                      ndynamic=0, # number of dyn params expected
                      ):
       self.ndynamic = 0
       self.alldistinct = alldistinct
       self.select_list = select_list
       self.table_list = table_reference_list
       self.where_pred = where_pred
       self.group_list = group_list
       self.having_cond = having_cond
       self.union_select = union_select
       self.order_by = order_by_spec
       self.union_spec = "DISTINCT" # default union mode
       self.relbindings = None # binding of relations
       
   def relbind(self, db, outerbindings=None):
       ad = self.alldistinct
       sl = self.select_list
       tl = self.table_list
       wp = self.where_pred
       gl = self.group_list
       hc = self.having_cond
       us = self.union_select
       ob = self.order_by
       usp= self.union_spec
       test = db.bindings(tl)
       #print len(test)
       #for x in test: 
            #print x
       (attbindings, relbindings, ambiguous, ambiguousatts) = test
       if outerbindings:
          # bind in outerbindings where unambiguous
          for (a,r) in outerbindings.items():
              if ((not attbindings.has_key(a))
                  and (not ambiguousatts.has_key(a)) ):
                 attbindings[a] = r
       # fix "*" select list
       if sl=="*":
          sl = TupleCollector()
          for (a,r) in attbindings.items():
              sl.addbinding(None, BoundAttribute(r,a))
          for (dotted, (r,a)) in ambiguous.items():
              sl.addbinding(dotted, BoundAttribute(r,a))
       sl = sl.relbind(attbindings, db)
       wp = wp.relbind(attbindings, db)
       if gl is not None: gl = gl.relbind(attbindings, db)
       if hc is not None: hc = hc.relbind(attbindings, db)
       if us is not None: us = us.relbind(db, attbindings)
       if ob is not None: ob = ob.relbind(attbindings, db)
       result = Selector(ad, sl, tl, wp, gl, hc, us, ob)
       result.union_spec = usp
       result.relbindings = relbindings
       result.ndynamic = self.ndynamic
       return result
       
   def attributes(self):
       return self.select_list.attorder
       
   def eval(self, dynamic=None, outerboundtuple=None):
       """leaves a lot to be desired.
          dynamic and outerboundtuple are mutually
          exclusive.  dynamic is only pertinent to
          top levels, outerboundtuple to subqueries"""
       where_pred = self.where_pred.detrivialize()
       select_list = self.select_list
       # shortcut
       if where_pred is not None and where_pred.false: 
          return Relation0(select_list.attorder, [])
       bt = self.where_pred.constraints
       if bt is None: bt = BoundTuple()
       ndynamic = self.ndynamic
       if outerboundtuple is not None: 
          bt = bt + outerboundtuple
       elif ndynamic:
          dyn = dynamic_binding(ndynamic, dynamic)
          bt = bt + dyn
          #print "dynamic", bt
       relbindings = self.relbindings
       allrels = relbindings.keys()
       #print relbindings
       allrels = bt.relorder(relbindings, allrels)
       #print allrels
       btseq = [bt]
       #print btseq
       for rel in allrels:
           #print rel
           btseq = hashjoin(btseq, rel, relbindings[rel])
           #for x in btseq: 
                #print x
       if where_pred is not None:
          btseq = filter(None, where_pred(btseq))
       (tups, attorder) = select_list.map(btseq)
       return Relation0(attorder, tups)
       
   def __repr__(self):
       union_spec = None
       if self.union_select:
          union_spec = self.union_select.union_spec
       ndyn = ""
       if self.ndynamic:
          ndyn = "\n[%s dynamic parameters]" % self.ndynamic
       result = SELECT_TEMPLATE % (
         self.alldistinct,
         self.select_list,
         self.table_list,
         self.where_pred,
         self.group_list,
         self.having_cond,
         union_spec,
         self.union_select,
         self.order_by,
         ndyn
         )
       return result   

class Database0:
   """quick and dirty in core database representation."""
   
   def __init__(self):
       """dictionary of relations."""
       self.rels = {}
       
   def __setitem__(self, name, relation):
       """bind a name (uppercased) to tuples as a relation."""
       from string import upper
       self.rels[ upper(name) ] = relation
       
   def __getitem__(self, name):
       from string import upper
       return self.rels[upper(name)]
       
   def __delitem__(self, name):
       from string import upper
       del self.rels[upper(name)]
       
   def relations(self):
       return self.rels.keys()
       
   def has_relation(self, name):
       return self.rels.has_key(name)
       
   def __repr__(self):
       l = []
       for (name, rel) in self.rels.items():
           l.append(name + ":")
           l.append(`rel`)
       from string import join
       return join(l, "\n\n")
       
   def bindings(self, fromlist):
       """return (attdict, reldict, amb, ambatts) from fromlist = [(name,alias)...]
          where reldict: alias --> tuplelist
                attdict: attribute_name --> unique_relation
                amb: dict of dottedname --> (rel, att)
                ambatts: dict of ambiguous_name --> witness_alias
       """
       from string import upper
       rels = self.rels
       ambiguous_atts = {}
       ambiguous = {}
       relseen = {}
       attbindings = {}
       relbindings = {}
       for (name,alias) in fromlist:
           name = upper(name)
           alias = upper(alias)
           if relseen.has_key(alias):
              raise NameError, `alias` + ": bound twice in from list"
           relseen[alias]=alias
           try:
               therel = rels[name]
           except KeyError:
               raise NameError, `name` + " no such relation in DB"
           relbindings[alias] = therel.rows()
           for attname in therel.attributes():
               if not ambiguous_atts.has_key(attname):
                  if attbindings.has_key(attname):
                     oldrel = attbindings[attname]
                     oldbind = (oldrel, attname)
                     ambiguous[ "%s.%s" % oldbind] = oldbind
                     del attbindings[attname]
                     ambiguous_atts[attname]=alias
                     newbind = (alias, attname)
                     ambiguous[ "%s.%s" % newbind ] = newbind
                  else:
                     attbindings[attname] = alias
               else:
                  newbind = (alias, attname)
                  ambiguous[ "%s.%s" % newbind ] = newbind
       return (attbindings, relbindings, ambiguous, ambiguous_atts)
       
class File_Storage0:
   """quick and dirty file storage mechanism.
        relation names in directory/dbname.gfd
          contains a white separated list of relation names
        relations in directory/relname.grl
          contains sequence of marshalled tuples reps
          prefixed by marshalled list of atts
   """
   
   def __init__(self, dbname, directory):
       """directory must exist."""
       self.dbname = dbname
       self.directory = directory
       
   def load(self):
       result = Database0()
       relnames = self.get_relnames()
       for r in relnames:
           result[r] = self.get_relation(r)
       return result
       
   def relfilename(self, name):
       return "%s/%s.grl" % (self.directory, name)
       
   def get_relation(self, name):
       fn = self.relfilename(name)
       f = open(fn, "rb")
       from marshal import load
       tups = []
       atts = load(f)
       try:
          while 1:
             data = load(f) # gets a dict
             #print data
             tups.append(maketuple(data))
       except EOFError:
          pass
       return Relation0(atts, tups)
       
   def dbfilename(self):
       return "%s/%s.gfd" % (self.directory, self.dbname)
       
   def get_relnames(self):
       fn = self.dbfilename()
       f = open(fn)
       from string import split
       data = f.read()
       names = split(data)
       f.close()
       return names
       
   def dump(self, db):
       relations = db.relations()
       for r in relations:
           self.dumprelation(r, db[r])
       self.dumpnames(relations)
       
   def dumprelation(self, name, rel):
       fn = self.relfilename(name)
       f = open(fn, "wb")
       from marshal import dump
       dump(rel.attributes(), f)
       for t in rel.rows():
           # coerce to std dict
           data = {}
           for (a,b) in t.items():
               data[a] = b
           dump(data, f)
       f.close()
       
   def dumpnames(self, names):
       fn = self.dbfilename()
       f = open(fn, "w")
       from string import join
       f.write(join(names,"\n"))
       f.close()
       
class Relation0:
   """quick and dirty in core relation representation."""
   def __init__(self, attribute_names, tuples=None, filter=None):
       self.attribute_names = attribute_names
       if tuples is None:
          tuples = []
       self.filter = filter
       self.set_empty()
       self.add_tuples(tuples)
       
   def __repr__(self):
       rows = self.rows()
       atts = self.attributes()
       list_rep = [list(atts)]
       for r in rows:
           rlist = []
           for a in atts:
               try:
                   elt = r[a]
               except KeyError:
                   elt = "NULL"
               else:
                   elt = str(elt)
               rlist.append(elt)
           list_rep.append(rlist)
       # compute maxen for formatting
       maxen = [0] * len(atts)
       for i in xrange(len(atts)):
           for l in list_rep:
               maxen[i] = max(maxen[i], len(l[i]))
       for i in xrange(len(atts)):
           mm = maxen[i]
           for l in list_rep:
                old = l[i]
                l[i] = old + (" " * (mm-len(old)))
       from string import join
       for i in xrange(len(list_rep)):
           list_rep[i] = join(list_rep[i], " | ")
       first = list_rep[0]
       list_rep.insert(1, "=" * len(first))
       return join(list_rep, "\n")
       
   def set_empty(self):
       self.tuples = []
       
   def add_tuples(self, tuples):
       tuples = filter(self.filter, tuples)
       oldtuples = self.tuples
       for t in tuples:
           oldtuples.append(t)
           
   def attributes(self):
       return self.attribute_names
       
   def rows(self):
       return self.tuples
       
class Parse_Context:
   """contextual information for parsing
        p.param() returns a new sequence number for external parameter.
   """
   parameter_index = 0
   
   # no __init__ yet
   def param(self):
       temp = self.parameter_index
       self.parameter_index = temp+1
       return temp
       
   def ndynamic(self):
       return self.parameter_index
       
CTFMT = """\
CREATE TABLE %s (
  %s 
  )"""
       
class CreateTable:
   """create table operation"""
   
   def __init__(self, name, colelts):
       self.name = name
       self.colelts = colelts
       self.indb = None # db in which to create
       
   def __repr__(self):
       from string import join
       elts = map(repr, self.colelts)
       return CTFMT % (self.name, join(elts, "\n  "))
       
   def relbind(self, db):
       """check that table doesn't already exist"""
       if db.has_relation(self.name):
          raise NameError, "cannot create %s, exists" % (self.name,)
       self.indb = db
       return self
       
   def eval(self, dyn=None):
       "create the relation now"
       # datatypes currently happily ignored :)
       db = self.indb
       name = self.name
       if db.has_relation(self.name):
          raise NameError, "relation %s exists, cannot create" % (self.name,)
       attnames = []
       for x in self.colelts:
           attnames.append(x.colid)
       r = Relation0(attnames)
       db[name] = r
       
class DropTable:
   def __init__(self, name):
       self.name = name
       self.indb = None
   def __repr__(self):
       return "DROP TABLE %s" % (self.name,)
   def relbind(self, db):
       self.indb = db
       if not db.has_relation(self.name):
          raise NameError, `self.name` + ": cannot delete, no such table"
       return self
   def eval(self, dyn):
       db = self.indb
       self.relbind(db)
       del db[self.name]
       
COLDEFFMT = "%s %s %s %s"

class ColumnDef:

   def __init__(self, colid, datatype, defaults, constraints):
       self.colid = colid
       self.datatype = datatype
       self.defaults = defaults
       self.constraints = constraints
       
   def __repr__(self):
       return COLDEFFMT % (self.colid, self.datatype, self.defaults, self.constraints)
       

UPDFMT = """\
UPDATE %s
SET %s
WHERE %s"""

class UpdateOp:
   def __init__(self, name, assns, condition):
       self.name = name
       self.assns = assns
       self.condition = condition
       
   def __repr__(self):
       return UPDFMT % (self.name, self.assns, self.condition)
       
   def relbind(self, db):
       name = self.name
       target = self.target = db[name]
       (attb, relb, amb, ambatts) = db.bindings( [ (name, name) ] )
       assns = self.assns = self.assns.relbind(attb, db)
       self.condition = self.condition.relbind(attb, db)
       # check that atts of assns are atts of target
       #print dir(assns)
       resultatts = assns.attorder
       kjSet = kjbuckets.kjSet
       resultatts = kjSet(resultatts)
       allatts = kjSet(target.attribute_names)
       self.preserved = allatts - resultatts
       huh = resultatts - allatts
       if huh:
          raise NameError, "%s lacks %s attributes" % (name, huh.items())
       return self
       
   def eval(self, dyn=None):
       # RELIES ON MUTATIONS INTO RELATION STRUCTURE
       name = self.name
       cond = self.condition
       assns = self.assns
       preserved = self.preserved
       tuples = self.target.tuples
       if dyn:
          dynbind = dynamic_binding(len(dyn), dyn)
       else:
          dynbind = None
       for i in xrange(len(tuples)):
           tup = tuples[i]
           bt = BoundTuple()
           bt.bind(name, tup)
           if dynbind is not None:
              bt = bt + dynbind
           test = filter(None, cond( [bt] ))
           if test:
              (tps, attorder) = assns.map(test)
              [ new ] = tps
              tuples[i] = new + preserved*tup

class DeleteOp:

   def __init__(self, name, where):
       self.name = name
       self.condition = where
       
   def __repr__(self):
       return "DELETE FROM %s WHERE %s" % (self.name, self.condition)
       
   def relbind(self, db):
       name = self.name
       target = self.target = db[name]
       (attb, relb, amb, ambatts) = db.bindings( [ (name, name) ] )
       self.condition = self.condition.relbind(attb, db)
       return self
       
   def eval(self, dyn=None):
       # THIS RELIES ON MUTATIONS INTO RELATION STRUCTURE
       name = self.name
       target = self.target
       tuples = target.tuples
       cond = self.condition
       if dyn:
          dynbind = dynamic_binding(len(dyn), dyn)
       else:
          dynbind = None
       for i in xrange(len(tuples)):
           tup = tuples[i]
           bt = BoundTuple()
           bt.bind(name, tup)
           if dynbind is not None:
              bt = bt + dynbind
           test = filter(None, cond( [bt] ))
           if test:
              tuples[i] = None
       target.tuples = filter(None, tuples)

INSFMT = """\
INSERT INTO %s 
%s
%s"""

class InsertOp:

   def __init__(self, name, optcolids, insertspec):
       self.name = name
       self.optcolids = optcolids
       self.insertspec = insertspec
       self.target = None # target relation
       self.collector = None # name map for attribute translation
       
   def __repr__(self):
       return INSFMT % (self.name, self.optcolids, self.insertspec)
       
   def relbind(self, db):
       name = self.name
       # determine target relation
       target = self.target = db[name]
       targetatts = target.attributes()
       kjSet = kjbuckets.kjSet
       targetset = kjSet(targetatts)
       # check or set colid bindings
       colids = self.optcolids
       if colids is None:
          colids = self.optcolids = target.attributes()
       colset = kjSet(colids)
       ### for now all attributes must be in colset
       cdiff = colset-targetset
       if cdiff:
          raise NameError, "%s: no such attributes in %s" % (cdiff.items(), name)
       cdiff = targetset-colset
       ### temporary!!!
       if cdiff:
          raise NameError, "%s: not set in insert on %s" % (cdiff.items(), name)
       # bind the insertspec
       insertspec = self.insertspec
       self.insertspec = insertspec = insertspec.relbind(db)
       # create a collector for result
       collector = self.collector = TupleCollector()
       # get ordered list of expressions to eval on bound attributes of insertspec
       resultexps = insertspec.resultexps()
       if len(resultexps)!=len(colset):
          raise ValueError, "result and colset of differing length %s" % (colset,)
       pairs = map(None, colids, resultexps)
       for (col,exp) in pairs:
           collector.addbinding(col, exp)
       return self
       
   def eval(self, dyn=None):
       resultbts = self.insertspec.eval(dyn)
       (resulttups, resultatts) = self.collector.map(resultbts)
       self.target.add_tuples(resulttups)
                     
class InsertValues:

   def __init__(self, List):
       self.list = List
       
   def __repr__(self):
       return "VALUES " +` tuple(self.list) `
       
   def resultexps(self):
       return self.list
       
   def relbind(self, db):
       l = self.list
       bindings = {}
       for i in xrange(len(self.list)):
           l[i] = l[i].relbind(bindings, db)
       return self
       
   def eval(self, dyn=None):
       if dyn:
          dynbt = dynamic_binding(len(dyn), dyn)
       else:
          dynbt = BoundTuple()
       return [dynbt] # ??
       
class InsertSubSelect:

   def __init__(self, subsel):
       self.subsel = subsel
       
   def __repr__(self):
       return "[subsel] %s" % (self.subsel,)
       
   def resultexps(self):
       # get list of result bindings
       subsel = self.subsel
       atts = self.subsel.attributes()
       # bind each as "result.name"
       exps = []
       for a in atts:
           exps.append( BoundAttribute("result", a) )
       return exps # temp
       
   def relbind(self, db):
       self.subsel = self.subsel.relbind(db)
       return self
       
   def eval(self, dyn=None):
       rel = self.subsel.eval(dyn)
       tups = rel.rows()
       for i in xrange(len(tups)):
           tups[i] = BoundTuple(result=tups[i])
       return tups

####### testing
# test helpers
def tp(**kw):
    return maketuple(kw)
    
def st(**kw):
    return BTPredicate(BoundTuple(r=kw))
    
