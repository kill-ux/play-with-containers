# Installing the Guest Additions on a GUI-less server

* Once the host has booted, click Devices | Insert Guest Additions CD Image.
* Log in to your guest server.
* Mount the CD-ROM with the command sudo mount `/dev/cdrom /media/cdrom`.
* Change into the mounted directory with the command `cd /media/cdrom`.
* Install the necessary dependencies with the command `sudo apt-get install -y dkms build-essential linux-headers-generic linux-headers-$(uname -r)`.
* Change to the root user with the command `sudo su`.
Install the Guest Additions package with the command `./VBoxLinuxAdditions.run`.

