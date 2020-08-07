import ctypes  # find process title
import time  # for sleep
from pycaw.pycaw import AudioUtilities  # mute


def findSpotifyAppSession():
    sessions = AudioUtilities.GetAllSessions()
    for t in sessions:
        if "name='Spotify.exe'" in t.Process.__str__():
            return t


def adWasFound(b):  # b - true if found, false otherwise
    spotify_volume = findSpotifyAppSession().SimpleAudioVolume
    if (b):
        print("Ad found - muting")
        spotify_volume.SetMute(1, None)
    else:
        spotify_volume.SetMute(0, None)


# not mine magic ;P
def getTitles():
    ####### Modules to gather data
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    titles = []  # list for titles (As String Objects)

    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True

    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return titles


def main():
    print("Running, to stop just close the window ;)")
    SLEEP_TIME_NO_AD = 4  # in seconds, time between each check for ad
    SLEEP_TIME_DURING_AD = 1
    waiting_time = SLEEP_TIME_NO_AD
    ads_muted_counter = 0
    iter_counter = 0
    titles = getTitles()
    is_muted = False
    while True:
        if iter_counter == 10:  # each 10*SLEEP_TIME seconds
            iter_counter = 0
            titles = getTitles()  # update titles

        # mute if app is named 'Spotify' or 'Advertisement'
        # unmute Spotify if an app is named as 'Spotify Free' or else
        if "Advertisement" in titles or "Spotify" in titles:
            adWasFound(True)
            is_muted = True
            waiting_time = SLEEP_TIME_DURING_AD
            time.sleep(5)  # because usual adds have around 15s to 30s
        elif is_muted:
            ads_muted_counter += 1
            print("Total muted ads:")
            waiting_time = SLEEP_TIME_NO_AD
            adWasFound(False)

        iter_counter += 1
        time.sleep(waiting_time)  # Sleep between checks (in seconds)


if __name__ == '__main__':
    main()
