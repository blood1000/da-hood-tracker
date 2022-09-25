import requests
import time
import threading
targets = [
  "1164354690", # kimbladi
  "1645496291", # streaky
  "150055944", # jakynol
  "969192549", # alpha savage
  "752396154", # curliyo
  "1593707423", # 6ghxst
  "2462227637", # angel
  "2395613299", # bullet
  "1829554086", # icy
  "3750119432" #blood
]

games = [
  "2788229376", # da hood
  "5602055394", # hood modded
  "9183932460", # untitled hood
  "9824221333", # da hood aim trainer
  "9825515356" # hood customs
]


def post(place, servers, target):
  data=requests.get(f"https://users.roblox.com/v1/users/{target}").json()
  username=data["name"]
  display=data["displayName"]
  gamename = requests.get("https://games.roblox.com/v1/games?universeIds=" + str(requests.get(f"https://api.roblox.com/universes/get-universe-containing-place?placeid={place}").json()["UniverseId"])).json()["data"][0]["name"]
  headshot=requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={target}&size=150x150&format=Png&isCircular=true").json()["data"][0]["imageUrl"]
  description = f"**Place ID: `{place}`\nGame: `{gamename}`\n Servers: `{servers}`**"
  payload = {
    "content": None,
    "embeds": [
      {
        "title": display,
        "description": description,
        "color": None,
        "author": {
          "name": username
        },
        "footer": {
          "text": f"Da Hood Tracker"
        },
        "thumbnail": {
          "url": headshot
        }
      }
    ],
    "attachments": []
  }
  r=requests.post("webhookhere", json=payload)


def rosearch(place, target):
  cursor = ""
  data = []
  servers = []
  while True:
    r=requests.get(f"https://games.roblox.com/v1/games/{place}/servers/Public?limit=100&cursor={cursor}").json()
    for server in r["data"]:
      payload = []
      headshots = []
      for token in server["playerTokens"]:
        payload.append(
          {
            "token": token,
            "type": "AvatarHeadshot",
            "size": "150x150",
            "requestId": server["id"]
          }
        )
      while True:
        r=requests.post(
          "https://thumbnails.roblox.com/v1/batch",
          json=payload
        ).json()
        print(r)
        if str(r) == "{'errors': [{'code': 0, 'message': 'TooManyRequests'}]}":
          time.sleep(1)
        else:
          break
      for result in r["data"]:
        data.append(
          {"headshot": result["imageUrl"], "server": result["requestId"]}
        )
    try:
      cursor = r["nextPageCursor"]
    except:
      break
  headshot = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={target}&size=150x150&format=Png").json()["data"][0]["imageUrl"]
  for user in data:
    if user["headshot"] == headshot:
      servers.append(user["server"])
  if len(servers) == 0:
    return False
  return servers


def track(target):
  currentlyonline = False
  while True:
    r=requests.get(
      f"https://api.roblox.com/users/{target}/onlinestatus/"
    ).json()
    if r["IsOnline"] == True and r["PresenceType"] == 2:
      if currentlyonline == False:
        print(target)
        if r["PlaceId"] != None:
          if r["GameId"] != None:
            post(r["placeId"], r["GameId"], target)
          else:
            servers=rosearch(r["PlaceId"], target)
            if servers != False:
              post(game, servers, target)
        else:
          for game in games:
            servers=rosearch(game, target)
            if servers != False:
              post(game, servers, target)
              break
      currentlyonline = True
    else:
      currentlyonline = False
      time.sleep(3)
for target in targets:
  threading.Thread(target=track, args=(target, )).start()
while True:
  time.sleep(1)
