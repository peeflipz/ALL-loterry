from tkinter import *
import tkinter as tk
import customtkinter as ctk
import sqlite3
from PIL import Image, ImageTk
from tkinter import ttk
import datetime
from tkinter import messagebox
from datetime import datetime
import tkinter.messagebox
import io
from tkinter import filedialog
import random
import api_payment

class main:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1080x620")
        self.root.title("Alllotery")
        
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        self.create_data()
        self.isLogin = False
        self.login_store()
        

    def create_data(self):
        try:
            self.c.execute('''CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY,
                username varchar(30) NOT NULL,
                password text NOT NULL,
                fname varchar(30) NOT NULL,
                lname varchar(30) NOT NULL,
                Age varchar(2) NOT NULL,
                email varchar(30) NOT NULL,
                Bank_Number varchar(12) NOT NULL,
                Bank_Name varchar(30) NOT NULL,
                Address varchar(200) NOT NULL,
                phone varchar(10) NOT NULL,
                access varchar(20) NOT NULL)''')
           
            self.c.execute('''CREATE TABLE IF NOT EXISTS lottery(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_lottery VARCHAR(30) NOT NULL,
                num_id TEXT NOT NULL,
                price INTEGER NOT NULL,
                amount INTEGER NOT NULL,
                img_lottery BLOB NOT NULL)''')
            self.conn.commit()
            
            self.c.execute('''CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                User_orders varchar(30) NOT NULL,
                orders_lottery_num TEXT NOT NULL,
                img_lottery_orders BLOB NOT NULL,
                amount_orders INTEGER NOT NULL,
                price_orders INTEGER NOT NULL,
                Cash INTEGER NOT NULL,
                status text NOT NULL
            )''')
            self.conn.commit()
        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {e}")
        finally:
            self.conn.close()
            
    def create_admin(self):
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        d = (
            'admin',              # username
            'admin',              # password
            'Admin',              # fname 
            'User',               # lname
            '20',                 # Age 
            '',                   # email
            '000000000000',       # Bank_Number 
            '',                   # Bank_Name
            'COMED',              # Address
            '0000000000',         # phone 
            'admin'               # access
        )
        try:
            self.c.execute('''INSERT INTO users(username, password, fname, lname, Age, email,
                            Bank_Number, Bank_Name, Address, phone, access)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?)''', d)
            self.conn.commit()
          
        except Exception as e:
            print(f'เกิดข้อผิดพลาด {e}')
        finally:
            self.conn.close()

    def login_store(self):
        # สร้าง Frame พื้นหลังสีขาว
        tk.Frame(self.root, bg="white", width=1080, height=620).pack()
        
        # uilogin
        self.image = Image.open('img/login.png')
        self.image = self.image.resize((1080, 620), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(self.root, image=self.photo, bg="#e32020",width=1080,height=620)
        self.label.place(x=0, y=0)

        self.username_entry = tk.Entry(self.root, font=('Prompt',12), fg='black', bg='white', border=0)
        self.username_entry.place(x=705, y=253)

        # สร้าง Entry สำหรับรับข้อมูล (password)
        self.password_entry = tk.Entry(self.root, font=('Prompt',12), fg='black', bg='white', border=0, show="*")
        self.password_entry.place(x=705, y=323)

        # btn
        self.signin_button = ctk.CTkButton(self.root, font=('Prompt',16),text='เข้าสู่ระบบ',
                                           width=260,height=38
                                           ,fg_color='#e32320',
                                           hover_color='#c20300'
                                           ,command= self.login)
        self.signin_button.place(x=695, y=372)
        
        self.signup_button = ctk.CTkButton(self.root, font=('Prompt',16), 
                                           width =260,height=38, 
                                           text="สมัครสมาชิก",
                                           fg_color='#2b2b2b',
                                        hover_color='#000000'
                                      ,command=self.signup_form)
        self.signup_button.place(x=695, y=413)

    def register(self):
        pass
    
    def login(self):
        self.username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.username or not password:
            tkinter.messagebox.showerror("Error", "กรุณากรอกข้อมูลให้ครบ")
            return

        try:
            self.conn = sqlite3.connect('data.db')
            self.c = self.conn.cursor()
            
            self.c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (self.username, password))
            result = self.c.fetchone()

            if result:
                self.user_id = result[0]
                self.user_role = result[11]  # ตรวจสอบสิทธิ์การเข้าถึง

                if self.user_role == "admin":
                    self.admin_menu_ui()  # ถ้าเป็นผู้ดูแลระบบ
                    self.isLogin = True
                else:
                    self.main_store_ui()  # ถ้าเป็นผู้ใช้ธรรมดา
                    self.isLogin = True
            else:
                tkinter.messagebox.showerror("Error", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
        except Exception as e:
            print(f"Error logging in: {e}")
        finally:
            self.conn.close()     

    def signup_form(self):
        self.signup_ui = tk.Toplevel(self.root)
        self.signup_ui.geometry("960x540")
        self.bg = tk.Frame(self.signup_ui, bg="#e32320", width=1920, height=1080)
        self.bg.pack()

        self.image_signup = Image.open('img/signup.png')
        self.image_signup = self.image_signup.resize((960, 540), Image.LANCZOS)
        self.photo_signup = ImageTk.PhotoImage(self.image_signup)
        self.label = tk.Label(self.signup_ui, image=self.photo_signup, bg="#e32320")
        self.label.place(x=0, y=0)

        self.et_fname = tk.Entry(self.signup_ui,font=('Prompt',12), fg='black', bg='white', border=0)
        self.et_fname.place(x = 260,y=106)
        self.et_lname = tk.Entry(self.signup_ui,font=('Prompt',12), fg='black', bg='white', border=0)
        self.et_lname.place(x = 260,y=166)
        
        style = ttk.Style()
        style.theme_use("default")  # ธีมอื่น ๆ ที่อาจลองใช้ได้เช่น 'alt' หรือ 'default'

        # ปรับสไตล์ของ Combobox ให้ border ดูบางลงหรือหายไป
        style.configure("TCombobox", 
                        fieldbackground="white",   # สีพื้นหลังใน combobox
                        borderwidth=0,             # ความหนาของขอบ
                        relief="flat",              # กำหนดลักษณะ relief ให้แบน
                    )
        style.configure("Vertical.TScrollbar", 
                gripcount=0,
                background="#cfcfcf",  # สีพื้นหลัง Scrollbar
                darkcolor="#2b2b2b",
                lightcolor="#2b2b2b",
                troughcolor="white",     # สีพื้นหลังราง Scrollbar
                bordercolor="white",
                arrowcolor="black",
                relief = "flat")
        
        self.dob_day = ttk.Combobox(self.signup_ui, values=list(map(str,range(1, 32))),
                                    width=3, height=8,style="TCombobox",
                                    font=('Prompt', 8),background='white',justify='center')
        self.dob_day.place(x=255, y=237,width=52) 
        
        self.dob_month_Option = tk.StringVar()

       
        self.dob_month = ttk.Combobox(
            master=self.signup_ui,
            font=('Prompt',8),
            values=[
                
                "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
                "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
            ],
            width=18,
            height=8,justify='center'
        )
        self.dob_month.place(x=320, y=237,width=120)
        current_year = datetime.now().year
        self.dob_year = ttk.Combobox(self.signup_ui, values=list(range(current_year, 1923, -1)),
                                     width=6,justify='center', font=('Prompt', 8))
        self.dob_year.place(x=458, y=237,width=52)

        self.et_phone = tk.Entry(self.signup_ui,width=18,font=('Prompt',12), fg='black', bg='white', border=0)
        self.et_phone.place(x =260,y=300)
        self.et_email = tk.Entry(self.signup_ui,width=18,font=('Prompt',12), fg='black', bg='white', border=0)
        self.et_email.place(x =260,y=368)
        self.et_banknumber = tk.Entry(self.signup_ui, width=14, font=('Prompt', 12), fg='black', bg='white', border=0)
        self.et_banknumber.place(x=260, y=428,width=130)
        self.et_bankname = ttk.Combobox(self.signup_ui, values=[
            "ธนาคารกรุงเทพ", "ธนาคารกสิกรไทย", "ธนาคารกรุงไทย", "ธนาคารทหารไทย", "ธนาคารไทยพาณิชย์", 
            "ธนาคารกรุงศรีอยุธยา", "ธนาคารเกียรตินาคิน", "ธนาคารซีไอเอ็มบีไทย", "ธนาคารทิสโก้", 
            "ธนาคารธนชาต", "ธนาคารยูโอบี", "ธนาคารสแตนดาร์ดชาร์เตอร์ด (ไทย)", 
            "ธนาคารไทยเครดิตเพื่อรายย่อย", "ธนาคารแลนด์ แอนด์ เฮาส์", 
            "ธนาคารไอซีบีซี (ไทย)", "ธนาคารพัฒนาวิสาหกิจขนาดกลางและขนาดย่อมแห่งประเทศไทย", 
            "ธนาคารเพื่อการเกษตรและสหกรณ์การเกษตร", "ธนาคารเพื่อการส่งออกและนำเข้าแห่งประเทศไทย", 
            "ธนาคารออมสิน", "ธนาคารอาคารสงเคราะห์", "ธนาคารอิสลามแห่งประเทศไทย", 
            "ธนาคารแห่งประเทศจีน", "ธนาคารซูมิโตโม มิตซุย ทรัสต์ (ไทย)", 
            "ธนาคารฮ่องกงและเซี้ยงไฮ้แบงกิ้งคอร์ปอเรชั่น จำกัด"
        ], width=20, font=('Prompt', 8),justify='center')
        self.et_bankname.place(x=408, y=428,width=98,height=25)

        self.et_adress = tk.Text(self.signup_ui,width=22,heigh=8,font=('Prompt',8), fg='black', bg='white',border=0)
        self.et_adress.place(x=550,y=118,width=196)
        self.et_username = tk.Entry(self.signup_ui,width=18,font=('Prompt',8), fg='black', bg='white', border=0)
        self.et_username.place(x =560,y=304)
        self.et_password = tk.Entry(self.signup_ui,width=18,font=('Prompt',8), fg='black', bg='white', border=0, show='*')
        self.et_password.place(x =560,y=364,width=190)
        self.et_password_confirm = tk.Entry(self.signup_ui,width=18,font=('Prompt',8), fg='black', bg='white', border=0, show='*')
        self.et_password_confirm.place(x =560,y=422,width=190)

        self.et_submit = ctk.CTkButton(self.signup_ui, text="Submit", 
                                       width=150, font=('Prompt',13), 
                                       text_color='white', fg_color='#2b2b2b',
                                        bg_color='#e32320',
                                       hover_color= 'black',
                                       corner_radius=5,
                                       border_width=0,
                                       border_color='#e32320',
                                       command=self.signup)
        self.et_submit.place(x=550, y=460)
       

    def signup(self):
        self.username = self.et_username.get()
        password = self.et_password.get()
        email = self.et_email.get()
        password_confirm = self.et_password_confirm.get()
        
        self.fname = self.et_fname.get()
        self.lname = self.et_lname.get()
        phone = self.et_phone.get()
        self.address = self.et_adress.get("1.0", "end-1c")
        self.bank_number = self.et_banknumber.get()
        self.bank_name = self.et_bankname.get()

        day = self.dob_day.get()
        month = self.dob_month.get()
        year = self.dob_year.get()

        # ตรวจสอบว่ามีการกรอกข้อมูลครบหรือไม่
        if not self.username or not password or not email or not day or not month or not year:
            tkinter.messagebox.showerror("Error", "กรุณากรอกข้อมูลให้ครบ")
            return

        if password != password_confirm:
            tkinter.messagebox.showerror("Error", "รหัสผ่านไม่ตรงกัน")
            return

        if not phone.isdigit() or len(phone) != 10:
            tkinter.messagebox.showerror("Error", "กรุณากรอกเบอร์โทรศํพท์ให้ถูกต้อง")
            return

        if not self.bank_number.isdigit() or not (10 <= len(self.bank_number) <= 12):
            tkinter.messagebox.showerror("Error", "กรุณากรอกเลขบัญชีธนาคารให้ถูกต้อง")
            return

        if "@" not in email or "." not in email or email.count("@") != 1 or email.startswith("@") or email.endswith("@") or email.endswith("."):
            tkinter.messagebox.showerror("Error", "กรุณากรอกอีเมลให้ถูกต้อง เช่น allottery@gmail.com")
            return


        # แปลงเดือนจากชื่อไทยเป็นตัวเลข
        month_dict = {
            "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4, "พฤษภาคม": 5, 
            "มิถุนายน": 6, "กรกฎาคม": 7, "สิงหาคม": 8, "กันยายน": 9, "ตุลาคม": 10, 
            "พฤศจิกายน": 11, "ธันวาคม": 12
        }
        month_number = month_dict[month]

        # คำนวณอายุ
        today = datetime.today()
        birth_date = datetime(int(year), month_number, int(day))
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        # ตรวจสอบอายุไม่ถึง 20 ปี
        if age < 20:
            tkinter.messagebox.showerror("Error", "คุณต้องมีอายุมากกว่า 20 ปีขึ้นไปจึงจะสามารถสมัครได้")
            return

        # ดำเนินการเก็บข้อมูลลงในฐานข้อมูล
        try:
            self.conn = sqlite3.connect('data.db')
            self.c = self.conn.cursor()

            # ตรวจสอบว่าผู้ใช้งานซ้ำหรือไม่
            self.c.execute("SELECT * FROM users WHERE username = ?", (self.username,))
            if self.c.fetchone():
                tkinter.messagebox.showerror("Error", "มีชื่อผู้ใช้งานอยู่ในระบบ")  
                return

            # เพิ่มข้อมูลผู้ใช้พร้อมอายุลงในฐานข้อมูล
            self.c.execute("INSERT INTO users (username, password, fname, lname, Age, email, phone, Bank_Number, Bank_Name, Address, access) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                        (self.username, password, self.fname, self.lname, str(age), email, phone, self.bank_number, self.bank_name, self.address, "user"))
            self.conn.commit()
            tkinter.messagebox.showinfo("Success", "สร้างบัญชีเสร็จสิ้น")  
            self.signup_ui.destroy()  # ปิดหน้าต่างสมัครสมาชิก
            self.login_store()  # กลับไปหน้าล็อกอิน
        except Exception as e:
            print(f"Error inserting user data: {e}")
        finally:
            self.conn.close()
            
            
    def clear_frameItem_con(self):
        for widget in  self.frame_item_con.winfo_children():
            widget.destroy()
            
    def clear_main_con(self):
        if self.container:
            for widget in  self.container.winfo_children():
                widget.destroy()
        


    def main_store_ui(self):
        self.root.destroy()  # ปิดหน้าต่างหลัก
        self.store = tk.Tk()  # สร้างหน้าต่างใหม่สำหรับหน้าร้าน
        self.store.tk.call('tk', 'scaling', 1.5)
        self.store.geometry("1080x620")
        self.store.title('ALL LOTTERY')
        self.store.configure(bg ="white")
        
        
    #รวมเมนูต่างๆ    

        bar_icon = tk.Frame(self.store,background='#e32320',width=100,height=1080)
        bar_icon.place(x=0,y=0)
        
       
        # โหลดภาพและปรับขนาดโดยใช้ CTkImage
        home_image = Image.open(r'D:\python_finalproject\img\icon\white\22.png')  # แก้ไขเส้นทางให้ถูกต้อง
        home_img_icon = ctk.CTkImage(home_image, size=(80, 40))  # ปรับขนาดที่ต้องการ
        # สร้าง CTkButton พร้อมภาพ
        self.home_btn = ctk.CTkButton(
            bar_icon,
            fg_color='#e32320',
            border_width=0,
            corner_radius=0,
            width=100,
            height=10,
            image=home_img_icon,
            text="หน้าหลัก",
            font=('Kanit Regular',14),
            compound=TOP,
            bg_color='#e32320',
            hover_color='#e32320',  # เปลี่ยนสีเมื่อ hover
            command=self.home_page
        )
        self.home_btn.place(x=0, y=85)    
           
        cart_image = Image.open(r'D:\python_finalproject\img\icon\white\26.png')  
        cart_img_icon = ctk.CTkImage(cart_image, size=(80, 40)) 
        
        self.cart_btn = ctk.CTkButton(bar_icon,fg_color='#e32320',
            border_width=0,
            corner_radius=0,
            width=100,
            height=90,
            image=cart_img_icon,
            text='ตะกร้า',
            font=('Kanit Regular',14),
            compound=TOP,
            bg_color='#e32320',
            hover_color='#e32320',
            command = self.cart_page # เปลี่ยนสีเมื่อ hover
           )
        self.cart_btn.place(x=0,y=175)


        save_image = Image.open(r'D:\python_finalproject\img\icon\white\27.png')  # แก้ไขเส้นทางให้ถูกต้อง
        save_img_icon = ctk.CTkImage(save_image, size=(80, 40))  # ปรับขนาดที่ต้องการ

        self.save_btn = ctk.CTkButton(bar_icon,fg_color='#e32320',
            border_width=0,
            corner_radius=0,
            width=100,
            height=90,
            image=save_img_icon,
            text='ตู้เซฟ',
            font=('Kanit Regular',14),
            compound=TOP,
            bg_color='#e32320',
            hover_color='#e32320',
            command=self.Mysave_page
           )
        self.save_btn.place(x=0,y=265)
        

        
        profile_image = Image.open(r'D:\python_finalproject\img\icon\white\24.png')  # แก้ไขเส้นทางให้ถูกต้อง
        profile_img_icon = ctk.CTkImage(profile_image, size=(80, 40))  # ปรับขนาดที่ต้องการ
        
        self.profile_btn = ctk.CTkButton(bar_icon,fg_color='#e32320',
            border_width=0,
            corner_radius=0,
            width=100,
            height=90,
            image=profile_img_icon,
            text='ข้อมูลส่วนตัว',
            font=('Kanit Medium',14),
            compound=TOP,
            bg_color='#e32320',
            hover_color='#e32320',
            command=self.profile_page
           )
        self.profile_btn.place(x=0,y=355)
        
        logout_image = Image.open(r'D:\python_finalproject\img\icon\white\25.png')  # แก้ไขเส้นทางให้ถูกต้อง
        logout_img_icon = ctk.CTkImage(logout_image, size=(80, 40))  # ปรับขนาดที่ต้องการ
        logout_btn = ctk.CTkButton(bar_icon,fg_color='#e32320',
            border_width=0,
            corner_radius=0,
            width=100,
            height=90,
            image=logout_img_icon,
            text='ออกจากระบบ',
            font=('Kanit Medium',14),
            compound=TOP,
            bg_color='#e32320',
            hover_color='#e32320'  # เปลี่ยนสีเมื่อ hover
           )
        logout_btn.place(x=0,y=500)
        
        


        self.home_page()
        
    def changeColor_icon(self, page, add_icon, icon_config):
        # ไอคอนสีดำเมื่ออยู่ในหน้าเฉพาะ
        icon_settings = {
            "home": r'D:\python_finalproject\img\icon\black\Home black.png',
            "cart": r'D:\python_finalproject\img\icon\black\cart black.png',
            "profile": r'D:\python_finalproject\img\icon\black\profile black.png',
            "save": r'D:\python_finalproject\img\icon\black\save black.png'
        }

        # ไอคอนสีขาวเมื่อไม่อยู่ในหน้าเฉพาะ
        icon_settings_white = {
            "home": r'D:\python_finalproject\img\icon\white\22.png',
            "cart": r'D:\python_finalproject\img\icon\white\26.png',
            "profile": r'D:\python_finalproject\img\icon\white\24.png',
            "save": r'D:\python_finalproject\img\icon\white\27.png'
        }
        
        # รีเซ็ตทุกปุ่มให้เป็นไอคอนสีขาวก่อน
        buttons = {
            "home": self.home_btn,
            "cart": self.cart_btn,
            "profile": self.profile_btn,
            "save": self.save_btn
        }
        
        for name, button in buttons.items():
            img = Image.open(icon_settings_white[name])
            img_icon = ctk.CTkImage(img, size=(80, 40))
            button.configure(image=img_icon, text_color='#ffffff')
        
        # ถ้าอยู่ในหน้าที่ระบุให้ตั้งไอคอนเป็นสีดำเฉพาะปุ่มนั้น ๆ
        if page:
            img = Image.open(icon_settings[add_icon])
            img_icon = ctk.CTkImage(img, size=(80, 40))
            icon_config.configure(image=img_icon, text_color='#2b2b2b')   
                 
    def main_container(self,):
        # สร้าง Frame หลักสำหรับการแสดงข้อมูล
        self.container = ctk.CTkFrame(self.store, width=980, height=550, corner_radius=0, fg_color='white')
        self.container.place(x=100, y=0 )
        
        # สร้าง Canvas
        self.scroll_canvas = tk.Canvas(self.container, bg='white',highlightthickness=0,width=980,height=500)
        self.scroll_canvas.grid(row = 1 ,column =0,sticky = 'nsew')

        # สร้าง Scrollbar
        self.scrollbar1 = ctk.CTkScrollbar(self.container, orientation='vertical',hover='white'
                                           ,corner_radius=10,
                                           fg_color='white',
                                           bg_color='white',button_color='white',
                                           width=10,height=100
                                           ,command=self.scroll_canvas.yview)
        
        self.scrollbar1.grid(row=1, column=1, sticky="ns")
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar1.set)

        # สร้าง Frame ภายใน Canvas
        self.main_con = tk.Frame(self.scroll_canvas, bg='#ffffff')

        self.scroll_canvas.create_window((0, 0), window=self.main_con, anchor='nw')

        # ปรับ scrollregion อัตโนมัติเมื่อขนาดของ main_con เปลี่ยนแปลง
        def update_scroll_region(event):
            self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

        self.main_con.bind("<Configure>", update_scroll_region)
        
        # ฟังก์ชันสำหรับการเลื่อนด้วย Scroll Wheel
        def on_mouse_scroll(event):
            self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        # ผูก Scroll Wheel เข้ากับ Canvas
        self.scroll_canvas.bind_all("<MouseWheel>", on_mouse_scroll)  # สำหรับ Windows

      
        
        self.scroll_canvas.bind_all("<MouseWheel>", on_mouse_scroll) 
        self.scroll_canvas.bind_all("<Up>", on_mouse_scroll)# สำหรับ Windows
        self.scroll_canvas.bind_all("<Down>", on_mouse_scroll)# สำหรับ Windows        
        
        
    def home_page(self):
        self.changeColor_icon(self.home_page,"home",self.home_btn)
        self.main_container()
        self.header_frame = ctk.CTkFrame(self.container,fg_color='#2b2b2b'
                                         ,width=1920,height=50,
                                         corner_radius=0)
        self.header_frame.grid(row  = 0,column = 0 ,sticky='nsew')
                               
        self.ads_frame = ctk.CTkFrame(self.main_con,fg_color='#b91c1c',
                                      width=400,height=250,
                                      corner_radius=0)
        self.ads_frame.grid(row =0,column = 0,pady= 0,sticky = 'nsew')
        
        self.ads_item_con = ctk.CTkFrame(self.ads_frame,fg_color='#b91c1c',width=800 ,height=250,corner_radius=0)
        self.ads_item_con.grid(row = 1 ,column = 0)
        
        # สร้าง Frame สำหรับปุ่มหวย
        self.button_frame = tk.Frame(self.main_con, bg='#ffffff')
        self.button_frame.grid(row=2, column=0,padx=20,sticky = NSEW,pady = 8)  
       
        self.search_con = ctk.CTkFrame(self.button_frame,width=1080,height=40,fg_color='white')
        self.search_con.grid(row = 0 , column= 3,sticky =NSEW,pady= 8,padx =20)
        et_search = ctk.CTkEntry(
                                self.search_con,
                                font=('Prompt', 14),          
                                width=200,
                                height=32,
                                fg_color='white',                  
                                bg_color='white',
                                border_color='#cfcfcf',
                                text_color='black',
                                corner_radius=10)
        et_search.place(x = 0,y=3) 
        
        def findlot():
            self.conn = sqlite3.connect('data.db')
            self.c = self.conn.cursor()
            
            try:
                search = et_search.get()
                self.c.execute('SELECT img_lottery,amount,price,type_lottery,num_id FROM lottery WHERE num_id = ?',(search,))
                show_search = self.c.fetchall()
                                
                if show_search:    
                    if self.oddLot:
                        self.oddlottery_data = show_search
                       
                    elif self.pairLot:
                        self.pairlottery_data = show_search
                       
                    elif self.allLot:
                        self.alllottery_data = show_search
                    
                else:
                    self.clear_frameItem_con()
                    not_fond= tk.Label(self.frame_item_con,text="ไม่พบลอตเตอรี่",
                                       font = ('Prompt',16),fg= 'red',bg='white')
                    not_fond.place(x= 330,y= 20)
                     
                                       
            except Exception as e:
                print(f'can not find : {e}')
            finally:
                self.conn.close()
                
        def random_lottery():
                self.conn = sqlite3.connect('data.db')
                self.c = self.conn.cursor()
                
                try:                   
                    self.c.execute('SELECT img_lottery,amount,price,type_lottery,num_id FROM lottery')
                    radom = self.c.fetchall()
                    random_lottery = random.choice(radom)
                                                                
                    if random_lottery:
                        if self.oddLot:
                            
                            self.oddlottery_data = [random_lottery]
                        elif self.pairLot:
                            
                            self.pairlottery_data  =  [random_lottery]
                        elif self.allLot:
                            
                            self.alllottery_data = [random_lottery]    
                                                
                except Exception as e:
                    print(f'can not find : {e}')
                finally:
                    self.conn.close()
            
        search_btn = ctk.CTkButton(self.search_con,text='ค้นหา',font=('Prompt',12),
                                        fg_color='#2b2b2b',
                                        width=50,height=32,
                                        hover_color="#000000",
                                        command=findlot)
        search_btn.place(x = 210, y = 3 ) 
        
        random_btn = ctk.CTkButton(self.search_con,text='สุ่ม',font=('Prompt',12),
                                        fg_color='#2b2b2b',
                                        width=50,height=32,
                                        hover_color="#000000",
                                        command= random_lottery) 
        random_btn.place(x = 270, y = 3 )    

        # ปุ่มหวย - วางใน button_frame
        self.allLot_btn = ctk.CTkButton(self.button_frame, text='ทั้งหมด', font=('Prompt', 12),
                                        width=84, height=35,
                                        fg_color='#e32320',
                                        hover_color='#e32320',
                                        text_color='white',
                                        command=self.allLot)
        self.allLot_btn.grid(row=0, column=0, padx=5)  # ใช้ grid แทน place

        self.pairLot_btn = ctk.CTkButton(self.button_frame, text='หวยชุด', font=('Prompt', 12),
                                        width=84, height=35,
                                        fg_color='#cfcfcf',
                                        hover_color='#cfcfcf',
                                        text_color='#2b2b2b',
                                        command=self.pairLot)
        self.pairLot_btn.grid(row=0, column=1, padx=5)  # ใช้ grid แทน place

        self.oddLot_btn = ctk.CTkButton(self.button_frame, text='หวยเดี่ยว', font=('Prompt', 12),
                                        width=84, height=35,
                                        fg_color='#cfcfcf',
                                        hover_color='#cfcfcf',
                                        text_color='#2b2b2b',
                                        command=self.oddLot)
        self.oddLot_btn.grid(row=0, column=2, padx=5)  # ใช้ grid แทน place
        
        
        self.frame_item_con = ctk.CTkFrame(self.main_con,fg_color='white',
                                           width=900,height=1000) 
        self.frame_item_con.grid(row = 3,column =0,
                                 sticky = NSEW,padx = 5)        
        
        self.allLot()
        
        
    def allLot(self):
        self.clear_frameItem_con()
        self.allLot_btn.configure(fg_color='#e32320',hover_color='#e32320', text_color='white')
        self.pairLot_btn.configure(fg_color='#cfcfcf',hover_color='#cfcfcf', text_color='#2b2b2b')
        self.oddLot_btn.configure(fg_color='#cfcfcf',hover_color='#cfcfcf', text_color='#2b2b2b')
                    
        # เชื่อมต่อฐานข้อมูล
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()

        # ดึงข้อมูลภาพและเลขหวยจากฐานข้อมูล
        try:    
            self.c.execute('SELECT img_lottery,amount,price,type_lottery,num_id  FROM lottery')
            self.alllottery_data = self.c.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return

        if not self.alllottery_data:
            print("No images or lottery types found in the database.")
            return
        self.store_loterry(self.alllottery_data)

    def pairLot(self):
     
        self.clear_frameItem_con()
        self.allLot_btn.configure(fg_color='#cfcfcf',hover_color='#cfcfcf', text_color='#2b2b2b')
        self.pairLot_btn.configure(fg_color='#e32320',hover_color='#e32320', text_color='white')
        self.oddLot_btn.configure(fg_color='#cfcfcf',hover_color='#cfcfcf', text_color='#2b2b2b')
            

        # เชื่อมต่อฐานข้อมูล
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        
        try:
            self.c.execute("SELECT img_lottery,amount,price,type_lottery,num_id  FROM lottery WHERE type_lottery ='หวยคู่' ")
            self.pairlottery_data = self.c.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return

        if not self.pairlottery_data:
            print("No images or lottery types found in the database.")
            return
        
        self.store_loterry(self.pairlottery_data)
        


    def oddLot(self):
        
        self.clear_frameItem_con()
        self.allLot_btn.configure(fg_color='#cfcfcf',hover_color='#cfcfcf', text_color='#2b2b2b')
        self.pairLot_btn.configure(fg_color='#cfcfcf',hover_color='#cfcfcf', text_color='#2b2b2b')
        self.oddLot_btn.configure(fg_color='#e32320',hover_color='#e32320', text_color='white')
        
 
        # เชื่อมต่อฐานข้อมูล
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        
        try:
            self.c.execute("SELECT img_lottery,amount,price, type_lottery,num_id FROM lottery WHERE type_lottery ='หวยเดี่ยว' ")
            self.oddlottery_data = self.c.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return
        

        if not self.oddlottery_data:
            print("No images or lottery types found in the database.")
            return
        self.store_loterry(self.oddlottery_data)
        
    
    def store_loterry(self, typelot):
        # แสดงข้อมูลภาพและ Combobox ในหน้า
        index = 0  # แถว table
        for i in range(len(typelot)):  # กำหนดจำนวนแถว
            for j in range(4):  # กำหนดจำนวนคอลัมน์
                if index < len(typelot):
                    img_data, amount_data, price_data, typelot_data,num_lottery = typelot[index]

                    # แปลงข้อมูล BLOB เป็นภาพ
                    img1 = Image.open(io.BytesIO(img_data))
                    img1 = img1.resize((200, 100))
                    self.img_lot = ImageTk.PhotoImage(img1)

                    # สร้างกรอบสำหรับสินค้า
                    frame_item = ctk.CTkFrame(self.frame_item_con, width=226, height=180, corner_radius=10, fg_color='#2b2b2b')
                    frame_item.grid(row=i, column=j, padx=8, pady=10)
                    self.frame_item_con.configure(width=980, height=1920)

                    # ใส่รูปภาพในกรอบสินค้า
                    self.label_image = tk.Label(frame_item, image=self.img_lot)
                    self.label_image.image = self.img_lot  # เก็บ reference ให้กับ image
                    self.label_image.place(x=10, y=35)

                    # แสดงประเภทหวย
                    typelot_label = tk.Label(frame_item, text=typelot_data, font=('Prompt', 10), fg='white', bg='#2b2b2b', width=9)
                    typelot_label.place(x=65, y=5)

                    # สร้าง Combobox สำหรับเลือกจำนวน
                    amount_combo = ctk.CTkComboBox(frame_item,
                                                    values=[str(amount_data)],
                                                    width=50, height=23,
                                                    corner_radius=5, border_width=0,
                                                    bg_color='#2b2b2b', fg_color='white',
                                                    text_color='#2b2b2b',
                                                    dropdown_fg_color='white',
                                                    dropdown_hover_color='#ebe8e8',
                                                    dropdown_text_color='#2b2b2b',
                                                    button_color='white',
                                                    button_hover_color='#ebe8e8')
                    amount_combo.place(x=12, y=148)

                    # ปุ่มหยิบใส่ตระกร้า
                    cartPick_image = Image.open(r'D:\python_finalproject\img\icon\white\26.png')
                    cartPick_img_icon = ctk.CTkImage(cartPick_image, size=(30, 20))

                    pick_btn = ctk.CTkButton(frame_item, text='หยิบใส่ตระกร้า',
                                            image=cartPick_img_icon,
                                            compound=tk.RIGHT,
                                            anchor='w',
                                            font=('Prompt', 12),
                                            width=45, height=16,
                                            border_width=0,
                                            bg_color='#2b2b2b',
                                            fg_color='#2b2b2b',
                                            hover_color='black',
                                            command=lambda n=num_lottery,i= img_data, a=amount_combo, p=price_data: self.add_cart(n, i,a.get(), p))
                    pick_btn.place(x=70, y=145)

                index += 1  # เพิ่มตัวนับรูปภาพ

        self.conn.close()

    def add_cart(self, num_lottery, img_data, amount_selected, price_data):
        # เชื่อมต่อกับฐานข้อมูล
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()

        try:
            # แปลง amount_selected เป็นจำนวนเต็ม
            amount = int(amount_selected)
            
            # สมมติว่า self.username คือชื่อผู้ใช้ปัจจุบัน
            username = self.username  

            # ตรวจสอบว่ามีรายการนี้ในฐานข้อมูลแล้วหรือไม่
            self.c.execute('SELECT * FROM orders WHERE orders_lottery_num = ? AND User_orders = ?', 
                        (num_lottery, username))
            current_amount = self.c.fetchone()

            if current_amount:
                # ถ้าพบรายการแล้ว ให้เพิ่มจำนวนเข้าไป
                new_amount = current_amount[3] +amount
                self.c.execute('''
                    UPDATE orders 
                    SET img_lottery_orders = ?, 
                        amount_orders = ?, 
                        price_orders = ?, 
                        cash = ?, 
                        status = ?
                    WHERE orders_lottery_num = ? AND User_orders = ?
                ''', (img_data, new_amount, (int(price_data) *int( new_amount,)) ,0, 'ยังไม่จ่าย', num_lottery, username))
            else:
                # ถ้าไม่พบรายการ ให้เพิ่มรายการใหม่
                self.c.execute('''
                    INSERT INTO orders (User_orders, orders_lottery_num, img_lottery_orders, amount_orders, price_orders, cash, status) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (username, num_lottery, img_data, amount, int(price_data) * int(amount), 0, 'ยังไม่จ่าย'))

            # ยืนยันการเปลี่ยนแปลงในฐานข้อมูล
            self.conn.commit()
            tkinter.messagebox.showinfo("Success", "เพิ่มล็อตเตอรี่ลงในตะกร้าเรียบร้อยแล้ว!")

        except Exception as e:
            print(f"Error adding to cart: {e}")
        finally:
            self.conn.close()
    

    def cart_page(self):
        # เชื่อมต่อกับฐานข้อมูล
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        self.changeColor_icon(self.Mysave_page, "cart", self.cart_btn)
        self.clear_main_con()
        self.main_container()

        # ดึงข้อมูลการสั่งซื้อจากฐานข้อมูล
        try:
            self.c.execute('SELECT User_orders, orders_lottery_num, img_lottery_orders, amount_orders, price_orders, cash, status FROM orders WHERE User_orders = ?', (self.username,))
            orders_data = self.c.fetchall()
        except Exception as e:
            print(f"Error fetching orders: {e}")
            orders_data = []
    
        # สร้าง Frame สำหรับ Cart List
        self.cartList_con = ctk.CTkFrame(self.main_con, fg_color='#2b2b2b', width=500, height=200, corner_radius=15)
        self.cartList_con.grid(row=0, column=0,padx=245,sticky= 'nsew',pady = 5)

        # สร้าง Canvas สำหรับเลื่อนแนวนอน
        self.cart_canvas = tk.Canvas(self.cartList_con, bg='#2b2b2b', highlightthickness=0, height=200)
        self.cart_canvas.place(x=20, y=0)

        # สร้าง Scrollbar แนวนอนสำหรับ Canvas
        self.scrollbar = ctk.CTkScrollbar(self.cartList_con, orientation='horizontal', command=self.cart_canvas.xview)
        self.scrollbar.place(x=5, y=180)
        self.cart_canvas.configure(xscrollcommand=self.scrollbar.set)

        # สร้าง Frame ภายใน Canvas สำหรับรายการสินค้า
        self.cart_items_frame = tk.Frame(self.cart_canvas, bg='#fbf5f5')
        self.cart_canvas.create_window((0, 0), window=self.cart_items_frame, anchor='nw')

        # อัปเดต scroll region เมื่อ cart_items_frame เปลี่ยนขนาด
        def update_scroll_region(event=None):
            self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all"))

        self.cart_items_frame.bind("<Configure>", update_scroll_region)
        
        # สร้าง container สำหรับข้อมูลการสั่งซื้อ
        list_orders_con = ctk.CTkFrame(self.main_con, width=500 ,fg_color='#ebe8e8'
                                       ,border_width=2,border_color='#cfcfcf')
        list_orders_con.grid(row=1, column=0, pady=10,padx=245,sticky= 'nsew')
        # แสดงรายการสินค้าในตะกร้า
        for i, order in enumerate(orders_data):
            username_data, num_lottery, img_lot, amount, price, cash, status = order

            # โหลดและแสดงภาพลอตเตอรี่
            try:
                img1 = Image.open(io.BytesIO(img_lot)).resize((200, 100))
                img_lottery = ImageTk.PhotoImage(img1)
            except Exception as e:
                print(f"Error loading image: {e}")
                continue

            # สร้าง container สำหรับสินค้าแต่ละรายการ
            img_con = tk.Label(self.cart_items_frame, width=100, height=200, bg="#2b2b2b")
            img_con.grid(row=0, column=i)

            # ใส่รูปภาพใน container
            label_image = tk.Label(img_con, image=img_lottery)
            label_image.image = img_lottery  # เก็บ reference เพื่อป้องกัน garbage collection
            label_image.place(x=100, y=50)

            list_label = ctk.CTkLabel(list_orders_con, text='รายการลอตเตอรี่', font=('Prompt', 16),
                                      text_color='black')
            list_label.grid(row=0, column=0,padx=125,pady= 5,sticky= 'nsew' )
            
            # ตั้งค่าให้ list_orders_con ขยายแถวและคอลัมน์ที่ Allorders_list_con อยู่
            list_orders_con.rowconfigure(0, weight=1)   # กำหนดแถว 1 ให้ขยาย
            list_orders_con.columnconfigure(1, weight=1)  # กำหนดคอลัมน์ 0 ให้ขยาย

            # Frame สำหรับรายละเอียดการสั่งซื้อทั้งหมด
            Allorders_list_con = ctk.CTkFrame(list_orders_con, width=480, fg_color='#ebe8e8'
                                             )
            Allorders_list_con.grid(row=1, column=0,pady=5,padx=10,sticky= 'nsew')

            # Frame สำหรับรายละเอียดการสั่งซื้อเฉพาะรายการ
            orders_list_con = ctk.CTkFrame(Allorders_list_con, width=480, height=200, 
                                        fg_color='#ffffff',
                                        border_width=1,border_color='#b8b8b8')
            orders_list_con.grid(row=i, column=0,columnspan = 2,pady=0,padx =0,sticky ='nsew')           

            # ตั้งค่าให้ Allorders_list_con ขยายแถวและคอลัมน์ที่ orders_list_con อยู่
            Allorders_list_con.columnconfigure(3, weight=1)  # กำหนดคอลัมน์ 0 ให้ขยาย


            # เพิ่มปุ่มลบ พร้อมคำสั่งลบสินค้าออกจากตะกร้า
            delete_btn = ctk.CTkButton(orders_list_con, width=40, height=40, corner_radius=5,
                                       text ='X',font=('Prompt', 16),
                                       fg_color='#e32320',hover_color='#c20300',

                                    command=lambda o=order: self.delete_item_from_cart(o))
            delete_btn.grid(row=0, column=0, sticky='w', padx=5,pady =5)

            # แสดงจำนวนและราคา
            num_label = ctk.CTkLabel(orders_list_con, text=f'{num_lottery}',
                                                font=('Prompt', 16),
                                                text_color='black')
            num_label.grid(row=0, column=1, padx=10, sticky='w')
            
            amount_label = ctk.CTkLabel(orders_list_con, text=f'x{amount}',
                                                font=('Prompt', 14),
                                                text_color='#cfcfcf')
            amount_label.grid(row=0, column=2, padx=2, sticky='w')
            
            price_label = ctk.CTkLabel(orders_list_con, text=f'{price} บาท',
                                                font=('Prompt', 16),
                                                text_color='black', anchor='e')
            price_label.grid(row=0, column=3, sticky='e',padx =10,)
            orders_list_con.columnconfigure(3, weight=1)
            
            total_price_text = ctk.CTkLabel(Allorders_list_con, text='ยอดรวม',
                                                font=('Prompt', 16),
                                                text_color='black', anchor='w')
            total_price_text.grid(row=2, column=0, sticky='w',padx =10,pady=10)
            
            
            total_price_label = ctk.CTkLabel(Allorders_list_con, text=f'{price} บาท',
                                                font=('Prompt', 16),
                                                text_color='black', anchor='e')
            total_price_label.grid(row=2, column=1, sticky='e',padx =10,pady=10)
            
            pay_btn = ctk.CTkButton(Allorders_list_con
                                    ,text = 'ชำระเงิน',font = ('Prompt',16)
                                    ,width=480,height=40,
                                    text_color='white',fg_color='#e32320',
                                    hover_color='#c20300',
                                    command=self.payment_ui
                                    )
            pay_btn.grid(row = 3,column =0,columnspan = 2, padx =10 ,pady =5,sticky ='nsew')


        # ปิดการเชื่อมต่อฐานข้อมูล
        self.conn.close()
        
    def payment_ui(self):
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM orders WHERE User_orders = ?', (self.username,))
        d = self.c.fetchone()  # ใช้ fetchone() แทน fetchall() หากดึงข้อมูลรายการเดียว
        
        # สร้างอินสแตนซ์
        api_pay = api_payment.API_PAYMENT()
        
        # 1. รับค่า access_token ที่ได้จาก API
        access_token = api_pay.get_oauth_token()
        if access_token:
            # ข้อมูลสำหรับการสร้าง QR Code
            biller_id = "838570584253024"  # รหัส Biller
            price = d[5]  # จำนวนเงิน ควรตรวจสอบดัชนีของ d ก่อนใช้
            ref1 = "TESTREF1"  # หมายเลขอ้างอิง
            ref2 = "TESTREF2"  # หมายเลขอ้างอิง

            # 2. ส่งข้อมูลเพื่อสร้าง QR CODE ชำระเงิน
            qr_image_base64 = api_pay.create_qr_code(access_token, biller_id, price, ref1, ref2)

            if qr_image_base64:  # ตรวจสอบว่ามีข้อมูล Base64
                # 3. แสดงหน้าชำระเงิน
                self.payment_page = tk.Toplevel(self.store)
                self.payment_page.geometry('400x400')
                self.payment_page.title('ชำระเงิน')

                OR_IMG = api_pay.save_qr_image_from_base64(qr_image_base64)  # ดึงรูป QR Code ที่สร้างได้
                if OR_IMG:
                    QR_LABEL = tk.Label(self.payment_page, image=OR_IMG)
                    QR_LABEL.image = OR_IMG  # เก็บอ้างอิงเพื่อไม่ให้ภาพถูกเก็บขยะ
                    QR_LABEL.pack()
                else:
                    print("Failed to load QR Code image.")
            else:
                print("Failed to create QR Code.")
        else:
            print("Failed to obtain access token.")

        # 4. เมื่อชำระเงินเสร็จ ให้ปิดหน้าต่างชำระเงิน
        # เพิ่มการตรวจสอบด้วย biller_id, ref1, transaction_date
        transaction_date = "2020-01-01"  # ตัวอย่างวันที่ (ปรับเป็นค่าจริงตามต้องการ)
        if api_pay.payment_success() == "Success":
            self.payment_page.destroy()

        self.conn.close()


    def delete_item_from_cart(self, order):
        try:
            # ลบรายการออกจากฐานข้อมูล
            self.conn = sqlite3.connect('data.db')
            self.c = self.conn.cursor()
            self.c.execute('DELETE FROM orders WHERE User_orders = ? AND orders_lottery_num = ?', (self.username, order[1]))
            self.conn.commit()
            self.conn.close()
            
            # รีเฟรชหน้าตะกร้า
            self.cart_page()
        except Exception as e:
            print(f"Error deleting item: {e}")


          
    def Mysave_page(self):
        self.changeColor_icon(self.Mysave_page,"save",self.save_btn)
        self.clear_main_con()
       
        
    
    def profile_page(self):
        self.changeColor_icon(self.profile_page,"profile",self.profile_btn)
        self.clear_main_con() 
    def admin_menu_ui(self):
        self.root.destroy()  # ปิดหน้าต่างหลัก
        self.admin_store = tk.Tk()  # สร้างหน้าต่างใหม่สำหรับหน้าผู้ดูแลระบบ
        self.admin_store.tk.call('tk', 'scaling', 1.5)
        self.admin_store.geometry("1080x620")
        self.admin_store.title('ALL LOTTERY - Admin')
        self.admin_store.configure(bg="white")
        
        # สร้างเมนูด้านซ้าย
        admin_bar = tk.Frame(self.admin_store, background='#ff914d', width=100, height=1080)
        admin_bar.place(x=0, y=0)

        # ปุ่มดูรายการสั่งซื้อ
        adminhome_image = Image.open(r'D:\python_finalproject\img\icon\white\22.png')  # แก้ไขเส้นทางให้ถูกต้อง
        adminhome_img_icon = ctk.CTkImage(adminhome_image, size=(80, 40))  # ปรับขนาดที่ต้องการ
        # สร้าง CTkButton พร้อมภาพ
        self.adminhome_btn = ctk.CTkButton(
            admin_bar,
            fg_color='#ff914d',
            border_width=0,
            corner_radius=0,
            width=100,
            height=10,
            image=adminhome_img_icon,
            text="หน้าหลัก",
            font=('Kanit Regular',14),
            compound=TOP,
            bg_color='#ff914d',
            hover_color='#ff914d',  # เปลี่ยนสีเมื่อ hover
            command=self.admin_page
        )
        self.adminhome_btn.place(x=0, y=85)    

        add_lottery_image = Image.open(r'D:\python_finalproject\img\icon\white\addlottery.png')
        add_lottery_img_icon = ctk.CTkImage(add_lottery_image, size=(80, 40))
        self.addlottery_btn = ctk.CTkButton(
            admin_bar,
            fg_color='#ff914d',
            border_width=0,
            corner_radius=0,
            width=100,
            height=90,
            image=add_lottery_img_icon,
            text='จัดการหวย',
            font=('Kanit Regular', 14),
            compound=TOP,
            bg_color='#ff914d',
            hover_color='#ff914d',
            command=self.add_lottery_page
        )
        self.addlottery_btn.place(x=0, y=180)
        
        
        # ปุ่มออกจากระบบ
        logout_image = Image.open(r'D:\python_finalproject\img\icon\white\25.png')
        logout_img_icon = ctk.CTkImage(logout_image, size=(80, 40))
        self.logout_btn = ctk.CTkButton(
            admin_bar,
            fg_color='#ff914d',
            border_width=0,
            corner_radius=0,
            width=100,
            height=90,
            image=logout_img_icon,
            text='ออกจากระบบ',
            font=('Kanit Regular', 14),
            compound=TOP,
            bg_color='#ff914d',
            hover_color='#ff914d',
            
        )
        self.logout_btn.place(x=0, y=495)
        
        
        # สร้างพื้นที่สำหรับแสดงข้อมูล (เช่น รายการหวยหรือผู้ใช้)
        self.admin_main_con = ctk.CTkCanvas(self.admin_store)
        self.admin_main_con.place(x=100, y=0, width=1820, height=1080)
    
        # เรียกแสดงหน้าแรกของ Admin
        self.admin_page()

    def admin_page(self):
        # สร้าง Container หลักสำหรับ Admin Page
        self.container = ctk.CTkFrame(self.admin_store, width=1920, height=600, corner_radius=0, fg_color='#ebe8e8')
        self.container.place(x=100, y=0, relwidth=1, relheight=1)

        self.greyframebg = ctk.CTkFrame(self.container, corner_radius=15, width=800, height=420, fg_color='white')
        self.greyframebg.place(x=50, y=100)

        self.button_frame = tk.Frame(self.greyframebg, bg='white')  
        self.button_frame.place(relx=0, rely=0.5, anchor='w') 

        # ปุ่มจัดการข้อมูลลอตเตอรี่
        manage_lottery_image = Image.open(r'D:\python_finalproject\img\icon\viewlottery.png')  
        manage_lottery_icon = ctk.CTkImage(manage_lottery_image, size=(740, 136))  
        self.manage_lottery_btn = ctk.CTkButton(
            self.button_frame,
            fg_color='white',  
            border_width=0,  
            corner_radius=10,  
            width=740,  
            height=136,  
            image=manage_lottery_icon,
            command=self.manage_lottery_page, 
            hover_color='white'  
        )
        self.manage_lottery_btn.grid(row=0, column=0, padx=20, pady=20)  

        # ปุ่มจัดการข้อมูลผู้ใช้
        manage_user_image = Image.open(r'D:\python_finalproject\img\icon\viewuser.png')  
        manage_user_icon = ctk.CTkImage(manage_user_image, size=(740, 136))  
        self.manage_user_btn = ctk.CTkButton(
            self.button_frame,
            fg_color='white', 
            border_width=0,  
            corner_radius=10,  
            width=740,  
            height=136,  
            image=manage_user_icon,
            command=self.manage_user_page, 
            hover_color='white'  
        )
        self.manage_user_btn.grid(row=1, column=0, padx=20, pady=20)  


        # อัปเดตแสดงผล
        self.container.update

    def clear_admin_main_con(self):
        for widget in self.admin_main_con.winfo_children():
            widget.destroy()


    def manage_lottery_page(self):
        self.clear_admin_main_con() 
        self.container = ctk.CTkFrame(self.admin_store, width=1920, height=600, corner_radius=0, fg_color='white')
        self.container.place(x=100, y=0, relwidth=1, relheight=1)

        self.greyframebg = ctk.CTkFrame(self.container, corner_radius=15, width=800, height=500, fg_color='#fbf5f5')  
        self.greyframebg.place(x=50, y=50) 

        self.text_header = ctk.CTkLabel(self.greyframebg, text="ดูข้อมูลสลากกินแบ่ง", font=('Kanit Regular', 20))
        self.text_header.place(x=280, y=10)

        search_frame = ctk.CTkFrame(self.greyframebg, fg_color="#fbf5f5")  
        search_frame.place(x=180, y=50)

        self.text_search = ctk.CTkLabel(search_frame, text="ค้นหาสลาก", font=('Kanit Regular', 16))
        self.text_search.grid(row=0, column=0, padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(search_frame, width=200)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)

        self.search_btn = ctk.CTkButton(search_frame, text="ค้นหา", font=('Kanit Regular', 16), fg_color='black', command=self.search_lottery)
        self.search_btn.grid(row=0, column=2, padx=10, pady=5)

        frame = tk.Frame(self.greyframebg)
        frame.place(x=10, y=100, width=780, height=300)

        vert_scrollbar = tk.Scrollbar(frame, orient="vertical")
        vert_scrollbar.pack(side="right", fill="y")

        horiz_scrollbar = tk.Scrollbar(frame, orient="horizontal")
        horiz_scrollbar.pack(side="bottom", fill="x")

        columns = ("ID", "Type", "Number ID", "Price", "Amount")
        self.lottery_tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=vert_scrollbar.set, xscrollcommand=horiz_scrollbar.set)

        for col in columns:
            self.lottery_tree.heading(col, text=col)
            self.lottery_tree.column(col, width=100, minwidth=100, stretch=False)

        self.lottery_tree.pack(fill="both", expand=True)

        vert_scrollbar.config(command=self.lottery_tree.yview)
        horiz_scrollbar.config(command=self.lottery_tree.xview)

        edit_btn = ctk.CTkButton(self.greyframebg, text="แก้ไข", font=('Kanit Regular', 16), fg_color='black', command=self.edit_lottery)
        edit_btn.place(x=20, y=420)

        delete_btn = ctk.CTkButton(self.greyframebg, text="ลบข้อมูล", font=('Kanit Regular', 16), fg_color='black', command=self.delete_lottery)
        delete_btn.place(x=180, y=420)

        back_btn = ctk.CTkButton(self.greyframebg, text="กลับ", font=('Kanit Regular', 16), fg_color='black', command=self.admin_page)
        back_btn.place(x=650, y=420)

        self.refresh_lottery_list()  

    def refresh_lottery_list(self):
        self.connect_to_db() 
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)

        self.c.execute('SELECT id, type_lottery, num_id, price and amount FROM lottery')
        rows = self.c.fetchall()
        for row in rows:
            self.user_tree.insert("", tk.END, values=row)

        self.close_db()  

    def search_lottery(self):
        search_term = self.search_entry.get()
        self.connect_to_db()

        query = "SELECT id, type_lottery, num_id, price and amount FROM lottery WHERE num_id LIKE ? or type_lottery LIKE ?"
        self.c.execute(query, ('%' + search_term + '%',))

        rows = self.c.fetchall()

        for row in self.user_tree.get_children():
            self.user_tree.delete(row)

        for row in rows:
            self.user_tree.insert("", tk.END, values=row)

        self.close_db()

    def edit_lottery(self):
        pass

    def delete_lottery(self):
        selected_item = self.lottery_tree.selection()
        if selected_item:
            lottery_id = self.lottery_tree.item(selected_item)['values'][0] 
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM lottery WHERE id=?", (lottery_id,))
            conn.commit()
            conn.close()
            self.refresh_lottery_list() 

    def manage_user_page(self):
        self.clear_admin_main_con() 
        self.container = ctk.CTkFrame(self.admin_store, width=1920, height=600, corner_radius=0, fg_color='white')
        self.container.place(x=100, y=0, relwidth=1, relheight=1)

        self.greyframebg = ctk.CTkFrame(self.container, corner_radius=15, width=800, height=500, fg_color='#fbf5f5')  
        self.greyframebg.place(x=50, y=50) 

        self.text_header = ctk.CTkLabel(self.greyframebg, text="ดูข้อมูลผู้ใช้งานทั้งหมด", font=('Kanit Regular', 20))
        self.text_header.place(x=280, y=10)

        search_frame = ctk.CTkFrame(self.greyframebg, fg_color="#fbf5f5")  
        search_frame.place(x=180, y=50)

        self.text_search = ctk.CTkLabel(search_frame, text="ค้นหาผู้ใช้", font=('Kanit Regular', 16))
        self.text_search.grid(row=0, column=0, padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(search_frame, width=200)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)

        self.search_btn = ctk.CTkButton(search_frame, text="ค้นหา", font=('Kanit Regular', 16), fg_color='black', bg_color='#cfcfcf',command=self.search_user)
        self.search_btn.grid(row=0, column=2, padx=10, pady=5)

        frame = tk.Frame(self.greyframebg)
        frame.place(x=10, y=100, width=780, height=300)

        vert_scrollbar = tk.Scrollbar(frame, orient="vertical")
        vert_scrollbar.pack(side="right", fill="y")

        horiz_scrollbar = tk.Scrollbar(frame, orient="horizontal")
        horiz_scrollbar.pack(side="bottom", fill="x")


        columns = ("ID", "Username", "Password", "First Name", "Last Name", "Age", "Email", "Bank Number", "Bank Name", "Address", "Phone", "Access")
        self.user_tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=vert_scrollbar.set, xscrollcommand=horiz_scrollbar.set)

        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=100, minwidth=100, stretch=False)  

        self.user_tree.pack(fill="both", expand=True)

        vert_scrollbar.config(command=self.user_tree.yview)
        horiz_scrollbar.config(command=self.user_tree.xview)

        
        edit_btn = ctk.CTkButton(self.greyframebg, text="แก้ไข", font=('Kanit Regular', 16), fg_color='black', command=self.edit_user)
        edit_btn.place(x=20, y=420)

        delete_btn = ctk.CTkButton(self.greyframebg, text="ลบข้อมูล", font=('Kanit Regular', 16), fg_color='black', command=self.delete_user)
        delete_btn.place(x=180, y=420)

        back_btn = ctk.CTkButton(self.greyframebg, text="กลับ", font=('Kanit Regular', 16), fg_color='black', command=self.admin_page)
        back_btn.place(x=650, y=420)


        self.refresh_user_list()

        
    def connect_to_db(self):
        self.conn = sqlite3.connect('data.db')  
        self.c = self.conn.cursor()  

    def close_db(self):
        if self.conn:
            self.conn.close()  

    def refresh_user_list(self):
        self.connect_to_db()  # เปิดการเชื่อมต่อกับฐานข้อมูล
        # ล้างข้อมูลใน Treeview ก่อน
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)

        # ดึงข้อมูลจากฐานข้อมูลมาแสดง
        self.c.execute('SELECT id, username, password, fname, lname, Age, email, Bank_Number, Bank_Name, Address, phone, access FROM users')
        rows = self.c.fetchall()
        for row in rows:
            self.user_tree.insert("", tk.END, values=row)

        self.close_db()  # ปิดการเชื่อมต่อหลังจากทำงานเสร็จ

    def search_user(self):
        # รับข้อมูลที่ผู้ใช้ป้อนในช่องค้นหา
        search_term = self.search_entry.get()

        # เชื่อมต่อกับฐานข้อมูล
        self.connect_to_db()

        # สร้างคำสั่ง SQL เพื่อค้นหาผู้ใช้ตามเงื่อนไข
        query = "SELECT id, username, password, fname, lname, Age, email, Bank_Number, Bank_Name, Address, phone, access FROM users WHERE username LIKE ? OR fname LIKE ? OR lname LIKE ?"
        self.c.execute(query, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))

        # ดึงข้อมูลที่ตรงกับการค้นหา
        rows = self.c.fetchall()

        # ล้างข้อมูลเก่าจากตาราง Treeview ก่อนแสดงข้อมูลใหม่
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)

        # แสดงข้อมูลใหม่ใน Treeview
        for row in rows:
            self.user_tree.insert("", tk.END, values=row)

        # ปิดการเชื่อมต่อกับฐานข้อมูล
        self.close_db()

    def edit_user(self):
        # สร้างหน้าต่างย่อย
        self.edit_window = ctk.CTkToplevel(self.container)
        self.edit_window.title("แก้ไขข้อมูลผู้ใช้งาน")
        self.edit_window.geometry("400x700")  
        
        # กำหนดกรอบสำหรับฟอร์มการแก้ไข
        form_frame = ctk.CTkFrame(self.edit_window, fg_color="white")
        form_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # สร้าง Label และช่องกรอกข้อมูลสำหรับแต่ละฟิลด์
        labels = ["ID", "Username", "Password", "First Name", "Last Name", "Age", "Email", 
                "Bank Number", "Bank Name", "Address", "Phone", "Access"]
        self.entries = []  # เก็บรายการของช่องกรอกข้อมูล
        
        # สร้างฟอร์มอัตโนมัติจากลิสต์ labels
        for i, label in enumerate(labels):
            ctk.CTkLabel(form_frame, text=label, font=('Kanit Regular', 16)).grid(row=i, column=0, padx=10, pady=10)
            entry = ctk.CTkEntry(form_frame)
            entry.grid(row=i, column=1, padx=10, pady=10)
            self.entries.append(entry) 

        # ปุ่มยืนยันการแก้ไข
        save_btn = ctk.CTkButton(form_frame, text="บันทึก", font=('Kanit Regular', 16), command=self.save_user_edits)
        save_btn.grid(row=len(labels), column=0, columnspan=2, pady=20)

        self.load_user_data_to_edit()

    def load_user_data_to_edit(self):
        selected_item = self.user_tree.selection()
        if selected_item:
            user_data = self.user_tree.item(selected_item, "values")
            for i, entry in enumerate(self.entries):
                entry.insert(0, user_data[i])

    def save_user_edits(self):
        new_data = [entry.get() for entry in self.entries]

        selected_item = self.user_tree.selection()
        if selected_item:
            self.user_tree.item(selected_item, values=new_data)
        
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()

            user_id = new_data[0] 
            username = new_data[1]
            password = new_data[2]
            fname = new_data[3]
            lname = new_data[4]
            age = new_data[5]
            email = new_data[6]
            bank_number = new_data[7]
            bank_name = new_data[8]
            address = new_data[9]
            phone = new_data[10]
            access = new_data[11]

            # อัพเดตข้อมูลในฐานข้อมูล SQLite
            cursor.execute('''
                UPDATE users 
                SET username=?, password=?, fname=?, lname=?, age=?, email=?, bank_number=?, bank_name=?, address=?, phone=?, access=?
                WHERE id=?
            ''', (username, password, fname, lname, age, email, bank_number, bank_name, address, phone, access, user_id))

            conn.commit()
            conn.close()

        self.edit_window.destroy()

    def delete_user(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "กรุณาเลือกผู้ใช้ที่ต้องการลบ!")
            return

        user_id = self.user_tree.item(selected_item, 'values')[0]

        confirm = messagebox.askyesno("Confirm", "คุณแน่ใจว่าจะลบผู้ใช้นี้หรือไม่?")
        if confirm:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()

            cursor.execute('DELETE FROM users WHERE id=?', (user_id,))

            conn.commit()
            conn.close()

            self.user_tree.delete(selected_item)

            self.refresh_user_list()

    #หน้าแอดมินน
    def add_lottery_page(self):
        self.clear_admin_main_con()
        self.container = ctk.CTkFrame(self.admin_store, width=1920, height=600, corner_radius=0, fg_color='white')
        self.container.place(x=100, y=0, relwidth=1, relheight=1)

        self.greyframebg = ctk.CTkFrame(self.container, corner_radius=15, width=800, height=500, fg_color='#fbf5f5')  
        self.greyframebg.place(x=50, y=50) 

        self.text_header = ctk.CTkLabel(self.greyframebg, text="คลังลอตเตอรี่", font=('Kanit Regular', 20))
        self.text_header.place(x=300, y=10)

        lottery_number_label = ctk.CTkLabel(self.greyframebg, text="หมายเลขลอตเตอรี่", font=('Kanit Regular', 16))
        lottery_number_label.place(x=100, y=100)

        self.lottery_number_entry = ctk.CTkEntry(self.greyframebg, width=300)
        self.lottery_number_entry.place(x=300, y=100)

        lottery_type_label = ctk.CTkLabel(self.greyframebg, text="ประเภทลอตเตอรรี่", font=('Kanit Regular', 16))
        lottery_type_label.place(x=100, y=150)

        self.lottery_type_entry = ctk.CTkEntry(self.greyframebg, width=300)
        self.lottery_type_entry.place(x=300, y=150)

        amount_label = ctk.CTkLabel(self.greyframebg, text="จำนวน", font=('Kanit Regular', 16))
        amount_label.place(x=100, y=200)

        self.amount_entry = ctk.CTkEntry(self.greyframebg, width=300)
        self.amount_entry.place(x=300, y=200)

        price_label = ctk.CTkLabel(self.greyframebg, text="ราคาต่อหน่วย", font=('Kanit Regular', 16))
        price_label.place(x=100, y=250)

        self.price_entry = ctk.CTkEntry(self.greyframebg, width=300)
        self.price_entry.place(x=300, y=250)
        
        self.select_label = ctk.CTkLabel(self.greyframebg,text='เลือกรูปลอตเตอรี่ : ',font=('Kanit Regular', 16))
        self.select_label.place(x=100,y=300)
        
        self.select_con =  ctk.CTkFrame(self.greyframebg,width=280,height=130,fg_color='white')
        self.select_con.place(x = 300 , y =300)
        self.select_status = ctk.CTkLabel(self.select_con,text='',font=('Kanit Regular', 14))
        self.select_status.place(x = 0 , y = 0)
        
        self.select_file_btn = ctk.CTkButton(self.greyframebg,text='เลือกไฟล์', font=('Kanit Regular', 16),
                                             command=self.select_file)
        self.select_file_btn.place(x=600,y=300)
        self.file_path =None

        save_btn = ctk.CTkButton(self.greyframebg, text="บันทึก", font=('Kanit Regular', 16), fg_color='black', command=self.add_lottery)
        save_btn.place(x=400, y=450)
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="เลือกรูปลอตเตอรี่",
            filetypes=(("JPEG files", "*.jpg"), ("All files", "*.*"))
        )
        if file_path:
            self.file_path = file_path
            img = Image.open(file_path)
            img = img.resize((280, 130))  # ปรับขนาดภาพให้พอดีกับหน้าจอ
            self.img_ctk = ctk.CTkImage(img, size=(280, 130))
          
            self.select_status.configure(image =self.img_ctk,text ='' )
        
        pass
    
    def add_lottery(self):
        # เชื่อมต่อกับฐานข้อมูล
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        
        num_lottery = self.lottery_number_entry.get()
        type_lottery = self.lottery_type_entry.get()
        amount = self.amount_entry.get()
        price = self.price_entry.get()
        image_path = self.file_path
        # เปิดภาพ
        self.img_lottery = Image.open(image_path)
        
        # แปลงภาพเป็นข้อมูลไบนารี
        img_binary = io.BytesIO()
        self.img_lottery.save(img_binary, format='JPEG')
        img_binary_data = img_binary.getvalue()

           
        try:
            self.c.execute('SELECT * FROM lottery WHERE num_id = ?',
                        (num_lottery,))
            current_amount = self.c.fetchone()

            if current_amount:
                # ถ้าพบรายการแล้ว ให้เพิ่มจำนวนเข้าไป
                new_amount = current_amount[3] 
                self.c.execute('''
                    UPDATE lottery 
                    SET img_lottery = ?, 
                        amount = ?, 
                        price = ? 
                    WHERE num_id = ? 
                ''', (img_binary_data, new_amount, price * new_amount, num_lottery))
            else:
                # ถ้าไม่พบรายการ ให้เพิ่มรายการใหม่
                self.c.execute('''
                    INSERT INTO lottery (num_id, img_lottery, amount, price,type_lottery) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (num_lottery, img_binary_data, amount, int(price) * int(amount),type_lottery))

            # ยืนยันการเปลี่ยนแปลงในฐานข้อมูล
            self.conn.commit()
            tkinter.messagebox.showinfo("Success", "เพิ่มล็อตเตอรี่ลงในตะกร้าเรียบร้อยแล้ว!")
                                
        except Exception as e:
            print(f"Error inserting data: {e}")
        finally:
            self.conn.close()

    def save_lottery(self):
        lottery_number = self.lottery_number_entry.get()
        lottery_type = self.lottery_type_entry.get()
        amount = self.amount_entry.get()
        price = self.price_entry.get()

        # Validate inputs
        if lottery_number and lottery_type and amount.isdigit() and price.isdigit():
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO lottery (num_id, type_lottery, amount, price) VALUES (?, ?, ?, ?)",
                        (lottery_number, lottery_type, int(amount), int(price)))
            conn.commit()
            conn.close()
            self.clear_add_lottery_fields()
            self.refresh_lottery_list()
        else:
            print("กรุณากรอกข้อมูลให้ครบถ้วนและถูกต้อง")  

    def clear_add_lottery_fields(self):
        self.lottery_number_entry.delete(0, tk.END)
        self.lottery_type_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)       
            
            
# เรียกใช้งานโปรแกรม
if __name__ == "__main__":
    root = tk.Tk()
    app = main(root)
    default_font = ("Prompt",8)  # ตั้งฟอนต์ภาษาไทย เช่น "Prompt" ขนาด 14
    root.option_add("*Font", default_font)

    root.mainloop()
