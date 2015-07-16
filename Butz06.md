C. J. Butz, S. Hua, and R. B. Maguire. 2006. A web-based bayesian intelligent tutoring system for computer programming. _Web Intelli. and Agent Sys._ 4, 1 (January 2006), 77-97.

They create a web-based application called BITS that uses Bayesian Networks for its decision making. BITS help students navigate through online computer science information, recommends information to learn by setting these as goals, and generates curriculums. When a student uses BITS to retrieve information on something, they use a Bayesian Network with a DAG to inform the student of the prior information that is of importance to the specific thing they wish to learn. For example, to learn a for loop, they must learn incrementing operators, comparison operators, and variable assignment. BITS would present this information to them as a series of links.

Though what we will be implementing will allow a student to actually write code, breaking down student problems within code could be aided by this BITS programming. If writing an ITS that focuses on teaching iteration, we can break down categories of problems that could be hit by students into smaller, simpler concepts in programming languages. RD

DJW adds, In the background part of the paper, they distinguish two types of ITSs being problem solving support and curriculum sequencing (helping the user navigate through a static set of materials in the most efficient way to meet their learning goals).  They constructed a DAG (of prerequisite relationships) of introductory programming topics manually with the help of their textbook (the same Nell Dale C++ book Salisbury used to use for their CS1).  The entire DAG they constructed is given as an appendix at the end of the paper.  The BITS system updates the student model by either directly asking the user if they understand a concept or giving them a short quiz.  It also annotates (visibly to the user) each of the materials with whether it is relevant to the user's current learning goals and whether the user has demonstrated understanding of it or its prerequisites.  If a student fails to demonstrate understanding of a concept, rather than just having the user revisit those materials, it has them revisit the prerequisite materials.