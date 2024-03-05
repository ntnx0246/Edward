import discord
from discord.ext import commands
import cv2
import curses
import argparse
import time
from functools import lru_cache

bot = commands.Bot(command_prefix='!')


@bot.command()
async def playascii(ctx, video_path):
    args = argparse.Namespace(width=120, fps=30, show=False, inv=False, video=video_path)

    video = args.video
    try:
        video = int(video)
    except ValueError:
        pass

    width = args.width
    characters = [' ', '.', ',', '-', '~', ':', ';', '=', '!', '*', '#', '$', '@']
    if args.inv:
        characters = characters[::-1]
    char_range = int(255 / len(characters))

    @lru_cache
    def get_char(val):
        return characters[min(int(val/char_range), len(characters)-1)]

    try:
        if type(video) is str and not os.path.isfile(video):
            await ctx.send("Failed to find the video.")

        video = cv2.VideoCapture(video)
        ok, frame = video.read()
        if not ok:
            await ctx.send("Could not extract frame from the video.")

        ratio = width/frame.shape[1]
        height = int(frame.shape[0]*ratio) // 2  # character height is 2 times character width

        curses.initscr()
        window = curses.newwin(height, width, 0, 0)

        frame_count = 0
        frames_per_ms = args.fps/1000
        start = time.perf_counter_ns()//1000000
        while True:
            ok, orig_frame = video.read()
            if not ok:
                break

            frame = cv2.resize(orig_frame, (width, height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # ASCII art conversion
            ascii_frame = ""
            for y in range(0, frame.shape[0]):
                for x in range(0, frame.shape[1]):
                    try:
                        window.addch(y, x, get_char(frame[y, x]))
                        ascii_frame += get_char(frame[y, x])
                    except (curses.error):
                        pass

            await ctx.send(f'```{ascii_frame}```')  # Send ASCII art to Discord

            elapsed = (time.perf_counter_ns()//1000000) - start
            supposed_frame_count = frames_per_ms * elapsed
            if frame_count > supposed_frame_count:
                time.sleep((frame_count-supposed_frame_count)*(1/frames_per_ms)/1000)
            frame_count += 1
    finally:
        cv2.destroyAllWindows()
        curses.endwin()
        fps = frame_count / (((time.perf_counter_ns()//1000000) - start) / 1000)
        await ctx.send(f"Played on average at {fps:.2f} fps.")


bot.run('BOT TOKEN HERE')
