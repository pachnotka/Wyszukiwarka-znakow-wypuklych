# importowanie bibliotek
import tkinter
import tkinter as tk
from tkinter import filedialog
import cv2
import math
import os
import customtkinter
from PIL import Image

# wczytanie obrazu
def open_image():
    global image, iwidth, iheight
    # otwieranie obrazu za pomocą eksploratora
    imgpath = tk.filedialog.askopenfilename(initialdir=os.getcwd())
    if imgpath == "":
        return
    image = cv2.imread(imgpath)
    # odczytywanie wymiarów obrazu
    iheight, iwidth, _ = image.shape

    # zmiana rozmiaru wyświetlanego obrazu tak, aby mieścił się w ramce
    if iwidth > fsize:
        imageratio = fsize / (iwidth - 20)
        iwidth = fsize - 40
        iheight = iheight * imageratio
    elif iheight > fsize:
        imageratio = fsize / (iheight - 20)
        iwidth = iwidth * imageratio - 20
        iheight = fsize

    img = customtkinter.CTkImage(light_image=Image.open(imgpath),
                                  dark_image=Image.open(imgpath),
                                  size=(iwidth, iheight))
    # usunięcie wcześniejszego obrazu i obrazu wynikowego
    for widget in frame.winfo_children():
        widget.destroy()
    for widget in frameresult.winfo_children():
        widget.destroy()
    # umieszczenie wczytanego obrazu w widocznej części programu po lewej stronie
    limage1 = customtkinter.CTkLabel(master=frame, text="", image=img)
    limage1.pack(padx=20, pady=20, fill=tkinter.BOTH, expand=True)

# zmiana koloru ramki
def change_color(new_color):
    global framecolor
    framecolor = new_color

# zmiana grubości ramki
def change_thickness(new_thickness):
    global thickness
    thickness = new_thickness

# znajdowanie wypukłości i rysowanie ramek
def convex():
    global image, iwidth, iheight, framecolor, imgCont, thickness
    # kopiowanie oryginalnego obrazu
    imgCont = image.copy()
    imgFinal = image.copy()

    # pobranie wymiarów obrazu
    iheight2, iwidth2, _ = image.shape

    # konwersja obrazu z RGB na skalę szarości
    imggray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("szary.png", imggray)
    # detekcja krawędzi za pomocą algorytmu Canny
    imgcanny = cv2.Canny(imggray, 200, 240)
    cv2.imwrite("canny.png", imgcanny)
    # znalezienie konturów
    contours, _ = cv2.findContours(imgcanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # utworzenie pustej listy na wymiary ramek
    rect_d = []
    # wzór na rozmiar minimalnego elementu który zostanie umieszczony w ramce
    min_cont_area = math.log((iheight2 * iwidth2)) * 8
    i = 0

    for cnt in contours:
        i += 1
        # ograniczenie liczby konturów
        if cv2.contourArea(cnt) > min_cont_area:
            # określenie i zapisanie wymiarów ramek
            box_d = cv2.boundingRect(cnt)
            x, y, w, h = box_d
            rect_d.append([x, y, w, h])
            # wyliczenie wypukłości konturu
            hull = cv2.convexHull(cnt)
            if cv2.contourArea(hull) != 0:
                convex = cv2.contourArea(cnt) / cv2.contourArea(hull)
            # ograniczenie konturów do wypukłych
            if convex > 0.65 and w > iwidth2 / 100 and h > iheight2 / 100:
                # rysowanie ramki
                cv2.rectangle(imgCont, (x, y), (x + w, y + h), framecolor, thickness)



    imgCont2 = cv2.cvtColor(imgCont, cv2.COLOR_BGR2RGB)
    imgCont2 = Image.fromarray(imgCont2)

    img = customtkinter.CTkImage(light_image=imgCont2,
                                 dark_image=imgCont2,
                                 size=(iwidth, iheight))
    # usunięcie wszystkich elementów z frame
    for widget in frameresult.winfo_children():
        widget.destroy()
    # umieszczenie obrazu z ramkami w widocznej części programu po prawej stronie
    limage2 = customtkinter.CTkLabel(master=frameresult, text="", image=img)
    limage2.pack(padx=20, pady=20, fill=tkinter.BOTH, expand=True)

# zapisywanie obrazu do pliku
def saveimg():
    global imgCont
    result = filedialog.asksaveasfilename(
        title="Zapisz plik",
        filetypes=(
            ("JPEG", ("*.jpg", "*.jpeg", "*.jpe")),
            ("PNG", "*.png"),
            ("BMP", ("*.bmp", "*.jdib")),
        ),
        defaultextension="*.png",
    )
    cv2.imwrite(result, imgCont)

#ustawienia gui
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.geometry("1400x600")
app.title("Symbole wypukłe")

# ramki lewa i prawa
fsize = 550
frame = customtkinter.CTkFrame(master=app,
                               width=fsize,
                               height=fsize,
                               corner_radius=10)
frame.pack(padx=20, pady=20, side="left", fill="both", expand=False)

frameresult = customtkinter.CTkFrame(master=app,
                               width=fsize,
                               height=fsize,
                               corner_radius=10)
frameresult.pack(padx=20, pady=20, side="right", fill="both", expand=False)

# tekst proszący o wybór opcji
labelcolors = customtkinter.CTkLabel(master=app,
                               text="Wybierz kolor i grubość ramek:",
                               width=120,
                               height=25,
                               fg_color=("white", "gray75"),
                               corner_radius=8)
labelcolors.pack(anchor="center",pady=10)

# guziki wyboru koloru ramek
var = tk.IntVar()
red_button = customtkinter.CTkRadioButton(master=app, fg_color="#e40000", hover_color="#fd4848", text="Czerwony", variable=var, value=1, command=lambda: change_color((0,0,255)))
green_button = customtkinter.CTkRadioButton(master=app, fg_color="#00e400", hover_color="#48fd48", text="Zielony", variable=var, value=2, command=lambda: change_color((0,255,0)))
blue_button = customtkinter.CTkRadioButton(master=app, fg_color="#0000e4", hover_color="#4848fd", text="Niebieski", variable=var, value=3, command=lambda: change_color((255,0,0)))

red_button.pack(anchor="w",padx = 20)
green_button.pack(anchor="w",padx = 20)
blue_button.pack(anchor="w",padx = 20)

# guziki wyboru grubości ramek
var2 = tk.IntVar()
px2_button = customtkinter.CTkRadioButton(master=app, text="2 px", variable=var2, value=1, command=lambda: change_thickness(2))
px4_button = customtkinter.CTkRadioButton(master=app, text="4 px ", variable=var2, value=2, command=lambda: change_thickness(4))
px8_button = customtkinter.CTkRadioButton(master=app, text="8 px", variable=var2, value=3, command=lambda: change_thickness(8))

px2_button.place(x=730,y=46)
px4_button.place(x=730,y=68)
px8_button.place(x=730,y=90)

# duże przyciski
bopen = customtkinter.CTkButton(master=app, text="Otwórz obraz", command=open_image)
bopen.pack(padx=20,ipady=40, pady=30, anchor="s")

buttonob = customtkinter.CTkButton(master=app, text="Znajdź \nwybrzuszenia", command=convex)
buttonob.pack(padx=20, ipady=40, pady=30, anchor="s")

bmain = customtkinter.CTkButton(master=app, text="Zapisz obraz \nwynikowy", command=saveimg)
bmain.pack(padx=20,ipady=40, pady=30, anchor="s")

app.resizable(False, False)
app.mainloop()