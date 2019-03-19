import sys
from IntervalPattern import Pattern, PatternConfig, pattern_parser_for_testing
from diagram import init_diagram, add_intent, add_object, clean_flags

if __name__ == "__main__":
    p1 = Pattern(dirty=False)
    p1.intervals = pattern_parser_for_testing('1,2 3,4 3,6')

    p2 = Pattern(dirty=False)
    p2.intervals = pattern_parser_for_testing('1.5,3 1,5 5,7')

    p12 = p1.intersect(p2)
    print 'p1', p1
    print 'p2', p2
    print 'p12', p12

    p3 = Pattern(dirty=False)
    p3.intervals = pattern_parser_for_testing('1.1,1.2 3.3,3.4 4,5')

    p4 = Pattern(dirty=False)
    p4.intervals = pattern_parser_for_testing('1.5,3 1,5 5,7')

    p5 = Pattern(dirty=False)
    p5.intervals = pattern_parser_for_testing('0.1,1.2 3.3,3.4 4,5')

    print 'p5', p5
    print 'p1<=p3', p1 <= p3
    print 'p1>=p3', p1 >= p3
    print 'p2==p4', p2 == p4
    print 'p1<=p5', p1 <= p5
    print 'p1>=p5', p1 >= p5
