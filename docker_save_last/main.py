# Copyright 2018, Bryan Thornbury
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import os
import sys
import time
import uuid
import time
import signal

from command import Command


def getOpenPort():
    """
    https://stackoverflow.com/questions/2838244/get-open-tcp-port-in-python
    """
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def runDindDockerContainer(tag, name, port):
    print("Running dind-save container...")

    Command("docker", [
        "run", "-d",
        "--privileged",
        "-v", "/var/lib/docker/image:/var/lib/docker/image",
        "-v", "/var/lib/docker/overlay2:/var/lib/docker/overlay2",
        "--name", name,
        "--security-opt", "label=disable",
        "-p", "127.0.0.1:" + str(port) + ":2375",
        tag
        ]).environment_dict(os.environ).execute().throwIfFailed()

    time.sleep(4)


def runDockerSave(port, args):
    print("Running docker save...")

    Command("docker", [
        "-H", "127.0.0.1:{0}".format(port),
        "save"] + args).environment_dict(os.environ).execute().throwIfFailed().printStdOut()
    

def cleanup(containerName):
    print("Cleaning up...")

    Command("docker", [
        "rm", "-f", containerName
    ]).environment_dict(os.environ).execute().throwIfFailed()


def main():
    parser = argparse.ArgumentParser(
        description="A command line utility effectively replicating `docker save` except that it " +
            "will only save the LAST layer of the image in the output archive. \n\n" +
            "Arguments and options are identical to `docker save` see `docker save --help` for more help.\n")
    
    # Parse just to allow for "-h"
    parser.parse_known_args()

    containerName = "docker_save_last_" + str(uuid.uuid4())

    def signal_handler(sig, frame):
        cleanup(containerName)
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        port = getOpenPort()
        runDindDockerContainer("brthornbury/dind-save:18.09", containerName, port)
        runDockerSave(port, sys.argv[1:])
    except Exception:
        cleanup(containerName)
        sys.exit(1)


if __name__ == "__main__":
    main()