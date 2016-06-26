; 13/04/2016 - Domain 7 (ECAI submission)

(define (domain StrategicArgumentation)
    (:requirements :ADL :TYPING :FLUENTS)
    (:types arg setOfArgsO setOfArgsP agent)
    (:predicates   
        (canAssertP ?a - arg)
        (canAssertO ?M - setOfArgsO ?A - agent ?D - setOfArgsP)

        (successful ?D1 - setOfArgsP ?D2 - setOfArgsO)
        (ineffective ?A - agent)

        (addP ?a - arg ?X ?Y - setOfArgsP)
        (addO ?X ?Y ?Z - setOfArgsO)

        (dialogueP ?D - setOfArgsP)
        (dialogueO ?A - agent ?D - setOfArgsO)
        (temp ?A - agent ?D - setOfArgsO) 
	)
   
    (:functions
        (stage)
        (prob-belief ?A - agent)
        (prob-of-success)    
    )


(:action proponent
    :parameters (?a - arg)
    
    :precondition (and (canAssertP ?a) 
                       (or (= (stage) 0) (= (stage) 1))
                  )                    
						
    :effect (and (assign (stage) 1)
                 (not (canAssertP ?a)) 


                 ;update P component of dialogue
                 (forall (?X ?Y - setOfArgsP)
                         (when (and (dialogueP ?X) 
                                    (addP ?a ?X ?Y)
                                    (not (= ?X ?Y))
                                )
                                (and (dialogueP ?Y)
                                     (not (dialogueP ?X))
                                )
                         )
                  )


                 ; pre-processing for (opponent) action
                 (forall (?A - agent)
                         (forall (?D - setOfArgsO)
                                 (when (dialogueO ?A ?D) 
                                       (and (temp ?A ?D) 
                                            (not (dialogueO ?A ?D))
                                       )
                                 )
                         )
                  )

                  (forall (?A - agent)
                          (not (ineffective ?A))
                                  
                  )
                

                 

              
             )   
)


(:action opponent
    :parameters ()
    :precondition (and (= (stage) 1)
                  )                 
						
    :effect (and (assign (stage) 2)
   
                 ; update opponent component
                 (forall (?A - agent)
                         (forall (?D - setOfArgsP)
                                 (forall (?X ?Y ?M - setOfArgsO)
                                         (when (and (dialogueP ?D)
                                                    (temp ?A ?X)
                                                    (canAssertO ?M ?A ?D)
                                                    (addO ?M ?X ?Y)
                                                    (not (successful ?D ?Y))
                                               )
                                               (and (dialogueO ?A ?Y) 
                                                    (ineffective ?A)
                                               )     
                                          )
                                 )
                         )
                 )

                 ; erase (temp)
                 (forall (?A - agent)
                         (forall (?D - setOfArgsO)
                                 (not (temp ?A ?D))
                         )
                  )


            )
                                                            
                  
)

(:action add-probability
    :parameters ()
    :precondition (= (stage) 2)

    :effect (and (assign (stage) 0)

                 (forall (?A - agent)
                         (when (and (not (ineffective ?A))
                                    (> (prob-belief ?A) 0)
                               )
                               (and (increase (prob-of-success) (prob-belief ?A))
                                    (assign (prob-belief ?A) 0)
                               )
                         )
                 )
                 
            )
)

 


)
