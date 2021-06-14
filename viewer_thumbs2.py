import os, sys, math
from tkinter import *
from PIL import Image
from PIL.ImageTk import PhotoImage



def makeThumbs(imgdir, size=(100, 100), subdir='thumbs'):
    thumbdir = os.path.join(imgdir, subdir)
    if not os.path.exists(thumbdir):
        os.mkdir(thumbdir)

    thumbs = []
    for imgfile in os.listdir(imgdir):
        thumbpath = os.path.join(thumbdir, imgfile)

        imgpath = os.path.join(imgdir, imgfile)
        try:
            imgobj = Image.open(imgpath)  # make new thumb
            imgobj.thumbnail(size, Image.ANTIALIAS)  # best downsize filter
            imgobj.save(thumbpath)  # type via ext or passed
            thumbs.append((imgfile, imgobj))
        except:  # not always IOError
            print("Skipping: ", imgpath)
    return thumbs


def viewer(obj, imgdir, kind, numcols=None, height=500, width=500):
    """
    use fixed-size buttons, scrollable canvas;
    sets scrollable (full) size, and places thumbs at absolute x,y
    coordinates in canvas;  caveat: assumes all thumbs are same size
    """
    win = kind()
    win.title('Simple viewer: ' + imgdir)

    canvas = Canvas(win, borderwidth=0)
    vbar = Scrollbar(win)
    hbar = Scrollbar(win, orient='horizontal')

    vbar.pack(side=RIGHT, fill=Y)  # pack canvas after bars
    hbar.pack(side=BOTTOM, fill=X)  # so clipped first
    canvas.pack(side=TOP, fill=BOTH, expand=YES)

    vbar.config(command=canvas.yview)  # call on scroll move
    hbar.config(command=canvas.xview)
    canvas.config(yscrollcommand=vbar.set)  # call on canvas move
    canvas.config(xscrollcommand=hbar.set)
    canvas.config(height=height, width=width)  # init viewable area size
    # changes if user resizes
    thumbs = makeThumbs(imgdir)  # [(imgfile, imgobj)]
    numthumbs = len(thumbs)
    label = Label(win, text="총 {}개의 이미지 검색됨".format(numthumbs), bg='beige')
    label.pack(side=BOTTOM, fill=X)
    a = Frame(win)
    list_save_button = Button(a, text='DB에 저장', command=obj.image_into_DB)
    list_save_button.pack(side='right', anchor='w')
    list_view_button = Button(a, text="DB목록보기", repeatdelay=1000, repeatinterval=100,
                              command=obj.createNewWindow3)
    list_view_button.pack(side='left', anchor='s')
    a.pack(fill='x')

    if not numcols:
        numcols = int(math.ceil(math.sqrt(numthumbs)))  # fixed or N x N
    numrows = int(math.ceil(numthumbs / numcols))  # 3.x true div

    linksize = max(thumbs[0][1].size)  # (width, height)
    fullsize = (0, 0,  # upper left  X,Y
                (linksize * numcols), (linksize * numrows))  # lower right X,Y
    canvas.config(scrollregion=fullsize)  # scrollable area size

    rowpos = 0
    savephotos = []
    while thumbs:
        thumbsrow, thumbs = thumbs[:numcols], thumbs[numcols:]
        colpos = 0
        for (imgfile, imgobj) in thumbsrow:
            photo = PhotoImage(imgobj, master=win)
            link = Button(canvas, image=photo)
            handler = lambda savefile=imgfile: obj.ImageWindow(imgdir, savefile)
            link.config(command=handler, width=linksize, height=linksize)
            link.pack(side=LEFT, expand='yes')
            canvas.create_window(colpos, rowpos, anchor=NW,
                                 window=link, width=linksize, height=linksize)
            colpos += linksize
            savephotos.append(photo)
        rowpos += linksize
    return win, savephotos