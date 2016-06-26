(define (problem temp)
    (:domain StrategicArgumentation)
    (:objects a b c d e f - arg
              S0 S1 S8 S32 S9 S33 S40 S41 - setOfArgsP
              T0 T4 T2 T16 T6 T20 T18 T22 - setOfArgsO
              A0 A1 A2 - agent )

    (:init (= (stage) 0)

           (canAssertP a)
           (canAssertP d)
           (canAssertP f)

           (= (prob-belief A0) 40)
           (= (prob-belief A1) 50)
           (= (prob-belief A2) 10)

           (= (prob-of-success) 0)

           (successful S1 T0)		; (['a'], [])
           (successful S1 T16)		; (['a'], ['e'])
           (successful S9 T0)		; (['a', 'd'], [])
           (successful S9 T2)		; (['a', 'd'], ['b'])
           (successful S9 T16)		; (['a', 'd'], ['e'])
           (successful S33 T0)		; (['a', 'f'], [])
           (successful S33 T4)		; (['a', 'f'], ['c'])
           (successful S33 T16)		; (['a', 'f'], ['e'])
           (successful S33 T20)		; (['a', 'f'], ['c', 'e'])
           (successful S41 T0)		; (['a', 'd', 'f'], [])
           (successful S41 T4)		; (['a', 'd', 'f'], ['c'])
           (successful S41 T2)		; (['a', 'd', 'f'], ['b'])
           (successful S41 T16)		; (['a', 'd', 'f'], ['e'])
           (successful S41 T6)		; (['a', 'd', 'f'], ['c', 'b'])
           (successful S41 T20)		; (['a', 'd', 'f'], ['c', 'e'])

           (dialogueP S0)
           (dialogueO A0 T0)
           (dialogueO A1 T0)
           (dialogueO A2 T0)

           (addP a S0 S1)		; a + [] = ['a']
           (addP a S1 S1)		; a + ['a'] = ['a']
           (addP a S8 S9)		; a + ['d'] = ['a', 'd']
           (addP a S32 S33)		; a + ['f'] = ['a', 'f']
           (addP a S9 S9)		; a + ['a', 'd'] = ['a', 'd']
           (addP a S33 S33)		; a + ['a', 'f'] = ['a', 'f']
           (addP a S40 S41)		; a + ['d', 'f'] = ['a', 'd', 'f']
           (addP a S41 S41)		; a + ['a', 'd', 'f'] = ['a', 'd', 'f']
           (addP d S0 S8)		; d + [] = ['d']
           (addP d S1 S9)		; d + ['a'] = ['a', 'd']
           (addP d S8 S8)		; d + ['d'] = ['d']
           (addP d S32 S40)		; d + ['f'] = ['d', 'f']
           (addP d S9 S9)		; d + ['a', 'd'] = ['a', 'd']
           (addP d S33 S41)		; d + ['a', 'f'] = ['a', 'd', 'f']
           (addP d S40 S40)		; d + ['d', 'f'] = ['d', 'f']
           (addP d S41 S41)		; d + ['a', 'd', 'f'] = ['a', 'd', 'f']
           (addP f S0 S32)		; f + [] = ['f']
           (addP f S1 S33)		; f + ['a'] = ['a', 'f']
           (addP f S8 S40)		; f + ['d'] = ['d', 'f']
           (addP f S32 S32)		; f + ['f'] = ['f']
           (addP f S9 S41)		; f + ['a', 'd'] = ['a', 'd', 'f']
           (addP f S33 S33)		; f + ['a', 'f'] = ['a', 'f']
           (addP f S40 S40)		; f + ['d', 'f'] = ['d', 'f']
           (addP f S41 S41)		; f + ['a', 'd', 'f'] = ['a', 'd', 'f']

           (addO T0 T0 T0)		; [] + [] = []
           (addO T0 T4 T4)		; [] + ['c'] = ['c']
           (addO T0 T2 T2)		; [] + ['b'] = ['b']
           (addO T0 T16 T16)		; [] + ['e'] = ['e']
           (addO T0 T6 T6)		; [] + ['c', 'b'] = ['c', 'b']
           (addO T0 T20 T20)		; [] + ['c', 'e'] = ['c', 'e']
           (addO T0 T18 T18)		; [] + ['b', 'e'] = ['b', 'e']
           (addO T0 T22 T22)		; [] + ['c', 'b', 'e'] = ['c', 'b', 'e']
           (addO T4 T0 T4)		; ['c'] + [] = ['c']
           (addO T4 T4 T4)		; ['c'] + ['c'] = ['c']
           (addO T4 T2 T6)		; ['c'] + ['b'] = ['c', 'b']
           (addO T4 T16 T20)		; ['c'] + ['e'] = ['c', 'e']
           (addO T4 T6 T6)		; ['c'] + ['c', 'b'] = ['c', 'b']
           (addO T4 T20 T20)		; ['c'] + ['c', 'e'] = ['c', 'e']
           (addO T4 T18 T22)		; ['c'] + ['b', 'e'] = ['c', 'b', 'e']
           (addO T4 T22 T22)		; ['c'] + ['c', 'b', 'e'] = ['c', 'b', 'e']
           (addO T2 T0 T2)		; ['b'] + [] = ['b']
           (addO T2 T4 T6)		; ['b'] + ['c'] = ['c', 'b']
           (addO T2 T2 T2)		; ['b'] + ['b'] = ['b']
           (addO T2 T16 T18)		; ['b'] + ['e'] = ['b', 'e']
           (addO T2 T6 T6)		; ['b'] + ['c', 'b'] = ['c', 'b']
           (addO T2 T20 T22)		; ['b'] + ['c', 'e'] = ['c', 'b', 'e']
           (addO T2 T18 T18)		; ['b'] + ['b', 'e'] = ['b', 'e']
           (addO T2 T22 T22)		; ['b'] + ['c', 'b', 'e'] = ['c', 'b', 'e']
           (addO T16 T0 T16)		; ['e'] + [] = ['e']
           (addO T16 T4 T20)		; ['e'] + ['c'] = ['c', 'e']
           (addO T16 T2 T18)		; ['e'] + ['b'] = ['b', 'e']
           (addO T16 T16 T16)		; ['e'] + ['e'] = ['e']
           (addO T16 T6 T22)		; ['e'] + ['c', 'b'] = ['c', 'b', 'e']
           (addO T16 T20 T20)		; ['e'] + ['c', 'e'] = ['c', 'e']
           (addO T16 T18 T18)		; ['e'] + ['b', 'e'] = ['b', 'e']
           (addO T16 T22 T22)		; ['e'] + ['c', 'b', 'e'] = ['c', 'b', 'e']
           (addO T6 T0 T6)		; ['c', 'b'] + [] = ['c', 'b']
           (addO T6 T4 T6)		; ['c', 'b'] + ['c'] = ['c', 'b']
           (addO T6 T2 T6)		; ['c', 'b'] + ['b'] = ['c', 'b']
           (addO T6 T16 T22)		; ['c', 'b'] + ['e'] = ['c', 'b', 'e']
           (addO T6 T6 T6)		; ['c', 'b'] + ['c', 'b'] = ['c', 'b']
           (addO T6 T20 T22)		; ['c', 'b'] + ['c', 'e'] = ['c', 'b', 'e']
           (addO T6 T18 T22)		; ['c', 'b'] + ['b', 'e'] = ['c', 'b', 'e']
           (addO T6 T22 T22)		; ['c', 'b'] + ['c', 'b', 'e'] = ['c', 'b', 'e']
           (addO T20 T0 T20)		; ['c', 'e'] + [] = ['c', 'e']
           (addO T20 T4 T20)		; ['c', 'e'] + ['c'] = ['c', 'e']
           (addO T20 T2 T22)		; ['c', 'e'] + ['b'] = ['c', 'b', 'e']
           (addO T20 T16 T20)		; ['c', 'e'] + ['e'] = ['c', 'e']
           (addO T20 T6 T22)		; ['c', 'e'] + ['c', 'b'] = ['c', 'b', 'e']
           (addO T20 T20 T20)		; ['c', 'e'] + ['c', 'e'] = ['c', 'e']
           (addO T20 T18 T22)		; ['c', 'e'] + ['b', 'e'] = ['c', 'b', 'e']
           (addO T20 T22 T22)		; ['c', 'e'] + ['c', 'b', 'e'] = ['c', 'b', 'e']
           (addO T18 T0 T18)		; ['b', 'e'] + [] = ['b', 'e']
           (addO T18 T4 T22)		; ['b', 'e'] + ['c'] = ['c', 'b', 'e']
           (addO T18 T2 T18)		; ['b', 'e'] + ['b'] = ['b', 'e']
           (addO T18 T16 T18)		; ['b', 'e'] + ['e'] = ['b', 'e']
           (addO T18 T6 T22)		; ['b', 'e'] + ['c', 'b'] = ['c', 'b', 'e']
           (addO T18 T20 T22)		; ['b', 'e'] + ['c', 'e'] = ['c', 'b', 'e']
           (addO T18 T18 T18)		; ['b', 'e'] + ['b', 'e'] = ['b', 'e']
           (addO T18 T22 T22)		; ['b', 'e'] + ['c', 'b', 'e'] = ['c', 'b', 'e']
           (addO T22 T0 T22)		; ['c', 'b', 'e'] + [] = ['c', 'b', 'e']
           (addO T22 T4 T22)		; ['c', 'b', 'e'] + ['c'] = ['c', 'b', 'e']
           (addO T22 T2 T22)		; ['c', 'b', 'e'] + ['b'] = ['c', 'b', 'e']
           (addO T22 T16 T22)		; ['c', 'b', 'e'] + ['e'] = ['c', 'b', 'e']
           (addO T22 T6 T22)		; ['c', 'b', 'e'] + ['c', 'b'] = ['c', 'b', 'e']
           (addO T22 T20 T22)		; ['c', 'b', 'e'] + ['c', 'e'] = ['c', 'b', 'e']
           (addO T22 T18 T22)		; ['c', 'b', 'e'] + ['b', 'e'] = ['c', 'b', 'e']
           (addO T22 T22 T22)		; ['c', 'b', 'e'] + ['c', 'b', 'e'] = ['c', 'b', 'e']

           (canAssertO T0 A0 S0)		; A0: [] -> []
           (canAssertO T2 A0 S0)		; A0: [] -> ['b']
           (canAssertO T0 A0 S1)		; A0: ['a'] -> []
           (canAssertO T2 A0 S1)		; A0: ['a'] -> ['b']
           (canAssertO T0 A0 S8)		; A0: ['d'] -> []
           (canAssertO T2 A0 S8)		; A0: ['d'] -> ['b']
           (canAssertO T0 A0 S32)		; A0: ['f'] -> []
           (canAssertO T2 A0 S32)		; A0: ['f'] -> ['b']
           (canAssertO T16 A0 S32)		; A0: ['f'] -> ['e']
           (canAssertO T18 A0 S32)		; A0: ['f'] -> ['b', 'e']
           (canAssertO T0 A0 S9)		; A0: ['a', 'd'] -> []
           (canAssertO T2 A0 S9)		; A0: ['a', 'd'] -> ['b']
           (canAssertO T0 A0 S33)		; A0: ['a', 'f'] -> []
           (canAssertO T2 A0 S33)		; A0: ['a', 'f'] -> ['b']
           (canAssertO T16 A0 S33)		; A0: ['a', 'f'] -> ['e']
           (canAssertO T18 A0 S33)		; A0: ['a', 'f'] -> ['b', 'e']
           (canAssertO T0 A0 S40)		; A0: ['d', 'f'] -> []
           (canAssertO T2 A0 S40)		; A0: ['d', 'f'] -> ['b']
           (canAssertO T16 A0 S40)		; A0: ['d', 'f'] -> ['e']
           (canAssertO T18 A0 S40)		; A0: ['d', 'f'] -> ['b', 'e']
           (canAssertO T0 A0 S41)		; A0: ['a', 'd', 'f'] -> []
           (canAssertO T2 A0 S41)		; A0: ['a', 'd', 'f'] -> ['b']
           (canAssertO T16 A0 S41)		; A0: ['a', 'd', 'f'] -> ['e']
           (canAssertO T18 A0 S41)		; A0: ['a', 'd', 'f'] -> ['b', 'e']
           (canAssertO T0 A1 S0)		; A1: [] -> []
           (canAssertO T4 A1 S0)		; A1: [] -> ['c']
           (canAssertO T0 A1 S1)		; A1: ['a'] -> []
           (canAssertO T4 A1 S1)		; A1: ['a'] -> ['c']
           (canAssertO T0 A1 S8)		; A1: ['d'] -> []
           (canAssertO T4 A1 S8)		; A1: ['d'] -> ['c']
           (canAssertO T0 A1 S32)		; A1: ['f'] -> []
           (canAssertO T4 A1 S32)		; A1: ['f'] -> ['c']
           (canAssertO T16 A1 S32)		; A1: ['f'] -> ['e']
           (canAssertO T20 A1 S32)		; A1: ['f'] -> ['c', 'e']
           (canAssertO T0 A1 S9)		; A1: ['a', 'd'] -> []
           (canAssertO T4 A1 S9)		; A1: ['a', 'd'] -> ['c']
           (canAssertO T0 A1 S33)		; A1: ['a', 'f'] -> []
           (canAssertO T4 A1 S33)		; A1: ['a', 'f'] -> ['c']
           (canAssertO T16 A1 S33)		; A1: ['a', 'f'] -> ['e']
           (canAssertO T20 A1 S33)		; A1: ['a', 'f'] -> ['c', 'e']
           (canAssertO T0 A1 S40)		; A1: ['d', 'f'] -> []
           (canAssertO T4 A1 S40)		; A1: ['d', 'f'] -> ['c']
           (canAssertO T16 A1 S40)		; A1: ['d', 'f'] -> ['e']
           (canAssertO T20 A1 S40)		; A1: ['d', 'f'] -> ['c', 'e']
           (canAssertO T0 A1 S41)		; A1: ['a', 'd', 'f'] -> []
           (canAssertO T4 A1 S41)		; A1: ['a', 'd', 'f'] -> ['c']
           (canAssertO T16 A1 S41)		; A1: ['a', 'd', 'f'] -> ['e']
           (canAssertO T20 A1 S41)		; A1: ['a', 'd', 'f'] -> ['c', 'e']
           (canAssertO T0 A2 S0)		; A2: [] -> []
           (canAssertO T4 A2 S0)		; A2: [] -> ['c']
           (canAssertO T2 A2 S0)		; A2: [] -> ['b']
           (canAssertO T6 A2 S0)		; A2: [] -> ['c', 'b']
           (canAssertO T0 A2 S1)		; A2: ['a'] -> []
           (canAssertO T4 A2 S1)		; A2: ['a'] -> ['c']
           (canAssertO T2 A2 S1)		; A2: ['a'] -> ['b']
           (canAssertO T6 A2 S1)		; A2: ['a'] -> ['c', 'b']
           (canAssertO T0 A2 S8)		; A2: ['d'] -> []
           (canAssertO T4 A2 S8)		; A2: ['d'] -> ['c']
           (canAssertO T2 A2 S8)		; A2: ['d'] -> ['b']
           (canAssertO T6 A2 S8)		; A2: ['d'] -> ['c', 'b']
           (canAssertO T0 A2 S32)		; A2: ['f'] -> []
           (canAssertO T4 A2 S32)		; A2: ['f'] -> ['c']
           (canAssertO T2 A2 S32)		; A2: ['f'] -> ['b']
           (canAssertO T16 A2 S32)		; A2: ['f'] -> ['e']
           (canAssertO T6 A2 S32)		; A2: ['f'] -> ['c', 'b']
           (canAssertO T20 A2 S32)		; A2: ['f'] -> ['c', 'e']
           (canAssertO T18 A2 S32)		; A2: ['f'] -> ['b', 'e']
           (canAssertO T22 A2 S32)		; A2: ['f'] -> ['c', 'b', 'e']
           (canAssertO T0 A2 S9)		; A2: ['a', 'd'] -> []
           (canAssertO T4 A2 S9)		; A2: ['a', 'd'] -> ['c']
           (canAssertO T2 A2 S9)		; A2: ['a', 'd'] -> ['b']
           (canAssertO T6 A2 S9)		; A2: ['a', 'd'] -> ['c', 'b']
           (canAssertO T0 A2 S33)		; A2: ['a', 'f'] -> []
           (canAssertO T4 A2 S33)		; A2: ['a', 'f'] -> ['c']
           (canAssertO T2 A2 S33)		; A2: ['a', 'f'] -> ['b']
           (canAssertO T16 A2 S33)		; A2: ['a', 'f'] -> ['e']
           (canAssertO T6 A2 S33)		; A2: ['a', 'f'] -> ['c', 'b']
           (canAssertO T20 A2 S33)		; A2: ['a', 'f'] -> ['c', 'e']
           (canAssertO T18 A2 S33)		; A2: ['a', 'f'] -> ['b', 'e']
           (canAssertO T22 A2 S33)		; A2: ['a', 'f'] -> ['c', 'b', 'e']
           (canAssertO T0 A2 S40)		; A2: ['d', 'f'] -> []
           (canAssertO T4 A2 S40)		; A2: ['d', 'f'] -> ['c']
           (canAssertO T2 A2 S40)		; A2: ['d', 'f'] -> ['b']
           (canAssertO T16 A2 S40)		; A2: ['d', 'f'] -> ['e']
           (canAssertO T6 A2 S40)		; A2: ['d', 'f'] -> ['c', 'b']
           (canAssertO T20 A2 S40)		; A2: ['d', 'f'] -> ['c', 'e']
           (canAssertO T18 A2 S40)		; A2: ['d', 'f'] -> ['b', 'e']
           (canAssertO T22 A2 S40)		; A2: ['d', 'f'] -> ['c', 'b', 'e']
           (canAssertO T0 A2 S41)		; A2: ['a', 'd', 'f'] -> []
           (canAssertO T4 A2 S41)		; A2: ['a', 'd', 'f'] -> ['c']
           (canAssertO T2 A2 S41)		; A2: ['a', 'd', 'f'] -> ['b']
           (canAssertO T16 A2 S41)		; A2: ['a', 'd', 'f'] -> ['e']
           (canAssertO T6 A2 S41)		; A2: ['a', 'd', 'f'] -> ['c', 'b']
           (canAssertO T20 A2 S41)		; A2: ['a', 'd', 'f'] -> ['c', 'e']
           (canAssertO T18 A2 S41)		; A2: ['a', 'd', 'f'] -> ['b', 'e']
           (canAssertO T22 A2 S41)		; A2: ['a', 'd', 'f'] -> ['c', 'b', 'e']
    )

    (:goal (> (prob-of-success) 0))

    (:metric maximize (prob-of-success) )
)