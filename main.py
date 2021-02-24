import time
import hololive
import threading
import datetime
import subprocess
import re
import sys
asmr_chars = re.compile("asmr|special", re.IGNORECASE)
karaoke_chars = re.compile("karaoke|🎵|sing", re.IGNORECASE)
game_chars = re.compile("undertale|minecraft", re.IGNORECASE)


class downloads:
    scheduled = {}
    done = []

# Because stream is not a copy, but a pointer, there is no need to
# implement rescheduling logic, simply syncing should do the trick
def schedule_download(stream, output, category):
    while not stream["youtube_url"] in downloads.done:
        time.sleep(10)
        current_time = datetime.datetime.now()
        stream_time = stream["datetime"]
        if current_time > stream_time :
            continue
        cmd = ["streamlink", stream["youtube_url"], "best", "-o", output]
        print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)
        p.communicate()
        if p.returncode != 0:
            print(stream)
            continue # Retry untill it works

        return finish_download(stream, output, category)

    pass

def finish_download(stream, output, category):
    # Handle streams once they're finished
    pass

for day in hololive.streams.schedule["schedule"]:
    for stream in day["schedules"]:
        category = ""
        if karaoke_chars.search(stream["title"]):
            category = "karaoke"

        elif asmr_chars.search(stream["title"]):
            category = "asmr"

        elif game_chars.search(stream["title"]):
            category = "game"
            
        else:
            continue

        print("{} is a wanted {} stream. Planning to archive it!".format(stream["title"],category))

        output = "/mnt/array/hololive/tmp/{}/{}.mkv".format(category, stream["youtube_url"].split("?v=")[1])
        t = threading.Thread(target=schedule_download,args=(stream,output,category))
        t.start()

try:
    input()
except:
    sys.exit(0)