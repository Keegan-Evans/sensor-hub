# Setting up Sensor Hub
## Required Items
- Ansible installed on the host computer
- An SSH key
- A local clone of the [4CSCC/sensor-hub
  repository](https://github.com/4cscc/sensor-hub).
- A microSD card
- Raspberry Pi Imager
- Raspberry Pi 3, 4, or 5
- A wired, Ethernet connection

## Steps
### Preparation

- Begin by installing Ansible and the Raspberry Pi Imaging software onto the
  machine you will be using to setup the Pi.

- Create an SSH key if you do not already have one. [GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) has a good guide to
  doing this if you have not set one up before.

- Clone the `sensor-hub` repository to your local machine or download the 

### Prepare Image
- Place SD card in reader and open up Raspberry Pi Imager.
- Select `RASPBERRY PI OS(64-BIT)` under `Operating System` and select your
  microSD from under `Storage`.

- Before writing the card, we have some configuration to do first, so click
  the gear at the bottom-right corner of Imager.

- Set hostname to something that will be easy to recognize on your network
- Click the box to select `Enable SSH`, and select the radio button for
  `Alllow public-key authentication only`, then from your machine copy and
  paste the public key for the key-pair that you generated earlier and paste
  it on the line next to where it says `set authorized_keys for:`

- Then set the username and password for the pi you would like to set up, for
  the demo one we will be using 'beta' and 'FourCorners'. If you use something
  else here, just be sure to update the `pis.ini` file before running the
  playbook.

  !["demo image of PiImager config"](./docs/images/imager_options_config.jpg)

- Everything else here should be ok with the defaults, scroll to the bottom
  and click `SAVE`, when the `Advanced Options` dialog closes, you may then
  click the the `WRITE` button.

- When finished writing/verifying, insert microSD card into the Pi, and plug
  the Pi into an ethernet cable and power.

