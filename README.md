# CLI Pin

This is a very simple script to store and invoke CLI commands using
tags, to reduce the repetitiveness and verbosity of working with
some command line tools.

>[!NOTE]
>This is not a robust script, and may have issues,
>use with caution.

## Operating System Suppport

This script should work on the *big three*
(i.e., Linux, MacOS, Windows).

## Build Requirements

python >= v3.10.x

## Usage

```sh
usage: clipin.py [-h] [-t TAG] [-i INVOKE] command

Application to tag CLI commands for easy recall

positional arguments:
  command               The command to invoke: Add, Run, List, Delete, or Clear

options:
  -h, --help            show this help message and exit
  -t TAG, --tag TAG     The tag of the pin to interact with
  -i INVOKE, --invoke INVOKE
                        The CLI command to invoke
```

It is recommended to add call-function to terminal config (i.e., `.bashrc`, `powershell profile`)

Example for `.bashrc`:
```sh
clipin() { python3 <PROJECT PATH>/clipin.py "$@" ;}
```

