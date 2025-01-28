---
sidebar_position: 1
---

# DaRaft Specifications

DaRaft is a protocol used by Dafunk for the load balance of events to different services. 
It is directly inspired by Raft and some features have been added to obtain a charge balance

## Description

DaFunk is composed of a series of services that use events.
Services are to be considered as "Nodes" in a network that uses RAFT.

A service, after the boot phase sends a discovery message to the broker, then passes into a state called StandBy.
In this state the Service waits for discovery messages from any other services, the nome accept only discovery messages
from services from the same family.

After a time ( Default: 5s ) the Node move from the state of StandBy to the state Follower.

in this state we have three options:

1) **The Service received a Discovery message from an existing Leader**:
in this situation the node is a follower and continue with the process of Consensus

2) **The Service has no Leader information**:
From that moment, the network must take the decision to elect a Leader. The process is described below

3) **The Service, did not receive any Discovery message**:
This is the easiest use case, The service move from the status Follower to the status Leader.

If the Service has no peers, as a Leader he receives and process all the events

If the network already has a Leader, the Service, in the follower state, receive a message from the Leader
with the following information:

1) 





## Create your first Markdown Page

Create a file at `src/pages/my-markdown-page.md`:

```mdx title="src/pages/my-markdown-page.md"
# My Markdown page

This is a Markdown page
```

A new page is now available at [http://localhost:3000/my-markdown-page](http://localhost:3000/my-markdown-page).
