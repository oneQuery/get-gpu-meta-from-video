import subprocess
import os
import requests

def get_gpu_meta(video_path:str, log_file):

    process = subprocess.Popen(
        [exe, video_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )

    for output in process.stdout:
        
        if ("gps" in output.strip()) or ("GPS" in output.strip()):
            print(f"{video_path}: gps exists")
            log_file.write(f"{video_path}: gps exists\n")
            global num_have_gps
            num_have_gps += 1
            break
            
    global cnt_checked
    cnt_checked += 1
    print(f"({cnt_checked}/{cnt_total}) {video_path}: gps does not exist")
        
        
if __name__=="__main__":
    
    if not os.path.exists("Image-ExifTool-12.64.tar.gz"):
        print("Donwloading exiftool...")
        exiftool_url = "https://exiftool.org/Image-ExifTool-12.64.tar.gz"
        response = requests.get(exiftool_url)
        open("Image-ExifTool-12.64.tar.gz", "wb").write(response.content)
        untar_cmd = "tar -xzf Image-ExifTool-12.64.tar.gz"
        os.system(untar_cmd)
    
    root = "/Users/heesukim/Downloads"
    # poc_ver = "poc_01"
    # poc_ver = "poc_02"  # no gps info at all
    # poc_ver = "poc_03"
    poc_ver = "poc_04"
    # poc_ver = "poc_10"
    # poc_ver = "poc_11"
    exe = "Image-ExifTool-12.64/exiftool"
    
    video_root = os.path.join(root, poc_ver)
    video_files = os.listdir(video_root)
    video_paths = [os.path.join(video_root, file) for file in video_files]
    
    global cnt_total, cnt_checked, num_have_gps
    cnt_total = len(video_paths)
    cnt_checked = 0
    num_have_gps = 0
    
    # Open the log file
    with open(f'logfile_{poc_ver}.txt', 'w') as log_file:
    
        for video_path in video_paths:
            get_gpu_meta(video_path, log_file)
        
        log_file.write(f"num_have_gps: {num_have_gps}\n")
        log_file.write("done\n")
        
    print("num_have_gps:", num_have_gps)
    print("done")