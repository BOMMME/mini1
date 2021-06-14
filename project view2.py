import tkinter
from first_project_class import Crawl as wc
from tkinter import messagebox
import tkinter.ttk
import controller as ct
from controller import SQL as sql
from PIL import Image, ImageTk
import viewer_thumbs2 as vt
import os
import webbrowser





class Project:

    def __init__(self):
        self.num = 0
        self.window = tkinter.Tk()
        self.window.title("웹 크롤링")
        self.window.geometry("350x200+100+100")
        self.window.resizable(1, 1)
        self.RadioVariety = tkinter.IntVar()
        self.lb_kw = tkinter.Label(self.window, text="검색어", width=10, height=1, fg='white', bg="orange", relief='raised',
                                   padx=0, pady=0)
        self.lb_kw.grid(row=0, column=0)
        self.ent_kw = tkinter.Entry(self.window, width=22)
        self.ent_kw.grid(row=0, column=1)
        self.label_ent = tkinter.Label(self.window)
        self.label_ent.grid(column=0, row=2)


        self.lb_date = tkinter.Label(self.window, text="검색기간", width=10, height=1, fg='white', bg='green',
                                     relief='raised',
                                     padx=0, pady=0)
        self.lb_date.grid(row=1, column=0)
        self.ent_date = tkinter.Entry(self.window, width=22)
        self.ent_date.grid(row=1, column=1)

        self.ent_date = tkinter.Entry(self.window, width=22, bg='white', fg='grey')  # 플레이스홀더-회색
        self.ent_date.grid(row=1, column=1)

        self.ent_date.insert(0, "YYYYMMDD~YYYYMMDD")  # 플레이스홀더
        self.ent_date.bind("<FocusIn>", self.handle_focus_in)
        self.ent_date.bind("<FocusOut>", self.handle_focus_out)


        self.sel_img = tkinter.Radiobutton(self.window, text="이미지", value=1, variable=self.RadioVariety, command=self.SHOW)
        self.sel_img.grid(row=0, column=2, sticky='W')

        self.sel_news = tkinter.Radiobutton(self.window, text="뉴스", value=2, variable=self.RadioVariety,command=self.SHOW)
        self.sel_news.grid(row=1, column=2, sticky='W')

        self.but_exec = tkinter.Button(self.window, text="실 행", command=self.start_wc, repeatdelay=1000,
                                     repeatinterval=100)
        self.but_exec.place(x=300, y=10)


        self.result = tkinter.StringVar()  # 안내화면 레이블 위치
        self.res_Label = tkinter.Label(self.window, textvariable=self.result)
        self.res_Label.grid(column=1, row=3, padx=10)


        self.window.mainloop()

    def SHOW(self):  # 입력값 안내화면
        str = ''
        if self.RadioVariety.get() == 1:
            str = "이미지가 \n선택되었습니다"
        if self.RadioVariety.get() == 2:
            str = "뉴스가 \n선택되었습니다"
        self.result.set("{}\n{}에서\n{}까지\n{}".format(
            self.ent_kw.get(), self.ent_date.get().split('~')[0],self.ent_date.get().split('~')[1], str))

    def handle_focus_in(self,*args):  # placeholder 부분
        self.ent_date.delete(0, tkinter.END)
        self.ent_date.config(fg='black')
        print(self.ent_date.get())


    def handle_focus_out(self,*args):
        self.ent_date.config(fg='grey')
        if not self.ent_date.get():
            self.ent_date.insert(0, "YYYYMMDD~YYYYMMDD")

    def start_wc(self):
        check = ct.check_period(self.ent_date.get())
        if check is not True:
            messagebox.showerror("검색기간 오류", check)
        else:
            if self.RadioVariety.get() == 1:
                self.img_address, self.img_num = wc(self.ent_kw.get(), self.ent_date.get().split('~')[0], self.ent_date.get().split('~')[1], self.RadioVariety.get()).mini()
                # self.ImageWindow()
                self.main, self.save = vt.viewer(self, 'C:\image', kind=tkinter.Tk)
            else:
                self.kw_address, self.kw_title, self.kw_num = wc(self.ent_kw.get(), self.ent_date.get().split('~')[0], self.ent_date.get().split('~')[1], self.RadioVariety.get()).mini()
                self.NewsWindow()

    def NewsWindow(self):  # 뉴스1
        self.News_Window = tkinter.Toplevel(self.window)
        self.News_Window.geometry('640x400')
        self.News_Window.title("뉴스들")
        self.News_Window.resizable(False, False)
        self.btn_lbl = tkinter.Label(self.News_Window)
        self.Img_DB_Btn = tkinter.Button(self.btn_lbl, text="DB에 저장", command=self.news_into_DB)
        self.Img_DB_Btn.pack(side='left')
        self.list_view_button = tkinter.Button(self.btn_lbl, text="DB목록보기", repeatdelay=1000, repeatinterval=100,
                                               command=self.createNewWindow)
        self.list_view_button.pack(side='left')
        self.btn_lbl.pack(side='bottom')
        self.treeview = tkinter.ttk.Treeview(self.News_Window, columns=["기사", "주소", "검색 시작날짜", "검색 마지막날짜"],
                                             displaycolumns=["기사", "주소", "검색 시작날짜", "검색 마지막날짜"])
        self.news_scrlb = tkinter.ttk.Scrollbar(self.News_Window, command=self.treeview.yview)
        self.news_scrlb.configure(command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.news_scrlb.set)
        self.news_scrlb.pack(side='right', fill='y')
        self.treeview.pack(side='left', expand='True', fill='both')
        self.treeview.column("#0", width=20)
        self.treeview.heading("#0", text="NUM")
        self.treeview.column("기사", width=250)
        self.treeview.heading("기사", text="기사")
        self.treeview.column("주소", width=100)
        self.treeview.heading("주소", text="주소")
        self.treeview.bind("<Double-Button-1>", self.link_tree)


        self.treeview.column("검색 시작날짜", width=50, anchor='center')
        self.treeview.heading("검색 시작날짜", text="검색 시작날짜")
        self.treeview.column("검색 마지막날짜", width=50, anchor='center')
        self.treeview.heading("검색 마지막날짜", text="검색 마지막날짜")
        self.start_date_list = [self.ent_date.get().split('~')[0]] * len(self.kw_title)
        self.end_date_list = [self.ent_date.get().split('~')[1]] * len(self.kw_title)
        self.treeview_list = list(zip(self.kw_title, self.kw_address, self.start_date_list, self.end_date_list))
        for i in range(len(self.kw_title)):
            self.treeview.insert('', 'end', text=i+1, values=self.treeview_list[i], iid=str(i+1) + "번")

    def link_tree(self, event):
        selected_item = self.treeview.focus()
        sw = self.treeview.item(selected_item)['values'][1]  # 검색어
        webbrowser.open('{}'.format(str(sw)))

    def createNewWindow(self):  #뉴스2
        try:
            self.newWindow.destroy()
        except:
            pass
        self.newWindow = tkinter.Toplevel(self.window)
        result1, result2 = ct.SQL().select_all()
        self.sw_treeview = tkinter.ttk.Treeview(self.newWindow)
        self.sw_treeview['columns'] = ('search_word', 'start_date', 'end_date')
        self.sw_treeview.heading("#0", text='테이블 명', anchor='w')
        self.sw_treeview.column("#0", anchor="w")
        self.sw_treeview.heading('search_word', text='검색어')
        self.sw_treeview.column('search_word', anchor='center', width=100)
        self.sw_treeview.heading('start_date', text='시작기간')
        self.sw_treeview.column('start_date', anchor='center', width=100)
        self.sw_treeview.heading('end_date', text='끝기간')
        self.sw_treeview.column('end_date', anchor='center', width=100)
        self.select_view_button = tkinter.Button(self.newWindow, text="상세보기", repeatdelay=1000, repeatinterval=100,
                                                 command=self.selected_view_window)
        self.select_view_button.pack(side="bottom")
        self.sw_treeview.pack(side="left", expand=True)
        self.sb = tkinter.Scrollbar(self.newWindow, orient='v', command=self.sw_treeview.yview)
        self.sb.pack(side='right', fill='y')
        self.sw_treeview.configure(yscrollcommand=self.sb.set)
        for j in result2:
            self.sw_treeview.insert('', 'end', text=j[0], values=(j[1], j[2], j[3]))

    # 선택해서 가져오기
    def selected_view_window(self): #뉴스3 상세보기
        selected_item = self.sw_treeview.focus()
        table_name = self.sw_treeview.item(selected_item)['text']  # 테이블명
        sw = self.sw_treeview.item(selected_item)['values'][0]  # 검색어
        result = ct.SQL().select_search_word(sw, table_name)  # DB에서 가져온 CURSOR객체
        try:
            self.newWindow2.destroy()
        except:
            pass
        self.newWindow2 = tkinter.Toplevel(self.newWindow)
        self.sw_treeview2 = tkinter.ttk.Treeview(self.newWindow2)
        self.sw_treeview2['columns'] = ('title', 'href', 'start_date', 'end_date')
        self.sw_treeview2.column("#0", width=50)
        self.sw_treeview2.heading("#0", text="NUM")
        self.sw_treeview2.column("title", width=250)
        self.sw_treeview2.heading("title", text="기사")
        self.sw_treeview2.column("href", width=100)
        self.sw_treeview2.heading("href", text="주소")

        self.sw_treeview2.column("start_date", width=50, anchor='center')
        self.sw_treeview2.heading("start_date", text="검색 시작날짜")
        self.sw_treeview2.column("end_date", width=50, anchor='center')
        self.sw_treeview2.heading("end_date", text="검색 마지막날짜")
        self.sw_treeview2.grid(column=0, row=0)
        self.sb2 = tkinter.Scrollbar(self.newWindow2, orient='v', command=self.sw_treeview2.yview)
        self.sb2.grid(row=0, column=1, sticky='ns')
        for idx, val in enumerate(result):
            for idx2, title in enumerate(str(val[1]).split("/*/")):
                self.sw_treeview2.insert('', 'end', text=(idx2 + 1), values=(title, str(val[2]).split("/*/")[idx2], val[3], val[4]))

    def news_into_DB(self):
        self.kw_title_str = '/*/'.join(self.kw_title)
        self.kw_address_str = '/*/'.join(self.kw_address)
        self.newsDB = sql()
        self.newsDB.insert_news(self.ent_kw.get(), self.kw_address_str, self.kw_title_str,
                                self.ent_date.get().split('~')[0], self.ent_date.get().split('~')[1])

    #viewthumbs2 실행
    def ImageWindow(self, imgdir, imgfile):
        self.Image_Window = tkinter.Toplevel(self.window)
        self.Image_Window.geometry("400x500")
        self.Image_Window.title("다운받은 이미지들")
        self.Image_Window.resizable(1,1)

        self.img_list=[]

        for i in range(self.img_num):
            self.img_list.append(str(self.ent_kw.get())+str(i+1)+'.jpg')

        self.img_label = tkinter.Label(self.Image_Window)
        self.num = self.img_list.index(imgfile)
        imgpath = os.path.join(imgdir, imgfile)
        img = Image.open(imgpath)
        self.img_label.img = ImageTk.PhotoImage(img)
        self.img_label['image'] = self.img_label.img

        self.btnPrev = tkinter.Button(self.Image_Window, text="<< 이전", command=self.clickPrev)
        self.btnNext = tkinter.Button(self.Image_Window, text="다음 >>", command=self.clickNext)
        self.label3 = tkinter.Label(self.Image_Window,
                                    text="C:\image에 저장된\n {}{}.jpg".format(self.ent_kw.get(), self.num+1))
        self.label3.place(x=140, y=10)
        self.btnPrev.place(x=10, y=10)
        self.btnNext.place(x=300, y=10)
        self.img_label.place(x=15, y=50)

    def clickNext(self):
        self.num += 1
        if self.num > self.img_num-1:
            self.num = 0
        img = Image.open("C:/image/" + self.img_list[self.num])
        self.img_label.img = ImageTk.PhotoImage(img)
        self.img_label['image'] = self.img_label.img
        self.img_label.configure(image=self.img_label.img)

        self.label3 = tkinter.Label(self.Image_Window, text="C:\image에 저장된\n {}{}.jpg".format(self.ent_kw.get(),self.num+1))
        self.label3.place(x=140,y=10)
    def clickPrev(self):
        self.num -= 1
        if self.num < 0:
            self.num = self.img_num-1
        img = Image.open("C:/image/" + self.img_list[self.num])
        self.label3 = tkinter.Label(self.Image_Window, text="C:\image에 저장된\n {}{}.jpg".format(self.ent_kw.get(),self.num+1))
        self.label3.place(x=140, y=10)
        self.img_label.img = ImageTk.PhotoImage(img)
        self.img_label['image'] = self.img_label.img
        self.img_label.configure(image=self.img_label.img)

    def createNewWindow3(self):  #이미지 목록보기
        try:
            self.newWindow3.destroy()
        except:
            pass
        self.newWindow3 = tkinter.Toplevel(self.window)
        result1, result2 = ct.SQL().select_all()
        self.sw_treeview3 = tkinter.ttk.Treeview(self.newWindow3)
        self.sw_treeview3['columns'] = ('search_word', 'start_date', 'end_date')
        self.sw_treeview3.heading("#0", text='테이블 명', anchor='w')
        self.sw_treeview3.column("#0", anchor="w")
        self.sw_treeview3.heading('search_word', text='검색어')
        self.sw_treeview3.column('search_word', anchor='center', width=100)
        self.sw_treeview3.heading('start_date', text='시작기간')
        self.sw_treeview3.column('start_date', anchor='center', width=100)
        self.sw_treeview3.heading('end_date', text='끝기간')
        self.sw_treeview3.column('end_date', anchor='center', width=100)
        self.select_view_button2 = tkinter.Button(self.newWindow3, text="상세보기", repeatdelay=1000, repeatinterval=100,
                                                  command=self.selected_view_window2)
        self.select_view_button2.pack(side="bottom")
        self.sw_treeview3.pack(side="left", expand=True)
        self.sb3 = tkinter.Scrollbar(self.newWindow3, orient='v', command=self.sw_treeview3.yview)
        self.sb3.pack(side='right', fill='y')
        self.sw_treeview3.configure(yscrollcommand=self.sb3.set)
        for j in result1:
            self.sw_treeview3.insert('', 'end', text=j[0], values=(j[1], j[2], j[3]))


    #
    def link_tree1(self, event):
        selected_item = self.sw_treeview4.focus()
        sw = self.sw_treeview4.item(selected_item)['values'][0]  # 검색어
        webbrowser.open('{}'.format(str(sw)))

    def selected_view_window2(self): #이미지상세보기
        selected_item = self.sw_treeview3.focus()
        table_name = self.sw_treeview3.item(selected_item)['text']  # 테이블명
        sw = self.sw_treeview3.item(selected_item)['values'][0]  # 검색어
        result = ct.SQL().select_search_word(sw, table_name)  # DB에서 가져온 CURSOR객체
        try:
            self.newWindow4.destroy()
        except:
            pass
        self.newWindow4 = tkinter.Toplevel(self.newWindow3)
        self.sw_treeview4 = tkinter.ttk.Treeview(self.newWindow4)
        self.sw_treeview4['columns'] = ('href', 'start_date', 'end_date')
        self.sw_treeview4.column("#0", width=50)
        self.sw_treeview4.heading("#0", text="NUM")
        self.sw_treeview4.column("href", width=500)
        self.sw_treeview4.heading("href", text="주소")
        self.sw_treeview4.bind("<Double-Button-1>", self.link_tree1)
        self.sw_treeview4.column("start_date", width=200, anchor='center')
        self.sw_treeview4.heading("start_date", text="검색 시작날짜")
        self.sw_treeview4.column("end_date", width=200, anchor='center')
        self.sw_treeview4.heading("end_date", text="검색 마지막날짜")
        self.sw_treeview4.grid(column=0, row=0)
        self.sb4 = tkinter.Scrollbar(self.newWindow4, orient='v', command=self.sw_treeview4.yview)
        self.sb4.grid(row=0, column=1, sticky='ns')
        for idx, val in enumerate(result):
            for idx2, title in enumerate(str(val[1]).split("/*/")):
                self.sw_treeview4.insert('', 'end', text=(idx2 + 1), values=(title, val[2], val[3]))

    def image_into_DB(self):
        self.img_address_str = '/*/'.join(self.img_address)
        self.newsDB1 = sql()
        self.newsDB1.insert_image(self.ent_kw.get(), self.img_address_str,
                                  self.ent_date.get().split('~')[0], self.ent_date.get().split('~')[1])



if __name__ == '__main__':
    pj = Project()