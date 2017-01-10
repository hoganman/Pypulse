# Pypulse

The package is designed to improve user experience with the linux Pulse VPN clinet pulsesvc. It provides the user the ability to store username and realm information in one location and provide frequent updates about connection status.

How to download/get:
 git clone https://github.com/hoganman/Pypulse.git

Tested:
  Ubuntu 14 LTS
  python 2.7
  Pulse client 8.1 for Linux

Usage:
  python -c 'import Pulse; Pulse.PersistConnect()'

Known Issues:
 If pulsesvc is closed without exiting properly, VPN connection will persist although a proper tunnel is not established. This is an issue with pulsesvc. The solution is to use the client again to force a reconnection. Then end the client Pypulse normally.
