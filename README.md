Simple Optimal Strategies for Persuasion
======================================

To generate an optimal simple stratgy, run the python script *argstrat.py* with a single argument naming the example problem file. For example, 

    python argstrat.py ./examples/ECAI-example.txt
  
The script will generate the PDDL file *./examples/ECAI-example.pddl* and run the supplied implementation of the POPF planner automatically, returning an optimal simple strategy (should one exist).

The script also performs the naive search fon the same example problem, and returns a second (possible different) optimal simple stratgy.

The probability of success of both stratgies is reported, together with the search times taken by both approaches, for comparison. 


For more information, please see our short paper published in the proceedings of the 22nd European Conference on Artifical Intelligence (ECAI'16)

    http://ebooks.iospress.nl/ISBN/978-1-61499-672-9
