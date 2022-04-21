#!/usr/bin/env python3
from yt_dlp import YoutubeDL
import json
import sys

def ytpl(url):
  "How long is a Youtube Playlist?"
  opts = {"dump_single_json": True, "simulate": True, "quiet": True}
  with YoutubeDL(opts) as ydl:
    info = ydl.extract_info(url, download = False)
    sani = ydl.sanitize_info(info)
  with open("info.py", "w+", encoding = "utf8", newline = "\n") as f:
    print(info, file = f)
  with open("sani.py", "w+", encoding = "utf8", newline = "\n") as f:
    print(sani, file = f)
  # d = json.loads(info) # last stdout from ytdl
  
  print(info["title"])
  # print(d["title"])
  
  # tree walk to each, if ever they break the current format
  def dur(d):
    if isinstance(d, dict):
      if "duration" in d: yield int(d["duration"])
      for k, v in d.items():
        if isinstance(v, dict) and k != "fragments":
          yield from dur(v)
    elif isinstance(d, list):
      for v in d:
        if isinstance(v, dict):
          yield from dur(v)
  
  # seconds = sum(dur(d))
  
  # direct walk to durations in current format
  seconds = sum(v["duration"] for v in d["entries"])
  
  print(f"{seconds}s")
  minutes, seconds = seconds // 60, seconds % 60
  print(f"{minutes}m{seconds}s")
  if minutes >= 60:
    hours, minutes = minutes // 60, minutes % 60
    print(f"{hours}h{minutes}m{seconds}s")
    if hours >= 24:
      days, hours = hours // 24, hours % 24
      print(f"{days}d{hours}h{minutes}m{seconds}s")
      if days >= 7:
        weeks, days = days // 7, days % 7
        print(f"{weeks}w{days}d{hours}h{minutes}m{seconds}s")
  print()

if __name__ == "__main__":
  args = sys.argv[1:]
  for url in args:
    ytpl(url)
  else:
    ytpl("https://www.youtube.com/playlist?list=PLJzpzNSXetSPnQ0pr4ZX8DmrLFCNNFP-a")
    ytpl("https://www.youtube.com/playlist?list=PLJzpzNSXetSNHucm3uozwC8s5gn1CslAC")
