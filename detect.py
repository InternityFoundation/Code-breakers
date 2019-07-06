import tkinter as tk, threading
import imageio
from PIL import Image, ImageTk

#
frame_height = 400
frame_width = 800
margin = 20
frame_speed = 15
tolerance = 20
#
    
if __name__=="__main__":
    root = tk.Tk()
    frame=tk.Canvas(root, height=frame_height, width=frame_width)
    frame.pack()
    screen=frame.create_image(frame_width/2, frame_height/2)
    
    dot = 10
    vdots = 0
    vscan = []
    while dot < frame_height:
        vscan.append(( frame_width-margin, dot-2))
        dot += 15
        vdots += 1

    video = imageio.get_reader("slide.mp4")
    def scan():
        
        def grey(R,G=0,B=0):
            if B:
                return (R+G+B)/3
            return R

        def findW(W,Wp):
            for d in range(frame_speed,-1,-1):
                Wnew = (W[0]-d,W[1])
                if  grey(*imagefile.getpixel(Wnew)) - Wp < 10:
                    return Wnew

        W = 0
        E = 0
        N = [vdots,0]
        S = [0,0]
        for image in video.iter_data():
            imagefile=Image.fromarray(image)
            frame.itemconfig(screen, image=ImageTk.PhotoImage(imagefile))
            basepixel=grey(*imagefile.getpixel((frame_height-margin,5)))

            obj = False
            for i in vscan:
                if basepixel - grey(*imagefile.getpixel(i)) >= tolerance :
                    limit=False
                    if vscan.index(i) < N[0] :
                        N = [vscan.index(i), i]
                    if W:
                        obj = True
                        Wnew = findW(W, Wp)
                        if Wnew:
                            W = Wnew
                        E = i
                    else:
                        W = i
                        Wp = grey(*imagefile.getpixel(i))
                elif obj and limit == False:
                    if vscan.index(i) > S[0] :
                        S = [vscan.index(i),i]
                    limit=True
                    
            if obj == False and (N[1],S[1],W,E).count(0) == 0 :
                focus = frame.create_rectangle(W[0], N[1][1], E[0], S[1][1], outline='darkblue')
                W = 0
                E = 0
                N = [vdots, 0]
                S = [0, 0]
                Wp=0
                                
    threading.Thread(target=scan).start()
    root.mainloop()
