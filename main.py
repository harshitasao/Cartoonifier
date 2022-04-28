# necessary imports
import cv2
import easygui
import numpy as np
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import *

# creating main window using tkinter
win = tk.Tk()
win.geometry('700x450')
win.title('Cartoonifier')
win.config(background='#041042')
label = Label(win, background='black', font=('poppins', '20', 'bold'))

# Creating filebox for user to select the image
def selector():
    imagePath = easygui.fileopenbox()
    if imagePath is None:
        print("Please select an image.")
    else:
        if imagePath.lower().endswith(('.png', '.jpg', '.jpeg')):
            cartoonify(imagePath)
        else:
            print("Please select an image with proper file format.")

#Function which takes image as argument and cartoonifies it
def cartoonify(imagePath):
    # read the image
    originalImage = cv2.imread(imagePath)
    height = np.size(originalImage, 1)
    width = np.size(originalImage, 0)
    # Converting image from RGB to BGR, as oencv takes image in BGR
    originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)

    # Confirming that image is choosen
    if originalImage is None:
        print("Cannot find the appropriate image ")
        sys.exit()

    resized1 = cv2.resize(originalImage, (height, width))

    # Converting to grayscale
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

    # Smoothening of the image
    smoothGrayImage = cv2.medianBlur(grayImage, 5)

    # Retrieving th edges of the image for cartoon effect
    getEdge = cv2.adaptiveThreshold(smoothGrayImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Appylying bilateral filter to remove noise and keep edge sharp
    colorImage = cv2.bilateralFilter(originalImage, 9, 400, 400)

    # Masking the edged image or BEAUTIFY image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    resized2 = cv2.resize(cartoonImage, (height, width))

    # Plotting all transitions
    images = [resized1, resized2]
    fig, axes = plt.subplots(1, 2, figsize=(6, 6), subplot_kw={'xticks': [], 'yticks': []}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    # Button code used for saving the output image
    saving = Button(win, text='Save the cartoonified image', command=lambda: saveImage(resized2, imagePath), padx=10, pady=5)
    saving.configure(background='#C39EFC', foreground='black', font=('poppins', '20', 'bold'))
    saving.pack(side=TOP, pady=30)
    plt.show()

# Adding functionality to save the image
def saveImage(resized2, imagePath):
    # Saving image using imwrite
    newName = "cartoonified_image"
    path1 = os.path.dirname(imagePath)
    extension = os.path.splitext(imagePath)[1]
    newPath = os.path.join(path1, newName + extension)
    cv2.imwrite(newPath, cv2.cvtColor(resized2, cv2.COLOR_RGB2BGR))
    messageShown = "Image is saved by name " + newName + "at " + newPath
    tk.messagebox.showinfo(title="Output", message=messageShown)

# Buttons shown in the tkinter window
upload = Button(win, text="Cartoonify Image", command=selector, padx=10, pady=5)
upload.configure(background='#C39EFC', foreground='black', font=('poppins', '20', 'bold'))

# message shown in tkinter window
message1 = Label(win, text="Make a cartoon version of your photo and use it as your new profile picture.")
message1.config(background='#EADFFC', font=("poppins", 14))

message2 = Label(win, text="Click on the button below and get started!")
message2.config(background='#EADFFC', font=("poppins", 14))

message3 = Label(win, text="Enter an image with the file types \".png .jpg and .jpeg\"")
message3.config(background='#EADFFC', font=("poppins", 14))

message1.pack(side=TOP,pady=(50,3))
message2.pack(side=TOP,pady=3)
message3.pack(side=TOP,pady=3)
upload.pack(side=TOP, pady=(40,10))

win.mainloop()
