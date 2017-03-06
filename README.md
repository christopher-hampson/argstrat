Simple Optimal Strategies for Persuasion
======================================

To generate an optimal simple stratgy, run the python script *argstrat.py* with a single argument naming the example problem file. For example, 

    python argstrat.py ./examples/ECAI-example.txt
  
The script will generate the PDDL file *./examples/ECAI-example.pddl* and run the supplied implementation of the POPF planner automatically, returning an optimal simple strategy (should one exist).

The script also performs the naive search fon the same example problem, and returns a second (possible different) optimal simple stratgy.

The probability of success of both stratgies is reported, together with the search times taken by both approaches, for comparison. 


For more information, please see our short paper published in the proceedings of the 22nd European Conference on Artifical Intelligence (ECAI'16).

    http://ebooks.iospress.nl/volumearticle/45007


Copyright (C) 2016 Christopher Hampson
 
    This program is free software: you can redistribute it and/or modify it under the terms of the 
    GNU General Public License as published by the Free Software Foundation, either version 3 of 
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
    without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
    See the GNU General Public License for more details: http://www.gnu.org/licenses
