#!/usr/bin/env python3

# ============================================================
#                 SOCIAL DOWNLOADS
#                 Developed by Thiago
# ============================================================

import os
import sys
import re
import subprocess
import shutil
import importlib.util
import time
from urllib.parse import urlparse, parse_qs


# ============================================================
# COLORS
# ============================================================

RESET   = "\033[0m"
BOLD    = "\033[1m"

RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
GRAY    = "\033[90m"


# ============================================================
# TERMINAL
# ============================================================

def clear():
    os.system("clear")


def pause():
    input(f"\n{GRAY}Press ENTER to continue...{RESET}")


def line():
    print(f"{GRAY}{'─' * 65}{RESET}")


def title(text):
    print()
    print(f"{BOLD}{CYAN}{'═' * 65}{RESET}")
    print(f"{BOLD}{WHITE}{text.center(65)}{RESET}")
    print(f"{BOLD}{CYAN}{'═' * 65}{RESET}")
    print()


# ============================================================
# INSTALL / CHECK DEPENDENCIES
# ============================================================

def command_exists(command):
    return shutil.which(command) is not None


def python_package_exists(package):
    return importlib.util.find_spec(package) is not None


def run_command(command):
    try:
        subprocess.run(
            command,
            check=True
        )
        return True
    except Exception:
        return False


def install_python_package(package):
    print(
        f"{YELLOW}[INSTALL]{RESET} "
        f"Installing Python package: {CYAN}{package}{RESET}"
    )

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                package
            ],
            check=True
        )
        return True
    except Exception as e:
        print(f"{RED}Failed to install {package}: {e}{RESET}")
        return False


def install_termux_package(package):
    print(
        f"{YELLOW}[INSTALL]{RESET} "
        f"Installing Termux package: {CYAN}{package}{RESET}"
    )

    try:
        subprocess.run(
            ["pkg", "install", "-y", package],
            check=True
        )
        return True
    except Exception as e:
        print(f"{RED}Failed to install {package}: {e}{RESET}")
        return False


def setup_dependencies():

    print(f"\n{BOLD}{CYAN}Checking required tools...{RESET}\n")

    # --------------------------------------------------------
    # yt-dlp
    # --------------------------------------------------------

    if not python_package_exists("yt_dlp"):
        install_python_package("yt-dlp")

    # --------------------------------------------------------
    # curl_cffi
    # --------------------------------------------------------

    if not python_package_exists("curl_cffi"):
        install_python_package("curl_cffi")

    # --------------------------------------------------------
    # pyfiglet
    # --------------------------------------------------------

    if not python_package_exists("pyfiglet"):
        install_python_package("pyfiglet")

    # --------------------------------------------------------
    # FFmpeg
    # --------------------------------------------------------

    if not command_exists("ffmpeg"):
        print(f"{YELLOW}FFmpeg is required for merging/conversion.{RESET}")

        if command_exists("pkg"):
            install_termux_package("ffmpeg")

    # --------------------------------------------------------
    # Node.js
    # --------------------------------------------------------

    if not command_exists("node"):
        print(f"{YELLOW}Node.js was not found.{RESET}")

        if command_exists("pkg"):
            install_termux_package("nodejs")

    print(f"\n{GREEN}Dependency check completed.{RESET}\n")

    time.sleep(1)


# ============================================================
# ASCII LOGO
# ============================================================

def make_ascii(text):
    try:
        from pyfiglet import figlet_format

        return figlet_format(
            text,
            font="big"
        )

    except Exception:
        return text


def platform_logo(platform):

    colors = {
        "Facebook": BLUE,
        "Instagram": MAGENTA,
        "TikTok": CYAN,
        "YouTube": RED,
        "X": WHITE,
        "Twitter": WHITE
    }

    text = {
        "Facebook": "FACEBOOK",
        "Instagram": "INSTAGRAM",
        "TikTok": "TIKTOK",
        "YouTube": "YOUTUBE",
        "X": "X",
        "Twitter": "TWITTER"
    }

    color = colors.get(platform, WHITE)
    name = text.get(platform, platform.upper())

    print(
        color +
        BOLD +
        make_ascii(name) +
        RESET
    )


# ============================================================
# MAIN APP LOGO
# ============================================================

def main_logo():

    print(f"{CYAN}{BOLD}")

    print(r"""
 ███████╗ ██████╗  ██████╗██╗ █████╗ ██╗
 ██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║
 ███████╗██║   ██║██║     ██║███████║██║
 ╚════██║██║   ██║██║     ██║██╔══██║██║
 ███████║╚██████╔╝╚██████╗██║██║  ██║██║
 ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚═╝

    """)

    print(f"{RESET}{GRAY}                    Developed by Thiago{RESET}")
    print()


# ============================================================
# URL ID EXTRACTION
# ============================================================

def extract_id(url):

    import re
    from urllib.parse import urlparse, parse_qs

    url = url.strip()

    try:

        # ----------------------------------------------------
        # YouTube
        # ----------------------------------------------------

        if "youtu.be" in url:

            m = re.search(
                r"youtu\.be/([A-Za-z0-9_-]+)",
                url
            )

            if m:
                return m.group(1)

        if "youtube.com" in url:

            parsed = urlparse(url)
            qs = parse_qs(parsed.query)

            if "v" in qs:
                return qs["v"][0]

            m = re.search(
                r"/(?:shorts|embed|live)/([A-Za-z0-9_-]+)",
                url
            )

            if m:
                return m.group(1)

        # ----------------------------------------------------
        # TikTok
        # ----------------------------------------------------

        if "tiktok.com" in url:

            m = re.search(
                r"/video/(\d+)",
                url
            )

            if m:
                return m.group(1)

            # Short TikTok URLs may not expose ID directly.
            m = re.search(
                r"tiktok\.com/[^/]+/video/(\d+)",
                url
            )

            if m:
                return m.group(1)

        # ----------------------------------------------------
        # Instagram
        # ----------------------------------------------------

        if "instagram.com" in url:

            m = re.search(
                r"/(?:p|reel|reels|tv)/([A-Za-z0-9_-]+)",
                url
            )

            if m:
                return m.group(1)

        # ----------------------------------------------------
        # Facebook
        # ----------------------------------------------------

        if "facebook.com" in url or "fb.watch" in url:

            # /share/r/xxxxx
            m = re.search(
                r"/share/[rv]/([^/?]+)",
                url
            )

            if m:
                return m.group(1)

            # /videos/123456
            m = re.search(
                r"/videos/(\d+)",
                url
            )

            if m:
                return m.group(1)

            # /watch/?v=123456
            parsed = urlparse(url)
            qs = parse_qs(parsed.query)

            if "v" in qs:
                return qs["v"][0]

            # fb.watch/xxxxx
            m = re.search(
                r"fb\.watch/([A-Za-z0-9_-]+)",
                url
            )

            if m:
                return m.group(1)

        # ----------------------------------------------------
        # X / Twitter
        # ----------------------------------------------------

        if "x.com" in url or "twitter.com" in url:

            m = re.search(
                r"/status/(\d+)",
                url
            )

            if m:
                return m.group(1)

    except Exception:
        pass

    # --------------------------------------------------------
    # Safe fallback
    # --------------------------------------------------------

    try:
        last = url.rstrip("/").split("/")[-1]

        if "?" in last:
            last = last.split("?")[0]

        return last[:40]

    except Exception:
        return "video"


# ============================================================
# PLATFORM DETECTION
# ============================================================

def detect_platform(url):

    url = url.lower()

    if "youtube.com" in url or "youtu.be" in url:
        return "YouTube"

    if "facebook.com" in url or "fb.watch" in url:
        return "Facebook"

    if "instagram.com" in url:
        return "Instagram"

    if "tiktok.com" in url:
        return "TikTok"

    if "x.com" in url:
        return "X"

    if "twitter.com" in url:
        return "Twitter"

    return "Unknown"


# ============================================================
# DOWNLOAD DIRECTORIES
# ============================================================

def get_download_root():

    home = os.path.expanduser("~")

    # Termux shared Downloads
    termux_downloads = os.path.join(
        home,
        "storage",
        "downloads"
    )

    if os.path.exists(
        os.path.join(home, "storage")
    ):
        os.makedirs(
            termux_downloads,
            exist_ok=True
        )

        return termux_downloads

    # Fallback
    fallback = os.path.join(
        home,
        "Downloads"
    )

    os.makedirs(
        fallback,
        exist_ok=True
    )

    return fallback


def platform_folder(platform):

    folders = {

        "Facebook":
            "fb downloads",

        "Instagram":
            "instagram downloads",

        "TikTok":
            "tiktok downloads",

        "YouTube":
            "youtube downloads",

        "X":
            "x downloads",

        "Twitter":
            "twitter downloads"
    }

    folder = folders.get(
        platform,
        "other downloads"
    )

    path = os.path.join(
        get_download_root(),
        folder
    )

    os.makedirs(
        path,
        exist_ok=True
    )

    return path


# ============================================================
# SAFE FILE NAME
# ============================================================

def clean_filename(name):

    if not name:
        return "video"

    name = str(name)

    # Remove illegal filesystem characters
    name = re.sub(
        r'[\\/:*?"<>|]',
        "_",
        name
    )

    # Remove control characters
    name = re.sub(
        r"[\x00-\x1f]",
        "",
        name
    )

    # Remove excessive spaces
    name = re.sub(
        r"\s+",
        " ",
        name
    ).strip()

    # Avoid very long Android filenames
    name = name[:150]

    if not name:
        name = "video"

    return name


def unique_filename(folder, filename):

    filename = clean_filename(filename)

    base, ext = os.path.splitext(filename)

    if not ext:
        ext = ".mp4"

    path = os.path.join(
        folder,
        base + ext
    )

    if not os.path.exists(path):
        return path

    counter = 1

    while True:

        new_name = f"{base}({counter}){ext}"

        new_path = os.path.join(
            folder,
            new_name
        )

        if not os.path.exists(new_path):
            return new_path

        counter += 1


# ============================================================
# QUALITY MENU
# ============================================================

def quality_menu():

    title("SELECT VIDEO QUALITY")

    print(
        f"{GREEN}1.{RESET} Best quality"
    )

    print(
        f"{CYAN}2.{RESET} 1080p"
    )

    print(
        f"{CYAN}3.{RESET} 720p"
    )

    print(
        f"{CYAN}4.{RESET} 480p"
    )

    print(
        f"{CYAN}5.{RESET} 360p"
    )

    print(
        f"{YELLOW}6.{RESET} Audio only"
    )

    print()

    while True:

        choice = input(
            f"{BOLD}Choose quality: {RESET}"
        ).strip()

        if choice in (
            "1",
            "2",
            "3",
            "4",
            "5",
            "6"
        ):
            return choice

        print(
            f"{RED}Invalid choice.{RESET}"
        )


def quality_format(choice):

    formats = {

        "1":
            "bestvideo*+bestaudio/best",

        "2":
            "bestvideo[height<=1080]+bestaudio/"
            "best[height<=1080]",

        "3":
            "bestvideo[height<=720]+bestaudio/"
            "best[height<=720]",

        "4":
            "bestvideo[height<=480]+bestaudio/"
            "best[height<=480]",

        "5":
            "bestvideo[height<=360]+bestaudio/"
            "best[height<=360]",

        "6":
            "bestaudio/best"
    }

    return formats[choice]


# ============================================================
# DOWNLOAD PROGRESS
# ============================================================

def progress_hook(data):

    status = data.get("status")

    if status == "downloading":

        total = (
            data.get("total_bytes")
            or
            data.get("total_bytes_estimate")
            or
            0
        )

        downloaded = (
            data.get("downloaded_bytes")
            or
            0
        )

        if total:

            percent = (
                downloaded / total
            ) * 100

        else:

            percent = 0

        speed = data.get(
            "speed"
        ) or 0

        eta = data.get(
            "eta"
        )

        def size(value):

            units = [
                "B",
                "KB",
                "MB",
                "GB"
            ]

            value = float(value)

            for unit in units:

                if value < 1024:
                    return f"{value:.1f}{unit}"

                value /= 1024

            return f"{value:.1f}TB"

        speed_text = (
            f"{size(speed)}/s"
            if speed
            else "--"
        )

        eta_text = (
            f"{eta}s"
            if eta is not None
            else "--"
        )

        bar_length = 30

        filled = int(
            bar_length *
            percent /
            100
        )

        bar = (
            "█" * filled
            +
            "░" *
            (
                bar_length -
                filled
            )
        )

        print(
            f"\r"
            f"{CYAN}[{bar}]{RESET} "
            f"{GREEN}{percent:6.2f}%{RESET} "
            f"{WHITE}{size(downloaded)}"
            f"/{size(total)}{RESET} "
            f"{YELLOW}{speed_text}{RESET} "
            f"{GRAY}ETA {eta_text}{RESET}",
            end="",
            flush=True
        )

    elif status == "finished":

        print(
            f"\n{GREEN}✓ Download completed.{RESET}"
        )


# ============================================================
# DOWNLOAD FUNCTION
# ============================================================

def download_video(url, quality_choice):

    platform = detect_platform(url)

    if platform == "Unknown":

        print(
            f"{RED}Unsupported platform.{RESET}"
        )

        return False

    folder = platform_folder(
        platform
    )

    video_id = extract_id(url)

    print()
    line()

    platform_logo(platform)

    print(
        f"{GRAY}Platform:{RESET} "
        f"{WHITE}{platform}{RESET}"
    )

    print(
        f"{GRAY}Video ID:{RESET} "
        f"{WHITE}{video_id}{RESET}"
    )

    print(
        f"{GRAY}Folder:{RESET} "
        f"{WHITE}{folder}{RESET}"
    )

    line()

    try:

        import yt_dlp

    except ImportError:

        print(
            f"{RED}yt-dlp is not installed.{RESET}"
        )

        return False

    # --------------------------------------------------------
    # Audio
    # --------------------------------------------------------

    if quality_choice == "6":

        output_template = os.path.join(
            folder,
            "%(title).150s.%(ext)s"
        )

        options = {

            "format":
                "bestaudio/best",

            "outtmpl":
                output_template,

            "noplaylist":
                True,

            "quiet":
                True,

            "no_warnings":
                True,

            "progress_hooks":
                [progress_hook],

            "postprocessors": [

                {
                    "key":
                        "FFmpegExtractAudio",

                    "preferredcodec":
                        "mp3",

                    "preferredquality":
                        "192"
                }

            ],

            "restrictfilenames":
                False
        }

    # --------------------------------------------------------
    # Video
    # --------------------------------------------------------

    else:

        output_template = os.path.join(
            folder,
            "%(title).150s.%(ext)s"
        )

        options = {

            "format":
                quality_format(
                    quality_choice
                ),

            "outtmpl":
                output_template,

            "merge_output_format":
                "mp4",

            "noplaylist":
                True,

            "quiet":
                True,

            "no_warnings":
                True,

            "progress_hooks":
                [progress_hook],

            "restrictfilenames":
                False,

            # Helps with some websites
            "http_headers": {

                "User-Agent":
                    "Mozilla/5.0 "
                    "(Linux; Android 10; Mobile) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/130.0 Mobile Safari/537.36"
            }
        }

    # --------------------------------------------------------
    # curl_cffi impersonation
    # --------------------------------------------------------

    try:

        import curl_cffi

        options["http_client"] = "curl_cffi"

    except Exception:

        pass

    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    try:

        print(
            f"\n{CYAN}Starting download...{RESET}\n"
        )

        with yt_dlp.YoutubeDL(
            options
        ) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )

            title_name = info.get(
                "title"
            )

            if not title_name:

                title_name = video_id

            title_name = clean_filename(
                title_name
            )

            print(
                f"{WHITE}Title:{RESET} "
                f"{title_name}"
            )

            print()

            ydl.download(
                [url]
            )

        print()
        line()

        print(
            f"{GREEN}{BOLD}"
            f"✓ DOWNLOAD SUCCESSFUL"
            f"{RESET}"
        )

        print(
            f"{GRAY}Saved in:{RESET}"
        )

        print(
            f"{WHITE}{folder}{RESET}"
        )

        line()

        return True

    except KeyboardInterrupt:

        print(
            f"\n\n{YELLOW}"
            f"Download cancelled."
            f"{RESET}"
        )

        return False

    except Exception as e:

        print()
        line()

        print(
            f"{RED}{BOLD}"
            f"✗ DOWNLOAD FAILED"
            f"{RESET}"
        )

        print(
            f"{RED}{e}{RESET}"
        )

        line()

        return False


# ============================================================
# GET URL
# ============================================================

def get_url():

    print()

    url = input(
        f"{CYAN}Paste video URL:{RESET}\n> "
    ).strip()

    if not url:
        print(
            f"{RED}No URL entered.{RESET}"
        )
        return None

    platform = detect_platform(url)

    if platform == "Unknown":

        print(
            f"{RED}This URL is not supported.{RESET}"
        )

        return None

    print(
        f"\n{GREEN}Detected:{RESET} "
        f"{BOLD}{platform}{RESET}"
    )

    print(
        f"{GRAY}ID:{RESET} "
        f"{extract_id(url)}"
    )

    return url


# ============================================================
# SINGLE DOWNLOAD
# ============================================================

def single_download():

    clear()

    platform_logo("YouTube")

    title("SINGLE VIDEO DOWNLOAD")

    url = get_url()

    if not url:
        pause()
        return

    quality = quality_menu()

    download_video(
        url,
        quality
    )

    pause()


# ============================================================
# BATCH DOWNLOAD
# ============================================================

def batch_download():

    clear()

    title("MULTIPLE VIDEO DOWNLOAD")

    print(
        f"{GRAY}"
        "Paste URLs one by one."
        "\nType "
        f"{YELLOW}done{GRAY}"
        " when you have finished."
        f"{RESET}\n"
    )

    urls = []

    while True:

        url = input(
            f"{CYAN}URL {len(urls)+1}:{RESET} "
        ).strip()

        if url.lower() == "done":

            break

        if not url:

            continue

        platform = detect_platform(
            url
        )

        if platform == "Unknown":

            print(
                f"{RED}"
                "Unsupported URL."
                f"{RESET}"
            )

            continue

        urls.append(url)

        print(
            f"{GREEN}✓ {platform}"
            f" added{RESET}"
        )

    if not urls:

        print(
            f"{YELLOW}"
            "No URLs were added."
            f"{RESET}"
        )

        pause()
        return

    print()

    line()

    print(
        f"{BOLD}{WHITE}"
        f"{len(urls)} videos ready"
        f"{RESET}"
    )

    line()

    quality = quality_menu()

    successful = 0
    failed = 0

    for index, url in enumerate(
        urls,
        start=1
    ):

        clear()

        print(
            f"{BOLD}{CYAN}"
            f"DOWNLOAD {index}/{len(urls)}"
            f"{RESET}"
        )

        print()

        if download_video(
            url,
            quality
        ):

            successful += 1

        else:

            failed += 1

        time.sleep(1)

    clear()

    title("BATCH DOWNLOAD COMPLETE")

    print(
        f"{GREEN}Successful:{RESET} "
        f"{successful}"
    )

    print(
        f"{RED}Failed:{RESET} "
        f"{failed}"
    )

    print(
        f"{WHITE}Total:{RESET} "
        f"{len(urls)}"
    )

    pause()


# ============================================================
# PLATFORM DOWNLOAD SCREEN
# ============================================================

def platform_download(platform):

    while True:

        clear()

        platform_logo(platform)

        line()

        print(
            f"{GREEN}1.{RESET} "
            f"Download one video"
        )

        print(
            f"{CYAN}2.{RESET} "
            f"Download many videos"
        )

        print(
            f"{YELLOW}3.{RESET} "
            f"Back"
        )

        line()

        choice = input(
            f"\n{BOLD}Choose: {RESET}"
        ).strip()

        if choice == "1":

            clear()

            platform_logo(
                platform
            )

            title(
                f"{platform.upper()} DOWNLOAD"
            )

            url = get_url()

            if not url:
                pause()
                continue

            detected = detect_platform(
                url
            )

            if detected != platform:

                print(
                    f"{YELLOW}"
                    f"This is detected as "
                    f"{detected}, not {platform}."
                    f"{RESET}"
                )

                pause()
                continue

            quality = quality_menu()

            download_video(
                url,
                quality
            )

            pause()

        elif choice == "2":

            batch_download()

        elif choice == "3":

            return

        else:

            print(
                f"{RED}Invalid choice.{RESET}"
            )

            time.sleep(1)


# ============================================================
# SOCIAL MENU
# ============================================================

def social():

    platforms = {

        "1": "Facebook",
        "2": "Instagram",
        "3": "TikTok",
        "4": "YouTube",
        "5": "X"
    }

    while True:

        clear()

        main_logo()

        title("SOCIAL VIDEO DOWNLOADER")

        print(
            f"{BLUE}1.{RESET} "
            f"{BOLD}Facebook{RESET}"
        )

        print(
            f"{MAGENTA}2.{RESET} "
            f"{BOLD}Instagram{RESET}"
        )

        print(
            f"{CYAN}3.{RESET} "
            f"{BOLD}TikTok{RESET}"
        )

        print(
            f"{RED}4.{RESET} "
            f"{BOLD}YouTube{RESET}"
        )

        print(
            f"{WHITE}5.{RESET} "
            f"{BOLD}X / Twitter{RESET}"
        )

        print()

        print(
            f"{YELLOW}6.{RESET} "
            f"Exit"
        )

        line()

        choice = input(
            f"{BOLD}Select platform: {RESET}"
        ).strip()

        if choice in platforms:

            platform_download(
                platforms[choice]
            )

        elif choice == "6":

            clear()

            print(
                f"\n{GREEN}{BOLD}"
                "Thank you for using "
                "SOCIAL DOWNLOADS."
                f"{RESET}\n"
            )

            break

        else:

            print(
                f"{RED}"
                "Invalid option."
                f"{RESET}"
            )

            time.sleep(1)


# ============================================================
# TERMUX STORAGE SETUP
# ============================================================

def setup_storage():

    home = os.path.expanduser("~")

    storage_path = os.path.join(
        home,
        "storage"
    )

    # If Termux storage is not configured
    if not os.path.exists(
        storage_path
    ):

        print(
            f"{YELLOW}"
            "Termux shared storage is not configured."
            f"{RESET}"
        )

        print()

        answer = input(
            "Run 'termux-setup-storage' now? "
            "[Y/n]: "
        ).strip().lower()

        if answer in (
            "",
            "y",
            "yes"
        ):

            if command_exists(
                "termux-setup-storage"
            ):

                os.system(
                    "termux-setup-storage"
                )

                time.sleep(2)


# ============================================================
# MAIN
# ============================================================

def main():

    clear()

    print(
        f"{CYAN}{BOLD}"
        "\nStarting SOCIAL DOWNLOADS..."
        f"{RESET}\n"
    )

    setup_storage()

    setup_dependencies()

    time.sleep(1)

    social()


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()