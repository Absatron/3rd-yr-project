Default Memory on the CSF
The AMD 168-core Genoa nodes (-p multicore) have 8GB RAM per core. If your job needs more RAM on these nodes, request more cores.

The standard Intel nodes (-p serial and -p multicore_small) have 4GB to 6GB of RAM per core. If your job needs more RAM on these nodes, request more cores.

High-memory Intel nodes are also available, offering up to 2TB RAM in total , and if really needed, up to 4TB, and are described below. When using these nodes, the number of cores and amount of memory can be specified independently.

First we describe how to check if your jobs are running out of memory (RAM).

We only have a small number of high memory nodes. They should only be used for work that requires significant amounts of RAM. Incorrect use of these nodes may result in restrictions being placed on your account.
Does your parallel job need 8GB per core or less? The AMD nodes in the multicore partition may be suitable for your work
How to check memory usage of your job
The batch system keeps track of the resources your jobs are using, and also records statistics about the job once it has finished.

A completed (successful) job
You can see the peak memory usage with the seff command, passing in a JOBID:

[mabcxyz1@login1[csf3] ~]$ seff 12345
Job ID: 12345
Cluster: csf3.man.alces.network
User/Group: username/xy01
State: COMPLETED (exit code 0)
Nodes: 1
Cores per node: 2
CPU Utilized: 00:04:13
CPU Efficiency: 49.41% of 00:08:32 core-walltime
Job Wall-clock time: 00:04:16
Memory Utilized: 21.45 GB # Peak memory usage
Memory Efficiency:33.5% of 64.00 GB # A low memory efficiency means this job did NOT need # to use the himem partition. You should check this.
To check a specific jobarray task, use a JOBID of the form jobid_taskid:

seff 12345_501
Alternatively, use the sacct command to obtain various stats about a job;

sacct -j 12345

# Or to just get the memory usage

sacct -j 12345 -o maxrss
The sacct command offers lots of options – use man sacct to get more info.

Depending on the software you are using you may also find memory usage reported in output files.

A terminated (out of memory) job
If at any point during the running of the job, the job’s peak memory usage goes above the limit that the job is permitted to use, then the job will be terminated by the batch system.

The seff command will show:

[mabcxyz1@login1[csf3] ~]$ seff 12345
State: OUT_OF_MEMORY (exit code 0)
You may see the following in your slurm-12345.out file:

[mabcxyz1@login1[csf3] ~]$ cat slurm-12345.out

/var/spool/slurmd/job12345/slurm_script: line 4: 1851022 Killed ./some-app.exe -in data.dat -out results.dat
slurmstepd: error: Detected 1 oom_kill event in StepId=12345.batch. Some of the step tasks have been OOM Killed. # # OOM is "out of memory" - this means Slurm killed your job # because it tried to use more memory than allowed.
You will need to resubmit your job, either requesting more cores (if using the standard partitions) or use a high memory partition – see next.

Submitting High Memory Jobs
Please note: The 2TB himem nodes are freely available to everyone. The 4TB vhimem node is restricted. Please request access to this node from us before submitting jobs to this partition (we will check that your jobs are running out of memory on the 2TB nodes.)

Memory is a “consumable” resource in the himem and vhimem partitions in the CSF (Slurm) cluster – you can specify how many cores AND how much memory your job requires (in the multicore partition, you can’t do this – instead you get a fixed amount of RAM per core.)

For users that have previously used the CSF (SGE) cluster, there are no mem1500, mem2000 or mem4000 flags! There, memory was not a consumable – you had to request a certain number of cores, and the -l memXXXX flag would land the job on a node that gave a fixed amount of memory-per-core.

On the CSF (Slurm) cluster, your jobs will land on any of the high-memory nodes to meet your core and memory requirements. You can optionally specify a CPU architecture if that is important to your job, but this will restrict the pool of nodes available for Slurm to choose from, and so might lead to longer queue-wait times.

So, in summary, specify the amount of memory your job requires. If you need more than one core, specify the number of cores. But the number of cores does not necessarily determine the amount of memory.

High Memory Resources
The following resources are available to your job.

The partition (and wallclock limit) are required. All other flags are optional.

Note:

If not specified, a job will use 1 CPU core.
Memory units M (megabytes), G (gigabytes) or T (terabytes) can be specfied – e.g., 700G. If no units letter is used, it defaults to M megabytes.
Different Intel CPU architectures are available for high-memory jobs, but this is an optional flag. We recommend you do not specify an architecture. Slurm will place your job on any node that satisfies your core and memory requirements. You can request a particular architecture if required, but doing so may lead to longer queue-wait times.
Remember: you DO NOT specify the old SGE flags – Slurm knows nothing about these. Just say how much memory your job needs.

Partition (required) Default job mem-per-core if memory not requested (GB) Max job size (cores) Max job memory (GB) Arch Flag (optional, but will activate specific limits shown in the next columns) Max job size (cores) Max job memory (GB) Has SSD storage Old SGE flag (DO NOT USE)
himem 31 32 2000 -C haswell 16 496 No mem512
-C cascadelake 32 1472 No mem1500
-C icelake (also ssd) 32 2000 Yes mem2000
vhimem 125 32 4000 -C icelake (also ssd) 32 4000 Yes mem4000
If you have access to the 4TB node please do not submit lots of jobs to the queue at the same time, even if they genuinely need the RAM, we have to try and ensure that it not dominated by individuals so that everyone who needs it has an opportunity to run work on it.

Slurm Memory Flags
You will need to request an amount of memory for your high-memory job. You can use either of the following Slurm flags:

# Specify the total amount of memory your job will have access to

#SBATCH --mem=nG # A total of n Gigabytes

# OR, specify an amount of memory per core

#SBATCH --mem-per-cpu=mG # Your job will get numcores x m Gigabytes of RAM
DO NOT specify BOTH of the above memory flags – you should only specify one.

Example jobs
A high-memory job using the default 1-core and 31GB RAM. Remember – high-mem jobs can land on any of the high-memory compute nodes – you do not specify the old SGE mem2000 flag, for example.

#!/bin/bash --login
#SBATCH -p himem # (or --partition=) A high memory job
#SBATCH -t 1-0 # Wallclock limit, 1-0 is 1 day (max permitted is 7-0, 7 days)
module purge
module load apps/some/thing/1.2.3
some-app.exe
Further examples will only show the Slurm #SBATCH flags for brevity.

A high-memory job requesting 2 cores and 64GB RAM in total

#!/bin/bash --login
#SBATCH -p himem # (or --partition=) The high memory partition
#SBATCH -n 2 # (or --ntasks=) Number of cores
#SBATCH --mem=64G # Total memory for the job (actually per-node but jobs only run on one node)
#SBATCH -t 1-0
A high-memory job requesting an entire 2000GB node (32 cores max – if using all of the 2000 GB memory you might as well request all of the cores!)

#!/bin/bash --login
#SBATCH -p himem # (or --partition=) The high memory partition
#SBATCH -n 32 # (or --ntasks=) Number of cores
#SBATCH --mem=2000G # Total memory for the job (actually per-node but jobs only run on one node)
#SBATCH -t 1-0
A vhighmem 4000 GB node job, requesting more than 2000GB of RAM. Please request access to this node from us before submitting jobs to this partition. Please include some job IDs of jobs that have exceeded the memory of the nodes in the himem partition.

#!/bin/bash --login
#SBATCH -p vhimem # (or --partition=) The VERY high memory partition
#SBATCH -n 20 # (or --ntasks=) Number of cores (max is 32)
#SBATCH --mem=3000G # Total memory for the job (actually per-node but jobs only run on one node)
#SBATCH -t 1-0
Runtimes and queue times on high memory nodes
The maximum job runtime on higher-memory nodes is the same as other CSF nodes, namely 7 days.

Due to the limited number of high memory nodes we cannot guarantee that jobs submitted to these nodes will start within the 24 hours that we aim for on the standard CSF3 nodes. Queue times may be several days or more.

We monitor usage of all the high memory nodes and will from time to time advise people if we think they are being incorrectly used. Persistent unfair use of high memory nodes may result in a ban from the nodes or limitations being placed on your usage of them.
Local SSD storage on high memory nodes
Some of the newer nodes have particularly large, fast local SSD storage in the nodes. This can be useful if your jobs do a lot of disk I/O – frequently reading/writing large files. Your jobs may benefit from first copying your large datasets to the SSD drives, then running in that area where they can write output files. Finally, copy any results you want to keep back to your scratch area.

To ensure your high-memory job lands on a node with SSD storage, add -C ssd to your jobscript.

To access the SSD drives within a jobscript, use the preset environment variable $TMPDIR. For example

#!/bin/bash
#SBATCH -p highmem # (or --partition=) The high memory partition
#SBATCH -n 8 # (or --ntasks=) Number of cores (max is 32)
#SBATCH --mem=1200G # Total memory for the job
#SBATCH -C ssd # Guarantees that the job lands on a node with SSD storage
#SBATCH -t 1-0 # Wallclock time limit, 1-0 is 1 day (max permitted is 7-0, 7 days)

# Copy data from scratch to the local SSD drives

cp ~/scratch/my_huge_dataset.dat $TMPDIR

# Go to the SSD drives

cd $TMPDIR

# Run your app

myapp my_huge_dataset.dat -o my_huge_results.dat

# Copy result back to scratch

cp my_huge_results.dat ~/scratch
The $TMPDIR area (which is private to your job) will be deleted automatically by the batch system when the job ends.

Remember, the $TMPDIR location is local to each compute node. So you won’t be able to see the same $TMPDIR storage on the login nodes or any other compute node. It is only available while a job is running.

Last modified on June 24, 2026 at 10:55 am by Pen Richardson

Disclaimer Data Protection Copyright notice Web Accessibility Freedom of information Charitable status Royal Charter Number: RC000797
Help for Authors | Log in
