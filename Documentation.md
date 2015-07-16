### Launching RUR-ITS ###

RUR-ITS can be started by executing rur\_start.py

By default, RUR-ITS will start by launching a pretest, which will need to be completed before entering the system, and using the system will be followed by a post-test.  Problem selection will be a fixed order as it is set in the problems file (usually in increasing order of difficulty).

Also by default, the RUR-PLE problems given by RUR-ITS are all program tracing and prediction problems where the user is given an environment and code, and is asked to predict the behavior of the program.  RUR-ITS also has support for program writing problems.

RUR-ITS accepts a few command-line arguments to change the default behavior.  These arguments are not positional and are not flags, so they should be given as is, in any order.

skip - skip the pretest and post-test and enter the system immediately<br>
aps - use the adaptive problem selection algorithm to select the best problem every time<br>
fps - rank the problems by the adaptive problem selection algorithm after completing the pretest, and thereafter go through the problems in a fixed order from most to least helpful as determined by the algorithm<br>
write - use program writing problems instead of prediction problems<br>
<br>
<h3>Adding and modifying content</h3>

The default instructions file for prediction problems is lessons/en/instr.htm<br>
<br>
The instructions file for program writing problems is lessons/en/wrtinstr.htm<br>
<br>
The concept outline for the test questions and RUR-PLE problems is given on the first page of rurprogs.pdf, available in Downloads.<br>
<br>
The pretest and post-test questions are defined in rur_py/questions.py<br>
<br>
The lists defining which questions are in each test are defined at the bottom.  Each question is a Question object, with the following constructor arguments:<br>
instr - The text of the question.<br>
code - The code associated with the question.<br>
choices - A list of answer choices, each as a string, for multiple-choice questions.  For a short-answer question, this should be an empty list.<br>
correct - The correct answer.  For multiple-choice questions, this should be a 0-indexed index into the choices list.  For short-answer questions this should be a string containing the text of the correct answer.  Note that whitespace is stripped from the ends of answers and the end of each line (of both the correct answer and the user's answer) before checking for correctness.<br>
concepts - A list of outline identifiers of the concepts for the question, ex: ["IA1","IB2a"].<br>
<br>
The RUR-PLE problems are defined in rur_py/problems.py<br>
<br>
The lists defining which problems are program tracing problems and which are program writing problems are defined at the bottom (note that a problem can be in both lists).  Each problem is a function that returns a tuple containing (1) the environment and (2) the code.  The environment is a dictionary, and the environments are generated by functions in rur_py/environment.py.  The code is a string containing the implementation code for the problem.  Each function defining a problem has two class attributes attached to it:<br>
concepts - A list of outline identifiers of the concepts for the question, ex: ["IA1","IB2a"].<br>
difficulty - Difficulty level of the problem, on a scale from 1 to 10.<br>
<br>
For program writing problems, the problem definitions in rur_py/problems.py will work as follows.  The code returned by the function will not be loaded into RUR-ITS and should be the code for a correct implementation of the problem's solution.  The code may be used to check the user's solution.  There also needs to be an HTML file containing instructions for the problem, describing what the program the user is being asked to write should do.  This HTML file should be in lessons/en/probs and should have the same name as the problem's function, with a .html extension.  Any associated images should be stored in lessons/images/probs.<br>
<br>
<h3>Future work</h3>

Currently, RUR-ITS does not have the ability to check solutions to program writing problems for correctness.  We plan to add support for this in the future.<br>
<br>
<h3>Known Bugs</h3>

The only known bug affects the visualization when a user's prediction was incorrect.  While executing the visual diff of the program's correct behavior and the user's prediction, there is a glitch when executing the last correct robot command predicted before an incorrect prediction action.<br>
<br>
The blue robot (with the blue trace line) representing the user's prediction will execute the last correct command correctly.  The gray robot (with the green trace line) representing the correct behavior will not, however, execute the last correct action immediately thereafter as it should.  Once the blue robot has finished executing the incorrect actions, the gray robot will finally execute the last correct action that should have happened before the incorrect actions.  Basically once the prediction syncs up with the correct behavior, the gray robot will catch up to where it should have been.<br>
<br>
I believe this behavior is caused by the wx.Yield() statements sprinkled throughout the code (in rur_py/cpu.py) for executing the visualization, and is some sort of threading/locking-type problem.  I don't understand how this works well enough to fix it.<br>
<br>
<h3>Logging data</h3>

By default, RUR-ITS will log data during the user's usage of the system.  This can be disabled by changing the logData variable defined near the beginning of rur_start.py to False (this should probably be incorporated into RUR-PLE's configuration file at some point).  By default, the data that is stored is stored under RUR-PLE's configuration directory ($HOME/.config/rurple).  This location is defined by the logDataDir variable also in rur_start.py, and can be changed.<br>
<br>
When RUR-ITS starts, the user is asked to create a user for the system.  The user chooses an alphanumeric user name, and the system creates a numeric user ID.  These are logged in key.txt.  The numeric user IDs begin the filenames of the rest of the data that is logged.  The filenames (except for the demographics) end with a unique number that is generated when the system is started (it's technically a timestamp).  This prevents data from being overwritten during subsequent uses of the system.  The data that is logged is described below, and is stored in subdirectories under the log data directory:<br>
Demographics - The demographic information entered by the user when they created their user the first time they launched the system.<br>
Tests - The actual answers entered by the user on the pretest and post-test.<br>
Notes - The feedback entered by the user after the post-test.<br>
<br>
While doing RUR-PLE problems in the system, each problem is given a number (starting with 1 for the first problem and incrementing thereafter).  Each problem also has an index, which is an index into the list of problem templates defined in rur_py/problems.py.  Also logged:<br>
Logs - Information about the user's pretest questions, post-test questions, and RUR-PLE problems solved, is stored here.  For the pretest and post-test questions, it logs whether they were correct or incorrect.  For the RUR-PLE problems, it logs the problem number, problem index, and whether their solution was correct.<br>
Predictions - The list of robot commands predicted by the user for each RUR-PLE program prediction problem.  The problem number is included in the filename.<br>
SourceCode - The code for each RUR-PLE problem.  The problem number is included in the filename.<br>
Worlds - The environment dictionaries (world files) for each RUR-PLE problem.  The problem number is included in the filename.<br>
<br>
If the pretest and login screens are skipped (with the 'skip' command-line argument), a user ID of 0 is used.<br>
<br>
While in the system, some locked features can be unlocked by pressing F11.  This will un-hide hidden buttons, allow you to control the robot, and edit the code, environment, and console window.  Pressing F11 again will re-lock it.