Current System Configuration
Summary
Please note, the CSF3 is in active development with new hardware being added several times a year.

The compute hardware below is available to your jobs via the CSF3 Slurm Partitions.

Total CSF CPU cores: 17,016

Standard AMD nodes total #cores: 14,448
Standard Intel nodes total #cores: 1,736
High memory Intel nodes total #cores: 832More info…
HPC Pool Intel nodes total #cores: 0. New config coming soon. More info…
Total CSF Nvidia GPUs: 204

76 x Nvidia A100 (80GB) GPUs (Ampere, 80GB VRAM). More info…
8 x Nvidia A100 (40GB) GPUs (Ampere, 40GB VRAM). More info…
88 x Nvidia L40S (48GB) GPUs (Ada Lovelace, 48GB VRAM). More info…
32 x Nvidia H200 (141 GB) GPUs (Hopper, 141 GB VRAM). More info…
Total lustre storage (scratch): 1.9PB

Login nodes: 3 physical nodes, 96 cores each (2xAMD EPYC 9454 “Genoa” 48-Core), 768GB of memory, Nvidia Ampere A2 16GB GPU

Operating System: Redhat-based system

CPU nodes
Standard nodes
360 Haswell cores [node6nn]: 15 nodes of 2×12-core Intel Xeon E5-2690 v3 @ 2.60GHz + 128GB RAM

1376 Skylake cores [node9nn]: 43 nodes of 2×16-core Intel Xeon Gold 6130 CPU @ 2.10GHz + 192GB RAM + 100Gb/s (4X EDR) mlx5 Mellanox InfiniBand

14,448 AMD Genoa cores [node1201-node1286]: 86 nodes of 2×84-core AMD EPYC Genoa 9634 CPU @ 2.25GHz + 1.5TB RAM + 100GbE network.

High memory nodes
96 Skylake cores [node785-node787]: 3 nodes of 2×16-core Intel Xeon Gold 6130 CPU @ 2.10GHz + 1.5TB RAM

128 Cascade Lake cores [node788-node791]: 4 nodes of 2×16-core Intel Xeon Gold 5218 CPU @ 2.30GHz + 1.5TB RAM

480 Icelake cores [node120-node134]: 15 nodes of 2×16-core Intel Xeon Gold 6326 CPU @ 2.90GHz + 2TB RAM

96 Sapphire Rapids cores [node135-node137]: 3 nodes of 2×16-core Intel Xeon Gold 6426Y CPU @ 2.50Ghz + 2TB RAM

32 Icelake cores [node160]: 1 node of 2×16-core Intel Xeon Gold 6326 CPU @ 2.90GHz CPU + 4TB RAM

GPU nodes
A100 80GB nodes
19 nodes [node847-node865] : 4x Nvidia HGX A100-SXM4-80GB (Ampere) GPUs, 80GB GPU global mem, 6912 CUDA Cores + NVLink. 2×24-core AMD 7413 “Milan” CPU @ 2.65GHz + 512GB RAM + 100Gb/sec (6X HDR) mlx5 Mellanox InfiniBand + 1.6TB Intel Non Volatile memory (NVMe) SSD Controller as /tmp. [Most users may access].

A100 40GB nodes
2 nodes [node866 & node867]: 4x Nvidia HGX A100-SXM4-40GB (Ampere) GPUs 40GB GPU global mem, 6912 CUDA Cores + NVLink + InfiniBand. 2×24-core AMD 7413 “Milan” CPU @ 2.65GHz + 512GB RAM + 100Gb/sec (6X HDR) mlx5 Mellanox InfiniBand + 1.5TB Intel Non Volatile memory (NVMe) SSD Controller as /tmp. [Restricted Access, and most users of these cannot use others].

L40S nodes
22 nodes [node868-node889] : 4x Nvidia L40S (Ada Lovelace) GPUs 48GB GPU global mem, 18176 CUDA Cores. 2×24-core Intel Xeon(R) Gold 6442Y CPU @ 2.6GHz + 512GB RAM + 28TB SSD as /tmp. [Most users may access].

H200 nodes
4 nodes [node820-node823]: 8x Nvidia H200-SXM-141GB (Hopper) GPUs 141GB GPU global mem, 16896 CUDA Cores. 2×32-core Inten Xeon(R) Platinum 8562Y+ CPU @ 2.8 Ghz + 1.5 TB RAM + 7.5 TB Non Volatile memory (NVMe) as /tmp. [Limited Restricted Access].

The HPC Pool
This is a distinct pool of resources with a different access procedure to the CSF. Please consult The HPC Pool documentation for further information.

A new HPC Pool config is coming soon. 3968 Skylake cores [node1000-node1127]: 124 nodes of 2×16-core Intel Xeon Gold 6130 CPU @ 2.10GHz + 512GB RAM + 100Gb/s (4X EDR) mlx5 Mellanox InfiniBand (4 nodes are no longer in service due to hardware failures. Pool was originally 4,096 cores.)
