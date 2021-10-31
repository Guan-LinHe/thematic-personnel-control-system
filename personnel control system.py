'''
    系統名稱:人員進出管理系統
    學校:亞東技術學院
    系別/班級:電子工程系/C班
    更新日期:2020/09/13
    完成日期:2020/09/13
    版本:2.0
    指導老師:李炯三
    學生:何冠霖、譚晉杰
    功能說明:
        本系統是一個簡單的管理人員進出和查看系統，研究本系統的原因是希望能減輕門口的警衛或管理者管理方便，所研究出的系統。
'''

import tkinter as tk
import time
import datetime
import threading
import tkinter.messagebox
import pickle
import os.path
import shutil
import face_recognition as fr
import os
import cv2
import numpy
import numpy as np
import smtplib
import matplotlib
import matplotlib.pyplot as plt
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from functools import partial
from tkinter import ttk  # 匯入內部包
from os import listdir
from os.path import isfile, isdir, join
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)


# (1)新增系統管理員介面
def add_admin_window():
    # 即時拍照
    def photo_now():

        def again_picture():
            take_a_photo_now.destroy()
            photo_now()

        def confirm_imag():
            Photo_name = Photo_name_data.get()
            img_file = '../thematic personnel control system/administrator_photo_profile'
            cv2.imwrite(os.path.join(img_file, Photo_name + '.png'), bgra_cv2image)
            tk.messagebox.showinfo(title='拍照成功 Take a picture successfully',
                                   message='您以新增照片成功\nYou successfully added a photo')
            take_a_photo_now.destroy()
            photo_now()

        # 按下照相按鈕
        def take_pictures_picture():
            global bgra_cv2image
            cv2image = cv2.cvtColor(bgra_cv2image, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
            image_change = Image.fromarray(cv2image)  # 将图像转换成Image对象
            imgshow = ImageTk.PhotoImage(image=image_change)
            Photo_confirmation_box.imgtk = imgshow
            Photo_confirmation_box.config(image=imgshow)
            camera.release()
            take_pictures.config(state=tk.DISABLED)  # 把登入辨識的按鈕停止
            again.config(state=tk.NORMAL)  # 把登入辨識的按鈕開啟
            confirm_photo.config(state=tk.NORMAL)  # 把登入辨識的按鈕開啟
            tk.messagebox.showwarning('提醒!!remind!!', '拍照完成請確認照片\nPlease confirm the photo after taking a photo')
            # cv2.destroyAllWindows()
            # img_file = '../thematic personnel control system/user_photo_profile'
            # cv2.imwrite(os.path.join(img_file,Photo_name+'.png'), bgra_cv2image)

        # 姓名輸入完成按下按鈕開啟照相機
        def camera_program():
            global bgra_cv2image
            Photo_name.config(state=tk.DISABLED)  # 把登入辨識的按鈕停止
            Photo_name_complete.config(state=tk.DISABLED)  # 把登入辨識的按鈕停止
            take_pictures.config(state=tk.NORMAL)
            success, img = camera.read()  # 从摄像头读取照片
            cv2.waitKey(10)
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
            classfier = cv2.CascadeClassifier(
                "../thematic personnel control system/identify_documents/haarcascade_frontalface_alt.xml")
            faceRects = classfier.detectMultiScale(cv2image, scaleFactor=1.8, minNeighbors=3, minSize=(30, 30))
            Photo_name_value = Photo_name_data.get()
            if camera.isOpened() == False:
                tk.messagebox.showerror(title='錯誤 Error', message='沒有找到相機，請在試一次!! No camera found, please try again!!')
                camera.release()  # 釋放攝像頭
                cv2.destroyAllWindows()
            elif Photo_name_value == "":
                tk.messagebox.showerror(title='錯誤 Error',
                                        message='您的姓名是空的，請重新輸入!! Your name is empty, please re-enter!!')
                take_a_photo_now.destroy()
                photo_now()
                camera.release()  # 釋放攝像頭
                cv2.destroyAllWindows()
            elif len(faceRects) > 0:  # 大於0則檢測到人臉
                for i in range(0, 3):
                    for faceRect in faceRects:  # 單獨框出每一張人臉
                        x, y, w, h = faceRect
                        cv2.rectangle(cv2image, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 255, 0), 2)
                        image = cv2image[y - 10: y + h + 10, x - 10: x + w + 10]
                        bgra_cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
            image_change = Image.fromarray(cv2image)  # 将图像转换成Image对象
            imgshow = ImageTk.PhotoImage(image=image_change)
            image_frame_label.imgtk = imgshow
            image_frame_label.config(image=imgshow)
            root.after(1, camera_program)

        take_a_photo_now = tk.Toplevel()
        take_a_photo_now.title("立即拍照 Take A Photo Now")
        take_a_photo_now.geometry("800x700+350+80")
        take_a_photo_now.resizable(False, False)  # 限制視窗不能調整大小
        take_a_photo_now.config(background="#f0faf9")
        take_a_photo_now.iconbitmap('system_photos/photo_now_ico.ico')
        Photo_Now_label = Label(take_a_photo_now, text="立即拍照 Take A Photo Now",
                                font=("標楷體", 18), background="white", width=67, height=2)
        Photo_Now_label.place(x=0, y=0)

        Photo_name_label = tk.Label(take_a_photo_now, font=("標楷體", 15), background="#f0faf9", text="請輸入照片姓名*")
        Photo_name_label.place(x=30, y=70)

        text_label = tk.Label(take_a_photo_now, font=("標楷體", 10), background="#f0faf9", text="(請輸入英文 例如:Chen Xiaomin)")
        text_label.place(x=350, y=110)

        Photo_name_data = tk.StringVar()
        Photo_name = tk.Entry(take_a_photo_now, font=("標楷體", 25),
                              background="white",
                              foreground="black", textvariable=Photo_name_data)
        Photo_name.place(x=250, y=70, width=500)

        Photo_name_complete = tk.Button(take_a_photo_now, text="輸入完成(Input Complete)",
                                        compound="left", background="#477cde",
                                        foreground="white", font=('標楷體', 20))
        Photo_name_complete.place(x=325, y=140)

        take_pictures_label = tk.Label(take_a_photo_now,
                                       font=("標楷體", 20), background="#f0faf9", text="拍照")
        take_pictures_label.place(x=190, y=200)

        Photo_confirmation_label = tk.Label(take_a_photo_now,
                                            font=("標楷體", 20), background="#f0faf9", text="照片確認")
        Photo_confirmation_label.place(x=520, y=200)

        image_frame_label = tk.Label(take_a_photo_now, foreground="#e3962b", width=330, height=300,
                                     background="#f0faf9")
        image_frame_label.place(x=40, y=250)

        Photo_confirmation_box = tk.Label(take_a_photo_now, foreground="#e3962b", width=330, height=300,
                                          background="#f0faf9")
        Photo_confirmation_box.place(x=400, y=250)

        take_pictures_image = tk.PhotoImage(file='system_photos/take_pictures.png')
        take_pictures = tk.Button(take_a_photo_now, image=take_pictures_image, border=0,
                                  compound="left", background="#477cde",
                                  foreground="white", font=('標楷體', 20))
        take_pictures.place(x=180, y=600)

        again_image = tk.PhotoImage(file='system_photos/return_take_pictures.png')
        again = tk.Button(take_a_photo_now, image=again_image, border=0,
                          compound="left", background="#477cde",
                          foreground="white", font=('標楷體', 20))
        again.place(x=365, y=600)

        confirm_photo_image = tk.PhotoImage(file='system_photos/Photo_confirmation.png')
        confirm_photo = tk.Button(take_a_photo_now, image=confirm_photo_image, border=0,
                                  compound="left", background="#477cde",
                                  foreground="white", font=('標楷體', 20))
        confirm_photo.place(x=550, y=600)
        take_pictures.config(state=tk.DISABLED)  # 把登入辨識的按鈕停止
        again.config(state=tk.DISABLED)  # 把臉部辨識的按鈕停止
        confirm_photo.config(state=tk.DISABLED)  # 把臉部辨識的按鈕停止
        camera = cv2.VideoCapture(0)  # 攝像頭

        Photo_name_complete.config(command=camera_program)
        take_pictures.config(command=take_pictures_picture)
        again.config(command=again_picture)
        confirm_photo.config(command=confirm_imag)

        take_a_photo_now.mainloop()

    # 查看群組管理者照片和帳戶內容
    def View_photos_and_account():

        # 群組帳戶刪除管理
        def account_delete():
            del group_info1[select_item]
            # 更新pickle數據
            with open('identify_documents/administrator_account_secret.pickle','wb') as group_file:
                group_file = pickle.dump(group_info1, group_file)
                tk.messagebox.showinfo(title='成功 success', message=select_item + ' 照片已刪除成功 Photo deleted successfully')

        # 群組帳戶照片刪除管理
        def picture_delete():
            confirm_delete = tk.messagebox.askokcancel("刪除照片", message='您確定要刪除' + select_item + '照片嗎?')
            if confirm_delete == True:
                iids = tree.selection()
                for iid in iids:
                    tree.delete(iid)
                try:
                    os.remove(r"../thematic personnel control system/administrator_photo_profile/" + select_item)
                except OSError as Error:
                    tk.messagebox.showerror(title="錯誤 Error", message='錯誤訊息:' + Error)
                else:
                    tk.messagebox.showinfo(title='成功 success',
                                           message=select_item + ' 照片已刪除成功 Photo deleted successfully')

        # 選擇Treeview選項值
        def treeSelect(event):
            global select_item
            widgetobj = event.widget  # 取得控件
            itemselected = widgetobj.selection()[0]  # 取得選項
            col1 = widgetobj.item(itemselected, "value")[0]  # 取得第0欄位內容
            str = "{0}".format(col1)
            select_item = str

        # 更新
        def update():
            View_photos_and_account_contents.destroy()  # 關閉視窗
            View_photos_and_account()  # 開啟視窗

        files_data = {}
        # 指定要列出所有檔案的目錄
        path = "../thematic personnel control system/administrator_photo_profile"
        # 取得所有檔案與子目錄名稱
        files = listdir(path)
        All_lengths = len(files)
        data_loop = 0
        rowCount = 1
        for file_name in files:
            # 產生檔案的絕對路徑
            fullpath = join(path, file_name)
            t = os.stat(fullpath)
            t1 = time.localtime(t.st_mtime)

            all_time = [t1[0], '/', t1[1], '/', t1[2], ' ', t1[3], ':', t1[4], ':', t1[5]]
            set_up_time = ''
            # 檔案建立時間合併(使用迴圈)
            for time_loop in all_time:
                set_up_time += str(time_loop)
            # 檔案訪問時間
            interview_time = (time.ctime(t.st_atime))
            # 檔案大小
            size = os.path.getsize(fullpath)
            size = int(round(size / 1000))
            # 把檔案名稱、檔案建立時間、檔案大小、檔案訪問時間做陣列合併
            if data_loop != All_lengths:
                files_data[data_loop] = [file_name, set_up_time, size, interview_time]
                data_loop += 1

        # Select_window.destroy()  # 關閉視窗
        View_photos_and_account_contents = tk.Toplevel()
        View_photos_and_account_contents.title("查看系統管理員照片和帳戶內容 View system administrator photos and account contents")
        View_photos_and_account_contents.geometry("1000x800+800+130")
        View_photos_and_account_contents.resizable(False, False)
        View_photos_and_account_contents.config(background="white")
        View_photos_and_account_contents.iconbitmap('system_photos/admin.ico')

        View_Group_Administrator_Account = Label(View_photos_and_account_contents,
                                                 text="查看系統管理員照片內容 View the content of system administrator photos",
                                                 font=("標楷體", 18),
                                                 background="#2adb89", foreground="white", width=85, height=2)
        View_Group_Administrator_Account.place(x=0, y=0)

        # 建立Treeview
        tree = ttk.Treeview(View_photos_and_account_contents, columns=['1', '2', '3', '4'], show='headings')
        # y軸滾動條
        yscrollbar = ttk.Scrollbar(View_photos_and_account_contents, orient="vertical", command=tree.yview)
        yscrollbar.place(x=850, y=70, height=235)
        tree.configure(yscrollcommand=yscrollbar.set)
        # 格式化欄標題
        tree.column('1', width=200, anchor='center')
        tree.column('2', width=200, anchor='center')
        tree.column('3', width=100, anchor='center')
        tree.column('4', width=200, anchor='center')
        # 建立內容，#行號從0算起偶數行用顏色當底
        tree.tag_configure("evenColor", background="#2adb89")
        tree.tag_configure("nodata", background="#2adb89")
        # 建立欄標題
        tree.heading('1', text='檔名')
        tree.heading('2', text='日期')
        tree.heading('3', text='大小(KB)')
        tree.heading('4', text='訪問時間')

        # 資料夾沒資料顯示無資料
        if (All_lengths == 0):
            tree.insert('', index=0, text="無資料", values='無資料', tags=("nodata"))
        for k in range(0, All_lengths):
            if (rowCount % 2 == 1):  # 如果成立是基數
                tree.insert('', index=k, values=files_data[k])
            else:
                tree.insert('', index=k, values=files_data[k], tags=("evenColor"))
            rowCount += 1  # 行號數加1
        tree.bind("<<TreeviewSelect>>", treeSelect)  # Treeview控制Select發生
        tree.place(x=150, y=70)
        rubtn = tk.Button(View_photos_and_account_contents, text="更新(Update)", font=('標楷體', 20), width=12,
                          command=update,
                          background="#2adb89", foreground="white")
        rubtn.place(x=320, y=325)
        rubtn = tk.Button(View_photos_and_account_contents, text="刪除(delete)", font=('標楷體', 20), width=12,
                          command=picture_delete,
                          background="#2adb89", foreground="white")
        rubtn.place(x=520, y=325)

        View_Group_Administrator = Label(View_photos_and_account_contents,
                                         text="查看系統管理員帳戶內容 View system administrator account contents",
                                         font=("標楷體", 18),
                                         background="#2adb89", foreground="white", width=85, height=2)
        View_Group_Administrator.place(x=0, y=390)
        with open('identify_documents/administrator_account_secret.pickle','rb') as group_file:
            group_info1 = pickle.load(group_file)
            # 建立Treeview
            tree = ttk.Treeview(View_photos_and_account_contents, columns=['1'], show='headings')
            # y軸滾動條
            yscrollbar = ttk.Scrollbar(View_photos_and_account_contents, orient="vertical", command=tree.yview)
            yscrollbar.place(x=450, y=500, height=235)
            tree.configure(yscrollcommand=yscrollbar.set)
            # 格式化欄標題
            tree.column('1', width=300, anchor='center')
            # 建立內容，#行號從0算起偶數行用顏色當底
            tree.tag_configure("evenColor", background="#5cfab1")
            # 建立欄標題
            tree.heading('1', text='帳戶名稱')
            for i in group_info1:
                tree.insert('', index=END, values=i)
            tree.bind("<<TreeviewSelect>>", treeSelect)  # Treeview控制Select發生
            tree.place(x=150, y=500)
            rubtn = tk.Button(View_photos_and_account_contents, text="更新(Update)", font=('標楷體', 20), width=12,
                              command=update,
                              background="#2adb89", foreground="white")
            rubtn.place(x=600, y=550)
            rubtn = tk.Button(View_photos_and_account_contents, text="刪除(delete)", font=('標楷體', 20), width=12,
                              command=account_delete,
                              background="#2adb89", foreground="white")
            rubtn.place(x=600, y=650)

        select_file.config(command=choose_file)
        confirm_submission.config(command=copy_img)

        View_photos_and_account_contents.mainloop()

    # 新增系統管理員帳戶
    def add_admin():
        accountnew = new_account.get()
        passwordnew = new_password.get()
        repasswordnew = new_re_password.get()
        with open('identify_documents/administrator_account_secret.pickle','rb') as admin_file:
            admin_info = pickle.load(admin_file)
        if passwordnew != repasswordnew:
            tk.messagebox.showinfo("錯誤 Error",
                                   "密碼和確認密碼不匹配請重新輸入!\nPassword does not match confirmation password, please re-enter!.")
            new_account.set("")
            new_password.set("")
            new_re_password.set("")
        elif accountnew in admin_info:
            tk.messagebox.showinfo("錯誤 Error",
                                   "用戶已經註冊過了!\n The user has already signed up!")
            new_account.set("")
            new_password.set("")
            new_re_password.set("")
        elif accountnew == '':
            tk.messagebox.showinfo("錯誤 Error",
                                   "帳號不能空白請重新輸入!\n Account number cannot be blank, please re-enter!")
            new_account.set("")
            new_password.set("")
            new_re_password.set("")
        elif passwordnew == '':
            tk.messagebox.showinfo("錯誤 Error",
                                   "密碼或確認密碼不能空白請重新輸入!\nThe password or confirmation password cannot be blank, please re-enter!")
            new_account.set("")
            new_password.set("")
            new_re_password.set("")
        elif repasswordnew == "":
            tk.messagebox.showinfo("錯誤 Error",
                                   "密碼或確認密碼不能空白請重新輸入!\nThe password or confirmation password cannot be blank, please re-enter!")
            new_account.set("")
            new_password.set("")
            new_re_password.set("")
        else:
            admin_info[accountnew] = passwordnew  # 定義字典陣列加入用戶
            with open('identify_documents/administrator_account_secret.pickle','wb') as admin_file:
                pickle.dump(admin_info, admin_file)
            tk.messagebox.showinfo("恭喜 Congratulations",
                                   "您已成功註冊帳戶\nYou have successfully registered an account.")
            new_account.set("")
            new_password.set("")
            new_re_password.set("")

    # 圖像比例縮小
    def choose_file():
        def resize(w, h, w_box, h_box, pil_image):
            # 對一個pil_image對象進行縮放，讓它在一個矩形框內，還能保持比例
            f1 = 1.0 * w_box / w  # 1.0 forces float division in Python2
            f2 = 1.0 * h_box / h
            factor = min([f1, f2])  # 比較最小函數

            width = int(w * factor)  # 轉換成整數型態
            height = int(h * factor)  # 轉換成整數型態
            return pil_image.resize((width, height), Image.ANTIALIAS)

        # 期望圖像顯示的大小
        w_box = 250
        h_box = 250

        # 以一個PIL圖像對象打開
        global File
        File = filedialog.askopenfilename(parent=admin_labframe, initialdir="C:/", title='Choose an image.',
                                          filetypes=[('JPG', '*.jpg'), ('PNG', '*.png'), ('JFIF', '*.jfif'),
                                                     ('All Files', '*')])
        position.set(File)

        pil_image = Image.open(File)  # 讀寫方式打開

        # get the size of the image
        # 獲取圖像的原始大小
        w, h = pil_image.size
        # resize the image so it retains its aspect ration
        # but fits into the specified display box
        # 縮放圖像讓它保持比例，同時限制在一個矩形框範圍內
        pil_image_resized = resize(w, h, w_box, h_box, pil_image)
        # convert PIL image object to Tkinter PhotoImage object
        # 把PIL圖像對象轉變爲Tkinter的PhotoImage對象
        global tk_imag
        tk_image = ImageTk.PhotoImage(pil_image_resized)
        # put the image on a widget the size of the specified display box
        # Label: 這個小工具，就是個顯示框，小窗口，把圖像大小顯示到指定的顯示框

        # image(畫布)
        canvas = tk.Canvas(admin_labframe1, height=w_box, width=h_box, background="white")
        canvas.create_image(w_box, h_box, image=tk_image, anchor=SE)
        canvas.place(x=600, y=75)
        admin_labframe1.mainloop()

    # 照片存到資料夾
    def copy_img():

        if position.get() == "":
            tk.messagebox.showerror(title='錯誤 Error',
                                    message='請選擇您想要的照片。\n Please select the photo you want.')
            position.set("")
            admin_name.set("")

        elif admin_name.get() == "":
            tk.messagebox.showerror(title='錯誤 Error',
                                    message='請為照片命名。\n Please name your photo.')
            position.set("")
            admin_name.set("")
        else:
            image = tk.messagebox.askokcancel(title='確認 Confirm',
                                              message='請確認這是您要新增的相片。\n Please confirm this is the photo you want to add.')
            if image == True:
                local_img_name = File
                # 指定要複製的圖片路徑
                path = r'../thematic personnel control system/administrator_photo_profile/'
                # 指定存放圖片的目錄
                shutil.copy(local_img_name, path)
                os.rename(os.path.join(File, position.get()), os.path.join(path, admin_name.get()))
                name = os.path.basename(position.get())
                os.remove('../thematic personnel control system/administrator_photo_profile/' + name)
                tk.messagebox.showinfo(title='恭喜 Congratulations', message='照片新增成功。\n Photo added successfully.')
                position.set("")
                admin_name.set("")

    # Select_window.destroy()  # 關閉視窗
    add_administrator = tk.Toplevel()  # 設定子系視窗
    add_administrator.title("新增系統管理員帳戶Add System Administrator Account")  # 視窗圖示抬頭
    add_administrator.geometry("1000x800+800+130")  # 調整畫面大小和畫面位置設定
    add_administrator.resizable(False, False)  # 限制視窗不能調整大小
    add_administrator.config(background="white")  # 設定背景顏色
    add_administrator.iconbitmap('system_photos/admin.ico')  # 視窗圖示
    # 文字
    label1 = Label(add_administrator, text="新增系統管理員帳戶 Add System Administrator Account", font=("標楷體", 18),
                   background="#477cde", foreground="white", width=85, height=2)
    label1.place(x=0, y=0)
    # 文字
    admin_labframe = tk.LabelFrame(add_administrator,
                                   text="新增系統管理員帳戶(Add System Administrator Account)",
                                   font=("標楷體", 25), background="white")
    # 文字
    add_admin_accounttext = tk.Label(admin_labframe, font=("標楷體", 15),
                                     background="white",
                                     foreground="#477cde", text="帳號(Account Number)*")
    add_admin_accounttext.place(x=0, y=30)
    # 儲存帳號值
    new_account = tk.StringVar()
    add_admin_accountentry = tk.Entry(admin_labframe, font=("標楷體", 25),
                                      background="white",
                                      foreground="black", textvariable=new_account)
    add_admin_accountentry.place(x=350, y=30, width=600)
    # 文字
    add_admin_passwordtext = tk.Label(admin_labframe, font=("標楷體", 15),
                                      background="white",
                                      foreground="#477cde", text="密碼(Password)*")
    add_admin_passwordtext.place(x=0, y=80)
    # 儲存密碼值
    new_password = tk.StringVar()
    add_admin_passworentry = tk.Entry(admin_labframe, font=("標楷體", 25),
                                      background="white", show="‧",
                                      foreground="black", textvariable=new_password)
    add_admin_passworentry.place(x=350, y=80, width=600)
    # 文字
    admin_re_enter_passwordtext = tk.Label(admin_labframe, font=("標楷體", 15),
                                           background="white",
                                           foreground="#477cde",
                                           text="重新輸入密碼(Re-enter Password)*")
    admin_re_enter_passwordtext.place(x=0, y=130)
    # 重新輸入密碼值
    new_re_password = tk.StringVar()
    admin_re_enter_passwordentry = tk.Entry(admin_labframe, font=("標楷體", 25),
                                            background="white",
                                            foreground="black", show="‧",
                                            textvariable=new_re_password)
    admin_re_enter_passwordentry.place(x=350, y=130, width=600)
    # 確定新增按鈕
    admin_determine = tk.Button(admin_labframe, text="確定新增(OK To Add)", compound="left", background="#477cde",
                                foreground="white", font=('標楷體', 20), command=add_admin)
    admin_determine.place(x=500, y=180)
    admin_labframe.pack(padx=0, pady=75, ipadx=500, ipady=135)

    # 新增系統管理員照片
    admin_labframe1 = tk.LabelFrame(add_administrator,
                                    text="新增系統管理員照片(Add System Administator Photo)", font=("標楷體", 25),
                                    background="white")
    # 選擇資料夾路徑
    position = tk.StringVar()
    position_text = tk.Entry(admin_labframe1, width=40, font=('標楷體', 30),
                             selectborderwidth=50, justify=LEFT, textvariable=position)
    position_text.place(x=0, y=20)
    # 選擇檔案按鈕
    select_file = tk.Button(admin_labframe1, text="...", background="#477cde",
                            foreground="white", font=('標楷體', 20), command=choose_file)
    select_file.place(x=800, y=20)
    # 確認送出按鈕
    confirm_submission = tk.Button(admin_labframe1, text="確認送出(Confirm Submission)", background="#477cde",
                                   foreground="white", font=('標楷體', 20), command=copy_img)
    confirm_submission.place(x=0, y=290)
    # 文字
    browse_photos = tk.Label(admin_labframe1, font=("標楷體", 20),
                             background="white",
                             foreground="#477cde",
                             text="系統管理員名稱*\nSystem administrator name")
    browse_photos.place(x=0, y=75)
    # 統管理員名稱值
    admin_name = tk.StringVar()
    en = tk.Entry(admin_labframe1, width=20, font=('標楷體', 20), justify=LEFT,
                  textvariable=admin_name)
    en.place(x=0, y=150)
    # 文字
    browse_photos = tk.Label(admin_labframe1, font=("標楷體", 15),
                             background="white",
                             foreground="red",
                             text="瀏覽照片\nBrowse photos")
    browse_photos.place(x=450, y=75)
    # 文字
    caveat_text = tk.Label(admin_labframe1, font=("標楷體", 15),
                           background="white",
                           foreground="red",
                           text="注意:檔名+檔案格式\nNote: file name + file format\nEx:exit.jpg")
    caveat_text.place(x=0, y=200)
    admin_labframe1.pack(padx=0, pady=0, ipadx=500, ipady=190)
    # 查看照片和帳戶內容按鈕
    View_photos_and_account_contents = tk.Button(add_administrator, text="查看照片和帳戶內容", background="#477cde",
                                                 foreground="white", font=('標楷體', 20), command=View_photos_and_account)
    View_photos_and_account_contents.place(x=450, y=360)
    # 立即拍照按鈕
    take_a_photo = tk.Button(add_administrator, text="立即拍照", background="#477cde",
                             foreground="white", font=('標楷體', 20), command=photo_now)
    take_a_photo.place(x=300, y=360)
    # 迴圈
    add_administrator.mainloop()

# (2)系統管理員人員辨識管理
def personnel_identification():
    # 即時拍照
    def photo_now():

        def again_picture():
            take_a_photo_now.destroy()
            photo_now()

        def confirm_imag():
            Photo_name = Photo_name_data.get()
            img_file = '../thematic personnel control system/Person_identification_photos'
            cv2.imwrite(os.path.join(img_file, Photo_name + '.png'), bgra_cv2image)
            tk.messagebox.showinfo(title='拍照成功 Take a picture successfully',
                                   message='您以新增照片成功\nYou successfully added a photo')
            take_a_photo_now.destroy()
            photo_now()

        # 按下照相按鈕
        def take_pictures_picture():
            cv2image = cv2.cvtColor(bgra_cv2image, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
            image_change = Image.fromarray(cv2image)  # 将图像转换成Image对象
            imgshow = ImageTk.PhotoImage(image=image_change)
            Photo_confirmation_box.imgtk = imgshow
            Photo_confirmation_box.config(image=imgshow)
            camera.release()
            take_pictures.config(state=tk.DISABLED)  # 把登入辨識的按鈕停止
            again.config(state=tk.NORMAL)  # 把登入辨識的按鈕開啟
            confirm_photo.config(state=tk.NORMAL)  # 把登入辨識的按鈕開啟
            tk.messagebox.showwarning('提醒!!remind!!', '拍照完成請確認照片\nPlease confirm the photo after taking a photo')
            # cv2.destroyAllWindows()
            # img_file = '../thematic personnel control system/user_photo_profile'
            # cv2.imwrite(os.path.join(img_file,Photo_name+'.png'), bgra_cv2image)

        # 姓名輸入完成按下按鈕開啟照相機
        def camera_program():
            global bgra_cv2image
            Photo_name.config(state=tk.DISABLED)  # 把登入辨識的按鈕停止
            Photo_name_complete.config(state=tk.DISABLED)  # 把登入辨識的按鈕停止
            take_pictures.config(state=tk.NORMAL)
            success, img = camera.read()  # 从摄像头读取照片
            cv2.waitKey(10)
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
            classfier = cv2.CascadeClassifier(
                "../thematic personnel control system/identify_documents/haarcascade_frontalface_alt.xml")
            faceRects = classfier.detectMultiScale(cv2image, scaleFactor=1.8, minNeighbors=3, minSize=(30, 30))
            Photo_name_value = Photo_name_data.get()
            if camera.isOpened() == False:
                tk.messagebox.showerror(title='錯誤 Error', message='沒有找到相機，請在試一次!! No camera found, please try again!!')
                camera.release()  # 釋放攝像頭
                cv2.destroyAllWindows()
            elif Photo_name_value == "":
                tk.messagebox.showerror(title='錯誤 Error',
                                        message='您的姓名是空的，請重新輸入!! Your name is empty, please re-enter!!')
                take_a_photo_now.destroy()
                photo_now()
                camera.release()  # 釋放攝像頭
                cv2.destroyAllWindows()
            elif len(faceRects) > 0:  # 大於0則檢測到人臉
                for i in range(0, 3):
                    for faceRect in faceRects:  # 單獨框出每一張人臉
                        x, y, w, h = faceRect
                        cv2.rectangle(cv2image, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 255, 0), 2)
                        image = cv2image[y - 10: y + h + 10, x - 10: x + w + 10]
                        bgra_cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
            image_change = Image.fromarray(cv2image)  # 将图像转换成Image对象
            imgshow = ImageTk.PhotoImage(image=image_change)
            image_frame_label.imgtk = imgshow
            image_frame_label.config(image=imgshow)
            root.after(1, camera_program)

        take_a_photo_now = tk.Toplevel()  # 設定子系視窗
        take_a_photo_now.title("立即拍照 Take A Photo Now")  # 視窗圖示抬頭
        take_a_photo_now.geometry("800x700+350+80")  # 調整畫面大小和畫面位置設定
        take_a_photo_now.resizable(False, False)  # 限制視窗不能調整大小
        take_a_photo_now.config(background="#f0faf9")  # 設定背景顏色
        take_a_photo_now.iconbitmap('system_photos/photo_now_ico.ico')  # 視窗圖示
        # 文字
        Photo_Now_label = Label(take_a_photo_now, text="立即拍照 Take A Photo Now", font=("標楷體", 18), background="white",
                                width=67, height=2)
        Photo_Now_label.place(x=0, y=0)
        # 文字
        Photo_name_label = tk.Label(take_a_photo_now, font=("標楷體", 15), background="#f0faf9", text="請輸入照片姓名*")
        Photo_name_label.place(x=30, y=70)
        # 文字
        text_label = tk.Label(take_a_photo_now, font=("標楷體", 10), background="#f0faf9", text="(請輸入英文 例如:Chen Xiaomin)")
        text_label.place(x=350, y=110)
        # 儲存照片姓名
        Photo_name_data = tk.StringVar()
        Photo_name = tk.Entry(take_a_photo_now, font=("標楷體", 25),
                              background="white",
                              foreground="black", textvariable=Photo_name_data)
        Photo_name.place(x=250, y=70, width=500)
        # 輸入完成按鈕
        Photo_name_complete = tk.Button(take_a_photo_now, text="輸入完成(Input Complete)", compound="left",
                                        background="#e0519d",
                                        foreground="white", font=('標楷體', 20), command=camera_program)
        Photo_name_complete.place(x=325, y=140)
        # 拍照文字
        take_pictures_label = tk.Label(take_a_photo_now,
                                       font=("標楷體", 20), background="#f0faf9", text="拍照")
        take_pictures_label.place(x=190, y=200)
        # 文字
        Photo_confirmation_label = tk.Label(take_a_photo_now,
                                            font=("標楷體", 20), background="#f0faf9", text="照片確認")
        Photo_confirmation_label.place(x=520, y=200)
        # 顯示照片
        image_frame_label = tk.Label(take_a_photo_now, foreground="#e3962b", width=330, height=300,
                                     background="#f0faf9")
        image_frame_label.place(x=40, y=250)
        # 顯示照片
        Photo_confirmation_box = tk.Label(take_a_photo_now, foreground="#e3962b", width=330, height=300,
                                          background="#f0faf9")
        Photo_confirmation_box.place(x=400, y=250)
        # 確認照相按鈕
        take_pictures_image = tk.PhotoImage(file='system_photos/take_pictures.png')
        take_pictures = tk.Button(take_a_photo_now, image=take_pictures_image, border=0, compound="left",
                                  background="#e0519d",
                                  foreground="white", font=('標楷體', 20), command=take_pictures_picture)
        take_pictures.place(x=180, y=600)
        # 返回按鈕
        again_image = tk.PhotoImage(file='system_photos/return_take_pictures.png')
        again = tk.Button(take_a_photo_now, image=again_image, border=0, compound="left", background="#e0519d",
                          foreground="white", font=('標楷體', 20), command=again_picture)
        again.place(x=365, y=600)
        # 確認上傳到資料夾按鈕
        confirm_photo_image = tk.PhotoImage(file='system_photos/Photo_confirmation.png')
        confirm_photo = tk.Button(take_a_photo_now, image=confirm_photo_image, border=0, compound="left",
                                  background="#e0519d",
                                  foreground="white", font=('標楷體', 20), command=confirm_imag)
        confirm_photo.place(x=550, y=600)
        take_pictures.config(state=tk.DISABLED)  # 把登入辨識的按鈕停止
        again.config(state=tk.DISABLED)  # 把臉部辨識的按鈕停止
        confirm_photo.config(state=tk.DISABLED)  # 把臉部辨識的按鈕停止
        camera = cv2.VideoCapture(0)  # 攝像頭

        take_a_photo_now.mainloop()

    # 保持圖片比例
    def choose_file():
        def resize(w, h, w_box, h_box, pil_image):
            # 對一個pil_image對象進行縮放，讓它在一個矩形框內，還能保持比例

            f1 = 1.0 * w_box / w
            f2 = 1.0 * h_box / h
            factor = min([f1, f2])  # 比較最小函數

            width = int(w * factor)  # 轉換成整數型態
            height = int(h * factor)  # 轉換成整數型態
            return pil_image.resize((width, height), Image.ANTIALIAS)

        # 期望圖像顯示的大小
        w_box = 250
        h_box = 250

        # 以一個PIL圖像對象打開
        global File
        File = filedialog.askopenfilename(parent=admin_labframe1, initialdir="C:/", title='Choose an image.',
                                          filetypes=[('JPG', '*.jpg'), ('PNG', '*.png'), ('JFIF', '*.jfif'),
                                                     ('All Files', '*')])
        position.set(File)

        pil_image = Image.open(File)  # 讀寫方式打開

        # 獲取圖像的原始大小
        w, h = pil_image.size

        # 縮放圖像讓它保持比例，同時限制在一個矩形框範圍內
        pil_image_resized = resize(w, h, w_box, h_box, pil_image)

        # 把PIL圖像對象轉變爲Tkinter的PhotoImage對象
        global tk_imag
        tk_image = ImageTk.PhotoImage(pil_image_resized)

        # image(畫布)
        canvas = tk.Canvas(admin_labframe1, height=w_box, width=h_box, background="white")
        canvas.create_image(w_box, h_box, image=tk_image, anchor=SE)
        canvas.place(x=600, y=75)
        # 迴圈
        admin_labframe1.mainloop()

    # 照片上傳資料夾
    def copy_img():

        if position.get() == "":
            tk.messagebox.showerror(title='錯誤 Error',
                                    message='請選擇您想要的照片。\n Please select the photo you want.')

        elif admin_name.get() == "":
            tk.messagebox.showerror(title='錯誤 Error',
                                    message='請為照片命名。\n Please name your photo.')

        else:
            image = tk.messagebox.askokcancel(title='確認 Confirm',
                                              message='請確認這是您要新增的相片。\n Please confirm this is the photo you want to add.')
            if image == True:
                local_img_name = File
                # 指定要複製的圖片路徑
                path = r'../thematic personnel control system/Person_identification_photos/'
                # 指定存放圖片的目錄
                shutil.copy(local_img_name, path)
                os.rename(os.path.join(File, position.get()), os.path.join(path, admin_name.get()))
                name = os.path.basename(position.get())
                os.remove('../thematic personnel control system/Person_identification_photos/' + name)
                tk.messagebox.showinfo(title='恭喜 Congratulations', message='照片新增成功。\n Photo added successfully.')

    # 從資料夾刪除照片
    def delete():
        confirm_delete = tk.messagebox.askokcancel("刪除照片", message='您確定要刪除' + select_item + '照片嗎?')
        if confirm_delete == True:
            iids = tree.selection()
            for iid in iids:
                tree.delete(iid)
            try:
                os.remove(r"../thematic personnel control system/Person_identification_photos/" + select_item)
            except OSError as Error:
                tk.messagebox.showerror(title="錯誤 Error", message='錯誤訊息:' + Error)
            else:
                tk.messagebox.showinfo(title='成功 success', message=select_item + ' 照片已刪除成功 Photo deleted successfully')

    # 選擇Treeview選項值
    def treeSelect(event):
        global select_item
        widgetobj = event.widget  # 取得控件
        itemselected = widgetobj.selection()[0]  # 取得選項
        col1 = widgetobj.item(itemselected, "value")[0]  # 取得第0欄位內容
        str = "{0}".format(col1)
        select_item = str

    # 更新
    def update():
        add_aerson_adentification.destroy()  # 關閉視窗
        personnel_identification()

    files_data = {}
    # 指定要列出所有檔案的目錄
    path = "../thematic personnel control system/Person_identification_photos"
    # 取得所有檔案與子目錄名稱
    files = listdir(path)
    All_lengths = len(files)
    data_loop = 0
    rowCount = 1
    for file_name in files:
        # 產生檔案的絕對路徑
        fullpath = join(path, file_name)
        t = os.stat(fullpath)
        t1 = time.localtime(t.st_mtime)

        all_time = [t1[0], '/', t1[1], '/', t1[2], ' ', t1[3], ':', t1[4], ':', t1[5]]
        set_up_time = ''
        # 檔案建立時間合併(使用迴圈)
        for time_loop in all_time:
            set_up_time += str(time_loop)
        # 檔案訪問時間
        interview_time = (time.ctime(t.st_atime))
        # 檔案大小
        size = os.path.getsize(fullpath)
        size = int(round(size / 1000))
        # 把檔案名稱、檔案建立時間、檔案大小、檔案訪問時間做陣列合併
        if data_loop != All_lengths:
            files_data[data_loop] = [file_name, set_up_time, size, interview_time]
            data_loop += 1

    # Select_window.destroy()  # 關閉視窗
    add_aerson_adentification = tk.Toplevel()  # 設定子系視窗
    add_aerson_adentification.title("新增人員辨識帳戶Add Person Identification Account")  # 視窗圖示抬頭
    add_aerson_adentification.geometry("1000x800+800+130")  # 調整畫面大小和畫面位置設定
    add_aerson_adentification.resizable(False, False)  # 限制視窗不能調整大小
    add_aerson_adentification.config(background="white")  # 設定背景顏色
    add_aerson_adentification.iconbitmap('system_photos/admin.ico')  # 視窗圖示
    # 文字
    label1 = Label(add_aerson_adentification, text="人員辨識管理 Personnel Identification Management", font=("標楷體", 18),
                   background="#e0519d", foreground="white", width=85, height=2)
    label1.place(x=0, y=0)

    # 新增系統管理員照片
    admin_labframe1 = tk.LabelFrame(add_aerson_adentification,
                                    text="新增人員辨識照片(Add People To Identify Photos)", font=("標楷體", 25),
                                    background="white")
    # 選擇的人員辨識路徑儲存
    position = tk.StringVar()
    position_text = tk.Entry(admin_labframe1, width=40, font=('標楷體', 30),
                             selectborderwidth=50, justify=LEFT, textvariable=position)
    position_text.place(x=0, y=20)
    # 選擇資料按鈕
    select_file = tk.Button(admin_labframe1, text="...", background="#e0519d", foreground="white", font=('標楷體', 20),
                            command=choose_file)
    select_file.place(x=800, y=20)
    # 確認送出按鈕
    confirm_submission = tk.Button(admin_labframe1, text="確認送出(Confirm Submission)",
                                   background="#e0519d",
                                   foreground="white", font=('標楷體', 20),command=copy_img)
    confirm_submission.place(x=0, y=290)
    # 文字
    browse_photos = tk.Label(admin_labframe1, font=("標楷體", 20),
                             background="white",
                             foreground="#e0519d",
                             text="系統管理員名稱*\nSystem administrator name")
    browse_photos.place(x=0, y=75)
    # 系統管理員名稱儲存
    admin_name = tk.StringVar()
    en = tk.Entry(admin_labframe1, width=20, font=('標楷體', 20), justify=LEFT,
                  textvariable=admin_name)
    en.place(x=0, y=150)
    # 文字
    browse_photos = tk.Label(admin_labframe1, font=("標楷體", 15),
                             background="white",
                             foreground="red",
                             text="瀏覽照片\nBrowse photos")
    browse_photos.place(x=450, y=75)
    # 文字
    caveat_text = tk.Label(admin_labframe1, font=("標楷體", 15),
                           background="white",
                           foreground="red",
                           text="注意:檔名+檔案格式\nNote: file name + file format\nEx:exit.jpg")
    caveat_text.place(x=0, y=200)
    admin_labframe1.pack(padx=0, pady=70, ipadx=500, ipady=190)

    # 建立Treeview
    tree = ttk.Treeview(add_aerson_adentification, columns=['1', '2', '3', '4'], show='headings')
    # y軸滾動條
    yscrollbar = ttk.Scrollbar(add_aerson_adentification, orient="vertical", command=tree.yview)
    yscrollbar.place(x=850, y=515, height=235)
    tree.configure(yscrollcommand=yscrollbar.set)
    # 格式化欄標題
    tree.column('1', width=200, anchor='center')
    tree.column('2', width=200, anchor='center')
    tree.column('3', width=100, anchor='center')
    tree.column('4', width=200, anchor='center')
    # 建立內容，#行號從0算起偶數行用顏色當底
    tree.tag_configure("evenColor", background="#fc8dfc")
    tree.tag_configure("nodata", background="#f55d5d")
    # 建立欄標題
    tree.heading('1', text='檔名')
    tree.heading('2', text='日期')
    tree.heading('3', text='大小(KB)')
    tree.heading('4', text='訪問時間')

    # 資料夾沒資料顯示無資料
    if (All_lengths == 0):
        tree.insert('', index=0, text="無資料", values='無資料', tags=("nodata"))
    for k in range(0, All_lengths):
        if (rowCount % 2 == 1):  # 如果成立是基數
            tree.insert('', index=k, values=files_data[k])
        else:
            tree.insert('', index=k, values=files_data[k], tags=("evenColor"))
        rowCount += 1  # 行號數加1
    tree.bind("<<TreeviewSelect>>", treeSelect)  # Treeview控制Select發生
    tree.pack()
    # 更新按鈕
    rubtn = tk.Button(add_aerson_adentification, text="更新(Update)", font=('標楷體', 20), width=12, command=update,
                      background="#e0519d", foreground="white")
    rubtn.place(x=320, y=750)
    # 刪除按鈕
    rubtn = tk.Button(add_aerson_adentification, text="刪除(delete)", font=('標楷體', 20), width=12, command=delete,
                      background="#e0519d", foreground="white")
    rubtn.place(x=520, y=750)
    # 立即拍照按鈕
    take_a_photo = tk.Button(add_aerson_adentification, text="立即拍照", background="#e0519d",
                             foreground="white", font=('標楷體', 20),command=photo_now)
    take_a_photo.place(x=280, y=350)

    add_aerson_adentification.mainloop()

# (3)辨識人員查看
def Identification_personnel_View():
    # 取得選項並顯示照片
    def treeSelect(event):
        global select_item
        widgetobj = event.widget  # 取得控件
        itemselected = widgetobj.selection()[0]  # 取得選項
        col1 = widgetobj.item(itemselected, "value")[0]  # 取得第0欄位內容
        str = "{0}".format(col1)
        select_item = str

        # 顯示人員辨識照片和比對照片
        for filename in os.listdir(r"../thematic_personnel_control_system/Personnel_in_and_out_photos"):
            for filename in os.listdir(r"../thematic_personnel_control_system/Person_identification_photos"):

                try:
                    System_photo = cv2.imread('Person_identification_photos' + '/' + (select_item + '.jpg'))
                    cv2.imshow('Show System photo', System_photo)
                except:
                    System_photo = cv2.imread('Person_identification_photos' + '/' + (select_item + '.png'))
                    cv2.imshow('Show System photo', System_photo)
                finally:
                    try:
                        Live_photo = cv2.imread('Personnel_in_and_out_photos' + '/' + (select_item + '.png'))
                        cv2.imshow('Show Live photo', Live_photo)
                    except:
                        Live_photo = cv2.imread('Personnel_in_and_out_photos' + '/' + (select_item + '.jpg'))
                        cv2.imshow('Show Live photo', Live_photo)


    # 刪除資料
    def delete():
        personnel_record = []
        confirm_delete = tk.messagebox.askokcancel("刪除資料", message='您確定要刪除' + select_item + '這筆資料嗎?')
        if confirm_delete == True:
            iids = tree.selection()
            for iid in iids:
                tree.delete(iid)
            with open('identify_documents/personnel_identification.pickle','rb') as personnel_file_rb:

                personnel_record = pickle.load(personnel_file_rb)
                del personnel_record[select_item]

                with open('identify_documents/personnel_identification.pickle','wb') as personnel_file_wb:
                    pickle.dump(personnel_record, personnel_file_wb)

                for filename in os.listdir(r"../thematic personnel control system/Personnel_in_and_out_photos"):
                    try:
                        cv2.imread('Personnel_in_and_out_photos' + '/' + (select_item + '.png'))
                        os.remove('Personnel_in_and_out_photos' + '/' + (select_item + '.png'))
                        tk.messagebox.showinfo(title='成功 success',message=select_item + ' 刪除成功 Photo deleted successfully')

                    except:
                        cv2.imread('Personnel_in_and_out_photos' + '/' + (select_item + '.jpg'))
                        os.remove('Personnel_in_and_out_photos' + '/' + (select_item + '.jpg'))
                        tk.messagebox.showinfo(title='成功 success',message=select_item + ' 刪除成功 Photo deleted successfully')

    # 更新
    def update():
        View_personnel.destroy()  # 關閉視窗
        Identification_personnel_View()

    with open('identify_documents/personnel_identification.pickle','rb') as personnel_file:
        personnel_info = pickle.load(personnel_file)
    All_lengths = len(personnel_info)
    print(personnel_info)

    # Select_window.destroy()  # 關閉視窗
    View_personnel = tk.Toplevel()  # 設定子系視窗
    View_personnel.title("辨識人員查看Identification of personnel View")  # 視窗圖示抬頭
    View_personnel.geometry("800x400+800+130")  # 調整畫面大小和畫面位置設定
    View_personnel.resizable(False, False)  # 限制視窗不能調整大小
    View_personnel.config(background="white")  # 設定背景顏色
    View_personnel.iconbitmap('system_photos/admin.ico')  # 視窗圖示

    # 建立Treeview
    tree = ttk.Treeview(View_personnel, columns=['1', '2', '3', '4', '5', '6'], show='headings')
    # y軸滾動條
    yscrollbar = ttk.Scrollbar(View_personnel, orient="vertical", command=tree.yview)
    yscrollbar.place(x=750, y=0, height=235)
    tree.configure(yscrollcommand=yscrollbar.set)
    # 格式化欄標題
    tree.column('1', width=150, anchor='center')
    tree.column('2', width=100, anchor='center')
    tree.column('3', width=100, anchor='center')
    tree.column('4', width=150, anchor='center')
    tree.column('5', width=100, anchor='center')
    tree.column('6', width=120, anchor='center')
    # 建立內容，#行號從0算起偶數行用顏色當底
    tree.tag_configure("evenColor", background="#fc8dfc")
    tree.tag_configure("nodata", background="#f55d5d")
    # 建立欄標題
    tree.heading('1', text='姓名')
    tree.heading('2', text='性別')
    tree.heading('3', text='年齡')
    tree.heading('4', text='最後時間')
    tree.heading('5', text='進出次數')
    tree.heading('6', text='狀況')

    for name_info in personnel_info:
        # 資料夾沒資料顯示無資料
        if (All_lengths == 0):
            tree.insert('', index=0, text="無資料", values='無資料', tags=("nodata"))
        else:
            tree.insert('', index=END, values=(
                personnel_info[name_info]['Name'], personnel_info[name_info]['Gender'],
                personnel_info[name_info]['Age'],
                personnel_info[name_info]['Time'], personnel_info[name_info]['number_of_in_and_out'],
                personnel_info[name_info]['situation']))

    tree.bind("<<TreeviewSelect>>", treeSelect)  # Treeview控制Select發生
    tree.pack()
    # 更新按鈕
    rubtn = tk.Button(View_personnel, text="更新(Update)", font=('標楷體', 20), width=12, command=update,
                      background="#e0519d", foreground="white")
    rubtn.place(x=200, y=250)
    # 刪除按鈕
    rubtn = tk.Button(View_personnel, text="刪除(delete)", font=('標楷體', 20), width=12, command=delete,
                      background="#e0519d", foreground="white")
    rubtn.place(x=400, y=250)
    # 迴圈
    View_personnel.mainloop()

# (4)進出統計查看
def In_and_out_statistics_view():
    # 清除圖表資料
    def Chart_clear():
        confirm_delete = tk.messagebox.askokcancel("清除圖表 Clear chart",
                                                   message='您確定要清除圖表的資料嗎? Are you sure you want to clear the chart data?')
        # 寫入資料庫把圖表清空
        if confirm_delete == True:
            with open('identify_documents/statistics.pickle','wb') as statistics_file:
                clear_content = {}
                pickle.dump(clear_content, statistics_file)
            tk.messagebox.showinfo(title='成功 success', message=' 清除圖表成功 Clear chart successfully')
            # 關閉視窗
            Chart.destroy()
            In_and_out_statistics_view()

    statistics = {}
    upda_results = {}
    category_names = ['進出總人數', '男生人數', '女生人數', '陌生人數']
    # 讀取統計資料
    with open('identify_documents/statistics.pickle', 'rb') as statistics_file:
        statistics_info = pickle.load(statistics_file)
        statistics = statistics_info
    if statistics == {}:
        upda_results = {'無資料': [0, 0, 0, 0]}
    else:
        for i in statistics:
            results = {i: [statistics[i]['total_people_in_and_out'], statistics[i]['number_of_boys'],
                           statistics[i]['number_of_girls'],
                           statistics[i]['number_of_strangers']]}
            upda_results.update(results)
    time_stamp = datetime.datetime.now()
    date_now = time_stamp.strftime('%Y/%m/%d')
    matplotlib.use('TkAgg')
    Chart = tk.Tk()  # 設定子系視窗
    Chart.title("進出統計 In And Out Statistics")  # 視窗圖示抬頭
    Chart.geometry("800x700+350+80")  # 調整畫面大小和畫面位置設定
    Chart.resizable(False, False)  # 限制視窗不能調整大小
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 中文
    # 文字和資料設定
    labels = list(upda_results.keys())
    data = np.array(list(upda_results.values()))

    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 6))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())
    print(zip(category_names, category_colors))
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)
        xcenters = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            print(int(c))
            ax.text(x, y, str(int(c)), ha='center', va='center',
                    color=text_color, fontsize=15)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')
    # 把繪製的圖形顯示在窗口上
    canvas = FigureCanvasTkAgg(fig, master=Chart)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # 把matplotlib繪製的圖形顯示在tkinter窗口上
    toolbar = NavigationToolbar2Tk(canvas, Chart)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # 清除圖表按鈕
    clear_chart = tk.Button(Chart, text="清除圖表", font=('標楷體', 20), background='#ebedec', width=10, height=2,
                            command=Chart_clear)
    clear_chart.place(x=340, y=600)
    # 迴圈
    Chart.mainloop()

# 系統管理員新增視窗
def admin_select_Radiobutton(radio_text):
    # 新增系統和群組管理員
    if (radio_text.get() == "Add_all_staff"):
        Select_window = tk.Toplevel()  # 設定子系視窗
        Select_window.title("管理員選擇視窗(Administrator selection window)")  # 視窗圖示抬頭
        Select_window.geometry("600x530+800+130")  # 調整畫面大小和畫面位置設定
        Select_window.resizable(False, False)  # 限制視窗不能調整大小
        Select_window.config(background="white")  # 設定背景顏色
        Select_window.iconbitmap('system_photos/admin.ico')  # 視窗圖示
        # 文字
        label1 = Label(Select_window, text="選擇新增的管理者 Select new manager", font=("標楷體", 18),
                       background="#3981b3", foreground="white", width=50, height=2)
        label1.place(x=0, y=0)
        # 新增系統管理員按鈕
        add_admin_image = tk.PhotoImage(file='system_photos/admin.png')
        add_admin_button = tk.Button(Select_window, text='新增系統管理員 \nAdd system administrator', font=("標楷體", 25),
                                     image=add_admin_image,
                                     compound="top", background="#5eb1eb", foreground="white", width=500,
                                     command=add_admin_window)
        add_admin_button.place(x=45, y=100)
        # 新增群組管理員按鈕
        add_group_image = tk.PhotoImage(file='system_photos/group_manager.png')
        add_group_button = tk.Button(Select_window, text='新增群組管理員\nAdd group manager', font=("標楷體", 25),
                                     image=add_group_image,
                                     compound="top", background="#40cf5d", foreground="white", width=500,
                                     command=add_group_window)
        add_group_button.place(x=45, y=300)
        # 迴圈
        Select_window.mainloop()

    elif (radio_text.get() == "Personnel_identification_management"):
        # 系統管理員人員辨識管理
        personnel_identification()

    elif (radio_text.get() == "In_and_out_statistics_view"):
        # 辨識人員查看
        In_and_out_statistics_view()

    elif (radio_text.get() == "Identification_personnel_View"):
        # 進出統計查看
        Identification_personnel_View()

# 進入系統管理員(選擇視窗)
def administrator_radiobutton(user):
    # 返回登入視窗
    def return_login():
        administrator.destroy()  # 關閉視窗
        tk.messagebox.showinfo(title='登出 Sign out', message=user + '登出成功 Logout success.')

    administrator = tk.Toplevel(root)  # 設定父系視窗
    administrator.title("人員管制系統 Personnel control system(系統管理員)")  # 視窗圖示抬頭
    administrator.geometry("1000x700+50+50")  # 調整畫面大小和畫面位置設定
    administrator.resizable(False, False)  # 限制視窗不能調整大小
    administrator.config(background="#f7e4e4")  # 設定背景顏色
    administrator.iconbitmap('system_photos/admin.ico')  # 視窗圖示
    radio_text = StringVar()  # 選擇的選項
    radio_text.set(0)
    MODES = [
        ("新增全體人員", "Add_all_staff"),
        ("人員辨識管理", "Personnel_identification_management"),
        ("辨識人員查看", "Identification_personnel_View"),
        ("進出統計查看", "In_and_out_statistics_view"),
    ]
    # 文字
    user_text1 = tk.Label(administrator, font=("標楷體", 10), text="身分(Identity)",
                          background="#f7e4e4", foreground="green")
    user_text1.place(x=10, y=80)
    # 文字
    user_text1 = tk.Label(administrator, font=("標楷體", 15), text="系統管理員您好",
                          background="#f7e4e4", foreground="#212529")
    user_text1.place(x=10, y=100)
    # 文字
    user_text2 = tk.Label(administrator, font=("標楷體", 10), text="管理員名稱(Admin name)",
                          background="#f7e4e4", foreground="green")
    user_text2.place(x=10, y=130)
    # 使用者值的文字
    user_text2 = tk.Label(administrator, font=("標楷體", 15), text=user,
                          background="#f7e4e4", foreground="#212529")
    user_text2.place(x=10, y=150)
    # 時間格式設定
    time = '%Y-%m-%d %H:%M:%S'
    theTime = datetime.datetime.now().strftime(time)
    # 文字
    time_text1 = tk.Label(administrator, font=("標楷體", 10), text="登入日期、時間(Login date & Time)",
                          background="#f7e4e4", foreground="green")
    time_text1.place(x=10, y=180)
    # 時間值的文字
    time_text1 = tk.Label(administrator, font=("標楷體", 15), text=theTime,
                          background="#f7e4e4", foreground="#212529")
    time_text1.place(x=10, y=200)
    # 文字
    labFrame = LabelFrame(administrator, text="功能選單", font=("標楷體", 45), foreground="#DC143C",
                          background="#f7f7f7")
    labFrame.pack(ipadx=300, ipady=10, pady=50, padx=250, anchor=CENTER)
    # 顯示可以選擇值
    for text, mode in MODES:
        Radiobutton(labFrame, text=text, variable=radio_text, value=mode,
                    font=("標楷體", 38), background="#f7f7f7",
                    activeforeground="#1b18d6").pack(padx=15, pady=20, anchor=W)

    # 確認按鈕
    check_image = tk.PhotoImage(file='system_photos/check.png')
    Determine_button1 = Button(administrator, text="確定\n(Determine)", image=check_image,
                               compound="left", background="#61bf54", foreground="white", font=('標楷體', 25),
                               command=(partial(admin_select_Radiobutton, radio_text)))
    Determine_button1.place(x=260, y=605)
    # 登出按鈕
    logout_image = tk.PhotoImage(file='system_photos/logout.png')
    logout_button2 = Button(administrator, text="登出\n(Logout)", image=logout_image,
                            compound="left",
                            background="#b3dead", foreground="white", font=('標楷體', 25), command=return_login)
    logout_button2.place(x=530, y=605)
    # 迴圈
    administrator.mainloop()

#(1)人員辨識
def video():
    encoded = {}
    personnel_record = {}
    statistics1 = {}
    statistics = {}
    gender = ''
    age = ''
    #寄送email
    def Email():
        Email_Stop = threading.currentThread()#開始email
        while getattr(Email_Stop, "do_run", True):
            mime = MIMEMultipart('related')#組合html顯示內容
            mime["Subject"] = "[系統警告!]有陌生人員進入!!"  # 撰寫郵件標題
            mime["From"] = "人員管制系統"  # 撰寫你的暱稱或是信箱
            mime["To"] = ""  # 撰寫你要寄的人
            # mime["Cc"]="@gmail.com, @gmail.com" #副本收件人

            msgAlternative = MIMEMultipart('alternative')
            mime.attach(msgAlternative)

            # 以下為html內容
            mail_body = """
                                       <!DOCTYPE html>
                                       <html>
                                       <head>
                                           <meta charset="UTF-8">
                                           <title><strong>系統警告</strong></title>
                                           <style>
                                               h1#title{
                                               text-align:center;
                                               color:#38a5ff}
                                               h2#title1{color:#f77e7e;}
                                               table{border:3px solid #f5f5f5;padding-top:5px}
                                               th{background-color:#e3e8e3}
                                               td{text-align:center;}
                                               ul.circle{list-style-type:circle;}
                                               h2#title2{text-align:center;background-color:#6097b3;color:#73e2ff;}
                                               ul.square{list-style-type:square;color:#38a5ff;}
                                           </style>
                                       </head>
                                       <body>
                                           <h1 id="title">系統通知 System Notification</h1>
                                           <hr>
                                           <h2 id="title1">警告!! warning!!</h2>
                                           <p>有一位陌生人員於<a href="">%s</a>進入</p>
                                           <table border="1">
                                               <caption>陌生人員粗估資料</caption>
                                               <thead>
                                                   <tr><th>性別</th><th>年齡區間</th></tr>
                                               </thead>
                                               <tdoby>
                                                   <font size="5"><tr><td>%s</td> <td>%s</td></tr></font>
                                               </tdoby>
                                           </table>
                                           <p>照片：</p>
                                           <img src="cid:send_image" width="300">
                                           <ul class="circle">
                                               <li>本郵件是由系統自動寄送，請勿直接回覆。</li>
                                               <li>如有任何問題，請聯絡系統管理員。</li>
                                           </ul>
                                           <h2 id="title2">系統安全公告事項 System Security Notice</h2>
                                           <ul class="square">   
                                                <li>請勿隨意下載來路不明的程式或電子郵件，及使用公共場所之電腦。</li>
                                                <li>勿隨意洩漏您的帳戶資料或個人資料 (如個人生日、身分證字號...等 )。</li>
                                                <li>為了預防您離開電腦過久，以至遭他人竊用，若您欲離開帳戶，敬請務必執行登出，以保障您的權益及帳戶安全。</li>
                                                <li>請支持正版系統，勿裝來路不明的系統以免個資外洩或導致電腦中毒。</li>
                                           </ul>
                                           <hr>
                                           <p>亞東技術學院 電子工程系版權所有 ©Copyright 2020, GuanLinHu and GinJayTan,All Rights Reserved.</p>
                                       </body>
                                       </html>
                                       """
            msgText1 = mail_body % (date_now, gender, age)
            msgText = (MIMEText(msgText1, 'html', 'utf-8'))
            msgAlternative.attach(msgText)

            # 指定圖片為當前目錄
            fp = open('photo_comparison/Unknown.png', 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()

            # 定義圖片 ID，在 HTML 文字中參照
            msgImage.add_header('Content-ID', '<send_image>')
            mime.attach(msgImage)

            msg = mime.as_string()  # 將msg將text轉成str

            smtp = smtplib.SMTP("smtp.gmail.com", 587)  # googl的ping
            smtp.ehlo()  # 申請身分
            smtp.starttls()  # 加密文件，避免私密信息被截取
            smtp.login('oitroot@gmail.com', 'rootmailoit')
            from_addr = "oitroot@gmail.com"
            to_addr = ["alan011134@gmail.com"]
            status = smtp.sendmail(from_addr, to_addr, msg)
            '''
            if status == {}:
                print("郵件傳送成功!")
            else:
                print("郵件傳送失敗!")
            '''
            smtp.quit()#結束
            time.sleep(1)#等待1秒
        return

    def highlightFace(net, frame, conf_threshold=0.7):
        frameOpencvDnn = frame.copy()
        frameHeight = frameOpencvDnn.shape[0]
        frameWidth = frameOpencvDnn.shape[1]
        # 讀取圖像
        blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)
        # print(blob)
        # 輸入圖像傳遞到網絡來獲得輸出，得到置信度和位置。
        net.setInput(blob)
        # 輸出結果
        detections = net.forward()

        faceBoxes = []
        for i in range(detections.shape[2]):  # 矩陣的第二行
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                faceBoxes.append([x1, y1, x2, y2])
        return frameOpencvDnn, faceBoxes
    #使用模型
    faceProto = "../thematic personnel control system/identify_documents/opencv_face_detector.pbtxt"
    faceModel = "../thematic personnel control system/identify_documents/opencv_face_detector_uint8.pb"
    ageProto = "../thematic personnel control system/identify_documents/age_deploy.prototxt"
    ageModel = "../thematic personnel control system/identify_documents/age_net.caffemodel"
    genderProto = "../thematic personnel control system/identify_documents/gender_deploy.prototxt"
    genderModel = "../thematic personnel control system/identify_documents/gender_net.caffemodel"

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList = ['Male', 'Female']
    # 加載Tensorflow網絡模塊
    faceNet = cv2.dnn.readNet(faceModel, faceProto)
    ageNet = cv2.dnn.readNet(ageModel, ageProto)
    genderNet = cv2.dnn.readNet(genderModel, genderProto)

    cap = cv2.VideoCapture(0)  # 創建一個 VideoCapture 對象
    #找尋要辨識的資料照片
    for dirpath, dnames, fnames in os.walk("../thematic personnel control system/Person_identification_photos"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                # 資料夾姓名
                face = fr.load_image_file("../thematic personnel control system/Person_identification_photos/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    faces_encoded = list(encoded.values())  # values() 函数以列表返回字典中的所有值
    known_face_names = list(encoded.keys())  # keys() 函数以列表返回一个字典所有的
    '''
    防止Person_identification_photos資料夾沒照片警告使用者
    '''
    if faces_encoded == []:
        tk.messagebox.showerror(title="錯誤 Error",
                                message='人員辨識資料夾沒有照片，請到人員辨識管理新增照片。\nThere are no photos in the personnel identification folder, please go to the personnel identification management to add photos.')
        cap.release()  # 釋放攝像頭
        cv2.destroyAllWindows()  # 刪除建立的全部窗口
    elif known_face_names == []:
        tk.messagebox.showerror(title="錯誤 Error",
                                message='人員辨識資料夾沒有照片，請到人員辨識新增照片。\nThere are no photos in the personnel identification folder, please go to the personnel identification management to add photos.')
    elif cap.isOpened() == False:
        tk.messagebox.showerror(title='錯誤 Error', message='沒有找到相機，請在試一次!! No camera found, please try again!!')
        cap.release()  # 釋放攝像頭
        cv2.destroyAllWindows()  # 刪除建立的全部窗口

    cap.set(cv2.CAP_PROP_FPS, 50)
    cap.set(3, 800)
    cap.set(4, 800)
    # 取得預設的臉部偵測器
    # detector = dlib.get_frontal_face_detector()
    # 根據shape_predictor方法載入68個特徵點模型，此方法為人臉表情識別的偵測器
    # predictor = dlib.shape_predictor( 'shape_predictor_68_face_landmarks.dat')
    padding = 20
    while (cap.isOpened()):  # 循環讀取每一幀
        ret, img = cap.read()
        if img is None:
            print("there is no img!")
            break
        resultImg, faceBoxes = highlightFace(faceNet, img)
        width = int(img.shape[1])
        height = int(img.shape[0])
        time_stamp = datetime.datetime.now()
        date_now = time_stamp.strftime('%Y.%m.%d-%H:%M:%S')
        cv2.putText(img, date_now, (int(width / 20), int(height / 8)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                    cv2.LINE_AA)

        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

        # 將圖片BGR颜色（OpenCV使用的）轉換為RGB颜色（face_recognition使用）
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = fr.face_locations(rgb_small_frame)
        unknown_face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in unknown_face_encodings:
            for faceBox in faceBoxes:
                face = img[max(0, faceBox[1] - padding):
                           min(faceBox[3] + padding, img.shape[0] - 1), max(0, faceBox[0] - padding)
                                                                        :min(faceBox[2] + padding, img.shape[1] - 1)]
                # 取深度學習模型的輸入(圖像本身,每個像素值的縮放,設定網絡的大小,訓練時候設定的模型均值,否要裁剪圖像並採取中心裁剪)
                blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                genderNet.setInput(blob)
                genderPreds = genderNet.forward()
                # 取陣列裡最大
                gender = genderList[genderPreds[0].argmax()]

                ageNet.setInput(blob)
                agePreds = ageNet.forward()
                age = ageList[agePreds[0].argmax()]

                if gender == 'Male':
                    cv2.putText(img, f'{gender}, {age}', (faceBox[0], faceBox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (255, 204, 0), 2, cv2.LINE_AA)
                else:
                    cv2.putText(img, f'{gender}, {age}', (faceBox[0], faceBox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (255, 0, 217), 2, cv2.LINE_AA)
            # 查看人臉是否與已知人臉匹配
            matches = fr.compare_faces(faces_encoded, face_encoding, tolerance=0.50)
            name = "Unknown"

            #使用歐式距離查找最接近的人臉
            face_distances = fr.face_distance(faces_encoded, face_encoding)
            best_match_index = numpy.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            img_file = '../thematic personnel control system/Personnel_in_and_out_photos'
            cv2.imwrite(os.path.join(img_file, name + '.png'), img)

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                #縮放後臉位置，因為我們檢測到的幀被縮放為1/4尺寸
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # 儲存進出人員
                with open('identify_documents/personnel_identification.pickle', 'rb') as personnel_file:
                    personnel_info = pickle.load(personnel_file)
                    personnel_record = personnel_info

                with open('identify_documents/statistics.pickle', 'rb') as statistics_file:
                    statistics_info = pickle.load(statistics_file)
                    statistics = statistics_info

                # 框選人臉
                if name == "Unknown":
                    # 設定多邊形頂點座標
                    pts1 = np.array([[left, top], [left + 30, top], [left, top], [left, top + 30]], np.int32)  # 左上角
                    pts2 = np.array(
                        [[left, top + 144], [left, top + 144 - 30], [left, top + 144], [left + 30, top + 144]],
                        np.int32)  # 左下角
                    pts3 = np.array([[right, bottom - 144], [right, bottom - 144 + 30], [right, bottom - 144],
                                     [right - 30, bottom - 144]], np.int32)  # 右上角
                    pts4 = np.array([[right, bottom], [right - 30, bottom], [right, bottom], [right, bottom - 30]],
                                    np.int32)  # 右下角
                    # 將座標轉為 (頂點數量, 1, 2) 的陣列
                    pts1 = pts1.reshape((-1, 1, 2))
                    pts2 = pts2.reshape((-1, 1, 2))
                    pts3 = pts3.reshape((-1, 1, 2))
                    pts4 = pts4.reshape((-1, 1, 2))
                    # 繪製多邊形
                    cv2.polylines(img, [pts1], True, (0, 0, 255), 4)
                    cv2.polylines(img, [pts2], True, (0, 0, 255), 4)
                    cv2.polylines(img, [pts3], True, (0, 0, 255), 4)
                    cv2.polylines(img, [pts4], True, (0, 0, 255), 4)

                    # Draw a label with a name below the face
                    cv2.rectangle(img, (left, bottom + 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(img, name, (left + 6, bottom + 30), font, 1.0, (255, 255, 255), 1)
                    time_now = datetime.datetime.now()
                    date_ymd = time_now.strftime('%Y/%m/%d')
                    if name in personnel_record and date_ymd in statistics and statistics != {}:
                        # 現在時間分割成(時)
                        time_now = date_now[17:19]
                        # 儲存時間分割成(時)
                        dictionary_time = personnel_record[name]['Time'][17:19]
                        # 相減得到(時)
                        update_time = int(time_now) - int(dictionary_time)
                        # print(update_time)
                        if update_time >= 5:
                            # 傳Email照片
                            img_file = '../thematic personnel control system/photo_comparison'
                            cv2.imwrite(os.path.join(img_file, name + '.png'), img)
                            Email_Send = threading.Thread(target=Email)
                            Email_Send.start()
                            time.sleep(1)
                            Email_Send.do_run = False
                        # 現在時間分割成(時)
                        time_now = date_now[14:16]
                        # 儲存時間分割成(時)
                        dictionary_time = personnel_record[name]['Time'][14:16]
                        # 相減得到(時)
                        update_time = int(time_now) - int(dictionary_time)

                        # 判斷否一分鐘再做一次寫入
                        if update_time >= 1:
                            with open('identify_documents/personnel_identification.pickle', 'wb') as personnel_file:
                                personnel_record[name] = {'Name': name, 'Gender': gender, 'Age': age, 'Time': date_now,
                                                          'number_of_in_and_out': +1, 'situation': '警告'}
                                pickle.dump(personnel_record, personnel_file)
                            if gender == 'Male':
                                time_now = datetime.datetime.now()
                                date_ymd = time_now.strftime('%Y/%m/%d')
                                if gender == "":
                                    pass
                                with open('identify_documents/statistics.pickle', 'wb') as statistics_file:
                                    statistics[date_ymd] = {
                                        'total_people_in_and_out': int(
                                            statistics[date_ymd]['total_people_in_and_out']) + 1,
                                        'number_of_boys': int(statistics[date_ymd]['number_of_boys']) + 1,
                                        'number_of_girls': int(statistics[date_ymd]['number_of_girls']),
                                        'number_of_strangers': int(statistics[date_ymd]['number_of_strangers']) + 1}
                                    pickle.dump(statistics, statistics_file)
                            elif gender == 'Female':
                                time_now = datetime.datetime.now()
                                date_ymd = time_now.strftime('%Y/%m/%d')
                                if gender == "":
                                    pass
                                with open('identify_documents/statistics.pickle', 'wb') as statistics_file:
                                    statistics[date_ymd] = {
                                        'total_people_in_and_out': int(
                                            statistics[date_ymd]['total_people_in_and_out']) + 1,
                                        'number_of_boys': int(statistics[date_ymd]['number_of_boys']),
                                        'number_of_girls': int(statistics[date_ymd]['number_of_girls']) + 1,
                                        'number_of_strangers': int(statistics[date_ymd]['number_of_strangers']) + 1}
                                    pickle.dump(statistics, statistics_file)

                        else:
                            with open('identify_documents/personnel_identification.pickle', 'wb') as personnel_file:
                                personnel_record[name] = {'Name': name, 'Gender': gender, 'Age': age, 'Time': date_now,
                                                          'number_of_in_and_out': +1, 'situation': '警告'}
                                personnel_file = pickle.dump(personnel_record, personnel_file)

                            if gender == 'Male':
                                time_now = datetime.datetime.now()
                                date_ymd = time_now.strftime('%Y/%m/%d')
                                if gender == "":
                                    pass

                                with open('identify_documents/statistics.pickle', 'wb') as statistics_file:
                                    statistics[date_ymd] = {
                                        'total_people_in_and_out': int(
                                            statistics[date_ymd]['total_people_in_and_out']) + 1,
                                        'number_of_boys': int(statistics[date_ymd]['number_of_boys']) + 1,
                                        'number_of_girls': int(statistics[date_ymd]['number_of_girls']),
                                        'number_of_strangers': int(statistics[date_ymd]['number_of_strangers']) + 1}
                                    pickle.dump(statistics, statistics_file)
                                    # print(statistics)
                            elif gender == 'Female':
                                time_now = datetime.datetime.now()
                                date_ymd = time_now.strftime('%Y/%m/%d')

                                if gender == "":
                                    pass
                                with open('identify_documents/statistics.pickle', 'wb') as statistics_file:
                                    statistics[date_ymd] = {
                                        'total_people_in_and_out': int(
                                            statistics[date_ymd]['total_people_in_and_out']) + 1,
                                        'number_of_boys': int(statistics[date_ymd]['number_of_boys']),
                                        'number_of_girls': int(statistics[date_ymd]['number_of_girls']) + 1,
                                        'number_of_strangers': int(statistics[date_ymd]['number_of_strangers']) + 1}
                                    pickle.dump(statistics, statistics_file)

                            # 傳Email照片
                            img_file = '../thematic personnel control system/photo_comparison'
                            cv2.imwrite(os.path.join(img_file, name + '.png'), img)
                            Email_Send = threading.Thread(target=Email)
                            Email_Send.start()
                            time.sleep(1)
                            Email_Send.do_run = False

                    else:
                        with open('identify_documents/personnel_identification.pickle', 'wb') as personnel_file:
                            personnel_record[name] = {'Name': name, 'Gender': gender, 'Age': age, 'Time': date_now,
                                                      'number_of_in_and_out': +1, 'situation': '警告'}
                            personnel_file = pickle.dump(personnel_record, personnel_file)

                        if gender == 'Male':
                            time_now = datetime.datetime.now()
                            date_ymd = time_now.strftime('%Y/%m/%d')
                            if gender == "":
                                pass
                            '''
                            with open('identify_documents/statistics.pickle', 'wb') as statistics_file:
                                statistics[date_ymd] = {
                                    'total_people_in_and_out': int(statistics[date_ymd]['total_people_in_and_out']) + 1,
                                    'number_of_boys': int(statistics[date_ymd]['number_of_boys']) + 1,
                                    'number_of_girls': int(statistics[date_ymd]['number_of_girls']),
                                    'number_of_strangers': int(statistics[date_ymd]['number_of_strangers']) + 1}
                                pickle.dump(statistics, statistics_file)
                                # print(statistics)
                               
                        elif gender == 'Female':
                            time_now = datetime.datetime.now()
                            date_ymd = time_now.strftime('%Y/%m/%d')
                            if gender == "":
                                pass
                            with open('identify_documents/statistics.pickle', 'wb') as statistics_file:
                                statistics[date_ymd] = {
                                    'total_people_in_and_out': int(statistics[date_ymd]['total_people_in_and_out']) + 1,
                                    'number_of_boys': int(statistics[date_ymd]['number_of_boys']),
                                    'number_of_girls': int(statistics[date_ymd]['number_of_girls']) + 1,
                                    'number_of_strangers': int(statistics[date_ymd]['number_of_strangers']) + 1}
                                pickle.dump(statistics, statistics_file)
                                # print(statistics)
                        # 傳Email照片
                        img_file = '../thematic personnel control system/photo_comparison'
                        cv2.imwrite(os.path.join(img_file, name + '.png'), img)
                        Email_Send = threading.Thread(target=Email)
                        Email_Send.start()
                        time.sleep(1)
                        Email_Send.do_run = False
'''
                else:
                    # 設定多邊形頂點座標
                    pts1 = np.array([[left, top], [left + 30, top], [left, top], [left, top + 30]], np.int32)  # 左上角
                    pts2 = np.array(
                        [[left, top + 144], [left, top + 144 - 30], [left, top + 144], [left + 30, top + 144]],
                        np.int32)  # 左下角
                    pts3 = np.array([[right, bottom - 144], [right, bottom - 144 + 30], [right, bottom - 144],
                                     [right - 30, bottom - 144]], np.int32)  # 右上角
                    pts4 = np.array([[right, bottom], [right - 30, bottom], [right, bottom], [right, bottom - 30]],
                                    np.int32)  # 右下角
                    # 將座標轉為 (頂點數量, 1, 2) 的陣列
                    pts1 = pts1.reshape((-1, 1, 2))
                    pts2 = pts2.reshape((-1, 1, 2))
                    pts3 = pts3.reshape((-1, 1, 2))
                    pts4 = pts4.reshape((-1, 1, 2))
                    # 繪製多邊形
                    cv2.polylines(img, [pts1], True, (0, 255, 0), 4)
                    cv2.polylines(img, [pts2], True, (0, 255, 0), 4)
                    cv2.polylines(img, [pts3], True, (0, 255, 0), 4)
                    cv2.polylines(img, [pts4], True, (0, 255, 0), 4)
                    # 框選人臉
                    cv2.rectangle(img, (left, bottom + 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(img, name, (left + 6, bottom + 30), font, 1.0, (255, 255, 255), 1)
                    time_now = datetime.datetime.now()
                    date_ymd = time_now.strftime('%Y/%m/%d')
                    # 把人員資料寫到字典陣列裡
                    if name in personnel_record and date_ymd in statistics and statistics != {}:
                        # 現在時間分割成(時)
                        time_now = date_now[14:16]
                        # 儲存時間分割成(時)
                        dictionary_time = personnel_record[name]['Time'][14:16]
                        # 相減得到(時)
                        update_time = int(time_now) - int(dictionary_time)
                        # 判斷否兩分鐘再做一次寫入
                        if update_time >= 2:
                            if (int(personnel_record[name]['number_of_in_and_out']) % 2) == 0:
                                with open('identify_documents/personnel_identification.pickle', 'wb') as personnel_file:
                                    personnel_record[name] = {'Name': name, 'Gender': gender, 'Age': age,
                                                              'Time': date_now,
                                                              'number_of_in_and_out': int(
                                                                  personnel_record[name]['number_of_in_and_out']) + 1,
                                                              'situation': '進入中'}
                                    personnel_file = pickle.dump(personnel_record, personnel_file)
                                    # print(personnel_record)
                                if gender == 'Male':
                                    time_now = datetime.datetime.now()
                                    date_ymd = time_now.strftime('%Y/%m/%d')
                                    if gender == "":
                                        pass
                                    with open('identify_documents/statistics.pickle', 'wb') as statistics_file:
                                        statistics[date_ymd] = {'total_people_in_and_out': int(
                                            statistics[date_ymd]['total_people_in_and_out']) + 1, 'number_of_boys': int(
                                            statistics[date_ymd]['number_of_boys']) + 1, 'number_of_girls': int(
                                            statistics[date_ymd]['number_of_girls']), 'number_of_strangers': int(
                                            statistics[date_ymd]['number_of_strangers'])}
                                        pickle.dump(statistics, statistics_file)
                                        # print(statistics)
                                elif gender == 'Female':
                                    time_now = datetime.datetime.now()
                                    date_ymd = time_now.strftime('%Y/%m/%d')
                                    if gender == "":
                                        pass
                                    with open('identify_documents/statistics.pickle', 'wb') as statistics_file:
                                        statistics[date_ymd] = {'total_people_in_and_out': int(
                                            statistics[date_ymd]['total_people_in_and_out']) + 1, 'number_of_boys': int(
                                            statistics[date_ymd]['number_of_boys']), 'number_of_girls': int(
                                            statistics[date_ymd]['number_of_girls']) + 1, 'number_of_strangers': int(
                                            statistics[date_ymd]['number_of_strangers'])}
                                        pickle.dump(statistics, statistics_file)
                                        # print(statistics)
                            else:
                                with open('identify_documents/personnel_identification.pickle', 'wb') as personnel_file:
                                    personnel_record[name] = {'Name': name, 'Gender': gender, 'Age': age,
                                                              'Time': date_now,
                                                              'number_of_in_and_out': int(
                                                                  personnel_record[name]['number_of_in_and_out']) + 1,
                                                              'situation': '已出去中'}
                                    pickle.dump(personnel_record, personnel_file)

                                if gender == 'Male':
                                    time_now = datetime.datetime.now()
                                    date_ymd = time_now.strftime('%Y/%m/%d')
                                    if gender == "":
                                        pass
                                    with open('identify_documents/statistics.pickle', 'wb') as statistics_file:
                                        statistics[date_ymd] = {'total_people_in_and_out': int(
                                            statistics[date_ymd]['total_people_in_and_out']) + 1, 'number_of_boys': int(
                                            statistics[date_ymd]['number_of_boys']) + 1, 'number_of_girls': int(
                                            statistics[date_ymd]['number_of_girls']), 'number_of_strangers': int(
                                            statistics[date_ymd]['number_of_strangers'])}
                                        pickle.dump(statistics, statistics_file)

                                elif gender == 'Female':
                                    time_now = datetime.datetime.now()
                                    date_ymd = time_now.strftime('%Y/%m/%d')
                                    if gender == "":
                                        pass
                                    with open('identify_documents/statistics.pickle', 'wb') as statistics_file:
                                        statistics[date_ymd] = {'total_people_in_and_out': int(
                                            statistics[date_ymd]['total_people_in_and_out']) + 1, 'number_of_boys': int(
                                            statistics[date_ymd]['number_of_boys']), 'number_of_girls': int(
                                            statistics[date_ymd]['number_of_girls']) + 1, 'number_of_strangers': int(
                                            statistics[date_ymd]['number_of_strangers'])}
                                        pickle.dump(statistics, statistics_file)

                    else:
                        with open('identify_documents/personnel_identification.pickle', 'wb') as personnel_file:
                            personnel_record[name] = {'Name': name, 'Gender': gender, 'Age': age, 'Time': date_now,
                                                      'number_of_in_and_out': +1, 'situation': '進入中'}

                            pickle.dump(personnel_record, personnel_file)

                        time_now = datetime.datetime.now()
                        date_ymd = time_now.strftime('%Y/%m/%d')
                        if gender == 'Male':
                            if gender == "":
                                pass
                            with open('identify_documents/statistics.pickle', 'wb') as statistics_file:
                                statistics[date_ymd] = {'total_people_in_and_out': +1, 'number_of_boys': +1,
                                                        'number_of_girls': +0, 'number_of_strangers': +0}
                                pickle.dump(statistics, statistics_file)

                        elif gender == 'Female':
                            if gender == "":
                                pass
                            with open('identify_documents/statistics.pickle', 'wb') as statistics_file:
                                statistics[date_ymd] = {'total_people_in_and_out': +1, 'number_of_boys': +0,
                                                        'number_of_girls': +1, 'number_of_strangers': +0}
                                pickle.dump(statistics, statistics_file)


        cv2.imshow("Person identification", img)  # 窗口顯示，顯示名為 Capture_Test

        k = cv2.waitKey(1) & 0xFF  # 每幀數據延時 1ms，延時不能為 0，否則讀取的結果會是靜態幀
        if k == ord("q") or k == 27:  # 若檢測到按鍵 ‘q’，退出
            break
    cap.release()  # 釋放攝像頭
    cv2.destroyAllWindows()  # 刪除建立的全部窗口

#(2)群組管理員人員查看
def View_identification_personnel():
    # 取得索引值
    def treeSelect(event):
        global select_item
        widgetobj = event.widget  # 取得控件
        itemselected = widgetobj.selection()[0]  # 取得選項
        col1 = widgetobj.item(itemselected, "value")[0]  # 取得第0欄位內容
        str = "{0}".format(col1)
        select_item = str
    # 更新
    def update():
        group_View_identification.destroy()  # 關閉視窗
        View_identification_personnel()
    files_data = {}
    # 指定要列出所有檔案的目錄
    path = "../thematic personnel control system/Person_identification_photos"
    # 取得所有檔案與子目錄名稱
    files = listdir(path)
    All_lengths = len(files)
    data_loop = 0
    rowCount = 1
    for file_name in files:
        # 產生檔案的絕對路徑
        fullpath = join(path, file_name)
        t = os.stat(fullpath)
        t1 = time.localtime(t.st_mtime)

        all_time = [t1[0], '/', t1[1], '/', t1[2], ' ', t1[3], ':', t1[4], ':', t1[5]]
        set_up_time = ''
        # 檔案建立時間合併(使用迴圈)
        for time_loop in all_time:
            set_up_time += str(time_loop)
        # 檔案訪問時間
        interview_time = (time.ctime(t.st_atime))
        # 檔案大小
        size = os.path.getsize(fullpath)
        size = int(round(size / 1000))
        # 把檔案名稱、檔案建立時間、檔案大小、檔案訪問時間做陣列合併
        if data_loop != All_lengths:
            files_data[data_loop] = [file_name, set_up_time, size, interview_time]
            data_loop += 1

    group_View_identification = tk.Toplevel()#設定子系視窗
    group_View_identification.title("查看識別人員View Identification Personnel")#視窗圖示抬頭
    group_View_identification.geometry("800x400+800+130")#調整畫面大小和畫面位置設定
    group_View_identification.resizable(False, False)#限制視窗不能調整大小
    group_View_identification.config(background="white")#設定背景顏色
    group_View_identification.iconbitmap('system_photos/admin.ico')#視窗圖示

    # 建立Treeview
    tree = ttk.Treeview(group_View_identification, columns=['1', '2', '3', '4'], show='headings')
    # y軸滾動條
    yscrollbar = ttk.Scrollbar(group_View_identification, orient="vertical", command=tree.yview)
    yscrollbar.place(x=750, y=0, height=235)
    tree.configure(yscrollcommand=yscrollbar.set)
    # 格式化欄標題
    tree.column('1', width=200, anchor='center')
    tree.column('2', width=200, anchor='center')
    tree.column('3', width=100, anchor='center')
    tree.column('4', width=200, anchor='center')
    # 建立內容，#行號從0算起偶數行用顏色當底
    tree.tag_configure("evenColor", background="#fc8dfc")
    tree.tag_configure("nodata", background="#f55d5d")
    # 建立欄標題
    tree.heading('1', text='檔名')
    tree.heading('2', text='日期')
    tree.heading('3', text='大小(KB)')
    tree.heading('4', text='訪問時間')

    # 資料夾沒資料顯示無資料
    if (All_lengths == 0):
        tree.insert('', index=0, text="無資料", values='無資料', tags=("nodata"))
    for k in range(0, All_lengths):
        if (rowCount % 2 == 1):  # 如果成立是基數
            tree.insert('', index=k, values=files_data[k])
        else:
            tree.insert('', index=k, values=files_data[k], tags=("evenColor"))
        rowCount += 1  # 行號數加1
    tree.bind("<<TreeviewSelect>>", treeSelect)  # Treeview控制Select發生
    tree.pack()
    #更新按鈕
    rubtn = tk.Button(group_View_identification, text="更新(Update)", font=('標楷體', 20), width=12, command=update,background="#e0519d",foreground="white")
    rubtn.place(x=320, y=250)
    #迴圈
    group_View_identification.mainloop()

#(3)新增群組管理員介面
def add_group_window():
    #即時拍照
    def photo_now():
        def again_picture():
            take_a_photo_now.destroy()
            photo_now()
        def confirm_imag():
            Photo_name = Photo_name_data.get()
            img_file = '../thematic personnel control system/user_photo_profile'
            cv2.imwrite(os.path.join(img_file, Photo_name + '.png'), bgra_cv2image)
            tk.messagebox.showinfo(title='拍照成功 Take a picture successfully', message='您以新增照片成功\nYou successfully added a photo')
            take_a_photo_now.destroy()
            photo_now()
        # 按下照相按鈕
        def take_pictures_picture():
            cv2image = cv2.cvtColor(bgra_cv2image, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
            image_change = Image.fromarray(cv2image)  # 将图像转换成Image对象
            imgshow = ImageTk.PhotoImage(image=image_change)
            Photo_confirmation_box.imgtk = imgshow
            Photo_confirmation_box.config(image=imgshow)
            camera.release()
            take_pictures.config(state=tk.DISABLED)  # 把登入辨識的按鈕停止
            again.config(state=tk.NORMAL)  # 把登入辨識的按鈕開啟
            confirm_photo.config(state=tk.NORMAL)  # 把登入辨識的按鈕開啟
            tk.messagebox.showwarning('提醒!!remind!!','拍照完成請確認照片\nPlease confirm the photo after taking a photo')
            # cv2.destroyAllWindows()
            # img_file = '../thematic personnel control system/user_photo_profile'
            # cv2.imwrite(os.path.join(img_file,Photo_name+'.png'), bgra_cv2image)

        # 姓名輸入完成按下按鈕開啟照相機
        def camera_program():
            global bgra_cv2image
            Photo_name.config(state=tk.DISABLED)  # 把登入辨識的按鈕停止
            Photo_name_complete.config(state=tk.DISABLED)  # 把登入辨識的按鈕停止
            take_pictures.config(state=tk.NORMAL)
            success, img = camera.read()  # 从摄像头读取照片
            cv2.waitKey(10)
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
            classfier = cv2.CascadeClassifier("../thematic personnel control system/identify_documents/haarcascade_frontalface_alt.xml")
            faceRects = classfier.detectMultiScale(cv2image, scaleFactor=1.8, minNeighbors=3, minSize=(30, 30))
            Photo_name_value = Photo_name_data.get()
            if camera.isOpened() == False:
                tk.messagebox.showerror(title='錯誤 Error', message='沒有找到相機，請在試一次!! No camera found, please try again!!')
                camera.release()  # 釋放攝像頭
                cv2.destroyAllWindows()
            elif Photo_name_value == "":
                tk.messagebox.showerror(title='錯誤 Error', message='您的姓名是空的，請重新輸入!! Your name is empty, please re-enter!!')
                take_a_photo_now.destroy()
                photo_now()
                camera.release()  # 釋放攝像頭
                cv2.destroyAllWindows()
            elif len(faceRects) > 0:  # 大於0則檢測到人臉
                for i in range(0, 3):
                    for faceRect in faceRects:  # 單獨框出每一張人臉
                        x, y, w, h = faceRect
                        cv2.rectangle(cv2image, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 255, 0), 2)
                        image = cv2image[y - 10: y + h + 10, x - 10: x + w + 10]
                        bgra_cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
            image_change = Image.fromarray(cv2image)  # 将图像转换成Image对象
            imgshow = ImageTk.PhotoImage(image=image_change)
            image_frame_label.imgtk = imgshow
            image_frame_label.config(image=imgshow)
            root.after(1, camera_program)
        take_a_photo_now = tk.Toplevel()
        take_a_photo_now.title("立即拍照 Take A Photo Now")
        take_a_photo_now.geometry("800x700+350+80")
        take_a_photo_now.resizable(False, False)  # 限制視窗不能調整大小
        take_a_photo_now.config(background="#f0faf9")
        take_a_photo_now.iconbitmap('system_photos/photo_now_ico.ico')
        Photo_Now_label = Label(take_a_photo_now, text="立即拍照 Take A Photo Now",
                                font=("標楷體", 18), background="white", width=67, height=2)
        Photo_Now_label.place(x=0, y=0)

        Photo_name_label = tk.Label(take_a_photo_now, font=("標楷體", 15), background="#f0faf9", text="請輸入照片姓名*")
        Photo_name_label.place(x=30, y=70)

        text_label = tk.Label(take_a_photo_now, font=("標楷體", 10), background="#f0faf9", text="(請輸入英文 例如:Chen Xiaomin)")
        text_label.place(x=350, y=110)

        Photo_name_data = tk.StringVar()
        Photo_name = tk.Entry(take_a_photo_now, font=("標楷體", 25),
                              background="white",
                              foreground="black", textvariable=Photo_name_data)
        Photo_name.place(x=250, y=70, width=500)

        Photo_name_complete = tk.Button(take_a_photo_now, text="輸入完成(Input Complete)",
                                        compound="left", background="#61bf54",
                                        foreground="white", font=('標楷體', 20))
        Photo_name_complete.place(x=325, y=140)

        take_pictures_label = tk.Label(take_a_photo_now,
                                       font=("標楷體", 20), background="#f0faf9", text="拍照")
        take_pictures_label.place(x=190, y=200)

        Photo_confirmation_label = tk.Label(take_a_photo_now,
                                            font=("標楷體", 20), background="#f0faf9", text="照片確認")
        Photo_confirmation_label.place(x=520, y=200)

        image_frame_label = tk.Label(take_a_photo_now, foreground="#e3962b", width=330, height=300, background="#f0faf9")
        image_frame_label.place(x=40, y=250)

        Photo_confirmation_box = tk.Label(take_a_photo_now, foreground="#e3962b", width=330, height=300, background="#f0faf9")
        Photo_confirmation_box.place(x=400, y=250)

        take_pictures_image = tk.PhotoImage(file='system_photos/take_pictures.png')
        take_pictures = tk.Button(take_a_photo_now, image=take_pictures_image, border=0,
                                  compound="left", background="green",
                                  foreground="white", font=('標楷體', 20))
        take_pictures.place(x=180, y=600)

        again_image = tk.PhotoImage(file='system_photos/return_take_pictures.png')
        again = tk.Button(take_a_photo_now, image=again_image, border=0,
                          compound="left", background="green",
                          foreground="white", font=('標楷體', 20))
        again.place(x=365, y=600)

        confirm_photo_image = tk.PhotoImage(
            file='system_photos/Photo_confirmation.png')
        confirm_photo = tk.Button(take_a_photo_now, image=confirm_photo_image, border=0,
                                  compound="left", background="green",
                                  foreground="white", font=('標楷體', 20))
        confirm_photo.place(x=550, y=600)
        take_pictures.config(state=tk.DISABLED)  # 把登入辨識的按鈕停止
        again.config(state=tk.DISABLED)  # 把臉部辨識的按鈕停止
        confirm_photo.config(state=tk.DISABLED)  # 把臉部辨識的按鈕停止
        camera = cv2.VideoCapture(0)  # 攝像頭

        Photo_name_complete.config(command=camera_program)
        take_pictures.config(command=take_pictures_picture)
        again.config(command=again_picture)
        confirm_photo.config(command=confirm_imag)

        take_a_photo_now.mainloop()
    #查看群組管理者照片和帳戶內容
    def View_photos_and_account():

        # 群組帳戶刪除管理
        def account_delete():
            del group_info1[select_item]
            # 更新pickle數據
            with open('identify_documents/group_account_secret.pickle', 'wb') as group_file:
                group_file = pickle.dump(group_info1, group_file)
                tk.messagebox.showinfo(title='成功 success', message=select_item + ' 照片已刪除成功 Photo deleted successfully')
        #群組帳戶照片刪除管理
        def picture_delete():
            confirm_delete = tk.messagebox.askokcancel("刪除照片", message='您確定要刪除' + select_item + '照片嗎?')
            #把列表treeview清空
            if confirm_delete == True:
                iids = tree.selection()
                for iid in iids:
                    tree.delete(iid)
                try:
                    os.remove(r"../thematic personnel control system/user_photo_profile/" + select_item)
                except OSError as Error:
                    tk.messagebox.showerror(title="錯誤 Error", message='錯誤訊息:' + Error)
                else:
                    tk.messagebox.showinfo(title='成功 success',
                                           message=select_item + ' 照片已刪除成功 Photo deleted successfully')
        #取得索引值
        def treeSelect(event):
            global select_item
            widgetobj = event.widget  # 取得控件
            itemselected = widgetobj.selection()[0]  # 取得選項
            col1 = widgetobj.item(itemselected, "value")[0]  # 取得第0欄位內容
            str = "{0}".format(col1)
            select_item = str
        #更新
        def update():
            View_photos_and_account_contents.destroy()  # 關閉視窗
            View_photos_and_account()  # 開啟視窗

        files_data = {}
        # 指定要列出所有檔案的目錄
        path = "../thematic personnel control system/user_photo_profile"
        # 取得所有檔案與子目錄名稱
        files = listdir(path)
        All_lengths = len(files)
        data_loop = 0
        rowCount = 1
        for file_name in files:
            # 產生檔案的絕對路徑
            fullpath = join(path, file_name)
            t = os.stat(fullpath)
            t1 = time.localtime(t.st_mtime)

            all_time = [t1[0], '/', t1[1], '/', t1[2], ' ', t1[3], ':', t1[4], ':', t1[5]]
            set_up_time = ''
            # 檔案建立時間合併(使用迴圈)
            for time_loop in all_time:
                set_up_time += str(time_loop)
            # 檔案訪問時間
            interview_time = (time.ctime(t.st_atime))
            # 檔案大小
            size = os.path.getsize(fullpath)
            size = int(round(size / 1000))
            # 把檔案名稱、檔案建立時間、檔案大小、檔案訪問時間做陣列合併
            if data_loop != All_lengths:
                files_data[data_loop] = [file_name, set_up_time, size, interview_time]
                data_loop += 1

        View_photos_and_account_contents = tk.Toplevel()#設定子系視窗
        View_photos_and_account_contents.title("查看群組管理員照片和帳戶內容 View group manager photos and account contents")#視窗圖示抬頭
        View_photos_and_account_contents.geometry("1000x800+800+130")#調整畫面大小和畫面位置設定
        View_photos_and_account_contents.resizable(False, False)#限制視窗不能調整大小
        View_photos_and_account_contents.config(background="white")#設定背景顏色
        View_photos_and_account_contents.iconbitmap('system_photos/admin.ico')#視窗圖示
        #文字
        View_Group_Administrator_Account = Label(View_photos_and_account_contents,
                                                 text="查看群組管理員照片內容 View The Content Of The Group Administrator Account",
                                                 font=("標楷體", 18),
                                                 background="#2ff599", foreground="white", width=85, height=2)
        View_Group_Administrator_Account.place(x=0, y=0)

        # 建立Treeview
        tree = ttk.Treeview(View_photos_and_account_contents, columns=['1', '2', '3', '4'], show='headings')
        # y軸滾動條
        yscrollbar = ttk.Scrollbar(View_photos_and_account_contents, orient="vertical", command=tree.yview)
        yscrollbar.place(x=850, y=70, height=235)
        tree.configure(yscrollcommand=yscrollbar.set)
        # 格式化欄標題
        tree.column('1', width=200, anchor='center')
        tree.column('2', width=200, anchor='center')
        tree.column('3', width=100, anchor='center')
        tree.column('4', width=200, anchor='center')
        # 建立內容，#行號從0算起偶數行用顏色當底
        tree.tag_configure("evenColor", background="#2ff599")
        tree.tag_configure("nodata", background="#2ff599")
        # 建立欄標題
        tree.heading('1', text='檔名')
        tree.heading('2', text='日期')
        tree.heading('3', text='大小(KB)')
        tree.heading('4', text='訪問時間')

        # 資料夾沒資料顯示無資料
        if (All_lengths == 0):
            tree.insert('', index=0, text="無資料", values='無資料', tags=("nodata"))
        for k in range(0, All_lengths):
            if (rowCount % 2 == 1):  # 如果成立是基數
                tree.insert('', index=k, values=files_data[k])
            else:
                tree.insert('', index=k, values=files_data[k], tags=("evenColor"))
            rowCount += 1  # 行號數加1
        tree.bind("<<TreeviewSelect>>", treeSelect)  # Treeview控制Select發生
        tree.place(x=150, y=70)
        #更新按鈕
        rubtn = tk.Button(View_photos_and_account_contents, text="更新(Update)", font=('標楷體', 20), width=12, command=update,
                          background="#2ff599", foreground="white")
        rubtn.place(x=320, y=325)
        #刪除按鈕
        rubtn = tk.Button(View_photos_and_account_contents, text="刪除(delete)", font=('標楷體', 20), width=12, command=picture_delete,
                          background="#2ff599", foreground="white")
        rubtn.place(x=520, y=325)
        #文字
        View_Group_Administrator = Label(View_photos_and_account_contents,
                                         text="查看群組管理員帳戶內容 View the contents of the group manager account",
                                         font=("標楷體", 18),
                                         background="#2ff599", foreground="white", width=85, height=2)
        View_Group_Administrator.place(x=0, y=390)
        #讀取群組資料庫資料
        with open('identify_documents/group_account_secret.pickle', 'rb') as group_file:
            group_info1 = pickle.load(group_file)
            # 建立Treeview
            tree = ttk.Treeview(View_photos_and_account_contents, columns=['1'], show='headings')
            # y軸滾動條
            yscrollbar = ttk.Scrollbar(View_photos_and_account_contents, orient="vertical", command=tree.yview)
            yscrollbar.place(x=450, y=500, height=235)
            tree.configure(yscrollcommand=yscrollbar.set)
            # 格式化欄標題
            tree.column('1', width=300, anchor='center')
            # 建立內容，#行號從0算起偶數行用顏色當底
            tree.tag_configure("evenColor", background="#5cfab1")
            # 建立欄標題
            tree.heading('1', text='帳戶名稱')
            for i in group_info1:
                tree.insert('', index=END, values=i)
            tree.bind("<<TreeviewSelect>>", treeSelect)  # Treeview控制Select發生
            tree.place(x=150, y=500)
            #更新按鈕
            rubtn = tk.Button(View_photos_and_account_contents, text="更新(Update)", font=('標楷體', 20), width=12, command=update,
                              background="#2ff599", foreground="white")
            rubtn.place(x=600, y=550)
            #刪除按鈕
            rubtn = tk.Button(View_photos_and_account_contents, text="刪除(delete)", font=('標楷體', 20), width=12,
                              command=account_delete,
                              background="#2ff599", foreground="white")
            rubtn.place(x=600, y=650)
        #迴圈
        View_photos_and_account_contents.mainloop()

    # 新增群組管理員帳戶
    def add_group():
        #輸入框得到帳戶值
        accountnew = new_account1.get()
        # 輸入框得到密碼值
        passwordnew = new_password1.get()
        ##輸入框得到重複密碼值
        repasswordnew = new_re_password1.get()
        #讀取群組管理員帳戶的資料庫資料
        with open('identify_documents/group_account_secret.pickle', 'rb') as group_file:
            group_info = pickle.load(group_file)
        #檢查防範亂輸入造成的錯誤
        if passwordnew != repasswordnew:
            tk.messagebox.showinfo("錯誤 Error",
                                   "密碼和確認密碼不匹配請重新輸入\nPassword does not match confirmation password, please re-enter.")
            new_account1.set("")
            new_password1.set("")
            new_re_password1.set("")
        elif accountnew in group_info:
            tk.messagebox.showinfo("錯誤 Error",
                                   "用戶已經註冊過了!\n The user has already signed up!")
            new_account1.set("")
            new_password1.set("")
            new_re_password1.set("")
        elif accountnew == '':
            tk.messagebox.showinfo("錯誤 Error",
                                   "帳號不能空白請重新輸入!\n Account number cannot be blank, please re-enter!")
            new_account1.set("")
            new_password1.set("")
            new_re_password1.set("")
        elif passwordnew == '':
            tk.messagebox.showinfo("錯誤 Error",
                                   "密碼或確認密碼不能空白請重新輸入!\nThe password or confirmation password cannot be blank, please re-enter!")
            new_account1.set("")
            new_password1.set("")
            new_re_password1.set("")
        elif repasswordnew == "":
            tk.messagebox.showinfo("錯誤 Error",
                                   "密碼或確認密碼不能空白請重新輸入!\nThe password or confirmation password cannot be blank, please re-enter!")
            new_account1.set("")
            new_password1.set("")
            new_re_password1.set("")
        else:
            group_info[accountnew] = passwordnew  # 定義字典陣列加入用戶
            #寫入群組管理員帳戶的資料庫資料
            with open('identify_documents/group_account_secret.pickle', 'wb') as group_file:
                pickle.dump(group_info, group_file)
            tk.messagebox.showinfo("恭喜 Congratulations",
                                   "您已成功註冊帳戶\nYou have successfully registered an account.")
            new_account1.set("")
            new_password1.set("")
            new_re_password1.set("")

    #把選的照片顯示在Tkinter視窗上面
    def choose_file():
        def resize(w, h, w_box, h_box, pil_image):
            #對一個pil_image對象進行縮放，讓它在一個矩形框內，還能保持比例
            f1 = 1.0 * w_box / w
            f2 = 1.0 * h_box / h
            factor = min([f1, f2])  # 比較最小函數

            width = int(w * factor)  # 轉換成整數型態
            height = int(h * factor)  # 轉換成整數型態
            return pil_image.resize((width, height), Image.ANTIALIAS)

        # 期望圖像顯示的大小
        w_box = 250
        h_box = 250

        # 以一個PIL圖像對象打開
        global File
        File = filedialog.askopenfilename(parent=group_labframe1, initialdir="C:/",
                                          title='Choose an image.',
                                          filetypes=[('JPG', '*.jpg'), ('PNG', '*.png'), ('JFIF', '*.jfif'),
                                                     ('All Files', '*')])
        position.set(File)

        pil_image = Image.open(File)  # 讀寫方式打開
        # 獲取圖像的原始大小
        w, h = pil_image.size
        # 縮放圖像讓它保持比例，同時限制在一個矩形框範圍內
        pil_image_resized = resize(w, h, w_box, h_box, pil_image)
        # 把PIL圖像對象轉變爲Tkinter的PhotoImage對象
        global tk_imag
        tk_image = ImageTk.PhotoImage(pil_image_resized)
        # Label: 這個小工具，就是個顯示框，小窗口，把圖像大小顯示到指定的顯示框

        # image(畫布)
        canvas = tk.Canvas(group_labframe1, height=w_box, width=h_box, background="white")
        canvas.create_image(w_box, h_box, image=tk_image, anchor=SE)
        canvas.place(x=600, y=75)
        group_labframe1.mainloop()

    #新增照片
    def copy_img():

        if position.get() == "":
            tk.messagebox.showerror(title='錯誤 Error',
                                    message='請選擇您想要的照片。\n Please select the photo you want.')
            position.set("")
            admin_name.set("")

        elif admin_name.get() == "":
            tk.messagebox.showerror(title='錯誤 Error',
                                    message='請為照片命名。\n Please name your photo.')
            position.set("")
            admin_name.set("")

        else:
            image = tk.messagebox.askokcancel(title='確認 Confirm',
                                              message='請確認這是您要新增的相片。\n Please confirm this is the photo you want to add.')
            if image == True:
                local_img_name = File
                # 指定要複製的圖片路徑
                path = r'../thematic personnel control system/user_photo_profile'
                # 指定存放圖片的目錄
                shutil.copy(local_img_name, path)
                os.rename(os.path.join(File, position.get()), os.path.join(path, admin_name.get()))
                name = os.path.basename(position.get())
                os.remove('../thematic personnel control system/user_photo_profile/' + name)
                tk.messagebox.showinfo(title='恭喜 Congratulations', message='照片新增成功。\n Photo added successfully.')
                position.set("")
                admin_name.set("")

    add_group_account = tk.Toplevel()#設定子系視窗
    add_group_account.title("新增群組管理員帳戶 Add Group Manager Account")#視窗圖示抬頭
    add_group_account.geometry("1000x800+800+130")#調整畫面大小和畫面位置設定
    add_group_account.resizable(False, False)#限制視窗不能調整大小
    add_group_account.config(background="white")#設定背景顏色
    add_group_account.iconbitmap('system_photos/Group manager.ico')#視窗圖示
    #文字
    label1 = Label(add_group_account, text="新增群組管理員帳戶 Add Group Manager Account",
                   font=("標楷體", 18),
                   background="green", foreground="white", width=85, height=2)
    label1.place(x=0, y=0)
    #文字
    group_labframe = tk.LabelFrame(add_group_account,
                                   text="新增群組管理員帳戶(Add Group Manager Account)",
                                   font=("標楷體", 25), background="white")
    #文字
    add_group_accounttext = tk.Label(group_labframe,
                                     font=("標楷體", 15), background="white",
                                     foreground="green", text="帳號(Account Number)*")
    add_group_accounttext.place(x=0, y=30)
    #儲存帳號值
    new_account1 = tk.StringVar()
    add_group_accountentry = tk.Entry(group_labframe, font=("標楷體", 25),
                                      background="white",
                                      foreground="black", textvariable=new_account1)
    add_group_accountentry.place(x=350, y=30, width=600)
    #文字
    add_group_passwordtext = tk.Label(group_labframe,
                                      font=("標楷體", 15), background="white",
                                      foreground="green", text="密碼(Password)*")
    add_group_passwordtext.place(x=0, y=80)
    #儲存密碼值
    new_password1 = tk.StringVar()
    add_group_passworentry = tk.Entry(group_labframe, font=("標楷體", 25),
                                      background="white",show="‧",
                                      foreground="black", textvariable=new_password1)
    add_group_passworentry.place(x=350, y=80, width=600)
    #文字
    group_re_enter_passwordtext = tk.Label(group_labframe, font=("標楷體", 15),
                                           background="white",
                                           foreground="green",
                                           text="重新輸入密碼(Re-enter Password)*")
    group_re_enter_passwordtext.place(x=0, y=130)
    #儲存重新輸入值
    new_re_password1 = tk.StringVar()
    group_re_enter_passwordentry = tk.Entry(group_labframe, font=("標楷體", 25),
                                            background="white",
                                            foreground="black",show="‧",
                                            textvariable=new_re_password1)
    group_re_enter_passwordentry.place(x=350, y=130, width=600)
    #新增按鈕
    group_determine = tk.Button(group_labframe, text="確定新增(OK To Add)",compound="left", background="#61bf54",
                                foreground="white", font=('標楷體', 20),command=add_group)
    group_determine.place(x=500, y=180)
    group_labframe.pack(padx=0, pady=75, ipadx=500, ipady=135)

    # 新增系統管理員照片
    group_labframe1 = tk.LabelFrame(add_group_account,
                                    text="新增系統館理員照片(Add System Administator Photo)",
                                    font=("標楷體", 25), background="white")
    #儲存照片路徑值
    position = tk.StringVar()
    position_text = tk.Entry(group_labframe1, width=40, font=('標楷體', 30),
                             selectborderwidth=50, justify=LEFT, textvariable=position)
    position_text.place(x=0, y=20)
    #選擇檔案按鈕
    select_file = tk.Button(group_labframe1, text="...", background="#61bf54",
                            foreground="white", font=('標楷體', 20),command=choose_file)
    select_file.place(x=800, y=20)
    #確認送出按鈕
    confirm_submission = tk.Button(group_labframe1, text="確認送出(Confirm Submission)",
                                   background="#61bf54",foreground="white", font=('標楷體', 20),command=copy_img)
    confirm_submission.place(x=0, y=290)
    #文字
    browse_photos = tk.Label(group_labframe1, font=("標楷體", 20),
                             background="white",
                             foreground="green",
                             text="系統管理員名稱*\nSystem administrator name")
    browse_photos.place(x=0, y=75)
    #儲存名稱值
    admin_name = tk.StringVar()
    en = tk.Entry(group_labframe1, width=20, font=('標楷體', 20), justify=LEFT,
                  textvariable=admin_name)
    en.place(x=0, y=150)
    #文字
    browse_photos = tk.Label(group_labframe1, font=("標楷體", 15),
                             background="white",
                             foreground="red",
                             text="瀏覽照片\nBrowse photos")
    browse_photos.place(x=450, y=75)
    #說明文字
    caveat_text = tk.Label(group_labframe1, font=("標楷體", 15),
                           background="white",
                           foreground="red",
                           text="注意:檔名+檔案格式\nNote: file name + file format\nEx:exit.jpg")
    caveat_text.place(x=0, y=200)
    group_labframe1.pack(padx=0, pady=0, ipadx=500, ipady=190)
    #查看照片和帳戶內容按鈕
    View_photos_and_account_contents = tk.Button(add_group_account, text="查看照片和帳戶內容",background="#61bf54",
                                     foreground="white", font=('標楷體', 20),command=View_photos_and_account)
    View_photos_and_account_contents.place(x=450, y=360)
    #立即拍照按鈕
    take_a_photo = tk.Button(add_group_account, text="立即拍照",background="#61bf54",foreground="white", font=('標楷體', 20),command=photo_now)
    take_a_photo.place(x=300, y=360)

    add_group_account.mainloop()

#群組管理員新增視窗
def group_select_Radiobutton(radio_text):

    if(radio_text.get()=="Person_identification"):
        #人員辨識
        video()
    elif (radio_text.get() == "View_identification_personnel"):
        #查看識別人員
        View_identification_personnel()
    elif (radio_text.get() == "Add_group_people"):
        # 新增群組人員
        add_group_window()

# 進入群組管理員(選擇視窗)
def group_radiobutton(user):
    #返回副程式
    def return_login():
        group.destroy()  # 關閉視窗
        tk.messagebox.showinfo(title='登出 Sign out', message=user + '登出成功 Logout success.')

    group = tk.Toplevel()#設定子視窗
    group.title("人員管制系統 Personnel control system(群組管理員)")#視窗圖示抬頭
    group.geometry("1000x700+50+50")#調整畫面大小和畫面位置設定
    group.resizable(False, False)#限制視窗不能調整大小
    group.config(background="#dfeef2")#設定背景顏色
    group.iconbitmap('system_photos/Group manager.ico')#視窗圖示
    #選擇的選項
    radio_text = StringVar()
    radio_text.set(0)
    MODES = [
        ("人員辨識", "Person_identification"),
        ("查看識別人員", "View_identification_personnel"),
        ("新增群組人員", "Add_group_people"),

    ]
    #文字
    user_text1 = tk.Label(group, font=("標楷體", 10), text="身分(Identity)",
                          background="#dfeef2", foreground="green")
    user_text1.place(x=10, y=80)
    #文字
    user_text1 = tk.Label(group, font=("標楷體", 15), text="群組管理員您好",
                          background="#dfeef2", foreground="#212529")
    user_text1.place(x=10, y=100)
    #文字
    user_text2 = tk.Label(group, font=("標楷體", 10), text="管理員名稱(Admin name)",
                          background="#dfeef2", foreground="green")
    user_text2.place(x=10, y=130)
    #使用者文字值
    user_text2 = tk.Label(group, font=("標楷體", 15), text=user,
                          background="#dfeef2", foreground="#212529")
    user_text2.place(x=10, y=150)
    #時間格式設定
    time = '%Y-%m-%d %H:%M:%S'
    theTime = datetime.datetime.now().strftime(time)
    #文字
    time_text1 = tk.Label(group, font=("標楷體", 10), text="登入日期、時間(Login date & Time)",
                          background="#dfeef2", foreground="green")
    time_text1.place(x=10, y=180)
    #文字
    time_text1 = tk.Label(group, font=("標楷體", 15), text=theTime,
                          background="#dfeef2", foreground="#212529")
    time_text1.place(x=10, y=200)
    #文字
    labFrame = LabelFrame(group, text="功能選單", font=("標楷體", 45), foreground="#DC143C",
                          background="#f7f7f7")
    labFrame.pack(ipadx=300, ipady=10, pady=50, padx=250, anchor=CENTER)
    #顯示可選擇的值
    for text, mode in MODES:
        Radiobutton(labFrame, text=text, variable=radio_text, value=mode,font=("標楷體", 38), background="#f7f7f7",
                                   activeforeground="#1b18d6").pack(padx=15, pady=20, anchor=W)
    #確認按鈕
    check_image = tk.PhotoImage(file='system_photos/check.png')
    Determine_button1 = Button(group, text="確定\n(Determine)", image=check_image, compound="left",background="#61bf54", foreground="white", font=('標楷體', 25),command=(partial(group_select_Radiobutton,radio_text)))
    Determine_button1.place(x=260, y=605)
    #登出按鈕
    logout_image = tk.PhotoImage(file='system_photos/logout.png')
    logout_button2 = Button(group, text="登出\n(Logout)", image=logout_image,compound="left",background="#b3dead", foreground="white", font=('標楷體', 25),command=return_login)
    logout_button2.place(x=530, y=605)
    #迴圈
    group.mainloop()

# 臉部登入介面
def face_check():
    # 從資料夾得到人臉參數
    def facial_examination():
        checkid_button.config(state=tk.DISABLED)  # 把確認按鈕停止

        def get_encoded_faces():
            encoded = {}
            # 遞迴印出資料夾中所有目錄及檔名
            for dirpath, dnames, fnames in os.walk("./administrator_photo_profile"):
                # 所有的檔案名稱
                for f in fnames:
                    # 將圖像文件（jpg.png）加載到numpy中
                    if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jfif"):
                        # 找出資料夾有jpg、png、jfif資料
                        face = fr.load_image_file("administrator_photo_profile/" + f)
                        # 每個面部的128維面部編碼，則encodings數組將為空
                        encoding = fr.face_encodings(face)[0]
                        # split（）在分隔符處中斷字符串，並返回字符串列表
                        encoded[f.split(".")[0]] = encoding
            # 遞迴印出資料夾中所有目錄及檔名
            for dirpath, dnames, fnames in os.walk("./user_photo_profile"):
                # 所有的檔案名稱
                for f in fnames:
                    # 將圖像文件（jpg.png）加載到numpy中
                    if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jfif"):
                        # 找出資料夾有jpg、png資料
                        face = fr.load_image_file("user_photo_profile/" + f)
                        # 每個面部的128維面部編碼，則encodings數組將為空
                        encoding = fr.face_encodings(face)[0]
                        # split（）在分隔符處中斷字符串，並返回字符串列表
                        encoded[f.split(".")[0]] = encoding
            return encoded

        faces = get_encoded_faces()
        faces_encoded = list(faces.values())

        # 清單字典中的所有可用的列表
        known_face_names = list(faces.keys())

        # 方法從指定的文件加載圖像(1圖像的任何透明度都將被忽略)
        img = cv2.imread('../thematic personnel control system/photo_comparison/output.jpg', 1)
        # 使用cnn人臉檢測器返回圖像中人臉邊界框的二維數組
        face_locations = fr.face_locations(img)

        # 每個面部的128維面部編碼(編碼次數20)
        unknown_face_encodings = fr.face_encodings(img, face_locations, 20)

        face_names = []

        for face_encoding in unknown_face_encodings:
            # 將面部編碼列表與候選編碼進行比較，以查看它們是否匹配
            matches = fr.compare_faces(faces_encoded, face_encoding, tolerance=0.6)

            name = "Unknown"

            # 將其與已知的面部編碼進行比較，並獲得每個比較面部的歐式距離
            face_distances = fr.face_distance(faces_encoded, face_encoding)
            # 將其比較面部的歐式距離取列表最小值索引號
            best_match_index = numpy.argmin(face_distances)
            # 判斷編碼匹配列表的最小值索引號是否匹配
            if matches[best_match_index]:
                # 從可用的列表中取列表最小值索引號的名子
                name = known_face_names[best_match_index]
            # 把名子加到face_names的陣列
            face_names.append(name)
        if name == "Unknown":
            tk.messagebox.showerror(title="錯誤 Error", message='沒有這個使用者，請在試一次。\nNo such user, try again.')
        else:
            with open('identify_documents/administrator_account_secret.pickle',
                      'rb') as admin_file:
                admin_info = pickle.load(admin_file)
            with open('identify_documents/group_account_secret.pickle',
                      'rb') as group_file:
                group_info = pickle.load(group_file)

            if name in admin_info:
                # if name == admin_info[name]:
                faceid.destroy()  # 關閉視窗
                tk.messagebox.showinfo(title='歡迎 Welcome', message='歡迎' + name + '使用')
                administrator_radiobutton(name)
            elif name in group_info:
                # if name == group_info[name]:
                faceid.destroy()  # 關閉視窗
                tk.messagebox.showinfo(title='歡迎 Welcome', message='歡迎' + name + '使用')
                group_radiobutton(name)

            else:
                faceid.destroy()  # 關閉視窗
                tk.messagebox.showwarning('警告 warning',
                                          '查無此帳號，請跟系統管理員或群組管理員聯絡!!\nNo such account, please contact the system administrator or group administrator !!')
    #返回視窗
    def break_login():
        faceid.destroy()  # 關閉視窗
        root.deiconify()  # 還原視窗最小化

    faceid = tk.Toplevel()  # 設定子系視窗
    faceid.title("臉部登入 Face LogIn")  # 視窗圖示抬頭
    faceid.geometry("400x700+400+58")  # 調整畫面大小和畫面位置設定
    faceid.resizable(False, False)  # 限制視窗不能調整大小
    faceid.config(background="#f7f7f7")  # 設定背景顏色
    faceid.iconbitmap('system_photos/face.ico')  # 視窗圖示

    im = Image.open("/photo_comparison/output.jpg")
    ph = ImageTk.PhotoImage(im)
    image_label = tk.Label(faceid, image=ph)
    image_label.image = ph
    img_label2 = tk.Label(faceid, image=ph)
    img_label2.place(x=85, y=40)

    # 文字
    text_image1 = tk.Label(faceid, width=36, heigh=7, font=("標楷體", 15),
                           text="歡迎  Welcome\n\n請您確認這是您本人嗎?\nCould you confirm that this is you?",
                           wraplength=380, background="#f7f7f7", foreground="#212529")
    text_image1.place(x=15, y=250)
    # 文字
    text_image2 = tk.Label(faceid, width=36, heigh=4, font=("標楷體", 16),
                           text="***************************************\n請確認照片清楚度，才不會辨識錯誤。\nMake sure the photos are clear so\n you don’t recognize errors.\n***********************************",
                           wraplength=475, background="#f7f7f7", foreground="#e68173")
    text_image2.place(x=10, y=450)
    # 確認按鈕
    circle_image = tk.PhotoImage(file='system_photos/Circle.png')
    checkid_button = tk.Button(faceid, text='確認-->\nMake sure', font=("標楷體", 20), image=circle_image,
                               compound="left", background="#188c69", foreground="white", command=facial_examination)
    checkid_button.place(x=20, y=600)
    # 不確定按鈕
    fork_image = tk.PhotoImage(file='system_photos/fork.png')
    break_login_button = tk.Button(faceid, text='不確定\nuncertain', font=("標楷體", 20), image=fork_image,
                                   compound="left", background="#f7f7f7", foreground="#188c69", command=break_login)
    break_login_button.place(x=210, y=600)

    # 迴圈
    faceid.mainloop()

# 登入判斷
def login_user(user_name,user_password):
    #取得帳號
    user = user_name.get()
    #取得密碼
    password = user_password.get()
    try:
        #先讀取帳號密碼
        with open('identify_documents/administrator_account_secret.pickle', 'rb') as admin_file:
            admin_info = pickle.load(admin_file)
        with open('identify_documents/group_account_secret.pickle', 'rb') as group_file:
            group_info = pickle.load(group_file)
    except FileNotFoundError:
        #沒有帳號密碼就寫入預設帳號密碼
        with open('identify_documents/administrator_account_secret.pickle', 'wb') as admin_file:
            admin_info = {'GuanLin': 'admin'}
            pickle.dump(admin_info, admin_file)
        with open('identify_documents/group_account_secret.pickle', 'wb') as group_file:
            group_info = {'JinJie': 'group'}
            pickle.dump(group_info, group_file)
    #資料庫有沒有系統帳戶
    if user in admin_info:
        if password == admin_info[user]:
            user_name.set("")
            user_password.set("")
            tk.messagebox.showinfo(title='歡迎 Welcome', message='你好嗎? How are you?' + user)
            administrator_radiobutton(user)#系統管理員登入視窗
        else:
            user_name.set("")
            user_password.set("")
            tk.messagebox.showerror(title="錯誤 Error", message='你的密碼錯誤, 再試一次。\nyour password is wrong, try again.')
    # 資料庫有沒有群組帳戶
    elif user in group_info:
        if password == group_info[user]:
            user_name.set("")
            user_password.set("")
            tk.messagebox.showinfo(title='歡迎 Welcome', message='你好嗎? How are you?' + user)
            group_radiobutton(user)  # 群組管理員登入視窗
        else:
            user_name.set("")
            user_password.set("")
            tk.messagebox.showerror(title="錯誤 Error", message='你的密碼錯誤, 再試一次。\nyour password is wrong, try again.')
    else:
        user_name.set("")
        user_password.set("")
        tk.messagebox.showwarning('警告 warning','查無此帳號，請跟系統管理員或群組管理員聯絡!!\nNo such account, please contact the system administrator or group administrator !!')

# 進入系統(登入視窗)
def login():
    #人臉視訊轉換圖像副程式
    def face_id():
        global timer
        global num
        global image
        global faceRects

        login_button2.config(state=tk.DISABLED)  # 把登入辨識的按鈕停止
        face_button3.config(state=tk.DISABLED)  # 把臉部辨識的按鈕停止
        success, img = camera.read()  # 攝像頭讀取照片

        #攝影機是否開啟
        if camera.isOpened() == False:
            login_button2.config(state=tk.NORMAL)  # 把登入辨識的按鈕開啟
            face_button3.config(state=tk.NORMAL)  # 把臉部辨識的按鈕開啟
            tk.messagebox.showerror(title='錯誤 Error', message='沒有找到相機，請在試一次!! No camera found, please try again!!')#警告訊息提醒使用者
            camera.release()  # 釋放攝像頭
            cv2.destroyAllWindows()  # 刪除建立的全部窗口
        else:
            cv2.waitKey(10)
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)  # 轉换颜色從BGR到RGBA
            classfier = cv2.CascadeClassifier("identify_documents/haarcascade_frontalface_alt.xml")#找尋opencv分類器
            # 使用detectMultiScale函式,caleFactor=>每次搜尋方塊減少的比例,minNeighbors=>每個目標至少檢測到幾次以上，才可被認定是真數據。,minSize=>設定數據搜尋的最小尺寸。
            faceRects = classfier.detectMultiScale(cv2image, scaleFactor=1.8, minNeighbors=3, minSize=(30, 30))
            img_file = '../thematic personnel control system/photo_comparison'
            #設定文字
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(cv2image, "Please face the camera", (180, 380), font, 0.7, (0, 255, 255), 3)

            if len(faceRects) > 0:  # 大於0則檢測到人臉
                for i in range(0, 3):
                    for faceRect in faceRects:  # 單獨框出每一張人臉
                        x, y, w, h = faceRect
                        #框出臉部
                        cv2.rectangle(cv2image, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 255, 0), 2)
                        image = cv2image[y - 10: y + h + 10, x - 10: x + w + 10]
                        #計時3秒拍照偵測
                        num = 3 - i
                        if num == 1:
                            bgra_cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)  # 轉換颜色從BGR到RGBA
                            cv2.imwrite(os.path.join(img_file, 'output' + '.jpg'), bgra_cv2image)#儲存框臉圖片
                            camera.release()#釋放鏡頭
                            face_check()#臉部確認
                            cv2.VideoCapture().release()#釋放鏡頭
                            cv2.destroyAllWindows()#釋放視窗
                        time.sleep(1)
            current_image = Image.fromarray(cv2image)  # 將視訊轉换成Image对象
            imgtk = ImageTk.PhotoImage(image=current_image)#轉成圖像形式
            face_labe2.imgtk = imgtk #顯示在畫面上
            face_labe2.config(image=imgtk)#顯示在畫面上
            login.after(1, face_id)#視訊循環

    # 清除文字框副程式
    def Clear_text():
        user_name.set("") # 清除帳號
        user_password.set("") # 清除密碼

    # 返回主畫面
    def break_window():
        login.destroy()  # 關閉視窗
        root.deiconify()  # 還原視窗最小化

    login = tk.Toplevel()#設定子系視窗
    login.title("人員管制系統 Personnel control system")#視窗圖示抬頭
    login.geometry("1350x700+50+50")#調整畫面大小和畫面位置設定
    login.resizable(False, False)#限制視窗不能調整大小
    login.config(background="#f7f7f7")#設定背景顏色
    login.iconbitmap('system_photos/ico.ico')#視窗圖示

    # 畫布方式嵌入圖片在左邊(美編)
    canvas = tk.Canvas(login, height=800, width=640, background="white")
    image_file = tk.PhotoImage(file=("system_photos/oit.gif"))
    image = canvas.create_image(0, 150, anchor="nw", image=image_file)
    canvas.pack(side="left")
    # 文字
    title_labe1 = tk.Label(login, text="登入系統 Login System", foreground="#e3962b", font=('標楷體', 35), width=0,
                           height=0, background="#f7f7f7")
    title_labe1.place(x=745, y=20)
    # 文字
    face_labe2 = tk.Label(login, foreground="#e3962b", width=285, height=285, background="#f7f7f7")
    face_labe2.place(x=850, y=75)
    # 文字
    user_labe3 = tk.Label(login, text="帳號(Account Number)", foreground="#e3962b", font=('標楷體', 20), width=0,
                          height=0, background="#f7f7f7")
    user_labe3.place(x=770, y=375)
    #把文字框資料儲存到宣告變數(帳號)
    user_name = tk.StringVar()
    user_entry1 = tk.Entry(login, textvariable=user_name, width=35, font=('標楷體', 20), selectbackground="blue")
    user_entry1.place(x=770, y=420)
    # 文字
    password_labe4 = tk.Label(login, text="密碼(Password)", foreground="#e3962b", font=('標楷體', 20), width=0,
                              height=0, background="#f7f7f7")
    password_labe4.place(x=770, y=470)
    # 把文字框資料儲存到宣告變數(密碼)
    user_password = tk.StringVar()
    password_entry2 = tk.Entry(login, textvariable=user_password, show="‧", width=35, font=('標楷體', 20),
                               selectbackground="blue")
    password_entry2.place(x=770, y=510)
    # 清除文字框按鈕
    Clear_button1 = tk.Button(login, text="清除(Clear)", background="#eb7c7c", foreground="white", font=('標楷體', 15),
                              width=49, justify='center',command=Clear_text)
    Clear_button1.place(x=770, y=560)
    # 輸入文字框登入按鈕
    login_image = tk.PhotoImage(file='system_photos/login.png')
    login_button2 = tk.Button(login, text="登入\n(LogIn)", image=login_image, compound="left", background="#e3962b",
                              foreground="white", font=('標楷體', 25),command=partial(login_user,user_name,user_password))#partial傳遞引數
    login_button2.place(x=680, y=605)
    # 臉部登入按鈕
    face_image = tk.PhotoImage(file='system_photos/face.png')
    face_button3 = tk.Button(login, text="臉部登入\n(Face LogIn)", image=face_image, compound="left",
                             background="#a77657", foreground="white", font=('標楷體', 25),command=face_id)
    face_button3.place(x=870, y=605)
    # 返回主畫面按鈕
    break_image = tk.PhotoImage(file='system_photos/home_button.png')
    break_button4 = tk.Button(login, text="返回\n(Break)", image=break_image, compound="left", background="#a77657",
                              foreground="white", font=('標楷體', 25),command=break_window)
    break_button4.place(x=1145, y=605)
    camera = cv2.VideoCapture(0)  # 攝像頭
    # 副程式迴圈
    login.mainloop()

# 系統簡介視窗(簡介視窗)
def introduction():
    # 返回主視窗
    def break_home():
        introduction.destroy()  # 關閉視窗
        root.deiconify()  # 還原視窗最小化

    root.iconify()  # 將視窗最小化
    introduction = tk.Toplevel()#設定子系視窗
    introduction.title("人員管制系統 Personnel control system")#視窗圖示抬頭
    introduction.geometry("800x500+350+170")#調整畫面大小和畫面位置設定
    introduction.resizable(False, False)#限制視窗不能調整大小
    introduction.config(background="#a6684c")#設定背景顏色
    introduction.iconbitmap('system_photos/ico.ico')#視窗圖示
    # 文字方式嵌入圖片(美編)
    img_jpg = tk.PhotoImage(file='system_photos/introduction_image.png')
    label_img = tk.Label(introduction, image=img_jpg)
    label_img.place(x=30, y=245)
    # 文字
    title_labe1 = tk.Label(introduction, text="簡介\nIntroduction",
                           foreground="white", font=('標楷體', 35), width=12, height=2, background="#a6684c")
    title_labe1.place(x=0, y=20)
    # 文字
    title_labe2 = tk.Label(introduction, text=" 本系統由何冠霖和譚晉杰開發,經過\n無數的失敗和努力的心血才能完成本系\n統，經過李炯三老師指導才完成此專題。",
                           foreground="white", font=('新細明體', 20), width=35, height=3, background="#a6684c")
    title_labe2.place(x=300, y=20)
    # 文字
    title_labe3 = tk.Label(introduction,
                           text="__________________________________________________________________________________________________________",
                           foreground="white", font=('新細明體', 20), width=35, height=1, background="#a6684c")
    title_labe3.place(x=300, y=110)
    # 文字
    title_labe4 = tk.Label(introduction, text="操做方法:按下進入系統時就可以登錄((1)群組管理者(2)\n系統管理員)，也可以利用臉部來登錄。",
                           foreground="white", font=('新細明體', 15), width=44, height=2, background="blue")
    title_labe4.place(x=300, y=150)
    # 文字
    title_labe5 = tk.Label(introduction, text="一`群組管理者:登錄後可以點選((1)人員辨識(2)查看\n識別人員(3)新增群組人員),並可以達到人員進出的管控。",
                           foreground="white", font=('新細明體', 15), width=44, height=3, background="#a6684c")
    title_labe5.place(x=300, y=200)
    # 文字
    title_labe6 = tk.Label(introduction, text="二`系統管理員:登錄後可以點選((1)新增全體人員(2)\n人員辨識管理(3)辨識人員查看(4)進出統計查看),並可以\n管理人員進出的控管。",
                           foreground="white", font=('新細明體', 15), width=44, height=3, background="#a6684c")
    title_labe6.place(x=300, y=270)
    # 文字
    title_labe6 = tk.Label(introduction, text="注意:如有任何疏忽或出錯的地方請通知管理\n人員，也感謝您蒞臨使用此軟體。",
                           foreground="red", font=('新細明體', 18), width=37, height=2, background="#a6684c")
    title_labe6.place(x=300, y=340)
    # 文字
    student_labe1 = tk.Label(introduction, text="指導老師:李炯三\n專題學生:何冠霖\n專題學生:譚晉杰\n ©All rights reserved",
                             foreground="white", font=('標楷體', 20), width=20, height=4, background="#a6684c")
    student_labe1.place(x=0, y=150)
    # 返回主視窗按鈕和按鈕圖片設定
    break_image = tk.PhotoImage(file='system_photos/home_button.png')
    break_button1 = tk.Button(introduction, text="返回(Break)", image=break_image, compound="left",
                              background="white", foreground="green", font=('標楷體', 25),command=break_home)
    break_button1.place(x=400, y=410)
    # 副程式迴圈
    introduction.mainloop()

# 視窗時間(主視窗)
def get_time():
    timestr = time.strftime("%Y-%m-%d %H:%M:%S")# 獲取現在時間並轉為文字
    data_labe.configure(text=timestr)# 重置時間文本
    root.after(1000, get_time)#每隔一秒重新(gettime)更新時間

# 主視窗(歡迎視窗)
root = tk.Tk()#設定父系視窗
root.title("人員管制系統 Personnel control system")#視窗圖示抬頭
root.geometry("800x500+350+170") #調整畫面大小和畫面位置設定
root.resizable(False, False) #限制視窗不能調整大小
root.config(background="#05ed9b") #設定背景顏色
root.iconbitmap('system_photos/ico.ico') #視窗圖示

#主視窗文字(人員管制系統)
text_label1 = tk.Label(root, text="人員管制系統", foreground="white", font=('標楷體', 40), width=30, height=2,background="#05ed9b")
text_label1.grid(row=1, column=0)
#主視窗按鈕(進入系統)
conin_button1 = tk.Button(root, text="進入系統->", background="#f5ec49", foreground="red", font=('標楷體', 30), width=10,height=2,command=login)
conin_button1.place(x=300, y=120)
#主視窗按鈕(系統簡介)
introduction_button1 = tk.Button(root, text="系統簡介", foreground="green", font=('標楷體', 30), width=10, height=2,command=introduction)
introduction_button1.place(x=300, y=250)
#主視窗文字(0000-00-00 00:00:00)
data_labe = tk.Label(root, foreground="white", font=('標楷體', 27), width=46, height=2, background="#05ed9b")
data_labe.place(x=13, y=370)

get_time()  # 呼叫獲取時間的副程式

#主視窗文字(建議系統為Windows10、windows7。\n ©Copyright 2020, GuanLinHe and GinJayTan,All rights reserved.)
text_labe2 = tk.Label(root,text="建議系統為Windows10、windows7。\n ©Copyright 2020, GuanLinHe and GinJayTan,All rights reserved.",
                 foreground="red", font=('標楷體', 15), width=65, height=2, background="#05ed9b")
text_labe2.place(x=90, y=453)
#主程式迴圈
root.mainloop()