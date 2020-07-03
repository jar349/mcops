Minecraft Operations (MCOps)
---
A [pyslackops](https://github.com/jar349/pyslackops) chat operation for Minecraft servers.  It connects to your 
server's RCon.

If you are running pyslackops in your Slack instance, you can deploy this app somewhere and register `.mc`

Minecraft server commands must be whitelisted by [configuration](./config/mcops.yaml).

The hostname, port, and password can be passed by environment variables:

| name | default | description |
| --- | --- | --- |
| MCOPS_HOST | localhost | The hostname of your minecraft server (or really, wherever it is running RCON) |
| MCOPS_POST | 25575 | The port on which RCON is listening |
| MCOPS_PASSWORD |  | (_Required_) The password for your server's RCON |
 