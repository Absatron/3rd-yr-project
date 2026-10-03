Job Arrays (Multiple similar jobs, Slurm)
Why use a Job Array?
Suppose you wish to run a large number of almost identical jobs – for example you may wish to process a thousand different data files with the same application (e.g., processing 1000s of images with the same image-processing app). Or you may wish to run the same program many times with different arguments or parameters (e.g., to do a parameter sweep where you wish to find the best value of some variable.)

You may have used the Condor pool to do this (where idle PCs on campus are used to run your jobs overnight) but the CSF can also run these High Throughput Computing jobs.

How NOT to do it
The wrong way to do this would be to write a script (using Perl, Python or BASH for example) to generate all of the required sbatch jobscripts and then use another BASH script to submit them all (running sbatch 1000s of times).

This is not a good use of your time and it will do horrible things to the submit node (which manages the job queues) on a cluster. The sysadmins may kill such jobs to keep the system running smoothly!

Do not run sbatch 100s, 1000s, … of times to submit 100s, 1000s, … of individual jobs. This will strain the batch system. If you are about to do this, STOP. You should be using a job array instead. Please read through the examples below. Contact us via the Connect HPC Help form if you require further advice.
The right way to do it
A much better way is to use a SLURM Job Array. Simply put, a job array runs multiple copies (100s, 1000s, …) of your job in a way that places much less strain on the queue manager. You only write one jobscript and use sbatch once to submit that job.

Your jobscript includes a flag to say how many copies of it should be run. Each copy of the job is given a unique task id. You use the task id in your jobscript to have each task do some unique work (e.g., each task processes a different data file or uses a different set of input parameters).

Using the unique task id creatively in your jobscript is the key to writing a good job array script. You can be creative here – the task id can be used in many ways.

Below, we first describe how to submit a Slurm job array that runs several serial (single core) tasks. We also show how to submit a job array that will run SMP (multicore) tasks. The majority of this page then gives examples of how to use the task id in your jobscript in different ways.

We have users on the CSF that run job-arrays with 1,000’s of tasks – hence they are a very easy way of repeatedly running the same job on lots of different data files!

Job runtime
Each individual task in an array gets the wall-clock time limit you request for your job (a maximum of 7 days can be requested.) An array job is not terminated as a whole at the 7 day limit – it will remain in the system until all tasks complete.

Job Array Basics
Here is a simple example of a job array – notice the #SBATCH -a 1-1000 line and the use of the special $SLURM_ARRAY_TASK_ID variable. These will both be explained below.

#!/bin/bash --login
#SBATCH -p serial # Job will use 1 core for each task
#SBATCH -t 4-0 # Wallclock time limit - each task will run for up to 4 days (0 hours)

#SBATCH -a 1-1000 # An array job with 1000 "tasks", numbered 1...1000 # (Note: unlike CSF3 "SGE" job array, SLURM job arrays can also start at 0)

./myprog -in data.${SLURM_ARRAY_TASK_ID}.dat -out results.${SLURM_ARRAY_TASK_ID}.dat # # My input files are named: data.1.dat, data.2.dat, ..., data.1000.dat # 1000 tasks (copies of this job) will run. # Task 1 will read data.1.dat, task 2 will read data.2.dat, ...
Computationally, this is equivalent to 1000 individual queue submissions in which $SLURM_ARRAY_TASK_ID takes the values 1, 2, 3. . . 1000, and where input and output files have the task ID number in their name. Hence task 1 will read the file data.1.dat and write the results to results.1.dat. Task 2 will read data.2.dat and write the results to results.2.dat and so on, all the way up to task 1000.

The $SLURM_ARRAY_TASK_ID variable is automatically set for you by the batch system when a particular task runs.

Notation: Using $SLURM_ARRAY_TASK_ID and ${SLURM_ARRAY_TASK_ID} are equivalent (notice the curly-braces { and } around the variable name.) The use of ${....} is recommended and can help with readability when other text surrounds the variable name.

Note that $SLURM_JOB_ID is unique for each task in the job array. If you want the base job id of the entire job array, use $SLURM_ARRAY_JOB_ID, which is the same for all tasks in the job array.

To submit the job simply issue one sbatch command:

sbatch jobscript
where jobscript is the name of your script above.

Job Array Size Limit
The highest task-id number that can be requested is 25000. This effectively sets the maximum number of tasks in the job array to be 25001 because Slurm job arrays can begin at zero (unlike job arrays in SGE on CSF3 which have to begin at 1.) However, many people will prefer to start their job-arrays from 1 to match CSF3 jobscripts. For example:

#SBATCH -a 1-25000 # Highest permitted task-id is currently 250000 on CSF3. # (reminder: Slurm job-arrays can start at zero if you prefer.)
If you request a maximum task-id greater than 25000, you will receive the following error when trying to submit the job:

sbatch: error: Batch job submission failed: Invalid job array specification
Multi-core Job Array Tasks
Multi-core (SMP) tasks (e.g., OpenMP jobs) can also be run in jobarrays. Each task will run your program with the requested number of cores. Simply add a -p partition option to the jobscript and then tell your program how many cores it can use in the usual manner (see parallel job submission). Please be aware that each task will be requesting the specified resources (number of cores). It may take longer for each task to get through the batch queue, depending on how busy the system is.

An example SMP array job is given below:

#!/bin/bash --login
#SBATCH -p multicore # Each job array task will be a multicore job
#SBATCH -n 4 # Each job array task will use 4 cores in this example
#SBATCH -t 4-0 # Each job array task can run for up to 4 days (0 hours)
#SBATCH -a 1-1000 # A job-array with 1000 "tasks", numbered 1...1000

# My OpenMP program will read this variable to get how many cores to use.

# $SLURM_NTASKS is automatically set to the number specified on the -n line above.

export OMP_NUM_THREADS=$SLURM_NTASKS

./myOMPprog -in data.${SLURM_ARRAY_TASK_ID}.dat -out results.${SLURM_ARRAY_TASK_ID}.dat
Again, simply submit the job once using sbatch jobscript.

Advantages of Job Arrays
Job arrays have several advantages over submitting 100s or 1000s of individual jobs. In both of the above cases:

Only one sbatch command is issued (and only one scancel command would be required to delete all tasks).
The batch system will try to run many of your tasks at once (possibly hundreds simultaneously for serial job arrays, depending on what we have set the limit to be according to demand on the system). So you get a lot more than one task running in parallel from just one sbatch command. The system will churn through your tasks running them all as cores become free on the system, at which point the job is finished.
Only one entry appears to be pending (PD) in the squeue output for the job array, but each individual task running (R) will be visible. This makes reading your sbatch output a lot easier than if you’d submitted 1000s of individual jobs.
The load on the SLURM submit node (i.e., the cluster node responsible for managing the queues and scheduling which jobs run) is vastly less than that of submitting 1000 separate jobs.
There are many ways to use the ${SLURM_ARRAY_TASK_ID} variable to supply a different input to each task and several examples are shown below.

More General Task ID Numbering
It is not necessary that ${SLURM_ARRAY_TASK_ID} starts at 1; nor must the increment be 1. The general format is:

#SBATCH -a start-end:increment # #  
 # # The default :increment is 1 if not supplied # # The start task id CAN be zero in SLURM
For example:

#SBATCH -a 100-995:5
so that ${SLURM_ARRAY_TASK_ID} takes the values 100, 105, 110, 115... 995.

More ad-hoc numbering can also be used:

#SBATCH -a 0,6,20,50-100
Incidentally, in the case in which the upper-bound is not equal to the lower-bound plus an integer-multiple of the increment, for example

#SBATCH -a 1-42:6 # Tasks will be numbered 1, 7, 13, 19, 25, 31, 37 !!
SLURM automatically changes the upper bound, but this is only visible when you run squeue to check on the status of your job.

[username@login1[csf3] ~]$ sbatch array.slurm
Submitted batch job 529313

[username@login1[csf3] ~]$ squeue
JOBID PRIORITY PARTITION NAME USER ACCOUNT ST SUBMIT*TIME START_TIME TIME NODES CPUS NODELIST(REASON)
529345*[1-37:6] 0.01245 serial array.slurm username xy01 PD 01/12/22 14:38 N/A 0:00 1 1 (None) # # The squeue command shows the adjusted upper bound (37)
Note the 1-37 in the JOBID column: the final task id has been adjusted to be 37 rather than 42. Hence the tasks ids used will be 1,7,13,19,25,31,37.

Related Environment Variables
There are three more automatically created environment variables one can use, as illustrated by this simple jobscript script:

#!/bin/bash --login
#SBATCH -a 1-37:6 # Tasks will be numbered 1, 7, 13, 19, 25, 31, 37

# This will report that we requested an increment of 6

echo "The ID increment is: $SLURM_ARRAY_TASK_STEP"

# This will report that we have 7 tasks in this job array

echo "Number of tasks in job array: $SLURM_ARRAY_TASK_COUNT"

# This will report 529345 in this example (see sbatch command output above)

echo "Master job ID is: $SLURM_ARRAY_JOB_ID"

# These should be used with caution (see below for explanation)

if [[$SLURM_ARRAY_TASK_ID == $SLURM_ARRAY_TASK_MIN]]; then
echo "first task - I am $SLURM_ARRAY_TASK_ID"
elif [[$SLURM_ARRAY_TASK_ID == $SLURM_ARRAY_TASK_MAX]]; then
echo "last task - I am $SLURM_ARRAY_TASK_ID"
else
echo "neither - I am task $SLURM_ARRAY_TASK_ID"
fi
Note that the batch system will try to start your jobs in numerical order but there is no guarantee that they will finish in the same order — some tasks may take longer to run than others. So you cannot rely on the task with id ${SLURM_ARRAY_TASK_ID} being the last task to finish. Hence do not try something like:

# DO NOT do this in your jobscript - we may not be the last task to finish!

if [[$SLURM_ARRAY_TASK_ID == $SLURM_ARRAY_TASK_MAX]]; then

# Archive output files from all tasks (output.1, output.2, ...).

tar czf ~/scratch/all-my-results.tgz output.\* # # BAD: we may not be the last task to finish just because we are the last # BAD: task id. Hence we may miss some output files from other tasks that # BAD: are still running.
fi
The correct way to do something like this (where the work carried out by a task is dependent on other tasks having finished) is to use a job dependency which uses two separate jobs and automatically runs the second job only when the first job has completely finished. You would generally only use the $SLURM_ARRAY_TASK_MIN and $SLURM_ARRAY_TASK_MAX variables where you wanted those tasks to do something different but where they are still independent of the other tasks.

Examples
We now show example job scripts which use the job array environment variables in various ways. All of the examples below are serial jobs (each task uses only one core) but you could equally use multicore (smp) jobs if your code/executable supports multicore. You should adapt these examples to your own needs.

A List of Input Files
Suppose we have a list of input files, rather than input files explicitly indexed by a number. For example, your input files may have names such as:

C2H4O.dat
NH3.dat
C6H8O7.dat
PbCl2.dat
H2O.dat
... and so on ...
The files do not have the convenient 1, 2, 3, .... number sequence in their name. So how do we use a job array with these input files? We can put the names in to a simple text file, with one name per line (as above). We then ask the job array tasks to read a name from this master list of filenames. As you might expect, task number 1 will read the filename on line 1 of the master-list. Task number 2 will read the filename from line 2 of the master-list, and so on.

#!/bin/bash --login
#SBATCH -p serial # Job will use 1 core for each task
#SBATCH -t 4-0 # Each task has a maximum 4-day (0 hours) runtime
#SBATCH -a 1-42

# Task id 1 will read line 1 from my_file_list.txt

# Task id 2 will read line 2 from my_file_list.txt

# and so on...

# Each line contains the name of an input file to used by 'my_chemistry_prog'

# Use some Linux commands to save the filename read from 'my_file_list.txt' to

# a script variable named INFILE that we can use in other commands.

INFILE=$(awk "NR==${SLURM_ARRAY_TASK_ID}" my_file_list.txt) # # Can also use another linux tool named 'sed' to get the n-th line of a file: # INFILE=$(sed -n "${SLURM_ARRAY_TASK_ID}p" my_file_list.txt)

# We now use the value of our variable by using $INFILE.

# In task 1, $INFILE will be replaced with C2H4O.dat

# In task 2, $INFILE will be replaced with NH3.dat

# ... and so on ...

# Run the app with the .dat filename specific to this task

./my_chemistry_prog -in $INFILE -out result.$INFILE
Bash Scripting and Arrays
Another way of passing different parameters to your application (e.g., to run the same simulation but with different input parameters) is to list all the parameters in a bash array and index in to the array. For example:

#!/bin/bash --login
#SBATCH -p serial # Job will use 1 core for each task
#SBATCH -t 4-0 # Each task has a maximum 4-day (0 hours) runtime
#SBATCH -a 0-9 # Only 10 tasks in this example! # NOTE: We start at zero in this example - see below for why

# A bash array of my 10 input parameters

X_PARAM=( 3400 4500 9700 10020 20000 30000 40000 44400 50000 60910 )

# Bash arrays use zero-based indexing hence we start the task id at 0 (see "-a 0-9" above.)

# If you started the task id at 1 using "-a 1-10" then you should do the following to make

# our INDEX variable start from 0:

# INDEX=$((SLURM_ARRAY_TASK_ID-1))

# But we started the task id at zero so we can simply do

INDEX=${SLURM_ARRAY_TASK_ID}

# Run the app with one of the parameters

./myprog -xflag ${X_PARAM[$INDEX]} > output.${INDEX}.log
Running from Different Directories (simple)
Here we run each task in a separate directory (folder) that we create when each task runs. We run two applications from the jobscript – the first outputs to a file, the second reads that file as input and outputs to another file (your own applications may do something completely different). We run 1000 tasks, numbered 1…1000.

#!/bin/bash --login
#SBATCH -p serial # Job will use 1 core for each task
#SBATCH -t 4-0 # Each task has a maximum 4-day (0 hours) runtime
#SBATCH -a 1-1000

# Create a new directory for each task and go in to that directory

mkdir myjob-${SLURM_ARRAY_TASK_ID}
cd myjob-${SLURM_ARRAY_TASK_ID}

# Each task runs the same executables stored in the parent directory

../myprog-a.exe > a.output
../myprog-b.exe < a.output > b.output
In the above example all tasks use the same input and output filenames (a.output and b.output). This is safe because each task runs in its own directory.

Running from Different Directories (intermediate)
Here we use one of the techniques from above – read the names of folders (directories) we want to run in from a file. Task 1 will read line 1, task 2 reads line 2 and so on.

Create a simple text file (for example my_dir_list.txt) with each folder name you wish to run a job in listed on a new line.

We assume the file contains sub-directory names. For example, suppose we are currently working in a directory named ~/scratch/jobs/ (it is in our scratch directory). The subdirectories are named after some property such as:

s023nn/arun1206/
s023nn/arun1207/
s023nn/brun1208/
s023nx/brun1201/
s023nx/crun1731/

and so on - it doesn't really matter what the subdirectories are called.
Note that in this example we assume there are 500 lines (i.e. 500 directories)
in this file. This tells us how many tasks to run in the job array.
The jobscript reads a line from the above list and cd‘s in to that directory:

#!/bin/bash --login
#SBATCH -p serial # Job will use 1 core for each task
#SBATCH -t 4-0 # Each task has a maximum 4-day (0 hours) runtime
#SBATCH -a 1-500 # Assuming my_dir_list.txt has 500 lines

# Task id 1 will read line 1 from my_dir_list.txt

# Task id 2 will read line 2 from my_dir_list.txt

# and so on...

# This time we use the 'sed' command but we could use the 'awk' command (see earlier).

# Task 1 will read line 1 of my_dir_list.txt, task 2 will read line 2, ...

# Assign the name of this task's sub-directory to a variable named 'SUBDIR'

SUBDIR=$(sed -n "${SLURM_ARRAY_TASK_ID}p" my_dir_list.txt)

# Go in to the sub-directory for this task by reading the value of the variable

cd $SUBDIR

#

# You could use the subdir name to form a longer path, for example:

# cd ~/scratch/myjobs/medium_dataset/$SUBDIR

# Run our code. Each sub-directory contains a file named input.dat.

./myprog -in input.dat
The above script assumes that each subdirectory contains a file named input.dat which we process.

Running from Different Directories (advanced)
This example runs the same code but from different directories. Here we expect each directory to contain an input file. You can name your directories (and subdirectories) appropriately to match your experiments. We use BASH scripting to index in to arrays giving the names of directories. This example requires some knowledge of BASH but it should be straight forward to modify for your own work.

In this example we have the following directory structure (use whatever names are suitable for your code)

3 top-level directories named: Helium, Neon, Argon
2 mid-level directories named: temperature, pressure
4 bottom-level directories named: test1, test2, test3, test4
So the directory tree looks something like:

|
+---Helium---+---temperature---+---test1
| | +---test2
| | +---test3
| | +---test4
| |
| +------pressure---+---test1
| +---test2
| +---test3
| +---test4
|
+-----Neon---+---temperature---+---test1
| | +---test2
| | +---test3
| | +---test4
| |
| +------pressure---+---test1
| +---test2
| +---test3
| +---test4
|
+----Argon---+---temperature---+---test1
| +---test2
| +---test3
| +---test4
|
+------pressure---+---test1
+---test2
+---test3
+---test4
Hence we have 3 x 2 x 4=24 input files all named myinput.dat in paths such as

$HOME/scratch/chemistry/Helium/temperature/test1/myinput.dat
...
$HOME/scratch/chemistry/Helium/temperature/test4/myinput.dat
$HOME/scratch/chemistry/Helium/pressure/test1/myinput.dat
...
$HOME/scratch/chemistry/Neon/temperature/test1/myinput.dat
...
$HOME/scratch/chemistry/Argon/pressure/test4/myinput.dat
The following jobscript will run the executable mycode.exe in each path (so that we process all 24 input files). In this example the code is a serial code (hence no PE is specified).

#!/bin/bash --login
#SBATCH -p serial # Job will use 1 core for each task
#SBATCH -t 4-0 # Each task has a maximum 4-day (0 hours) runtime

# This creates a job array of 24 tasks numbered 1...24 (IDs can't start at zero)

#SBATCH -a 1-24

# Subdirectories will all have this common root (saves me some typing)

BASE=$HOME/scratch/chemistry

# Path to my executable

EXE=$BASE/exe/mycode.exe

# Arrays giving subdirectory names (note no commas - use spaces to separate)

DIRS1=( Helium Neon Argon )
DIRS2=( temperature pressure )
DIRS3=( test1 test2 test3 test4 )

# BASH script to get length of arrays

NUMDIRS1=${#DIRS1[@]}
NUMDIRS2=${#DIRS2[@]}
NUMDIRS3=${#DIRS3[@]}
TOTAL=$[$NUMDIRS1 * $NUMDIRS2 * $NUMDIRS3 ]
echo "Total runs: $TOTAL"

# Remember that $SLURM_ARRAY_TASK_ID will be 1, 2, 3, ... 24.

# BASH array indexing starts from zero so decrement.

TID=$[SLURM_ARRAY_TASK_ID-1]

# Create indices in to the above arrays of directory names.

# The first id increments the slowest, then the middle index, and so on.

IDX1=$[TID/$[NUMDIRS2*NUMDIRS3]]
IDX2=$[(TID/$NUMDIRS3)%$NUMDIRS2]
IDX3=$[TID%$NUMDIRS3]

# Index in to the arrays of directory names to create a path

JOBDIR=${DIRS1[$IDX1]}/${DIRS2[$IDX2]}/${DIRS3[$IDX3]}

# Echo some info to the job output file

echo "Running SLURM_ARRAY_TASK_ID $SLURM_ARRAY_TASK_ID in directory $BASE/$JOBDIR"

# Finally run my executable from the correct directory

cd $BASE/$JOBDIR
$EXE < myinput.dat > myoutput.dat
You may not need three levels of subdirectories and you’ll want to edit the names (BASE, EXE, DIRS1, DIRS2, DIRS3) and change the number of tasks requested.

To submit your job simply use sbatch myjobscript.sh, i.e., you only submit a single jobscript.

Running MATLAB (lock file error)
If you wish to run compiled MATLAB code in a job array please see MATLAB job arrays (CSF documentation) for details of an extra environment variable needed to prevent a lock-file error. This is a problem in MATLAB when running many instances at the same time, which can occur if running from a job array.

Our MATLAB documentation also contains an example of passing the ${SLURM_ARRAY_TASK_ID} value to your MATLAB code.

Limit the number of tasks to be run at the same time
By default the batch system will try attempt to run as many tasks as possible concurrently. If you do not want this to happen you can limit how many tasks can be running at the same time with the %N modifier. For example to limit it to 5 tasks:

#SBATCH -a 1-100%5 # A maximum of 5 tasks will run at the same time
Renaming the Slurm output files
The default Slurm output file generated for each job array task is:

slurm-ARRAYJOBID_TASKID.out # # EG: slurm-123456_1.out, slurm-123456_2.out, ... slurm-123456_1000.out
To instruct Slurm to use a different name, use the following flags:

# Example: Use myjobname.out.123456.1, myjobname.out.123456.2, ...

#SBATCH -o %x.out.%A.%a # # # # # # %a = SLURM_ARRAY_TASK_ID # # # # %A = SLURM_ARRAY_JOB_ID (same number for all tasks) # # %x = SLURM_JOB_NAME # Which is either given by "#SBATCH -J jobname" # or name of jobscript if -J not used. Note that -J does # NOT modify the default slurm-123456_1.out if -o flag # is not used.
Job Dependencies with Job Arrays
It is possible to make a job wait for an entire job array to complete or to make the tasks of a job array wait for the corresponding task of another job array. It is also possible to make the tasks within a job array wait for other tasks in the same job array (although this is limited). Examples are now given.

Unlike in SGE on CSF3, it is not possible to use a job name (rather than job ID number) when specifying dependencies. So we must capture the job ID number of submitted jobs and use that number in later jobs. Hence we recommend specifying the job dependency flag on the sbatch command-line rather than in the jobscript.

Wait for entire job array to finish
Suppose you want JobB to wait until all tasks in JobA have finished. JobB can be an ordinary job or another job array. But it will not run until all tasks in the job array JobA have finished. This is useful where you need to do something with the results of all tasks from a job array. Using a job dependency is the correct way to ensure that all tasks in a job array have completed (using the last task in a job array to do some extra processing is incorrect because not all tasks may have finished even if they have all started).

------------------- Time --------------------->
JobA.task1 -----> End |
JobA.task2 --------> End| # JobA tasks can run in parallel
... |
JobA.taskN ----> End |
|JobB -----> End # JobB won't start until all of
| # JobA's tasks have finished
Here is the jobscript for JobB – note we DO NOT specify the -d (dependency) requirements in the jobscript but instead do it on the sbatch command-line when we submit the job (see below.) This is because SLURM cannot use a job name in the jobscript – it requires a job id. But we don’t know the job id until we submit the job!

#!/bin/bash --login
#SBATCH -p serial # Job will use 1 core for each task
#SBATCH -t 4-0 # Each task has a maximum 4-day (0 hours) runtime
#SBATCH -J JobB
./myapp.exe
Submit the jobs in the expected order and JobB will wait for JobA to finish.

JID=$(sbatch --parsable jobscript_a)      # The job-array. We capture the jobid when it's submitted.
sbatch -d afterany:$JID jobscript_b # This job waits for the job-array to finish before starting # # afterany - the job will run when all tasks in the given jobid have completed (any status) # afterok - The job will run when all tasks in the given jobid have completed successfully
Wait for individual tasks to finish
Suppose you have two job arrays to run, both with the same number of tasks. You want task 1 from JobB to run after task 1 from JobA has finished. Similarly you want task 2 from JobB to run after task 2 from JobA has finished. And so on. This allows you to pipeline tasks but still have them run independently and in parallel with other tasks.

----------------------- Time ----------------------->
JobA.task1 -----> End JobB.task1 ------> END
JobA.task2 -------> End JobB.task2 -------> END # Tasks can run in parallel. JobA tasks
... # and JobB tasks form pipelines.
JobA.taskN -----> End JobB.taskN ----> END
We use the aftercorr flag to set up an array dependency. Here are the two jobscripts:

JobA’s jobscript:

#!/bin/bash --login
#SBATCH -t 4-0 # Each task has a maximum 4-day (0 hours) runtime
#SBATCH -J JobA # We are JobA
#SBATCH -a 1-20 # 20 Tasks in this example

./myAapp.exe data.$SLURM_ARRAY_TASK_ID.in > data.$SLURM_ARRAY_TASK_ID.A_result
JobB’s jobscript

#!/bin/bash
#SBATCH -p serial # Job will use 1 core for each task
#SBATCH -t 4-0 # Each task has a maximum 4-day (0 hours) runtime
#SBATCH -J JobB # We are JobB
#SBATCH -a 1-20 # 20 Tasks in this example (must be same as JobA)

./myBapp.exe data.$SLURM_ARRAY_TASK_ID.A_result > data.$SLURM_ARRAY_TASK_ID.B_result
Submit both jobs:

JID=$(sbatch --parsable jobscript_a)
sbatch -d aftercorr:$JID jobscript_b # # aftercorr - Each task in JobB will run after the corresponding task in JobA # has completed successfully
Note that the --parsable flag on the sbatch command-line changes the message output by sbatch to be just the JOB ID number:

sbatch myjobscript
Submitted batch job 529522

sbatch --parsable myjobscript
529522
This is useful when scripting the submission of jobs as we do above to create dependencies between jobs.

Tasks wait within a job array
It is possible to make the tasks within a jobarray wait for earlier tasks within the same jobarray. This is generally not recommend because it removes one of the advantages of job arrays – the ability to run independent jobs in parallel so that you get your results sooner. However, it does provide a method of easily submitting a large number of jobs where job N is dependent on the results of job N-1 so must wait for the previous job to finish. We use the %1 modifier to control the number of concurrent tasks that the job array can execute.

------------------------------- Time --------------------------------->
JobA.task1 -----> End
JobA.task2 -----> End
...
JobA.taskN -----> End
The %N flag added to the end of the usual job array option allows the job array to run N tasks in the job array at the same time. Without the flag the batch system will attempt to run as many tasks as possible concurrently. If you set this to 1 you effectively make each task wait for the previous task to finish:

#!/bin/bash --login
#SBATCH -p serial # Job will use 1 core for each task
#SBATCH -t 4-0 # Each task has a maximum 4-day (0 hours) runtime
#SBATCH -a 1-10%1 # Run only one task at a time
./myApp.exe data.$SLURM_ARRAY_TASK_ID.in > data.$SLURM_ARRAY_TASK_ID.out
Deleting Job Arrays
Deleting All Tasks
An entire job array can be deleted with one command. This will delete all tasks that are running and are yet to run from the batch system:

scancel 18305 # # replace 18305 with your own job id number
Deleting Specific Tasks
Alternatively, it is possible to delete specific tasks while leaving other tasks running or in the queue waiting to run. You may wish to change some input files for these tasks, for example, or it might be because specific tasks have crashed and you need to delete them and then resubmit them. Simply add the \_taskrange to the JOBID, where taskrange gives the tasks to delete. You must always give the job id followed by the tasks. For example:

To delete a single task (id 30) from a job (id 18205)
scancel 18205*30
To delete tasks 200-300 inclusive from a job (id 18205)
scancel 18205*[200-300]
To delete tasks 25,26,50,51,52,100 from a job (id 18205)
scancel 18205*[25-26] 18205*[50-52] 18205_100

Resubmitting Deleted/Failed Tasks
If you need to resubmit specific task ids that have failed (for whatever reason, e.g., the app you were running crashed or there was a hardware problem), you can specify those specific task id numbers on the sbatch command-line to override the range of task ids in the jobscript. For example, to resubmit the six ad-hoc tasks 25,26,50,51,52,100:

# The -a flag on the command-line will override any #SBATCH -a start-finish line in the jobscript.

# You do not need to edit your jobscript to remove the #SBATCH -a line.

sbatch -a 25-26,50-52,100 jobscript
Email from Jobarrays
Aug 2021: Please note a change of policy

Please DO NOT submit job-arrays that will send emails from each task when there are more than 20 tasks in the job-array. This is to protect the University mail routers which have recently blocked the CSF from sending emails due to large job-arrays sending 1000s of emails.
SLURM will by default only send one email once the entire job array has completed.

December 2025 – this policy is now enforced. Large job arrays that use the --mail-type=ARRAY_TASKS flag will be rejected.

As with ordinary batch jobs it is possible to have the job email you when it begins, ends or it aborts due to error. Unfortunately with a job array each task will email you. Hence you may receive 1000s of emails from a large job array. If this is what you require, please add the following to your jobscript:

#SBATCH --mail-user=your.name@manchester.ac.uk # Can use any address
#SBATCH --mail-type=END # # Could be: # BEGIN, END, FAIL, REQUEUE, ALL (which covers all types) # Others are also available. See 'man sbatch' for details. # Mail is NOT sent from each individual array task. Instead, # it is sent at the start / end of the entire job array.

# To send email from each job array task individually, add ARRAY_TASKS to the --mail-type

#SBATCH --mail-type=BEGIN,END,ARRAY_TASKS # # This will send A LOT of email - at the start and end of every # array task. To protect the University mail routers, this # flag can only be used when the number of tasks is at most 20. # Larger job arrays using this flag will be rejected.
Further Information
More on SLURM Job Arrays can be found at:

SLURM’s Job Array Documentation
