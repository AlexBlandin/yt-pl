#!/usr/bin/env python3
import sys

from yt_dlp import YoutubeDL


# tree walk to each, if ever they break the current format
def dur(d):
  if isinstance(d, dict):
    if "duration" in d:
      yield int(d["duration"])
    for k, v in d.items():
      if isinstance(v, dict) and k != "fragments":
        yield from dur(v)
  elif isinstance(d, list):
    for v in d:
      if isinstance(v, dict):
        yield from dur(v)


def ytpl(url):
  """How long is a Youtube Playlist?"""
  with YoutubeDL({"dump_single_json": True, "simulate": True, "quiet": True}) as ydl:
    d = ydl.extract_info(url, download=False)
  assert isinstance(d, dict)

  # direct walk to durations in current format
  seconds = sum(v["duration"] for v in d["entries"])

  print(d["title"])
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
  url = input("Youtube Playlist to check (leave empty to quit): ").strip()
  while url:
    ytpl(url)
    url = input("Youtube Playlist to check (leave empty to quit): ").strip()
  ytpl("https://www.youtube.com/playlist?list=PLJzpzNSXetSPnQ0pr4ZX8DmrLFCNNFP-a")
