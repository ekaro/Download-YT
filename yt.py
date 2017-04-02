import pafy #needs youtube-dl
import validators
import re

defdir = "C:/Downloads"
print("Default download directory is: %s" %defdir)

valid_input = False
while not valid_input:
    defchange = input("Do you want to download to this directory? (Y/N) ")

    if defchange.upper() == "N":
        ddir = input("Enter new directory: ")
        #ddir.replace("\\", "/")
        print("Video will be downloaded to %s: " %ddir)
        valid_input = True
        break
        '''
        valid_input2 = False
        while not valid_input2:
            set = input("Do you want to set this directory as default? (Y/N) ")
            if set.upper() == "Y":
                defdir = ddir
                print("New default download directory is: %s" %defdir)
                valid_input2 = True
            if set.upper() == "N":
                valid_input2 = True
            else:
                print("Wrong input, please enter Y or N")'''
               
    if defchange.upper() == "Y":
        ddir = defdir
        valid_input = True
        break

    else:
        print("Wrong input, please enter Y or N")

valid_url = False
while not valid_url:

    url = input("Enter url of video: ")
    valid_url = validators.url(url)

    if valid_url:
        if re.search("https://www.youtube.com", url):
            video = pafy.new(url)
            print("Your video is: ", video.title, url)
        else:
            valid_url = False
            print("Not valid youtube url, please enter again.")
    else:
        print("Not valid url, please enter again.")
        
streams = video.streams
print("You can download these sizes of the video:")

for stream in streams:        
    print(streams.index(stream)+1, "Resolution:", stream.resolution, "File:", stream.extension, "Size:", round(stream.get_filesize()/1024/1024, 2), "MB")

valid_input = False
while not valid_input:

    down = input("Select which video you want to download (1...%s) or select B for best quality: " %(len(streams)))

    if down.upper() == 'B':
        best = video.getbest()
        print("The best quality is: Resolution -", best.resolution, "Format -", best.extension, "Size -", round(best.get_filesize()/1024/1024, 2), "MB")      

        valid_input = False
        while not valid_input:
            yn = input("Do you wish to download? (Y/N) ")
            if yn.upper() == 'Y':
                try:
                    print("Downloading...")
                    best.download(quiet=True, filepath=ddir)                    
                    print("Download successful!")
                    valid_input = True
                    break
                except:
                    print("Download not successful. Please try again.")
            if yn.upper() == 'N':
                print("Download canceled")
                valid_input = True
            else:
                print("Wrong input, please enter Y or N")

        valid_input = True

    idown = int(down)       
    if idown <= len(streams) and idown > 0:
        print("You chose this video: Resolution -", streams[idown-1].resolution, "Format -", streams[idown-1].extension, "Size -", round(streams[idown-1].get_filesize()/1024/1024, 2), "MB") 

        valid_input = False
        while not valid_input:
            yn = input("Do you wish to download this video? (Y/N) ")
            if yn.upper() == 'Y':
                try:
                    print("Downloading...")
                    streams[idown-1].download(quiet=True, filepath=ddir)
                    print("Download successful!")
                    valid_input = True
                    break
                except:
                    print("Download not successful. Please try again.")
            if yn.upper() == 'N':
                print("Download canceled")
                valid_input = True
            else:
                print("Wrong input, please enter Y or N")

        valid_input = True

    else:
        print("Wrong input, please enter number between 1 and %s or enter B for best quality" %(len(streams)))
