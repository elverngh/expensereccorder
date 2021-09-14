from _ast import Lambda
from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime

GUI = Tk()
GUI.title('โปรแกรมคำนวณค่าใช้จ่าย')
GUI.geometry('720x700+500+50')

###############MENU####################
menubar = Menu(GUI)
GUI.config(menu=menubar)

# File menu
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label= 'Export to Google sheet')

# Help
def About():
    messagebox.showinfo('About', 'สวัสดีครับ โปรแกรมนี้คือโปรแกรมบันทึกข้อมูล\nสนใจบริจาคเราไหม? ขอ 1 BTC \nBTC Address: abc')

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About', command=About)

# Donate
donatemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Donate', menu=donatemenu)
#####################################



Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)  # width=400,height=400
T2 = Frame(Tab)  # width=400
Tab.pack(fill=BOTH, expand=1)

icon_t1 = PhotoImage(file='T1_expense.png')  # .subsample(2) ย่อรูป
icon_t2 = PhotoImage(file='T2_list.png')

Tab.add(T1, text=f'{"ค่าใช้จ่าย":^{30}}', image=icon_t1, compound='left')
Tab.add(T2, text=f'{"ค่าใข้จ่ายทั้งหมด":^{30}}', image=icon_t2, compound='left')

F1 = Frame(T1)
# F1.place(x=100,y=50)
F1.pack()

days = {'Mon': 'จันทร์',
        'Tue': 'อังคาร',
        'Wed': 'พุธ',
        'Thu': 'พฤหัสบดี',
        'Fri': 'ศุกร์',
        'Sat': 'เสาร์',
        'Sun': 'อาทิตย์'}


def Save(event=None):
    expense = v_expense.get()
    price = v_price.get()
    quantity = v_quantity.get()

    if expense == '':
        print('No Data')
        messagebox.showwarning('Error', 'อิดอก! กรอกข้อมูลให้ครบ')
        return
    elif price == '':
        messagebox.showwarning('Error', 'ราคาไม่ใส่กุจะคำนวณยังไงเล่า')
        return
    elif quantity == '':
        quantity = 1

    total = float(price) * float(quantity)
    try:
        total = float(price) * float(quantity)
        print('รายการ: {} ราคา: {}'.format(expense, price))
        print('จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity, total))
        text = 'รายการ: {} ราคา: {} บาท\n'.format(expense, price)
        text = text + 'จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity, total)
        # clear old data
        v_result.set(text)
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')

        # บันทึกข้อมูลลง csv อย่าลืม import csv ด้วย
        today = datetime.now().strftime('%a') # days['Mon'] = จันทร์
        print(today)
        stamp = datetime.now()
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        transactionid = stamp.strftime('%Y%m%d%H%M%f')
        dt = days[today] + '-' + dt
        with open('HWep5.csv', 'a', encoding='utf-8', newline='') as f:
            # with คือสั่งเปิดไฟล์แล้วปิดไฟล์อัติโนมัติ
            # 'a' การบันทึกไปเรื่อย ๆ เพิ่มข้อมูลต่อจากตัวเก่า
            # newline='' ทำให้ข้อมูลไม่มีบรรทัดว่าง
            fw = csv.writer(f) # สร้างฟังก์ชั่นสำหรับเขียนข้อมูล
            data = [transactionid, dt, expense, price, quantity, total]
            fw.writerow(data)

        # ให้cursor กลับไปอยู่ตำแหน่งช่องกรอก E1
        E1.focus()
        update_table()
    except:
        print('ERROR')
        # messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกข้อมูลผิด')
        messagebox.showwarning('Error', 'กรุณากรอกข้อมูลใหม่ คุณกรอกข้อมูลผิด')
        # messagebox.showinfo('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกข้อมูลผิด')
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')


GUI.bind('<Return>', Save)

FONT1 = (None, 20)

# -------Image------

main_icon = PhotoImage(file='mainicon.png')

Mainicon = Label(F1, image=main_icon)
Mainicon.pack()
# --------taxt1---------
L = Label(F1, text='รายการค่าใช้จ่าย', font=FONT1).pack()
v_expense = StringVar()
E1 = Entry(F1, textvariable=v_expense, font=FONT1)
E1.pack()
# ----------------------

# --------taxt2---------
L = Label(F1, text='ราคา', font=FONT1).pack()
v_price = StringVar()
E2 = Entry(F1, textvariable=v_price, font=FONT1)
E2.pack()
# ----------------------


# --------taxt3---------
L = Label(F1, text='จำนวน', font=FONT1).pack()
v_quantity = StringVar()
E3 = Entry(F1, textvariable=v_quantity, font=FONT1)
E3.pack()
# ----------------------

icon_b1 = PhotoImage(file='b1_button.png')

B2 = ttk.Button(F1, text=f'{"Save": >{10}}', image=icon_b1, compound='left', command=Save)
B2.pack(ipadx=20, ipady=20, pady=20)

v_result = StringVar()
v_result.set('------ผลลัพธ์-------')
result = Label(F1, textvariable=v_result, font=FONT1, fg='green')
# result = ttk.Label(F1, textvariable=v_result, font=FONT1,foreground='green')
result.pack(pady=20)


#################### TAB2 #################


def read_csv():
    with open('HWep5.csv', newline='', encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
    return data


# table

L = Label(T2, text='ตารางแสดงผลลัพธ์ทั้งหมด', font=FONT1).pack(pady=20)
header = ['รหัสรายการ','วัน-เวลา', 'รายการ', 'ค่าใช้จ่าย', 'จำนวน', 'รวม']
resulttable = ttk.Treeview(T2, columns=header, show='headings', height=10)
resulttable.pack()

# for i in range(len(header)):
#     resulttable.heading(header[i], text=header[i])

for h in header:
    resulttable.heading(h, text=h)

headerwidth = [170, 150, 130, 70, 70, 70]
for h, w in zip(header, headerwidth):
    resulttable.column(h, width=w)


# manual insert
# resulttable.insert('','end',value = ['จันทร์','น้ำดื่ม',30, 5, 150])
# resulttable.insert('', 0,value = ['อังคาร,'กล้วย',30, 5, 150])

alltransaction = {}

def updateCSV():
    with open('HWep5.csv','w', newline='', encoding='utf-8') as f:
        fw = csv.writer(f)
        #  เตรียมข้อมูลให้กลายเป็น list
        data = list(alltransaction.values())
        fw.writerows(data)  # multiple line from nested list [[],[],[]]
        print('Table was updated')


def DeleteRecord(event=None):
    check = messagebox.askyesno('Confirm?', 'เจ้าสิ่ลบข้อมูลบ่?')
    print('YES/NO:', check)

    if check == True:
        print('delete')
        select = resulttable.selection()
        print(select)
        data = resulttable.item(select)
        data = data['values']
        transactionid = data[0]
        print(transactionid)
        print(type(transactionid))
        del alltransaction[str(transactionid)]  # delete data in dict
        print(alltransaction)
        updateCSV()
        update_table()
    else:
        print('cancel')

BDelete = Button(T2, text='Delete', command=DeleteRecord)
BDelete.place(x=50, y=550)

resulttable.bind('<Delete>', DeleteRecord)

def update_table():
    resulttable.delete(*resulttable.get_children())
    # for c in resulttable.get_children():
    #     resulttable.delete(c)
    try:
        data = read_csv()
        for d in data:
            # create transaction data
            alltransaction[d[0]] = d  # d[0] = transactionid
            resulttable.insert('', 0, value=d)
        print(alltransaction)
    except EXCEPTION as e:
        print('No File')
        print('ERROR', e)



update_table()
print('GET CHILD:', resulttable.get_children())
GUI.mainloop()
