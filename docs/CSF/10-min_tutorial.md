Batch System 10 Minute Tutorial (Slurm)
Introduction
This page offers new CSF users a tutorial that covers usage of the Slurm batch system to run a simple job on the CSF.

The tutorial also provides some information about the storage areas on the CSF, and also some common Linux commands used to manage your files.

After doing the tutorial you’ll be able to use the CSF. A further tutorial is also available for running more complicated parallel jobs.

If you are interested in attending the 1-day Intro to CSF training course which runs a couple of times each semester, please take a look at the course booking page for details of the schedule and availability.

Before we begin the tutorial we’ll explain what the batch system is and why we need to use it.

Background: What is a batch system and why use it?
Click on each header below to expand the section:

Join the queue…
Initially a batch system can be thought of as a job queue. You submit jobs to the queue and the system will pick them out of the queue to run them.

The jobs will do whatever commands you ask them to do (for example run an app such as a chemistry app, or a bioinformatics app or whatever application is appropriate to your work).

When the jobs finish, you should have some new files containing the results.

At this point you might be thinking you don’t like the idea of your work (jobs) waiting in a queue. How long will it queue for? Why can’t it just run immediately? Read on to find out more.

Ask for extra memory, cores or a GPU?
The applications you’ll be running on the CSF usually need different amounts of memory, number of CPU cores or even GPUs.

You can request these specific resources for your job. Need a GPU? Simply request it in your job. Need a lot of memory to process a huge dataset? Simply ask for it.

The batch system ensures your job only runs when all of the required resources are available. It then allocates those resources to your job (so that it runs correctly) and makes sure no other jobs can grab your resources.

But don’t worry if you’re not sure what resources you’ll need – there are sensible defaults. After trying the defaults, you might find your app needs more memory to process your data, or that it can use more CPU cores to make it run faster.

So you might find that your first few attempts at running jobs don’t actually complete successfully. Maybe you’ll need to run the jobs again but request more memory. Don’t worry – failed jobs don’t do any harm. You can simply delete the output files from these failed jobs (if there are any), modify your jobscript to ask for more resources (more memory, CPUs, …) and then resubmit your jobs.

Fair usage
The batch system also ensures fair usage for you and others – there are many users and jobs on the system, all making different demands of the resources (memory, CPU cores, GPUs) and so allowing the batch system to choose exactly when to run your job is the only sensible way of running the system.

The fact that jobs are starting and finishing all the time means you rarely have to wait very long for your requested resource to become free so that your jobs can start.

There are other factors which control when jobs run (and how many of your jobs can run at the same time) but the use of a job queue should not put you off using the system.

Let the CSF get on with it
An added bonus of a batch system is that once you’ve submitted your jobs to the system, you don’t actually need to remain logged in. You can log off, go home or go to a meeting or do something else with your PC/laptop.

Meanwhile the batch system will run your jobs. It can even email you when a job has finished.

Without a batch system, you would need to remain logged in to the CSF until the job had finished, which could be a problem for a simulation that takes several days to complete.

No GUI
Something to note about batch jobs is that you never see an application’s graphical user interface (GUI), if it has one. Batch jobs run without any interaction – all options / flags / input files etc will be specified on the command-line in a jobscript (more on those later).

When the app is running, all output will be saved to files. This will be a new way of working if you are used to running an app in a desktop environment (e.g., on Windows).

Can I just run my app on the Login Node?
Running your code or application directly on the login nodes is not permitted.

The login nodes are for other tasks (transferring files on and off the system, editing jobscripts, submitting jobs to the system, checking results.) They don’t have a lot of memory, nor many cores, so trying to run your apps there is inefficient and may also adversely affect other users.

Applications found running on the login nodes may be killed by the sysadmins without warning.

Please do take the time to learn about the batch system. While it may be an unfamiliar way of working initially, particularly if you are used to simply running your apps immediately on a desktop PC, there are actually a lot of benefits to using the batch system – you’ll see it is a very powerful way of working as you begin to do your real work.
In this tutorial you can try out the sample job below – it shouldn’t take more than 10 minutes to work through the instructions on this page.

Which batch system does the CSF use?
The CSF3 now runs the Slurm batch system.

The three main Slurm commands you use are sbatch, squeue and possibly scancel.

10 Minute Tutorial: Submitting a First Job to the Batch System
This tutorial assumes you are already logged in to the CSF – please see the login instructions for more information.

Here we describe in detail how to submit a simple, first job to the batch system. Please read all of the text, don’t just look for the commands to type, as it will explain why you need to run the commands.

What type of job will we run?
We will run a serial job – i.e., it uses only one CPU core. We’ll see later that many of the real applications on the CSF can use more than one CPU core (a multi-core job) to speed up their processing, giving you the results sooner.

You could also request more memory than the default 5-6GB of RAM. You could also request a GPU.

But initially a simple 1-core (serial) job will help you become familiar with the principles of the batch system. These jobs are very common – you may well want to use this type of job in your real work after the tutorial.

Please remember: Do not simply run jobs on the login node – use the batch system as described below.

Step 0: Create a Folder for the Job Files
In the following steps we will be creating a jobscript file. We will explain more about the file in the next step. The job will also create some files (any output generated by the job is saved to files).

Hence we first create a directory (folder) for the job to keep all of the files together in one place. This is important – you will likely run a lot of jobs on the CSF so it will be easier to manage all of your work if you keep your files tidy.

When you login to the CSF you are placed in your home directory. This area of storage is private to you and, importantly, is backed-up (not all storage areas on the CSF are backed-up). It is strongly recommended that you keep important files in your home directory for safe keeping – and this includes your jobscripts.

Once you have logged in you’ll be at the command-line prompt:

[mxyzabc1@login1[csf3] ~]$ you will type your commands here, "at the prompt"
^ ^ ^ ^
| | | |
| | | +--- The directory (folder) you are currently in.
| | | ~ means your home folder, which is your private folder.
| | |
| | +--- Name of the system
| |
| +--- Name of the login node (some systems have more than one login node)
|
+--- Your username appears here
Now create a directory (usually referred to as a folder in Windows or MacOS) in your CSF home storage area, for our first test job, by running the following commands at the prompt:

# All of these commands are run on the CSF login node at the prompt

mkdir ~/first-job # Make (create) the directory (folder)
cd ~/first-job # Change to (go into) the directory (folder)
Notice that the prompt has changed to indicate you have moved in to the first-job folder:

[mxyzabc1@login1[csf3] first-job]$  
 ^
|
+--- The prompt shows we are now in the first-job folder
Step 1: Create a “Jobscript” – a job description file
The jobscript file is the thing you submit to the batch system (i.e, the queue of jobs.) It is just a simple plain-text file. It serves two main purposes:

It specifies the number of CPU cores, memory, maximum time the job is allowed to run for, and other resources you need to run your application.
It specifies the actual command(s) needed to run your application and anything else your job will do (e.g., copy files).
A key benefit of the jobscript is that it documents exactly what you did to run your job – no need to remember what you did 6 months ago as it is all there in the jobscript. If you ever need to run a job again, or run similar jobs, having the jobscript available is very useful.
Hence jobscripts should be considered part of your work that needs to be kept securely in your home directory. They are a record of how you ran a simulation or analysis, for example, or how you processed a particular dataset. Jobscripts are therefore part of your research methods.

We now use gedit or xnedit or another editor, on the CSF login node (running text editors on the login node is permitted) to create a file with exactly the following content (see below). You can name the file anything you like, as long as there are no spaces in the name – in this example we use first-job.txt but Linux doesn’t care what extension you use – .txt or .sbatch or .jobscript for example:

# Run this command on the CSF login node at the prompt

gedit first-job.txt

#

# If gedit opens, you can IGNORE any warnings / messages that appear in the terminal from gedit.

# For example: (gedit:5246): dconf-WARNING \*\*: .........

#

# Can't see gedit? Check your "dock" - it might have opened but the window is behind others on

# your desktop.

If you see an error similar to

(gedit:1639570): Gtk-WARNING \*\*: 16:21:05.503: cannot open display:
Please ensure you have logged-in using the method that allows GUI apps to be used – this mostly affect Mac user, so please take a look at the Mac login instructions.

Note for Windows users: You can create the jobscript below in Notepad and then transfer the file to CSF, although we don’t actually recommend this method. The file can have any name (we’re using first-job.txt but anything will be OK – you’ll find that Notepad names files with .txt at the end anyway).
However, you must run the following command on the login node to convert the file from Windows format to Linux format otherwise the job will report an error when you submit it to the batch system (this is only needed for jobscripts, not any other file)

# Run this command on the CSF login node at the prompt if jobscript was written in notepad

dos2unix first-job.txt # # or whatever filename you used (we assume notepad adds .txt)
But we recommend that Windows users install MobaXterm to log in to the CSF. You can then run gedit on the CSF login node and you’ll get a Linux text-editor very similar to Notepad. The file you write will be saved directly on the CSF and will not need converting with dos2unix because it is already in the correct format.

Here’s the jobscript content – put this in the text file you are creating either in gedit (run on the CSF login node) or notepad (run on your Windows PC):

#!/bin/bash --login

# Slurm options are those that begin with #SBATCH

#SBATCH -p serial # Run in the "serial" partition (compute nodes dedicated to 1-core jobs)
#SBATCH -t 5 # Allow a maximum wallclock time limit of 5 minutes # Our simple job actually only runs for about 2 minutes # but we always set the wallclock limit a little longer. # (Other time formats can be used for days and hours.)

# Now the example commands to be executed (programs to be run) on a compute node:

# In your real work, you'll run apps such as a chemistry app, or a bio-inf app.

# Pre & post processing steps can also be included here.

/bin/date
/bin/hostname
/bin/sleep 120
/bin/date
Note: lines must NOT be indented in your text file – there should NOT be any spaces at the start of the lines. Cut-n-paste from this web page will work correctly in most browsers in that it won’t copy any leading space.

This BASH script has three parts:

The first line, #!/bin/bash --login, means that the file you create is treated as a BASH script.
Linux provides several scripting languages but BASH is the one you use at the command-line once you’ve logged in. So we usually use it for jobscripts too. This means that any commands you would normally type at the command-line can also go into your jobscript to be run as part of a batch job.

The lines beginning with #SBATCH are commands to the batch system – they provide information about your job.
In this simple jobscript the lines are:

#SBATCH -p serial runs your job in the “serial” job area (partition). This is a dedicated set of compute nodes used to run serial (1-core) jobs.
#SBATCH -t 5 says that your job is allowed to run for no more than 5 minutes, once it starts. It is perfectly fine if your job completes its work in less time (and in fact our simple job will complete in about 2 minutes.) But if a job was still running once the wallclock time limit is reached, then the batch system will kill the job. So we always give a little extra time on the wallclock limit, just for safety.
Note that the job, when it runs, will be run from the folder (directory) from which you submitted the job. This will be where any output files are written. If the job needed to read some input data file (our job doesn’t) then they would be read from the submit directory too.
The remaining lines comprise our computational job – the applications we actually want to run.
In this example we have a trivial job which runs simple Linux commands to output the date and time, followed by the name of the compute node on which the job runs, then waits for two minutes and finally outputs the date and time again. In a real jobscript you would do something more interesting and useful – e.g., run MATLAB or Abaqus or a chemistry program.

Please Note:If applicable, pre‑ and post‑processing steps can be included in the same job script as the main computational task/job.

Step 2: Copy to scratch area
We now copy the jobscript to your scratch area.

We recommend you run jobs from the scratch filesystem: it is another area of storage on the CSF that is faster and larger. Your home directory is in an area that has a quota to be shared amongst everyone in your group – if your job fills up that area you will prevent your colleagues from working! Running jobs in the scratch area avoids this problem.
PLEASE NOTE: the scratch area is a temporary area – files unused in the last 3-months can be deleted by the system to free up space. You should always have a copy of important files in your home area (or other research data storage visible on the CSF that your research group may have access to). Think of scratch as fast, temporary storage – if your job reads and writes large files it will be faster if run from scratch.

A good way of working is to create your important files in the home area, then copy them to scratch when you need to use them in your jobs. That way you always have a safe copy in your home area.

So let’s copy our jobscript to the scratch area (we keep the original in our home area for safe keeping):

cp first-job.txt ~/scratch
We can now go into the scratch area:

cd ~/scratch
Our scratch directory is now our current working directory. When we submit the job to the batch queue (see next step) it will run in the scratch area – remember, the job runs from which ever directory you are in when you submit the job.

Any files that the job generates will also be written to the scratch area and if your job wants to read input data files (ours doesn’t in this example) then it would try to read them from the scratch area.

You will notice the prompt on the command-line will change to indicate where you are currently located:

[mxyzabc1@login2[csf3] scratch]$ # # The prompt shows your current directory
Step 3: Submit the Job to the Batch System
Recap: So far we have created a directory for the jobscript in our home area, written a jobscript text file there (where it is stored safely on backed-up storage), then copied it to the fast temporary scratch storage and changed directory to our scratch area where we’ll run the job from.

The next step is to actually submit the job to the batch system. Suppose, the above script is saved in a file called first-job.txt. Then the following command will submit your job to the batch system:

sbatch first-job.txt

# You'll see a message:

Submitted batch job 195501
The job id 195501 is a unique number identifying your job (obviously you will receive a different number). You may use this in other commands later.

Step 4: Check Job Status
To confirm that your job is queued, or perhaps already running, enter the command

squeue
If the job is still pending (waiting to run) the output from squeue will look like the following – notice the ST column (short for “State”) – it shows “PD” for pending:

                                                                                       NODELIST

JOBID PRIORITY PARTITION NAME USER ST SUBMIT_TIME START_TIME TIME NODES CPUS (REASON)
195501 0.019104 serial first-jo mxyzabc1 PD 21/05/25 9:51 N/A 0:00 1 1 (None)
If your job is already running, the output will look like the following – notice the ST column shows “R” for running and the NODELIST column shows the name of the compute node where your job is currently running. This shows that your job is not using the login node, even though that’s where you are running commands, but is instead using one of the more powerful servers in the CSF.

                                                                                       NODELIST

JOBID PRIORITY PARTITION NAME USER ST SUBMIT_TIME START_TIME TIME NODES CPUS (REASON)
195501 0.019104 serial first-jo mxyzabc1 R 21/05/25 9:55 ... 9:55 0:05 1 1 node003
If your jobs have finished, squeue will show no output – meaning you have no jobs in the queue, either running or waiting.

[mxyzabc1@login02 [CSF4] scratch]$ squeue
JOBID PRIORITY PARTITION NAME USER ST SUBMIT_TIME START_TIME TIME NODES CPUS (REASON)

#

# No jobs listed means you have no jobs waiting or running (all jobs have finished)

If something is wrong with your jobscript you’ll see F or some other code. There might also be a REASON to help diagnose the problem. Please contact us via the Connect Portal HPC Help form, stating your job-ID and the system you are logged in to and we’ll let you know what has gone wrong.

HINT: the most common error is making a typo in your jobscript. Errors don’t do any harm to the CSF, they just mean your job won’t do what you want it to do. Check the contents of your jobscript (see above for the original text.)

A typo on the first line of the jobscript is often the cause. Please type it carefully: #!/bin/bash --login (no spaces at the start of the line.) Once you have corrected the jobscript, resubmit it by running squeue jobscript again. Note that correcting a jobscript while it is waiting in the queue, or running, does not work. The batch system takes a copy of your jobscript when you run squeue. So any changes you make to your file won’t be seen by the batch system.

If there is no output from the squeuecommand, your job has finished.

Step 5: Review Job Results/Output
Each job will output least one file, containing any output that would normally have been printed to screen. This can including normal information from your app and also error message, if any occurred.

Let’s list the files in the current directory using the Linux ls command:

ls
first-job.txt slurm-195501.out
We can see our original jobscript first-job.txt and a new file slurm-195501.out that has been generated by the job (remember, the job ID number 195501 will be different for your job.)

To look at the contents of the output file:

cat slurm-195501.out
In this example the output file contains:

Wed May 21 09:55:49 BST 2025
node003
Wed May 21 09:57:49 BST 2025
shows the date, twice with a difference of 120 seconds (2 minutes), and the name of the compute node on which the job ran, as expected (refer back to the commands we ran in our first jobscript).

Note that the names of the output file is always, by default, slurm-JOBID.out. It might be easier to keep track of which job output which file if you make the output file use a similar name to that of your jobscript. You can change the start of the name of the output file by adding the following line to your jobscript (change myjobname to something meaningful for your job)

#SBATCH -o %x.o%j # %x will be replaced by the jobscript name # %j will be replaced by the JOBID number
This would generate an output file named first-job.txt.o195501 (which will be familiar to users of the SGE batch system, which we used to use on the CSF.)

You’ve now successfully run a job on the CSF. It was a simple 1-core job (it used only one CPU core) to run some basic Linux commands. The output of the commands was captured in to the slurm-195501.out file. By changing the Linux commands to something more useful (e.g., to run your favourite chemistry application) you can get lots of real work done on the CSF.

Step 6: Copy Results back to “home”
Earlier we said that the scratch storage area is temporary (but fast). Hence if we want to keep the results from this job then we should copy them back to the home storage area. Let’s assume we DO want to keep the output from this job. Apart from the usual slurm-195501.out file, it didn’t generate any other files. So we’ll just copy the .out file back to home:

# Copy from the current scratch dir to the job's directory in home

cp slurm-195501.out ~/first-job/ # # This number will be different for your job
That’s it, the output file is now stored in our backed-up home area. We could delete the file from scratch, although sometimes you may wish to leave your files there while you check their contents and possibly use them in future jobs. Remember though, the scratch filesystem will tidy up old files automatically, so at some point they will be deleted.

When you run a real app (e.g., a chemistry app or OpenFOAM) then your jobs may well generate other files (lots of them, possibly large files.) You’ll need to consider more carefully which files you want to keep.

Summary
Points to remember

Do not simply run your apps on the login node. Write a jobscript and submit it to the batch system. Your app will run on a more powerful node and won’t upset the login node (and the sysadmins!)
You can write your jobscript on the login node using gedit or xnedit.
Alternatively, if you use notepad on MS Windows, ensure you run dos2unix on the jobscript once you’ve transferred it to the CSF.
Keep your important files in your home area but copy them to the scratch area and run your jobs from there. Don’t forget to copy important results back to home.
Submit the job using sbatch
Check on the job using squeue
Look in the slurm-195501.out file generated by the job for output and errors.
If you have any questions please contact us via the Connect Portal HPC Help form – we’re here to help.
More on Using the Batch System (parallel jobs, GPUs, high-mem)
The batch system has a great deal more functionality than described above – by adding more #SBATCH special lines to your jobscript your jobs can make more use of the CSF capabilities. A list of features is given below with links to documentation. You may wish to try the Parallel Job Tutorial once you are familiar with running serial (1-core) jobs on the CSF.

Other features include:

Running parallel multi-core/SMP jobs (e.g., using OpenMP)
Running parallel multi-host jobs (e.g., using MPI)
Running job arrays — submitting 100s, 1000s of similar jobs by means of just one sbatch script/command
Running GPU jobs
Selecting high-memory hardware
These features are fully documented (with example job scripts) in the CSF Slurm documentation.

Application Software
Now that you’ve run a test job you might want to have a look to see whether the application software you intend to use is already installed on the CSF – a lot of apps are already installed.

Each centrally installed application has its own application webpage where you’ll find examples of how to submit a job for that specific piece of software and any other information relevant to running it in batch, such as extra settings that may be required for it to work.
