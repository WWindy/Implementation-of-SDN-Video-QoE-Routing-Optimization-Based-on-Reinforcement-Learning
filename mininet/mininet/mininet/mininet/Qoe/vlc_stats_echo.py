#!/bin/bash

# Set the host and port that VLC is listening on for remote control commands
HOST=localhost
PORT=4444

# Connect to VLC's remote control interface and enable verbose output
echo -e "new rc\nverbose on\n" | nc $HOST $PORT > /dev/null

# Start playing the video and wait for it to start
echo -e "add /home/windy/Redios/chat.m4v\n" | nc $HOST $PORT > /dev/null
sleep 5

# Get the current statistics and write them to a file
echo -e "stats\n" | nc $HOST $PORT > /home/windy/mininet/custom/vlc_stats.txt

# Stop playing the video and disconnect from VLC's remote control interface
echo -e "stop\nquit\n" | nc $HOST $PORT > /dev/null
