Simple Optimal Strategies for Persuasion
======================================

This work is described in the following paper:
 
    Black, E., Coles, A. J. & Hampson, C. S. Planning for persuasion. To appear in AAMAS '17 The 16th International Conference on Autonomous Agents and Multiagent Systems. 2017.
 
The domain file (which describes the actions) is "domain.pddl", in the "PDDLgen" folder. The files that describe the examples used for evaluation of the approach described in the Planning for Persuasion paper are in the "examples" folder.
 
We also include here the script we used to evaluate our approach. In order to run this, one needs to supply it with an automated planner. If you are interested in accessing the planner we used, please contact Amanda Coles (amander dot coles at kcl.ac.uk).

Once you have supplied the implementation with a planner, to generate an optimal simple strategy run the python script *argstrat.py* with a two arguments naming the path to your chosen planner and the path to your chosen example problem file. For example, 

    python argstrat.py ./planner ./examples/ECAI-example.txt
  
The script will generate the PDDL file *./examples/ECAI-example.pddl* and run the planner automatically, returning an optimal simple strategy (should one exist).

The script also performs the naive search fon the same example problem, and returns a second (possible different) optimal simple stratgy.

The probability of success of both stratgies is reported, together with the search times taken by both approaches, for comparison. 


To reference this work, please cite: 

    Black, E., Coles, A. J. & Hampson, C. S. Planning for persuasion. To appear in AAMAS '17 The 16th International Conference on Autonomous Agents and Multiagent Systems. 2017.




Copyright (C) 2016 Christopher Hampson
 
    This program is free software: you can redistribute it and/or modify it under the terms of the 
    GNU General Public License as published by the Free Software Foundation, either version 3 of 
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
    without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
    See the GNU General Public License for more details: http://www.gnu.org/licenses
