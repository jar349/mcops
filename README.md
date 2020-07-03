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

### Running
In the project root, you can build the docker image like so:
```bash
docker build -t jar349/mcops:latest .
```
And then you can run the docker container like so:
```bash
docker run -d --name mcops -p "8081:80" -e "MCOPS_HOST=your.minecraft.server" -e "MCOPS_PASSWORD=password" jar349/mcops:latest
```
Once running, you can run a command on your server via a REST API:
```bash
curl -X POST "http://localhost:8081/handle" \
  -H  "accept: application/json" \
  -H  "Content-Type: application/json" \
  -d "{\"namespace\":\"mc\",\"command\":\"list\",\"event\":{}}"
```
In response, you should see something similar to this:
```json
{
  "message": "There are 4 of a max of 20 players online: player_one, player_two, player_three, player_four"
}
```
