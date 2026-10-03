Nvidia GPU Jobs (Slurm)
Access
This page covers the Nvidia A100 (80GB), A100 (40GB) and L40S GPUs in Slurm.

Notes for Slurm users – please read:
All users have access to the A100 (80GB) and L40S GPUs – you do not need to submit a ticket to request access.
The A100 (40GB) GPUs are limited to a small number of users from a specific group.
The H200 GPUs have a specific access policy (please check before requesting access.)
See the Slurm Partitions page for the available hardware.
GPUs now run in “DEFAULT” compute mode, not “EXCLUSIVE_PROCESS”. Hence you can run multiple processes on the GPUs assigned to your job. Slurm will prevent other jobs from accessing the GPUs assigned to your job.
Feb 2026 update: a change has been made to the way in which the 4-GPU free-at-point-of-use GPU limits are applied – see below for details.
Free at Point of Use access
Please use the gpuA and/or gpuL paritions.

20-Feb-2026: The current limits are: up to four A100(80GB) or L40S GPUs in use at any one time. These can now be all of the same GPU type. For example you can use 4 x A100(80GB) GPUs or 4 x L40S GPUs or a mixture of the two. You can submit as many jobs as you wish – the system will run them within the limits.

Users that have previously had temporary increased limits via the gpuax4 or gpulx4 QOSs should no longer use those QOSs. Simply submit your 4xGPU jobs and the new f@pou limits will allow the jobs to run.

PLEASE NOTE: Now that the free-at-point-of-use limits have been modified to allow 4 of the same type of GPUs to be used, we will NOT accept requests for access to more than 4 GPUs.

Contributor access
Members of groups that have contributed GPUs will be informed of their limits when CSF accounts are created.

A100 (40GB) GPU access
The A100-40G nodes have been funded by a specific research group and so access is very restricted. You will be informed if you have access to these GPUs.

GPU batch job submission (Slurm)
For jobs that require GPUs – running on one or more GPUs in a single compute node. A jobscript template is shown below. Please also consult the Partitions page for details on available compute resources.

Please also consult the software page for the code / application you are running for advice on running that application.

A GPU job script will run in the directory (folder) from which you submit the job. The jobscript takes the form:

#!/bin/bash --login

### Choose ONE of the following partitions depending on your permitted access

#SBATCH -p gpuA # A100 (80GB) GPUs [up to 12 CPU cores per GPU permitted]
#SBATCH -p gpuA40GB # A100 (40GB) GPUs [up to 12 CPU cores per GPU permitted]
#SBATCH -p gpuL # L40S GPUs [up to 12 CPU cores per GPU permitted]

### Required flags

#SBATCH -G N # (or --gpus=N) Number of GPUs
#SBATCH -t 1-0 # Wallclock timelimit (1-0 is one day, 4-0 is max permitted)

### Optional flags

#SBATCH -n numcores # (or --ntasks=) Number of CPU (host) cores (default is 1) # See above for number of cores per GPU you can request. # Also affects host RAM allocated to job unless --mem=num used.

module purge
module load libs/cuda/x.y.z # See below for specific versions

echo "Job is using $SLURM_GPUS GPU(s) with ID(s) $CUDA_VISIBLE_DEVICES and $SLURM_NTASKS CPU core(s)"
gpuApp args ...
Note that the amount of host RAM your job has access to is dependent on the number of CPU cores you request, unless you request a specific amount of host memory for your job using the --mem=numG or --mem-per-gpu=numG flags. Note that the default units of memory are megabytes if no units are given (use G for gigabytes.)

GPU Max host cores per GPU Host RAM per core (GB) Max host RAM per GPU (GB)
A100(80GB) 12 10.4 125
A100(40GB) 12 10.4 125
L40S 12 10.4 125
Available Hardware and Resources
Please see the Partitions page for details on available compute resources.

Software Applications
A range of GPU capable software is available on the CSF.

List of installed GPU capable software.
List of installed Machine Learning specific software.

GPU Hardware and Driver
The CSF (Slurm) will contain the following GPU nodes, which offer different types of Nvidia GPUs and host CPUs.

For the current list of resources please see the Slurm Partitions page.

The following information is for reference only – it does not mean that all of these nodes are currently available in Slurm!

19 GPU nodes each hosting 4 x Nvidia A100 GPUs (80GB GPU RAM) giving a total of 64 A100 GPUs. The node spec is:

4 x NVIDIA HGX A100 SXM4 80GB GPU (Ampere architecture – hardware v8.0, compute architecture sm_80)
2 x 24-core AMD Epyc 7413 “Milan” 2.65GHz
512 GB RAM (host)
1.6TB local NVMe storage, 364GB local SSD storage
nVidia Driver 580.126.09 – CUDA vesrion 13.0
2 GPU nodes each hosting 4 x Nvidia A100 GPUs (40GB GPU RAM) giving a total of 8 A100_40G GPUs. The node spec is:

4 x NVIDIA A100 SXM4 40GB GPU (Ampere architecture – hardware v8.0, compute architecture sm_80)
2 x 24-core AMD Epyc 7413 “Milan” 2.65GHz
512 GB RAM (host)
1.6TB local NVMe storage, 364GB local SSD storage
nVidia Driver 580.126.09 – CUDA vesrion 13.0
21 GPU nodes hosting 4 x Nvidia L40S GPUs (48GB GPU RAM) giving a total of 12 L40S GPUs. The node spec is:

4 x NVIDIA L40S 48GB GPU (Ada Lovelace architecture – hardware v8.9, compute architecture sm_89)
2 x 24-core Intel Xeon(R) Gold 6442Y “Sapphire Rapids” 2.6GHz
512 GB RAM (host)
28TB local NVMe storage (under a RAID controller) mounted on /tmp
nVidia Driver 580.126.09 – CUDA vesrion 13.0
Fast NVMe storage on the node
The very fast, local-to-node NVMe storage is available as $TMPDIR on each node. This environment variable gives the name of a temporary directory which is created by the batch system at the start of your job. You must access this from your jobscript – i.e., on the node, not on the login node. See below for advice on how to use this in your jobs.

This directory (and all files in it) will be deleted automatically at the end of your job by the batch system.

Reminder: The above storage areas is local to the compute node where your job is running. You will not be able to access the files in the temporary storage on the login node.

Batch jobs running on the GPU nodes have a maximum runtime of 4 days.
Interactive GPU jobs have a maximum runtime of 1 day.
Job Basics
Batch and interactive jobs can be run. You must specify how many GPUs your job requires AND how many CPU cores you need for the host code.

A job can use up to 12 CPU cores per A100, A100_40G or L40S GPU. See below for example jobscripts.

A GPU jobscript should be of the form:

#!/bin/bash --login

### Choose ONE of the following partitions depending on your permitted access

#SBATCH -p gpuA # A100 (80GB) GPUs
#SBATCH -p gpuA40GB # A100 (40GB) GPUs
#SBATCH -p gpuL # L40S GPUs

### Required flags

#SBATCH -G N # (or --gpus=N) Number of GPUs
#SBATCH -t 1-0 # Wallclock timelimit (1-0 is one day, 4-0 is max permitted)

### Optional flags

#SBATCH -n numcores # (or --ntasks=) Number of CPU (host) cores (default is 1)

module purge
module load libs/cuda/x.y.z # See below for available versions
See below for a simple GPU job that you can run.

Runtime Limits
The maximum runtimes on the GPUs are as follows:

batch jobs: 4 days
interactive jobs: 1 day
CUDA Libraries and modulefiles
You will most likely need the CUDA software environment for your job, whether your application is pre-compiled (e.g., a python app) or an application you have written yourself and compiled using the Nvidia nvcc compiler. Please see our CUDA libraries documentation for advice on compiling your own code.

You can access the base CUDA toolkit, and load additional modulefiles for additional Nvidia libraries.

# The main CUDA library and compiler (other libs have separate modulefiles - see below)

module load libs/cuda/x.y.x # # If you omit the x.y.x version (libs/cuda) you will get version 11.6.2, # which is old now. We recommend specifying a version. # If you need additional libraries (e.g., cuDNN, NCCL and so on, see below)
Alternatively, the Nvidia HPC SDK which provides a complete set of CUDA libraries and tools:

module load libs/nvidia-hpc-sdk/x.y.z # # If you omit the version (libs/nvidia-hpc-sdk) you will get # the latest version installed. To see what # that is, use: module avail -L libs/nvidia-hpc-sdk
If your application requires a specific version, or you want to fix on a specific version for reproducibility reasons, use:

module load libs/cuda/12.8.1 # The latest available version on the CSF
module load libs/cuda/12.4.1 # A100 only. Please also load at least compilers/gcc/6.4.0
Older versions from CSF3 (SGE) are also available, but we recommend using the newer versions.

# To see available versions:

module avail libs/cuda
module avail libs/nvidia-hpc-sdk

# To just the latest available version

module avail -L libs/cuda
module avail -L libs/nvidia-hpc-sdk
The Nvidia cuDNN, NCCL and TensorRT libraries are also available. See:

module avail libs/cuDNN
module avail libs/nccl
module avail libs/tensorrt
For more information on available libraries and how to compile CUDA code please see our CUDA page.

Which GPUs will your job use (CUDA_VISIBLE_DEVICES)
When a job or interactive session runs, the batch system will set the environment variable $CUDA_VISIBLE_DEVICES to a comma-separated list of GPU IDs assigned to your job, where IDs always begin at 0 (for a single-GPU job), or will be 0,1 or 0,1,2 and so on, depending on how many GPUs you request. This differs from the SGE batch system, where the IDs did not always begin at zero.

The CUDA library will read this variable automatically and so most CUDA applications already installed on the CSF will simply use the correct GPUs.

The SLURM_GPUS variable gives the number of GPUs you requested for your job.

A Simple First Job – deviceQuery
Create a jobscript as follows:

#!/bin/bash --login
#SBATCH -p gpuL # The L40S GPUs. See above for all available GPU partition names.
#SBATCH -G 1 # 1 GPU
#SBATCH -t 5 # Job will run for at most 5 minutes
#SBATCH -n 8 # (or --ntasks=) Optional number of cores. The amount of host RAM # available to your job is affected by this setting.

echo "Job is using $SLURM_GPUS GPU(s) with ID(s) $CUDA_VISIBLE_DEVICES and $SLURM_NTASKS CPU core(s)"

# Get the CUDA software libraries and applications

module purge
module load libs/cuda/12.8.1

# Run the Nvidia app that reports GPU statistics

deviceQuery
Submit the job using sbatch jobscript. It will print out hardware statistics about the GPU device.

See below for more complex jobscripts.

NVMe fast local storage
The GPU host nodes contain a 1.6TB NVMe storage card. This is faster than SSD storage (and faster than your scratch area and the home storage area).

This extra storage on the GPU nodes is accessible via the environment $TMPDIR:

cd $TMPDIR
This will access a private directory, which is specific to your job, in the /tmp area on the compute node where you job is running (please do not use /tmp directly).

The actual name of the directory contains your job id number for the current job, so it will be unique to each job. It will be something like /tmp/slurm.4619712, but you can always use the $TMPDIR environment variable to access this rather than the actual directory name.

This directory (and all files in it) will be deleted automatically at the end of your job by the batch system.

It is highly recommended (especially for machine learning workloads) that you copy your data to $TMPDIR at the start of the job, process it from there and copy any results back to your ~/scratch area at the end of the job. If your job performs a lot of I/O (e.g., reading large datasets, writing results) then doing so from $TMPDIR on the GPU nodes will be faster. Even with the cost of copying data to and from the NVMe cards ($TMPDIR), using this area during the job usually provides good speed-up.

Remember that $TMPDIR is local to the node. So after your job has finished, you will not be able to access any files saved on the GPU node’s NVMe drive from the login node (i.e., $TMPDIR on the login node points to the login node’s local hard-disk, whereas $TMPDIR on the GPU node points to the GPU node’s local NVMe drive.) So you must ensure you do any file transfers back to the usual ~/scratch area (or your home area) within the jobscript.

Here is an example of copying data to the $TMPDIR area at the start of the job, processing the data and then cleaning up at the end of the job:

#!/bin/bash --login
#SBATCH -p gpuX # Select the type of GPU (where X = A, L or A40GB)
#SBATCH -G 1 # 1 GPU
#SBATCH -n 8 # Select the no. of CPU (host) cores
#SBATCH -t 2-0 # Job "wallclock" is required. Max permitted is 4 days (4-0).

module purge
module load libs/cuda/12.8.1
module load your/cuda/app

# Copy a directory of files from scratch to the GPU node's local NVMe storage

cp -r ~/scratch/dataset1/ $TMPDIR

# Process the data with a GPU app, from within the local NVMe storage area

cd $TMPDIR/dataset1/
some_GPU_app -i input.dat -o results.dat

# Copy the result file back to the main scratch area

cp results.dat ~/scratch/dataset1/

# Or to copy an entire directory back:

cp -r resultsdir ~/scratch/dataset1/

# The batch system will automatically delete the contents of $TMPDIR at the end of your job.

The above jobscript can be in your home or scratch storage. Submit it from there.

Etiquette
All users are reminded to log out of their interactive GPU session when it is no longer required. This will free up the GPU for other users. If an interactive GPU session is found to be idle for significant periods, making no use of the GPU, it may be killed. Interactive sessions should not be used to reserve a GPU for future use – only request a GPU when you need to use it.

Batch jobs that only use CPU cores should not be submitted to GPU nodes. If such jobs are found they will be killed and your access to GPU nodes may be removed. There are plenty of CPU-only nodes on which jobs will run.

Monitoring GPU jobs
You can now ssh to the compute-node where the GPU job is running – your ssh session will be adopted into the job. You can only ssh to a compute-node where you have a running job!

# On the login node, find out where your job is running:

squeue
JOBID PRIORITY PARTITION NAME USER ST ... NODELIST
123456 0.000054 gpuA myjob mabcxyz1 R ... node860

# Now ssh to the node:

ssh node860

# Now run nvitop or nvidia-smi, or other GPU monitoring / debugging tools

module load tools/bintools/nvitop
nvitop

nvidia-smi

# To return to the login node

exit
Note that nvitop will download the necessary python packages the first time you use it. These will be stored in your ~/.cache/uv/ directory, but they do not take up a lot of storage.

Alternatively, you can use srun to access the node where your job is running, by specifying the JOBID of the job:

# Login to the node where your job is running (will only give you access to your job's GPU)

srun --jobid=12345 --pty bash

# Use nvitop:

module load tools/bintools/nvitop
nvitop

# Use the standard Nvidia app:

nvidia-smi

# To return to the login node

exit
Batch Jobs – Example Jobscripts
The following section provides sample jobscripts for various combinations of number of GPUs requested and CPU cores requested.

Note that in the examples below, we load modulefiles inside the jobscript, rather than on the login node. This is so we have a complete record in the jobscript of how we ran the job.

Single GPU, Single CPU-core
The simplest case – a single-GPU, single-CPU-core jobscript:

#!/bin/bash --login
#SBATCH -p gpuL # L40S GPUs
#SBATCH -G 1 # 1 GPU
#SBATCH -t 1-0 # Wallclock limit (1-0 is 1 day, 4-0 is the max permitted) # The number of CPU cores is not specified, so you job will use only 1.

# Latest version of CUDA (add any other modulefiles you require)

module purge
module load libs/cuda/12.8.1

echo "Job is using $SLURM_GPUS GPU(s) with ID(s) $CUDA_VISIBLE_DEVICES and $SLURM_NTASKS CPU core(s)"

# Run an application (this Nvidia app will report info about the GPU). Replace with your app.

deviceQuery
Single GPU, Multi CPU-cores
Even when using a single GPU, you may need more than one CPU core if your host-code uses OpenMP, for example, to do some parallel processing on the CPU. You can request up to 12 CPU cores per A100 & L40S GPU. For example:

#!/bin/bash --login
#SBATCH -p gpuL # L40S GPUs
#SBATCH -G 1 # 1 GPU
#SBATCH -t 1-0 # Wallclock limit (1-0 is 1 day, 4-0 is the max permitted)
#SBATCH -n 1 # One Slurm task
#SBATCH -c 8 # 8 CPU cores available to the host code. # Can use up to 12 CPUs with an A100 GPU. # Can use up to 12 CPUs with an L40S GPU.

# Latest version of CUDA

module purge
module load libs/cuda/x.y.z

echo "Job is using $SLURM_GPUS GPU(s) with ID(s) $CUDA_VISIBLE_DEVICES and $SLURM_CPUS_PER_TASK CPU core(s)"

# This example uses OpenMP for multi-core host code - tell OpenMP how many CPU cores to use.

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

./mySimpleGPU_OpenMP_app
Multi GPU, Single CPU-core
A multi-GPU job should request the required number of GPUs and optionally up to 12 CPU cores per A100 & L40S GPU.

For example a 2-GPU job that runs serial host code on one CPU core would be:

#!/bin/bash --login
#SBATCH -p gpuL # L40S GPUs
#SBATCH -G 2 # 2 GPUs
#SBATCH -n 2 # Two Slurm tasks
#SBATCH -c 8 # 8 CPU cores available to each task. # Can use up to 12 CPUs with an A100 GPU. # Can use up to 12 CPUs with an L40S GPU.

# Latest version of CUDA

module purge
module load libs/cuda/x.y.z

echo "Job is using $SLURM_GPUS GPU(s) with ID(s) $CUDA_VISIBLE_DEVICES and $SLURM_NTASKS x $SLURM_CPUS_PER_TASK CPU core(s)"

./myMultiGPUapp.exe
Multi GPU, Multi CPU-cores
Finally a multi-GPU job that also uses multiple CPU cores for the host code (up to 12 CPUs per A100 & L40S GPU) would be:

#!/bin/bash --login
#SBATCH -p gpuL # L40S GPUs
#SBATCH -G 2 # 2 GPUs
#SBATCH -n 1 # One Slurm tasks
#SBATCH -c 16 # 16 CPU cores available to the host code # Can use up to 12 CPUs per GPU with an A100 GPU. # Can use up to 12 CPUs per GPU with an L40S GPU.

# Latest version of CUDA

module purge
module load libs/cuda/x.y.z

echo "Job is using $SLURM_GPUS GPU(s) with ID(s) $CUDA_VISIBLE_DEVICES and $SLURM_NTASKS x $SLURM_CPUS_PER_TASK CPU core(s)"

# This example uses OpenMP for multi-core host code - tell OpenMP how many CPU cores to use.

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# Will use $SLURM_CPUS_PER_TASK CPU cores via OpenMP

./myMultiGPU_OpenMP_app
Multi GPU, Multi CPU-cores for MPI Apps
Multi-GPU applications are often implemented using the MPI library – each MPI process (aka rank) uses a GPU to speed up its computation.

The GPUs (in Slurm) are run in Default compute mode, meaning multiple processes can use a GPU at any one time. However, other users’ jobs will NOT be able to access your job’s GPUs. But this allows you to run multiple processes on your assigned GPUs.

You can also run processes on multiple GPUs, if you job has requested more than one GPU.

The following CUDA-aware version of the OpenMPI libraries are available. This will usually give better performance when your application uses MPI to transfer data from one GPU to another (note that the openmpi modulefile will automatically load the cuda modulefile):

# GCC Compiler

module load mpi/gcc/openmpi/5.0.7-cuda-gcc-14.2.0 # CUDA 12.8.1

# Intel Compiler

mpi/intel-oneapi-2024.2.0/openmpi/5.0.7-cuda # CUDA 12.8.1
Note that when running multi-GPU jobs using MPI you usually start one MPI process per GPU. For example:

#!/bin/bash --login
#SBATCH -p gpuL # L40S GPUs
#SBATCH -G 4 # A 4-GPU request (Note: not all users have rights to run 4 GPUs.)
#SBATCH -n 4 # 4 CPU (host) cores. We'll run 4 MPI processes.
#SBATCH -t 1-0 # A 1-day wallclock limit. Max permitted is 4-0 (4 days.)

# MPI library (which also loads the cuda modulefile)

module purge
module load mpi/gcc/openmpi/5.0.7-cuda-gcc-14.2.0

echo "Job is using $SLURM_GPUS GPU(s) with ID(s) $CUDA_VISIBLE_DEVICES and $SLURM_NTASKS CPU core(s)"

# In this example we start one MPI process per GPU. We could use $SLURM_NTASKS or $SLURM_GPUS (both = 4)

# It is assumed the application will ensure each MPI process uses a different GPU. For example

# MPI rank 0 will use GPU 0, MPI rank 1 will use GPU 1 and so on.

mpirun -n $SLURM_GPUS ./myMultiGPU_MPI_app

# If your application does not map MPI ranks to GPUs correctly, you can try the following method

# where we explictly inform each rank which GPU to use via the CUDA_VISIBLE_DEVICES variable:

mpirun -n $SLURM_GPUS -x CUDA_VISIBLE_DEVICES=0 ./myMultiGPU_MPI_app : \
 -x CUDA_VISIBLE_DEVICES=1 ./myMultiGPU_MPI_app : \
 -x CUDA_VISIBLE_DEVICES=2 ./myMultiGPU_MPI_app : \
 -x CUDA_VISIBLE_DEVICES=3 ./myMultiGPU_MPI_app
Note that it also is possible to use a multi-threaded application (implemented using OpenMP for example to create multiple threads).

An alternative method, which allows multiple MPI processes to run on the same GPU is now available – please see the section below on the Nvidia MPS facility.

Interactive Jobs
You mainly use interactive jobs to run an GPU app that has a GUI, or to log-in to a GPU node to do app development and testing.

Interactive jobs should be run using srun (not sbatch) from the login node as follows.

We strongly advise that you use batch jobs rather than interactive jobs. Provided you have batch jobs in the queue, ready and waiting to be run, the system can select your jobs 24 hours a day. But interactive jobs require you to be logged in to the CSF and working at the terminal. You will get more work done on the system using batch jobs – the batch queues never need to go to sleeep!
Single GPU, Single CPU-core logging in to GPU node
Here we request an interactive session using 1-GPU and 1-CPU core, logging in to the node

# Using long flag names

srun --partition=gpuL --gpus=1 --ntasks=1 --time=1-0 --pty bash

# Using short flag names

srun -p gpuL -G 1 -n 1 -t 1-0 --pty bash
The above command will place you in your current directory when it logs you in to the GPU node.

GPU srun jobs are limited to 24 hours.

Multi GPU, Multi CPU-cores logging in to GPU node
Here we start an interactive session requesting 2-GPUs and 4-CPU cores, logging in to the node:

# Using long flag names

srun --partition=gpuL --gpus=2 --ntasks=4 --time=1-0 --pty bash

# Using short flag names

srun -p gpuL -G 2 -n 4 -t 1-0 --pty bash
Nvidia Multi-Process Service (MPS)
The GPUs (in Slurm) all use Default compute mode – meaning you can simply start multiple processes on your allocated GPUs. This differs from the SGE batch system (which used Exclusive Process mode.)
Hence there is no reason to use the Nvidia MPS feature.

Use of MPS will be removed soon and you are encouraged to use mpirun or srun in your jobscripts if you need to start multiple processes on your allocated GPUs.

However, should you wish to use MPS to match your earlier SGE usage, you can do so in Slurm.

The Nvidia Multi-Process Service (MPS) allows multiple processes to use the same GPU. You might want to do this for small MPI jobs, where each MPI process does not require the resources of an entire GPU. Hence all of the MPI processes could “fit” on a single GPU. Alternatively, if you have a lot of small jobs to run, you might be able to start multiple copies of the executable, all using the same GPU. Using MPI (mpirun) would be one method of doing this, even if the app itself is not an MPI job.

An extra flag is required to start the NVMPS facility on the node allocated to your job. Hence you should add:

--extra=mps
to your jobscript (or srun command.)

Note that you should still request enough CPU cores on which to run multiple processes. Even a GPU app does some work on the CPU and so if you are going to run several copies of an app, you should request the correct number of CPU cores so that each instance of your app has its own core(s) to run on. The examples below request 8 CPU cores (-n 8) so that we can run 8 copies of a GPU-capable application.

The following example demonstrates running the simpleMPI example found in the CUDA SDK on a single GPU. Multiple MPI processes are started and they all run on the same GPU. Without MPS, a GPU per MPI process would be required (see later for what happens if we run the same job without using MPS.)

#!/bin/bash --login
#SBATCH -p gpuL # L40S GPUs
#SBATCH -G 1 # 1 GPU
#SBATCH -n 8 # We want a CPU core for each process (see below)
#SBATCH --extra=mps # Extra flag to enable Nvidia MPS

# Load a CUDA-aware MPI modulefile which will also load a cuda modulefile

module purge
module load mpi/gcc/openmpi/5.0.7-cuda-gcc-14.2.0

# Let's take a copy of the already-compiled simpleMPI example (the whole folder)

# Not available in SLURM - TO-DO!

cp -a $CUDA_SDK/0_Simple/simpleMPI/ .
cd simpleMPI

# Now run more than 1 copy of the app. In fact we run with 8 MPI processes

# (Slurm knows you've requested 8 CPU-cores)

# But we are only using 1 GPU, not 8! So all processes will use the same GPU.

mpirun ./simpleMPI
Submit the above jobscript using sbatch jobscript. The job output will be something similar to:

Running on 8 nodes
Average of square roots is: 0.667337
PASSED
You can also use the NV MPS facility with interactive jobs:

# At the CSF login node, start an interactive session, requesting one GPU, 8 CPU cores and enable the NVMPS facility

[username@login1 [csf3] ~]$ srun -p gpuL -G 1 -n 8 -t 10 --extra=mps --pty bash

# Wait until you are logged in to a GPU node, then:

module purge
module load mpi/gcc/openmpi/5.0.7-cuda-gcc-14.2.0
cp -a $CUDA_SDK/0_Simple/simpleMPI .
cd simpleMPI

# Run more MPI processes than the 1 GPU we requested. This will only work when

# (Slurm knows you've requested 8 CPU-cores)

mpirun ./simpleMPI

# Return to the login node

exit
Profiling Tools
A number of profiling tools are available to help analyse and optimize your CUDA applications. We provide instructions on how to run (start) these tools below. Please note that instructions on how to use these tools are beyond the scope of this webpage. You should consult the Nvidia profiling documentation for detailed instructions on how to use the tools listed below.

We give the command name of each tool below. If running the profiler tool through its graphical user interface (GUI) or interactively on the command-line (i.e., not in a batch job which would be collecting profiling data without any interaction) then you must start an interactive session on a backend GPU node using the commands:

# On the CSF login node, request an interactive session on a GPU node

srun -p gpuL -G 1 -n 1 -t 1-0 --pty bash # Can instead use gpuA for the A100 GPUs

# Wait to be logged in to the node, then run:

module load libs/cuda/12.8.1 # Choose your required version
name-of-profiler-tool # See below for the command names
Nsight Compute
The Nvidia Nsight Compute profile tools are installed as of toolkit version 10.0.130 and later.
To run the profiler for CUDA toolkit versions up to 11.7.0 use:

module load libs/cuda/11.7.0

# Command-line version

nv-nsight-cu-cli

# GUI version

srun-x11 --partition=xxxX --gpus=x --ntasks=x --time=x-x
nv-nsight-cu
From CUDA toolkit version 12.0.1 or later use:

module load libs/cuda/12.8.1

# Command-line version

ncu

# GUI version

srun-x11 --partition=xxxX --gpus=x --ntasks=x --time=x-x
ncu-ui
Nsight Systems
The Nvidia Nsight Systems performance analysis tool designed to visualize an application’s algorithms is installed as of toolkit version 10.1.168. To run the profiler:

nsight-sys
Nvidia recommend you use the above newer tools for profiling rather than the following older tools, although these tools are still available and may be familiar to you.

Visual Profiler
The Nvidia Visual Profiler is installed as of toolkit version 7.5.18 and later. To run the profiler:

nvvp
Note that the Nvidia Visual Profiler nvvp can be used to view results collected by the nvprof command-line tool (see below). Hence you could use the the nvprof command in a batch job which will save profiling data to file, then view the results at a later time using the nvvp tool.

nvprof Command-line Profiler
The Nvidia command-line nvprof profiler is installed as of toolkit version 7.5.18 and later. To run the profiler:

nvprof
Note that the Nvidia Visual Profiler nvvp (see above) can be used to view results collected by the nvprof command-line tool. Hence you could use the the nvprof command in a batch job which will save profiling data to file, then view the results at a later time using the nvvp tool.
