Parallel Jobs 10 Minute Tutorial (Slurm)
Please note: It is assumed you have already done the Batch System 10 Minute Tutorial. If not, please do so before attempting this tutorial.

Another Tutorial: Submitting a Parallel Job to the Batch System
The following tutorial is optional and aimed at users wishing to run parallel jobs. You may wish to come back to this tutorial once you are more familiar with the CSF.

A parallel job can be used when your application software is known to support parallel processing.

These applications use more than one CPU core to improve their performance (i.e., give you the results sooner!) They can also access more memory than a serial (1-core) application and so can usually tackle larger problems (e.g., read in larger input data files, solve more equations, run larger simulations.)

Many of the centrally-installed applications on the CSF support parallel processing.

Parallel applications can use multiple CPU cores within a single compute node.

Some parallel applications even support running larger parallel jobs across multiple compute nodes.

Not all software supports parallel processing. If your application does not support it then there is no point running a parallel job – the CSF will not magically make it run on multiple CPU cores.

However, if you have a lot of data files to process, say, or a lot of simulations to run (a parameter sweep) then you may wish to run multiple copies of an application to process lots of different datasets at the same time using a type of batch job known as a job array. Even if the application is not a parallel application, running lots of copies of the app to process lots of datasets can give you your results sooner.

You should check the documentation for your particular application to see if it supports parallel processing.

In the following tutorial we will:

Run a simple matrix-multiplication application that multiplies two large square matrices of numbers together. This is a common task in many engineering applications. For the purposes of this tutorial it doesn’t matter what the task is, but it does demonstrate how to submit a parallel job to the batch system.
Repeat the job with a different number of cores to see how it affects performance.
The tutorial will also show how to use a modulefile to access a centrally installed application.
The following steps assume you have already logged in to the CSF and have followed the Batch System 10 Minute Tutorial (which explains some of the steps in more detail).

Step 1: Create a Job Description File (a jobscript)
As in the previous tutorial, we need a simple text file (the jobscript) describing the job we wish to run. We will add some extra information to the jobscript to request more than 1 CPU core (which is the default).

Create a directory (usually referred to as a folder in Windows or MacOS) in your CSF home storage area, for our second test job, by running the following commands at the prompt:

# All of these commands are run on the CSF login node at the prompt

mkdir ~/second-job # Create the directory (folder)
cd ~/second-job # Go in to the directory (folder)
Now use gedit, or another editor, on the CSF login node (running text editors on the login node is permitted) to create a file with exactly the following content (see below):

# Run this command on the CSF login node at the prompt

gedit second-job.txt

Here’s the jobscript content – put this in the text file you are creating

#!/bin/bash --login
#SBATCH -p multicore # (or --partition=) Job will use the compute nodes reserved for parallel jobs.
#SBATCH -n 4 # (or --ntasks=) Number of cores to use.
#SBATCH -t 0-1 # This is the wallclock time limit. 0-1 is 1 hour. Job will be terminated if # still running after after 1 hour.

# Set up to use the centrally installed tutorial application. The CSF has modulefiles for 100s of apps.

module purge
module load apps/intel-17.0/tutorial

# Inform the app how many cores we requested for our job. The app can use this many cores.

# The special $SLURM_NTASKS keyword is automatically set to the number used on the -n line above.

export OMP_NUM_THREADS=$SLURM_NTASKS

# Run the app, which in this tutorial is named 'pmp'

pmp
Note: lines must NOT be indented in your text file – there should NOT be any spaces at the start of the lines. Cut-n-paste from this web page will work correctly in most browsers in that it won’t copy any leading space.

This BASH script has the following parts:

The first line, #!/bin/bash --login, means that the file you create is treated as a BASH script (scripts in Linux can use several languages, BASH is the one we use for jobscripts). The --login is needed to make the module command work inside the jobscript.
The #SBATCH -p partition line is new – the partition is used to say what type of parallel job will be run. In this case we are running a single compute-node multi-core job. Other types of parallel job are available but we will not cover those here.
The #SBATCH -n 4 line is new – this makes the job a parallel job. It asks the batch system to reserve 4 cores (in this example) in the partition.
The #SBATCH -t 0-1 line sets the maximum time the job is allowed to run for to be 0 days, 1 hour. It is fine if your job completes sooner than this, but if still running after one hour (in this example) then Slurm will kill the job. Our simple parallel program will complete before one hour.
The module purge line is new – it ensure your job starts with a clean environment. Without this, your job will have inherited any modulefiles you had loaded on the login node.
The module load apps/intel-17.0/tutorial line is new – this will load a modulefile in to the job’s environment when it runs on a compute node. The modulefile will apply settings (possibly loading other modulefiles) needed to allow the pmp application to run. All of the centrally installed applications have modulefiles to make running the apps as easy as possible.
The export OMP_NUM_THREADS=$SLURM_NTASKS line is new – this is how we inform the pmp application how many CPU cores it is allowed to use. The app does not know this automatically. We reserved 4 cores in the batch system but we must then inform the application that it can use 4 cores.
The $SLURM_NTASKS variable is automatically set by the batch system to the number of cores requested on the #SBATCH -n line. So this is a convenient way of always getting the correct number of cores.

The pmp line is new – pmp is the name of the parallel matrix multiplication application we are going to run.
Step 2: Copy to scratch area
We now copy the jobscript to your scratch area – recall we recommend running jobs in your scratch area – it is faster and permits jobs to write large temporary files without filling up your group’s home directory quota. But you must remember to copy important results back to the home area for safe keeping.

cp second-job.txt ~/scratch
We can now go in to the scratch area:

cd ~/scratch
Our scratch directory is now our current working directory. When we submit the job to the batch queue (see next step) it will run in the scratch area, outputting any results files there.

Step 3: Submit the Job to the Batch System
Assuming your jobscript is called second-job.txt, submit your jobscript (the copy that is in your scratch area) to the batch system:

sbatch second-job.txt
You’ll see a message printed similar to:

Submitted batch job 195502
The job id 195502 is a unique number identifying your job (obviously you will receive a different number). You may use this in other commands later.

Step 4: Check Job Status
Use the squeue command to check the job status. By looking at the ST column (short for “State”), you should be able to determine if it is pending (PD), running (R), failed (F) or finished (squeue shows nothing).

Step 5: Review Job Results/Output
The job will have created an output file: slurm-195502.out, which contains the output from the job. This will include any normal output (e.g., if the pmp prints out any messages and also any error messages. Let’s have a look at the file size by doing a long listing which shows more information about the files:

# Run the 'ls' command with a '-ltr' flag added for a long listing

# with the most recently updated files listed at the bottom of the listing.

ls -ltr
-rw------- 1 username xy01 345 May 4 13:16 second-job.txt
-rw-r--r-- 1 username xy01 337 May 4 13:18 slurm-195502.out
^ ^ ^ |**\_\_\_**| ^ ^
| | | | | | Your job id number will be different
| | | | |
+-File permissions | | | +- Filenames
| | |
| | +- Date and time of last update
| | (i.e. when something was written to the file)
| |
| +- Filesize in bytes.
|
+- The group you are in. It usually indicates
your faculty or supervisor.
Examine the contents of the slurm-195502.out file – any output printed by the pmp app will have been captured in to here:

cat slurm-195502.out # # Use the jobid number for your job!
You will see the number of cores used by pmp reported, followed by the 2D matrix size used in the tests, followed by timing information for five runs of the matrix calculation.

Step 6: Repeat the job with a different number of cores
To show the effect of using more cores with the pmp application, edit your jobscript:

gedit second-job.txt
then change the number of cores

#SBATCH -n 8 # Use 8 cores instead of 4 previously
Save the file and resubmit it to the batch system:

sbatch second-job.txt
Submitted batch job 195503
When the job has completed (check using squeue) have a look at the timing information for the second run of the job. It should show the five runs of the calculation were done in approximately half the time:

cat slurm-195503.out # # Use the jobid number for your job!
If you wish to run the pmp application with a different number of cores (up to 168 cores are permitted in the multicore partition) then edit the jobscript again and resubmit the job.

Summary
You have now been able to run a parallel job. It was a single-node multi-core job which used multiple CPU cores within a single compute node. The application supports this type of parallel processing and we could verify that it ran quicker with more cores. We used a modulefile to give us access to the centrally installed pmp application.

More on Using the Batch System (parallel jobs, GPUs, high-mem)
The batch system, SGE, has a great deal more functionality than described above. Other features, including:

Running parallel multi-core/SMP jobs and the AMD nodes (e.g., using OpenMP)
Running job arrays — submitting many similar jobs by means of just one sbatch script/command
Running GPU jobs
Selecting high-memory jobs
These are fully documented (with example job scripts) in the CSF SGE documentation.

Finally, each centrally installed application has its own application webpage where you will find examples of how to submit a job for that specific piece of software and any other information relevant to running it in batch such as extra settings that may be required for it to work.
