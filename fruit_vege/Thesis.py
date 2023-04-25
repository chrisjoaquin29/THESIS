import tkinter as tk
import tkinter.font as tkfont
from PIL import ImageTk, Image
import cv2
import numpy as np
from keras.models import load_model
import pandas as pd
import sys
import qrcode

EMULATE_HX711=False

# if not EMULATE_HX711:
#     import RPi.GPIO as GPIO
#     from hx711py.hx711 import HX711
# else:
#     from hx711py.emulated_hx711 import HX711
# ===================================================
# set up main window
root = tk.Tk()
root.geometry('1366x768')
root.title('The Advanced Calorie Counter')

# tkfont.nametofont("TkDefaultFont").configure(family="song ti",size=20)
# print("\n", tkfont.Font().actual(), "\n")

# set size variables
root_width = 1366
root_height = 768
# ===================================================
# load model and labels
model = load_model('fruit_veggies.h5')

labels = ['Calmansi', 'Cucumber', 'Apple', 'Banana', 'Lettuce', 'Tomato', 'Ampalaya',
          'Eggplant', 'Lemon', 'Carrot', 'Kiwi', 'Mango', 'Orange', 'Pechay',
          'Bell pepper']
# ===================================================
# # open csv file using pandas
# fruits = pd.read_csv('Fruits_Details.csv')
# vegies = pd.read_csv('Vegetables_Details.csv')
# items = pd.concat([fruits,vegies])
# items = items.reset_index(drop=True)
# print(items)
# # save items to csv file
# items.to_csv('Items_Details.csv', index=False)
items = pd.read_csv('Items_Details.csv')
print(items.columns)
# ===================================================
# setup weight environment
base_weight = 100
weight = 200
# referenceUnit = 1
# hx = HX711(5, 6)
# hx.set_reading_format("MSB", "MSB")
# hx.set_reference_unit(referenceUnit)
# hx.reset()
# hx.tare()
# print("Tare done! Add weight now...")
# ===================================================
# Calculated list of Energy Factors
eng_list = []
final_image = None
# ===================================================

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()


def calculate_weight():
    global weight
    weight = hx.get_weight(5)
    print(weight)
    hx.power_down()
    hx.power_up()
    return weight


def bttn(x, y, img1, img2, cmd):
    image_a = ImageTk. PhotoImage(Image.open(img1))
    image_b = ImageTk. PhotoImage(Image.open(img2))

    def on_enter(e):
        mybtn['image'] = image_b

    def on_leave(e):
        mybtn['image'] = image_a

    mybtn = tk.Button(main_frame, image=image_b, border=0,
                      cursor='hand2', command=cmd)

    mybtn.bind("<Enter>", on_enter)
    mybtn.bind("<Leave>", on_leave)
    mybtn.place(relx=x, rely=y, anchor='center')


def button(x, y, img1, img2, window, cmd):
    image_a = ImageTk. PhotoImage(Image.open(img1))
    image_b = ImageTk. PhotoImage(Image.open(img2))

    def on_enter(e):
        mybtn['image'] = image_b

    def on_leave(e):
        mybtn['image'] = image_a

    mybtn = tk.Button(window, image=image_b, border=0,
                      cursor='hand2', command=cmd)

    mybtn.bind("<Enter>", on_enter)
    mybtn.bind("<Leave>", on_leave)
    mybtn.place(x=x, y=y)
    return mybtn


def create_popup():
    # Display camera stream in a label
    lmain = tk.Label(main_frame, bg='#c3c3c3')
    lmain.pack()
    lmain.place(relx=0.5, rely=0.5, anchor='center')
    # Capture video frames
    cap = cv2.VideoCapture(0)
    # Function for video streaming

    def show_frame():
        ret, frame = cap.read()
        if ret:
            # resize the frame to have a maximum width of 300 pixels
            # print(frame.shape)
            frame = cv2.resize(frame, (920, 690))
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)
    show_frame()
    # Stop video

    def stop():
        cap.release()
        output_screen()
        # capture_window.destroy()
        # root.destroy()

    # Buttons to control streaming
    popup_button = tk.Button(main_frame, command=bttn(
        0.5, 0.9, "Images and Buttons/Buttons/CAPTURE (Not yet click).png",
        "Images and Buttons/Buttons/CAPTURE (Not yet click).png", stop))
    popup_button.pack()


def output_screen():
    # delete_pages()
    global final_image
    eng_list.clear()
    cap = cv2.VideoCapture(0)
    _, imag = cap.read()
    # Predict the image
    name = model_predict(imag)
    eng_list.append(name)
    final_image = imag.copy()
    disp_frame = cv2.resize(imag, (800, 600))
    cv2image = cv2.cvtColor(disp_frame, cv2.COLOR_BGR2RGBA)
    image = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=image)
    # Display camera stream in a label
    lpic = tk.Label(main_frame, bg='#c3c3c3',
                    height=root_height, width=root_width, anchor='nw')
    lpic.imgtk = imgtk
    lpic.configure(image=imgtk)
    lpic.place(x=0, y=0)

    lcal = tk.Label(main_frame, text="Name:",
                    font=('Bold', 30), bg='#c3c3c3')
    lcal.place(x=900, y=50)
    lcal = tk.Label(main_frame, text="Weight:",
                    font=('Bold', 20), bg='#c3c3c3')
    lcal.place(x=900, y=150)
    lcal = tk.Label(main_frame, text="Calories:",
                    font=('Bold', 20), bg='#c3c3c3')
    lcal.place(x=900, y=200)
    lcal = tk.Label(main_frame, text="Carb:",
                    font=('Bold', 20), bg='#c3c3c3')
    lcal.place(x=900, y=250)
    lcal = tk.Label(main_frame, text="Fat:",
                    font=('Bold', 20), bg='#c3c3c3')
    lcal.place(x=900, y=300)
    lcal = tk.Label(main_frame, text="Protein:",
                    font=('Bold', 20), bg='#c3c3c3')
    lcal.place(x=900, y=350)
    # Caclulate weight
    # weight = calculate_weight()
    eng_list.append(str(weight))
    # find row of food using name
    row = items.loc[items['NAME'] == eng_list[0]]
    # print("Row: ", row)
    # get CALORIES (kcal) of food
    # print(row['CALORIES (kcal)'].values[0])
    ratio = int(eng_list[1]) / base_weight
    eng_list.append(str(row['CALORIES (kcal)'].values[0] * ratio))
    eng_list.append(str(row['CARBOHYDRATES'].values[0] * ratio))
    eng_list.append(str(row['FATS'].values[0] * ratio))
    eng_list.append(str(row['PROTEIN'].values[0] * ratio))

    lcal = tk.Label(main_frame, text=eng_list[0],
                    font=('Bold', 30), bg='#c3c3c3')
    lcal.place(x=1100, y=50)
    lcal = tk.Label(main_frame, text=eng_list[1],
                    font=('Bold', 20), bg='#c3c3c3')
    lcal.place(x=1100, y=150)
    lcal = tk.Label(main_frame, text=eng_list[2],
                    font=('Bold', 20), bg='#c3c3c3')
    lcal.place(x=1100, y=200)
    lcal = tk.Label(main_frame, text=eng_list[3],
                    font=('Bold', 20), bg='#c3c3c3')
    lcal.place(x=1100, y=250)
    lcal = tk.Label(main_frame, text=eng_list[4],
                    font=('Bold', 20), bg='#c3c3c3')
    lcal.place(x=1100, y=300)
    lcal = tk.Label(main_frame, text=eng_list[5],
                    font=('Bold', 20), bg='#c3c3c3')
    lcal.place(x=1100, y=350)

    popup_button = tk.Button(main_frame, command=bttn(
        0.3, 0.9, "Images and Buttons/Buttons/SAVE (Not yet click).png",
        "Images and Buttons/Buttons/SAVE (Not yet click).png", save))
    popup_button.pack()
    popup_button = tk.Button(main_frame, command=bttn(
        0.7, 0.9, "Images and Buttons/Buttons/EXIT (Not yet click).png",
        "Images and Buttons/Buttons/EXIT (Not yet click).png", main_page))
    popup_button.pack()


def model_predict(frame):
    img = cv2.resize(frame, (224, 224))
    img = img/255
    img = np.expand_dims(img, [0])
    answer = model.predict(img)
    y_class = answer.argmax(axis=-1)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    # print("\n", res, "\n")
    return res


def save():
    global final_image
    # generate a qr code wit final_image and eng_list information
    # concatenate the image and values into a single string
    cv2.imwrite("temp.png", final_image)
    final_image = cv2.imread("temp.png")
    # final_image = cv2.resize(final_image, (100, 100))
    # data = "{}|{}".format(final_image.tobytes(), ",".join(eng_list))
    data = "{}".format(",".join(eng_list))
    print(data)
    print(len(data))
    # create a QR code with the data
    qr = qrcode.QRCode(version=2, box_size=10, border=3, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(data, optimize=0)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # display the QR code on the tkinter window
    imgqr = ImageTk.PhotoImage(img)
    qr_label = tk.Label(main_frame, bg='#c3c3c3', 
                        height=root_height, width=root_width, anchor='center')
    qr_label.imgtk = imgqr
    qr_label.configure(image=imgqr)
    qr_label.place(x=0, y=0)

    popup_button = tk.Button(main_frame, command=bttn(
        0.5, 0.9, "Images and Buttons/Buttons/EXIT (Not yet click).png",
        "Images and Buttons/Buttons/EXIT (Not yet click).png", main_page))
    popup_button.pack()
    print("Saved")


def main_page():
    delete_pages()
    global img4
    img4 = tk.PhotoImage(
        file="Images and Buttons/Images/1 HOME 2 ABOUT 3 USER GUIDE/HOME.png")
    lb = tk.Label(main_frame, image=img4, font=('Bold,30'))
    lb.pack(side='top', fill='both', expand=True)
    menu()


def home_page():
    delete_pages()
    global img
    img = tk.PhotoImage(
        file="Images and Buttons/Images/1 HOME 2 ABOUT 3 USER GUIDE/HOME.png")
    lb = tk.Label(main_frame, image=img, font=('Bold,30'))
    lb.pack(side='top', fill='both', expand=True)
    popup_button = tk.Button(main_frame, command=bttn(
        0.5, 0.9, "Images and Buttons/Buttons/LAST1.png",
        "Images and Buttons/Buttons/LAST1.png", create_popup))
    popup_button.pack()


def userg_page():
    delete_pages()
    global img2
    img2 = tk.PhotoImage(
        file="Images and Buttons/Images/1 HOME 2 ABOUT 3 USER GUIDE/USER GUIDE.png")
    lb = tk.Label(main_frame, text='User Guide Page\n\nPage: 2',
                  image=img2, font=('Bold,30'))
    lb .pack(fill='both', expand=True)
    menu()


def about_page():
    delete_pages()
    global img3
    img3 = tk.PhotoImage(
        file="Images and Buttons/Images/1 HOME 2 ABOUT 3 USER GUIDE/ABOUT.png")
    lb = tk.Label(main_frame, text='About Page\n\nPage: 3',
                  image=img3, font=('Bold,30'))
    lb.pack(fill='both', expand=True)
    menu()


def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()


def menu():
    # place home button
    home_btn = tk.Button(main_frame, text='HOME', font=('Arial', 10), fg='#020203',
                         bd=0, bg='#c3c3c3', command=home_page)
    home_btn.place(relx=0.0, rely=0.25, relheight=0.15,
                   relwidth=0.1, bordermode="outside")
    # place user guide button
    userg_btn = tk.Button(main_frame, text='USER GUIDE', font=(
        'Segoe Script', 10), fg='#020203', bd=0, bg='#c3c3c3', command=userg_page)
    userg_btn.place(relx=0.0, rely=0.425, relheight=0.15,
                    relwidth=0.1, bordermode="outside")
    # place about button
    about_btn = tk.Button(main_frame, text='ABOUT ACC', font=(
        'Bold', 10), fg='#020203', bd=0, bg='#c3c3c3', command=about_page)
    about_btn.place(relx=0.0, rely=0.6, relheight=0.15,
                    relwidth=0.1, bordermode="outside")


# starting main screen code here
options_frame = tk.Frame(root, bg='#939393')
bg = Image.open(
    'Images and Buttons/Images/1 HOME 2 ABOUT 3 USER GUIDE/HOME.png')
converted_image = ImageTk.PhotoImage(bg)
main_frame = tk.Label(root, image=converted_image)
main_frame.pack(side=tk.LEFT)
main_frame.pack_propagate(False)
menu()


root.mainloop()
