from turtle import width
from fpdf import FPDF
from datetime import date
import tkinter 
from tkinter.constants import ANCHOR, NW
import PIL.Image,PIL.ImageTk
import cv2
from functools import partial
import threading
import imutils
title = 'Comapany Name'
SET_WIDTH = 366
SET_HEIGHT=768
window = tkinter.Tk()
window.title("Bill App")
window.geometry('900x500')
item_list=[]
item_list_main=[]
qty_list=[]
qty_list_main=[]
rate_list=[]
rate_list_main=[]
amount_list=[]
amount_list_main=[]
data_as_dict = {}
no_of_items = {"Number of items" : "" }
data_as_dict["Item name"] = []
data_as_dict["Qty"] = []
data_as_dict["Rate"] = []
data_as_dict["Amount"] = []
widget = []
No_Var=tkinter.IntVar()
Name_Var=tkinter.StringVar()

def print_item_name():
    num_of_items=No_Var.get()
    
    #--------------------Amount-------------------
    
    # label4 = tkinter.Label(window, text='')
    # label4.config(font=('helvetica', 10))
    # label4.grid(row=name_position,column=4,pady=20,padx=0)
    # for n in range(num_of_items):
    #     print(n)
    #     amount = int(rate_list[n].get())*int(qty_list[n].get())
    #     amount_list.append(str(amount))
    # for amount in amount_list:
    #     entry_list = entry_list + amount+'\n'
    #     label4.config(text = entry_list)
        
    
    for items in item_list:
        items_for_list = (str(items.get()))
        item_list_main.append(items_for_list)
    for qty in qty_list:
        qty_for_list = (str(qty.get()))
        qty_list_main.append(qty_for_list)
    for rate in rate_list:
        rate_for_list = (str(rate.get()))
        rate_list_main.append(rate_for_list)
    #--------------------Amount-------------------
    label6 = tkinter.Label(window, text=f'Amount')
    label6.config(font=('helvetica', 10))
    label6.grid(row=3,column=3,pady=20,padx=5)

    for i in range(num_of_items):   
        name_position = i+4
        amount = int(rate_list_main[i])*int(qty_list_main[i])
        amount_list.append(str(amount))
        entry5 = tkinter.Entry (window) 
        entry5.insert(0,amount)
        entry5.config(state= "disabled")
        entry5.grid(row=name_position,column=3,pady=20,padx=5)

    for amount in amount_list:
        amount_for_list = (str(amount))
        print(amount_for_list)
        amount_list_main.append(amount_for_list)
    data_as_dict = dict({"Item name": item_list_main,
                     "Qty":qty_list_main,
                     "Rate":rate_list_main,
                     "Amount":amount_list_main})
    print(data_as_dict)

def clear():
    pass

def name_take():
    num_of_items=No_Var.get()
    
    for i in range(num_of_items):
        
        name_position = i+4
        label3 = tkinter.Label(window, text=f'Name')
        label3.config(font=('helvetica', 10))
        label3.grid(row=3,column=0,pady=20,padx=5)
            
        entry3 = tkinter.Entry (window) 
        entry3.grid(row=name_position,column=0,pady=20,padx=5)
        item_list.append(entry3)
    
        #--------------Qty--------------------

        label4 = tkinter.Label(window, text=f'Qty')
        label4.config(font=('helvetica', 10))
        label4.grid(row=3,column=1,pady=20,padx=5)

        entry6 = tkinter.Entry (window) 
        entry6.insert(0,1)
        entry6.grid(row=name_position,column=1,pady=20,padx=5)
        qty_list.append(entry6)

        #--------------------Rate--------------------
        label5 = tkinter.Label(window, text=f'Rate')
        label5.config(font=('helvetica', 10))
        label5.grid(row=3,column=2,pady=20,padx=5)

        entry4 = tkinter.Entry (window) 
        entry4.insert(0,1)      
        entry4.grid(row=name_position,column=2,pady=20,padx=5)
        rate_list.append(entry4)

    
    btn1 = tkinter.Button(window,text="Done",width=10,command=print_item_name)
    btn1.grid(row=name_position,column=5,pady=20,padx=5)


   
    
# pdf = PDF()
# pdf.add_page()
# pdf.header('20,000 Leagues Under the Seas')  
# pdf.set_font("Times", size=10)
today = date.today()
d1 = today.strftime("%B %d, %Y")
# num_of_items = int(input('Enter the number of products\n'))
# cv_img = cv2.cvtColor(cv2.imread("welcome.png"),cv2.COLOR_BGR2RGB)
# canvas = tkinter.Canvas(window,width=SET_WIDTH,height=SET_HEIGHT)

# photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
# image_on_canavas= canvas.create_image(0,0, anchor=tkinter.NW,image=photo)

#--------------Your company--------------------
label = tkinter.Label(window, text='Your Company Name')
label.config(font=('helvetica', 10))
label.grid(row=0,column=0,pady=20,padx=5)

entry = tkinter.Entry (window) 
entry.insert(0,title)
entry.grid(row=0,column=1,pady=20,padx=5)


#--------------date--------------------
label1 = tkinter.Label(window, text='Date')
label1.config(font=('helvetica', 10))
label1.grid(row=1,column=0,pady=20,padx=5)

entry1 = tkinter.Entry (window) 
entry1.insert(0,d1)
entry1.grid(row=1,column=1,pady=20,padx=5)

#--------------No. products--------------------
label2 = tkinter.Label(window, text='Enter the number of products')
label2.config(font=('helvetica', 10))
label2.grid(row=2,column=0,pady=20,padx=5)

entry2 = tkinter.Entry (window,textvariable = No_Var) 
entry2.grid(row=2,column=1,pady=20,padx=5)

btn=tkinter.Button(window,text = 'Done', width = 10,command = name_take)
btn.grid(row=2,column=2,pady=20,padx=5)

btn2=tkinter.Button(window,text = 'Clear',width = 10)
btn2.grid(row=2,column=3,pady=20,padx=5) 



#--------------Qty--------------------

# label2 = tkinter.Label(window, text='Enter the quantity of products')
# label2.config(font=('helvetica', 10))
# canvas.create_window(100, 250, window=label2)

# entry2 = tkinter.Entry (window) 
# entry2.insert(0,1)
# canvas.create_window(250, 250, window=entry2,)
# # num_of_items = entry2.get()

# btn2 = tkinter.Button(window,text="Done",width=10,command=name_done_button)
# canvas.create_window(400, 250, window=btn2)







# sliced= item_name.split(',')
# for item in num_of_items:
#     data_as_dict.update({"Item name": [sliced[item]]})
# print(data_as_dict)

# def get_number_of_items():
#     for i in range(1, num_of_items + 1):
#             item_name = input(f'Enter name of product {i}\n')
#             item_list.append(item_name)


# for i in range(1, num_of_items + 1):
#         product_serial = i-1
#         rate = input(f'Enter rate of \'{item_list[product_serial]}\' \n')
#         rate_list.append(rate)

# for n in range(num_of_items):
#     amount = int(rate_list[n])*int(qty_list[n])
#     amount_list.append(str(amount))
# data_as_dict = dict({"Item name": item_list,
#                     "Qty":qty_list,
#                     "Rate":rate_list,
#                     "Amount":amount_list})
# print(data_as_dict)


# create_table(table_data = data_as_dict,title='', cell_width='even')
# pdf.ln()


# pdf.output('table_function.pdf')

# window.after(100,print_name_of_items(name_take()))
# window.attributes('-fullscreen', True)
window.mainloop()
# Need to create obejct as pdf