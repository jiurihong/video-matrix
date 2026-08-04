"""
NSFW check utility (placeholder). Attempts to extract a frame and run an image classifier if available.
Returns True if safe, False if flagged NSFW.
"""
import os, subprocess

def check_nsfw(video_path):
    # extract frame
    frame = '/tmp/vm_nsfw_check.jpg'
    try:
        subprocess.run(f"ffmpeg -i {video_path} -ss 00:00:01 -vframes 1 {frame} -y", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        return True
    # try to import an image classifier
    try:
        from transformers import pipeline
        clf = pipeline('image-classification', model='openai/clip-vit-base-patch32')
        res = clf(frame)
        # naive heuristic: if 'porn' in labels (not reliable) - placeholder
        for r in res:
            label = r.get('label','').lower()
            if 'porn' in label or 'nsfw' in label:
                return False
        return True
    except Exception:
        # no classifier available, assume safe (caller should use manual review if paranoid)
        return True
