# Wireless Sync
## About
This small Python project uses the system clock to "sync" two computers that are in no communication with each other.

It uses this system time to calculate a song and the current duration from a given directory. If that sounds confusing, then a simpler explanation is that this file acts like a radio station.

One computer can "tune in", and get the same song as another computer. Just like a radio station broadcasts the same song (at the same point) to every reciever. However, it does all of this with no central server or communication between the peers.

## Dependencies
This file currently depends on mutagen to work correctly. All other libraries come with the standard library. 

In the future, I would like to consider making my own alternative, making this a "dependency-free" project. However, this is a huge undertaking for what is a small weekend project.