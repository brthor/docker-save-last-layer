docker-save-last Command Line Utility
======================================

This is a command line utility effectively replicating `docker save` except that it will only save the LAST layer of the image in the output archive.

This is especially useful when combined with the experimental `docker build --squash` option, because it allows you to export only your changes on top of the base image without the entire base image file system in the output archive.

This means HUGE savings in file size.

General discussion on the issue can be found here:
https://github.com/moby/moby/issues/8039


## Installation

Use pip to install:
`pip install d-save-last`

## Required Dependencies

1. `docker` installed, on the PATH, and usable without sudo.

## Usage
Typical usage will look like `d-save-last -o ./path/to/output.tar YOUR_IMAGE_ID`

Arguments and options are identical to `docker save` see `docker save --help`.

```
$ docker save -h

Usage:	docker save [OPTIONS] IMAGE [IMAGE...]

Save one or more images to a tar archive (streamed to STDOUT by default)

Options:
  -o, --output string   Write to a file, instead of STDOUT
```

## How does it work?

This utility uses the special docker-in-docker image from https://github.com/brthor/dind-save 

That docker image contains a version of the docker daemon with patches to docker save built from https://github.com/brthor/engine

The utility launches the `dind-save` image in a container, and connects to its docker daemon over TCP.

## Caveats

- This is currently only tested with host machines that use the overlay2 storage driver. Any other storage driver will almost certainly not work. 

- Currently only supports docker version 18.09. Adding new versions requires changes in the docker daemon and `dind-save` image repository. Open an issue if you'd like a new version added for your purposes.

Feel free to contribute here if any of these are an issue and you'd like to use this utility. Pull Requests will be reviewed quickly.