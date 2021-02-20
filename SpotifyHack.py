import ctypes
import time
from pycaw.pycaw import AudioUtilities


def findSpotifyAppSession():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if "name='Spotify.exe'" in session.Process.__str__():
            return session

def adWasFound(wasFound):  
    spotify_volume = findSpotifyAppSession().SimpleAudioVolume
    if wasFound:
        print("Ad found - muting")
        spotify_volume.SetMute(1, None)
    else:
        spotify_volume.SetMute(0, None)

def getTitles():
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
    is_muted = False
    while True:
        titles = getTitles()  # update titles

        # mute if app is named 'Spotify' or 'Advertisement'
        # unmute Spotify if an app is named as 'Spotify Free' or else
        if "Advertisement" in titles or "Spotify" in titles:
            if not is_muted:
                adWasFound(True)
                is_muted = True
                waiting_time = SLEEP_TIME_DURING_AD
                time.sleep(5)
        elif is_muted:
            ads_muted_counter += 1
            print("Total muted ads:", ads_muted_counter)
            waiting_time = SLEEP_TIME_NO_AD
            adWasFound(False)
            is_muted = False

        time.sleep(waiting_time)  # Sleep between checks (in seconds)

if __name__ == '__main__':
    main()
