import os
import sys
import subprocess
import re
import time

def format_size(bytes_val):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} TB"

def render_progress_bar(percent, width=25):
    percent = max(0.0, min(100.0, percent))
    filled = int(width * percent / 100.0)
    bar = "=" * filled + (">" if filled < width else "") + " " * max(0, width - filled - 1)
    return bar

def read_stream_chunks(stream):
    """Yield progress chunks delimited by \r or \n."""
    buffer = bytearray()
    while True:
        chunk = stream.read(1)
        if not chunk:
            if buffer:
                yield buffer.decode('utf-8', errors='replace').strip()
            break
        if chunk in (b'\r', b'\n'):
            if buffer:
                text = buffer.decode('utf-8', errors='replace').strip()
                if text:
                    yield text
                buffer.clear()
        else:
            buffer.extend(chunk)

def main():
    print("=" * 75, flush=True)
    print("  GitHub Realtime Upload Monitor", flush=True)
    print("  Repository : https://github.com/ZubairZerok/SOWritten", flush=True)
    print("  Branch     : main", flush=True)
    print("=" * 75, flush=True)

    # File sizes
    lfs_file = "Bank Written Math 1986-2021.pdf"
    lfs_size = os.path.getsize(lfs_file) if os.path.exists(lfs_file) else 132632073
    git_obj_size = 313000000  # ~298.5 MiB
    total_upload_size = lfs_size + git_obj_size

    print(f"[*] Stage 1 (Git LFS File)   : {format_size(lfs_size)} ({lfs_file})", flush=True)
    print(f"[*] Stage 2 (Git Repository) : {format_size(git_obj_size)} (77 PDF documents & sheets)", flush=True)
    print(f"[*] Total Payload Size       : {format_size(total_upload_size)}", flush=True)
    print("-" * 75, flush=True)

    last_pct_logged = -1
    last_log_time = 0

    # --- STAGE 1: Git LFS Push ---
    print("\n[Stage 1/2] Uploading Git LFS object to GitHub LFS storage...", flush=True)
    cmd_lfs = ["git", "lfs", "push", "origin", "main"]
    
    proc_lfs = subprocess.Popen(
        cmd_lfs,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=0
    )

    lfs_bytes = 0
    lfs_percent = 0.0

    for raw_line in read_stream_chunks(proc_lfs.stdout):
        # Example: "Uploading LFS objects:  35% (0/1), 46 MB | 2.5 MB/s"
        match = re.search(r'Uploading LFS objects:\s+(\d+)%(?:.*?,\s*([0-9.]+)\s*([KMGT]?B))?(?:.*?\|\s*([0-9.]+\s*[KMGT]?B/s))?', raw_line)
        speed = ""
        if match:
            lfs_percent = float(match.group(1))
            lfs_bytes = lfs_size * (lfs_percent / 100.0)
            if match.group(4):
                speed = f" | Speed: {match.group(4)}"
        elif "100%" in raw_line:
            lfs_percent = 100.0
            lfs_bytes = lfs_size

        total_bytes = lfs_bytes
        total_percent = (total_bytes / total_upload_size) * 100.0

        now = time.time()
        # Log when percentage increments or at least every 2 seconds
        curr_int_pct = int(total_percent)
        if curr_int_pct > last_pct_logged or (now - last_log_time >= 2.0):
            bar = render_progress_bar(total_percent, width=25)
            line = f"[{total_percent:5.1f}%] [{bar}] {format_size(total_bytes):>9} / {format_size(total_upload_size)} | LFS: {lfs_percent:3.0f}%{speed}"
            print(line, flush=True)
            last_pct_logged = curr_int_pct
            last_log_time = now

    proc_lfs.wait()
    if proc_lfs.returncode != 0:
        print(f"\n[!] Error during Git LFS push. Exit code: {proc_lfs.returncode}", flush=True)
        sys.exit(proc_lfs.returncode)

    lfs_bytes = lfs_size
    stage1_total_pct = (lfs_bytes / total_upload_size) * 100.0
    bar = render_progress_bar(stage1_total_pct, width=25)
    print(f"[{stage1_total_pct:5.1f}%] [{bar}] Stage 1 Complete: LFS object uploaded!\n", flush=True)

    # --- STAGE 2: Git Push Objects ---
    print("[Stage 2/2] Uploading Git objects and branch references...", flush=True)
    cmd_git = ["git", "push", "--progress", "--no-verify", "-u", "origin", "main"]

    proc_git = subprocess.Popen(
        cmd_git,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=0
    )

    git_percent = 0.0
    git_bytes = 0
    speed_info = ""

    for raw_line in read_stream_chunks(proc_git.stdout):
        # Example: "Writing objects:  45% (35/78), 140.25 MiB | 4.10 MiB/s"
        match = re.search(r'Writing objects:\s+(\d+)%(?:.*?,\s*([0-9.]+)\s*([KMGT]?i?B))?(?:.*?\|\s*([0-9.]+\s*[KMGT]?i?B/s))?', raw_line)
        if match:
            git_percent = float(match.group(1))
            git_bytes = git_obj_size * (git_percent / 100.0)
            if match.group(4):
                speed_info = f" | Speed: {match.group(4)}"
        elif "Counting objects:" in raw_line or "Compressing objects:" in raw_line:
            speed_info = f" | {raw_line}"
        elif "Total" in raw_line or "To https://github.com" in raw_line:
            git_percent = 100.0
            git_bytes = git_obj_size

        total_bytes = lfs_bytes + git_bytes
        total_percent = min(100.0, (total_bytes / total_upload_size) * 100.0)

        now = time.time()
        curr_int_pct = int(total_percent)
        if curr_int_pct > last_pct_logged or (now - last_log_time >= 2.0):
            bar = render_progress_bar(total_percent, width=25)
            line = f"[{total_percent:5.1f}%] [{bar}] {format_size(total_bytes):>9} / {format_size(total_upload_size)} | Git: {git_percent:3.0f}%{speed_info}"
            print(line, flush=True)
            last_pct_logged = curr_int_pct
            last_log_time = now

    proc_git.wait()
    if proc_git.returncode != 0:
        print(f"\n[!] Error during Git push. Exit code: {proc_git.returncode}", flush=True)
        sys.exit(proc_git.returncode)

    bar = render_progress_bar(100.0, width=25)
    print(f"[100.0%] [{bar}] {format_size(total_upload_size):>9} / {format_size(total_upload_size)} | Upload Complete!", flush=True)
    print("\n" + "=" * 75, flush=True)
    print("  ALL FILES SUCCESSFULLY UPLOADED AND PUSHED TO GITHUB!", flush=True)
    print("  Repository : https://github.com/ZubairZerok/SOWritten", flush=True)
    print("  Branch     : main", flush=True)
    print("=" * 75, flush=True)

if __name__ == "__main__":
    main()
