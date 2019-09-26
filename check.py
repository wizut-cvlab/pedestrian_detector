import os
import glob
from tkinter import *
import json
import csv

from PIL import Image, ImageTk

rootdir = "C:\\Users\\asmolinski\\Desktop\\maruda\\"


class myGUI:
    def __init__(self, master):
        # main frame
        self.parent = master
        self.parent.title("Checking tool")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width=True, height=True)

        # variables
        self.cur = 0
        self.total = 0
        self.red = StringVar()
        self.red.set(0)
        self.green = StringVar()
        self.green.set(0)
        self.red_wrong = StringVar()
        self.red_wrong.set(0)
        self.green_wrong = StringVar()
        self.green_wrong.set(0)
        self.peop = StringVar()
        self.imageList = []
        self.imageDir = ""
        self.iou = StringVar()
        self.red.set(0)
        self.pictures = []

        # GUI stuff

        # chosing folder
        self.label = Label(self.frame, text="Image Dir:")
        self.label.grid(row=0, column=0, sticky=E)
        self.entry = Entry(self.frame)
        self.entry.insert(0, "test1\\t01")
        self.entry.grid(row=0, column=1, sticky=W + E)
        self.ldBtn = Button(self.frame, text="Load", command=self.loadDir)
        self.ldBtn.grid(row=0, column=2, sticky=W + E)

        # Image
        self.mainPanel = Canvas(self.frame, cursor="tcross")
        self.parent.bind("a", self.prevImage)  # press 'a' to go backforward
        self.parent.bind("d", self.nextImage)  # press 'd' to go forward
        self.mainPanel.grid(row=1, column=1, sticky=W + N)

        # control panel for image navigation
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row=2, column=1, columnspan=2, sticky=W + E)
        self.prevBtn = Button(
            self.ctrPanel, text="<< Prev", width=10, command=self.prevImage
        )
        self.prevBtn.pack(side=LEFT, padx=5, pady=3)
        self.nextBtn = Button(
            self.ctrPanel, text="Next >>", width=10, command=self.nextImage
        )
        self.nextBtn.pack(side=LEFT, padx=5, pady=3)
        self.progLabel = Label(self.ctrPanel, text="Progress:     /    ")
        self.progLabel.pack(side=LEFT, padx=5)
        self.tmpLabel = Label(self.ctrPanel, text="Go to Image No.")
        self.tmpLabel.pack(side=LEFT, padx=5)
        self.idxEntry = Entry(self.ctrPanel, width=5)
        self.idxEntry.pack(side=LEFT)
        self.goBtn = Button(self.ctrPanel, text="Go", command=self.gotoImage)
        self.goBtn.pack(side=LEFT)

        # showing bbox info & delete bbox
        self.detect = Frame(self.frame)
        self.detect.grid(row=1, column=2, sticky=N + W + E)
        self.lb1 = Label(self.detect, text="Objects on picture:")
        self.lb1.grid(row=0, column=1, sticky=W + N)
        self.label2 = Label(self.detect, text="People")
        self.label2.grid(row=2, column=1, sticky=N)
        self.people = Entry(self.detect, textvariable=self.peop)
        # self.people.insert(0,"0")
        self.people.grid(row=2, column=2, sticky=N)
        self.lb3 = Label(self.detect, text="Wrong detection:")
        self.lb3.grid(row=4, column=1, sticky=W + N)

        self.label3 = Label(self.detect, text="Red label")
        self.label3.grid(row=5, column=1, sticky=N)
        self.redlab2 = Entry(self.detect, textvariable=self.red_wrong)
        self.redlab2.grid(row=5, column=2, sticky=N)

        self.label4 = Label(self.detect, text="Green label")
        self.label4.grid(row=6, column=1, sticky=N)
        self.greenlab2 = Entry(self.detect, textvariable=self.green_wrong)
        self.greenlab2.grid(row=6, column=2, sticky=N)

        self.label7 = Label(self.detect, text="Green:")
        self.label7.grid(row=7, column=1, sticky=N)
        self.but1 = Button(self.detect, text="+", width=5, command=self.green_add)
        self.but1.grid(row=8, column=1, sticky=N)
        self.but2 = Button(self.detect, text="-", width=5, command=self.green_sub)
        self.but2.grid(row=9, column=1, sticky=N)

        self.label8 = Label(self.detect, text="Red:")
        self.label8.grid(row=7, column=2, sticky=N)
        self.but3 = Button(self.detect, text="+", width=5, command=self.red_add)
        self.but3.grid(row=8, column=2, sticky=N)
        self.but4 = Button(self.detect, text="-", width=5, command=self.red_sub)
        self.but4.grid(row=9, column=2, sticky=N)

        self.lb3 = Label(self.detect, text="Correct detection:")
        self.lb3.grid(row=11, column=1, sticky=W + N)

        self.label5 = Label(self.detect, text="Red label")
        self.label5.grid(row=12, column=1, sticky=N)
        self.redlab = Entry(self.detect, textvariable=self.red)
        self.redlab.grid(row=12, column=2, sticky=N)

        self.label6 = Label(self.detect, text="Green label")
        self.label6.grid(row=13, column=1, sticky=N)
        self.greenlab = Entry(self.detect, textvariable=self.green)
        self.greenlab.grid(row=13, column=2, sticky=N)

        self.lb4 = Label(self.detect, text="Avr. IOU")
        self.lb4.grid(row=15, column=1, sticky=W + N)
        self.lb5 = Label(self.detect, textvariable=self.iou)
        self.lb5.grid(row=15, column=2, sticky=W + N)

    def loadDir(self):
        s = self.entry.get()
        self.parent.focus()
        self.imageList = []
        self.pictures = []

        self.imageDir = os.path.join(rootdir + s)
        extensions = ("*.jpg", "*.jpeg", "*.png")
        for extension in extensions:
            self.imageList.extend(glob.glob(os.path.join(self.imageDir, extension)))
        if len(self.imageList) == 0:
            print("No .JPEG images found in the specified dir!")
            return
        self.cur = 1
        self.total = len(self.imageList)
        self.loadImage()
        if os.path.isfile(self.imageDir + ".csv"):
            csv_file = csv.reader(open(self.imageDir + ".csv", "r"), delimiter=",")
            self.pictures = list(csv_file)
        else:
            # dodanie nagłówków do pliku
            writer = csv.writer(open(self.imageDir + ".csv", "w", newline=""))
            self.pictures = [
                [
                    "Nazwa pliku",
                    "Postaci",
                    "Błedy Kaskady",
                    "Błędy CNN",
                    "Wykryte Kaskadą",
                    "Wykryte CNN",
                    "IOU",
                ]
            ]
            writer.writerows(self.pictures)

        print("%d images loaded from %s" % (self.total, s))

    def gotoImage(self):
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= self.total:
            self.saveImage()
            self.cur = idx
            self.loadImage()

    def prevImage(self):
        self.saveImage()
        if self.cur > 1:
            self.cur -= 1
            self.loadImage()

    def nextImage(self):
        self.saveImage()
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()

    def green_add(self):
        self.green.set(
            (int(self.green.get()) - 1) if (int(self.green.get()) - 1) > 0 else 0
        )
        self.green_wrong.set(int(self.green_wrong.get()) + 1)

    def red_add(self):
        self.red.set((int(self.red.get()) - 1) if (int(self.red.get()) - 1) > 0 else 0)
        self.red_wrong.set(int(self.red_wrong.get()) + 1)

    def green_sub(self):
        self.green_wrong.set(
            (int(self.green_wrong.get()) - 1)
            if (int(self.green_wrong.get()) - 1) > 0
            else 0
        )
        self.green.set(int(self.green.get()) + 1)

    def red_sub(self):
        self.red_wrong.set(
            (int(self.red_wrong.get()) - 1)
            if (int(self.red_wrong.get()) - 1) > 0
            else 0
        )
        self.red.set(int(self.red.get()) + 1)

    def saveImage(self):
        row = [
            self.imagepath,
            self.people.get(),
            self.red_wrong.get(),
            self.green_wrong.get(),
            self.red.get(),
            self.green.get(),
            self.iou.get(),
        ]
        change = False

        if len(self.pictures) > 0:
            for pic in self.pictures:
                if pic[0] == self.imagepath:
                    index = self.pictures.index(pic)
                    self.pictures[index][1] = self.people.get()
                    self.pictures[index][2] = self.red_wrong.get()
                    self.pictures[index][3] = self.green_wrong.get()
                    self.pictures[index][4] = self.red.get()
                    self.pictures[index][5] = self.green.get()
                    change = True
            if change != True:
                self.pictures.append(row)
        else:
            self.pictures.append(row)
        writer = csv.writer(open(self.imageDir + ".csv", "w", newline=""))
        writer.writerows(self.pictures)

    def loadImage(self):
        # load image
        self.imagepath = self.imageList[self.cur - 1]
        self.img = Image.open(self.imagepath)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.config(
            width=max(self.tkimg.width(), 400), height=max(self.tkimg.height(), 400)
        )
        self.mainPanel.create_image(0, 0, image=self.tkimg, anchor=NW)
        self.progLabel.config(text="%04d/%04d" % (self.cur, self.total))
        self.green_wrong.set(0)
        self.red_wrong.set(0)

        # green labels
        data_green = {}
        file = (
            self.imagepath.replace(self.entry.get(), self.entry.get() + "\out")
            .replace(".jpg", ".json")
            .replace(".png", ".json")
            .replace(".PNG", ".json")
        )
        with open(file) as json_file:
            data_green = json.load(json_file)
            self.green.set(len(data_green))
            for detect in data_green:
                self.mainPanel.create_rectangle(
                    detect["topleft"]["x"],
                    detect["topleft"]["y"],
                    detect["bottomright"]["x"],
                    detect["bottomright"]["y"],
                    width=2,
                    outline="green",
                )

        # red labels
        data_red = {}
        file = (
            self.imagepath.replace(".jpg", ".json")
            .replace(".png", ".json")
            .replace(".PNG", ".json")
        )
        with open(file) as json_file:
            data_red = json.load(json_file)
            self.red.set(len(data_red))
            for detect in data_red:
                self.mainPanel.create_rectangle(
                    detect["topleft"]["x"],
                    detect["topleft"]["y"],
                    detect["bottomright"]["x"],
                    detect["bottomright"]["y"],
                    width=2,
                    outline="red",
                )

        # IOU calc
        self.iou.set("")

        if len(data_red) > len(data_green):
            sm_data = data_green
            bg_data = data_red
        else:
            sm_data = data_red
            bg_data = data_green

        iou_sum = 0
        for ob1 in sm_data:
            max_iou = 0
            for ob2 in bg_data:
                iou = 0
                # POLICZYĆ IOU ob1 i ob2
                # determine the (x, y)-coordinates of the intersection rectangle
                xA = max(ob1["topleft"]["x"], ob2["topleft"]["x"])
                yA = max(ob1["topleft"]["y"], ob2["topleft"]["y"])
                xB = min(ob1["bottomright"]["x"], ob2["bottomright"]["x"])
                yB = min(ob1["bottomright"]["y"], ob2["bottomright"]["y"])

                # compute the area of intersection rectangle
                interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

                # compute the area of both the prediction and ground-truth
                # rectangles
                boxAArea = (ob1["bottomright"]["x"] - ob1["topleft"]["x"] + 1) * (
                    ob1["bottomright"]["y"] - ob1["topleft"]["y"] + 1
                )
                boxBArea = (ob2["bottomright"]["x"] - ob2["topleft"]["x"] + 1) * (
                    ob2["bottomright"]["y"] - ob2["topleft"]["y"] + 1
                )

                # compute the intersection over union by taking the intersection
                # area and dividing it by the sum of prediction + ground-truth
                # areas - the interesection area
                iou = interArea / float(boxAArea + boxBArea - interArea)

                if iou > max_iou:
                    max_iou = iou

            iou_sum = iou_sum + max_iou
        if len(sm_data) > 0:
            self.iou.set(iou_sum / len(sm_data))


root = Tk()
tool = myGUI(root)
root.mainloop()
