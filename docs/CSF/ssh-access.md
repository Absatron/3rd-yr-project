# CSF3 SSH from Mac (and Cursor agent)

**Host:** `csf3.itservices.manchester.ac.uk` · **Username:** `z29707aj` (see `runs/registry.yaml`).

Official login: [CSF3 connecting](https://ri.itservices.manchester.ac.uk/csf3/getting-started/connecting/) — **UoM IT password + Duo**. Off-campus: GlobalProtect VPN first.

## Public keys on login nodes

CSF3 login SSH advertises **`keyboard-interactive` only** (password + Duo via PAM). A key in `~/.ssh/authorized_keys` on CSF does **not** remove the password/Duo prompt on `csf3.itservices.manchester.ac.uk`. Keep keys for other hosts if useful; for CSF, use multiplexing below.

## Mac: GUI forwarding (`-Y`)

For X11 apps (e.g. gedit): install [XQuartz](https://www.xquartz.org/), reboot once, then:

```bash
ssh -Y csf3
```

`-Y` is unrelated to authentication. Prefer editing jobscripts in the repo on your Mac or with `nano`/`vim` on CSF.

**Common mistake:** `ssh -Y ~/.ssh/id_ed25519_csf3 ...` treats the key path as a hostname. Use `ssh -Y csf3` or `ssh -Y -i ~/.ssh/id_ed25519_csf3 z29707aj@csf3...`.

## Recommended `~/.ssh/config` (Mac)

```sshconfig
Host csf3
  HostName csf3.itservices.manchester.ac.uk
  User z29707aj
  IdentityFile ~/.ssh/id_ed25519_csf3
  IdentitiesOnly yes
  ForwardX11 yes
  ForwardX11Trusted yes
  ControlMaster auto
  ControlPath ~/.ssh/sockets/%r@%h-%p
  ControlPersist 8h
```

Create the socket directory once:

```bash
mkdir -p ~/.ssh/sockets
```

Unlock the key (passphrase-protected keys):

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519_csf3
```

## Agent / automation workflow

1. You open one session: `ssh -Y csf3` → enter password + approve Duo.
2. While **ControlMaster** is active (`ssh -O check csf3` → `Master running`), Cursor can run `ssh csf3 '…'` without a second Duo.
3. When the master expires (default **8h**) or you close it, log in again.

Do **not** store CSF or GitHub passwords in the project `.env` or git.

## Verify from Mac

```bash
ssh -O check csf3
ssh csf3 'hostname && ls ~/comp30030-mirage-ablation/README.md'
```

## CSF directory layout (this project)

| Path | Absolute example (z29707aj) | Role |
|------|-----------------------------|------|
| `~/comp30030-mirage-ablation/` | `/mnt/iusers01/fse-ugpgt01/compsci01/z29707aj/comp30030-mirage-ablation` | Git clone (home, backed up) |
| `~/scratch/comp30030-mirage-ablation/` | `/net/scratch/z29707aj/comp30030-mirage-ablation` | NSD sync, processed data, artifacts, Slurm logs |

Clone (on CSF, once):

```bash
git clone https://github.com/Absatron/3rd-yr-project.git ~/comp30030-mirage-ablation
mkdir -p ~/scratch/comp30030-mirage-ablation/{data/raw,data/processed,data/frozen_weights,artifacts,runs/slurm-logs}
```
