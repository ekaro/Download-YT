import pafy # needs youtube-dl
import validators

defdir = "C:/Downloads"
print("\nDefault download directory is: %s" %defdir)

# setting download directory
valid_input = False
while not valid_input:
    defchange = input("\nDo you want to download to this directory? (y/n) ")  
    if defchange.upper() == "N":
        ddir = input("\nEnter new directory: ")
        ddir.replace("\\", "/")
        print("\nVideo will be downloaded to %s: " %ddir)
        valid_input = True
        break           
    if defchange.upper() == "Y":
        ddir = defdir
        valid_input = True
        break       
    else:
        print("\nWrong input, please enter Y or N")

# validation of url
valid_url = False
while not valid_url:
    url = input("\nEnter url of youtube video: ")
    valid_url = validators.url(url) 
    if valid_url:
        try:
            video = pafy.new(url)
            print(video.title)
        except: 
            valid_url = False
            print("\n%s is not a valid youtube url, please enter again." %url)                            
    else:
        print("\n%s is not a valid url, please enter again." %url)

# printing possible formats of video        
streams = video.streams
print("\nYou can download these versions of the video:")
for stream in streams:        
    print("%s." %(streams.index(stream)+1), "Resolution: %s," %(stream.resolution), "Format: %s," %(stream.extension), "Size: %s MB" %(round(stream.get_filesize()/1024/1024, 2)))

# selecting quality of video and downloading
valid_input = False
while not valid_input:   
    down = input("\nSelect which quality of the video you want to download (1...%s) or select B for best quality: " %(len(streams)))
    
    if down.upper() == 'B':
        best = video.getbest()
        print("\nResolution: %s," %(best.resolution), "Format: %s," %(best.extension), "Size: %s MB" %(round(best.get_filesize()/1024/1024, 2)))      
        valid_input = False
        while not valid_input:
            yn = input("\nDo you wish to download this video? (y/n) ")
            if yn.upper() == 'Y':
                try:
                    print("\nDownloading...")
                    best.download(quiet=True, filepath=ddir) # TODO: if file exists...                  
                    print("\nDownload successful!")
                    valid_input = True
                    break
                except:
                    print("\nDownload not successful. Please try again later.")
                    valid_input = True
                    break
            if yn.upper() == 'N':
                valid_input = True                
            else:
                print("\nWrong input, please enter Y or N.")

        if yn.upper() == 'Y':
            valid_input = True            
        if yn.upper() == 'N':
            valid_input = False                

    try:    
        idown = int(down)
        downisnum = True
    except:
        downisnum = False        
        break
    
    if downisnum and idown <= len(streams) and idown > 0:
        print("\nResolution: %s," %(streams[idown-1].resolution), "Format: %s," %(streams[idown-1].extension), "Size: %s MB" %(round(streams[idown-1].get_filesize()/1024/1024, 2))) 
        valid_input = False
        while not valid_input:
            yn = input("\nDo you wish to download this video? (y/n) ")
            if yn.upper() == 'Y':
                try:
                    print("\nDownloading...")
                    streams[idown-1].download(quiet=True, filepath=ddir) # TODO: if file exists...
                    print("\nDownload successful!")
                    valid_input = True
                    break
                except:
                    print("\nDownload not successful. Please try again later.")
                    valid_input = True
                    break
            if yn.upper() == 'N':                
                valid_input = True                
            else:
                print("\nWrong input, please enter Y or N.")

        if yn.upper() == 'Y':
            valid_input = True
        if yn.upper() == 'N':
            valid_input = False
        
    else:
        print("\nWrong input, please enter number between 1 and %s or enter B for best quality." %(len(streams))) # need to fix showing of this after download is successful
