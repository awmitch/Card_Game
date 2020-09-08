# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 18:30:02 2016

@author: alecwmitchell
"""

from Tkinter import *
from time import sleep
from random import shuffle

class App:
    def __init__(self,master,pot_index,last_card):
        self.master = master
        self.master.title("Get Chan: Drunk: Battle")
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.default_color = self.master.cget("bg")
        self.menubar.add_command(label="Shuffle",command=self.shuffle_deck)
        self.menubar.entryconfig("Shuffle",state=DISABLED)
        self.suit = {'Hearts':['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King'],
                     'Diamonds':['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King'],
                     'Spades':['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King'],
                     'Clubs':['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']}      
        self.wrong_flag = 0
        self.pot_index = pot_index
        self.last_card = StringVar()
        self.pot_size = IntVar()
        self.old_pot = IntVar()
        self.old_card = StringVar()
        self.old_old_card = StringVar()
        self.pot_size_up = IntVar()
        self.turn_count = IntVar()
        self.old_turn_count = IntVar()
        self.notice = StringVar()
        self.card_count = IntVar()
#        self.time_count = IntVar()
        self.frame = Frame(master)
        self.frame.pack()
        self.resultframe = Frame(self.frame)
        self.infoframe = Frame(self.frame)
        self.turnframe = Frame(self.infoframe)
        self.oldturnframe = Frame(self.infoframe)
        self.drinkframe = Frame(self.infoframe)
        self.cardframe = Frame(self.infoframe)
        self.pot_size.set(0)
        self.turn_count.set(0)
#        self.time_count.set(0)
        if len(pot_index) != 0:
            self.card_count.set(52-len(pot_index))
        else:
            self.card_count.set(51)
        self.card_up = Label(self.frame,textvariable=self.last_card,font=("system", 20))
        self.pot_size_label = Label(self.frame,textvariable=self.pot_size_up,font=("system", 20))
        self.old_card_label = Label(self.infoframe,textvariable=self.old_card,font=("system", 20))
        self.old_old_card_label = Label(self.infoframe,textvariable=self.old_old_card,font=("system", 20))
        self.turn_count_label = Label(self.turnframe,textvariable=self.turn_count,font=("system", 20))
        self.old_turn_count_label = Label(self.oldturnframe,textvariable=self.old_turn_count,font=("system", 20))
        self.notice_label = Label(self.infoframe,textvariable=self.notice,font=("Times", 40, "bold"),fg='red')
        self.turn_label = Label(self.turnframe, text="Turn:",font=("system", 20))
        self.old_turn_label = Label(self.oldturnframe, text = "Last Turn:",font=("system", 20))
        self.drink_label = Label(self.drinkframe, text = "Drink for:",font=("system", 20))
        self.drink_count_label = Label(self.drinkframe,textvariable=self.old_pot,font=("system", 20))
        self.card_label = Label(self.cardframe,text="Cards left:",font=("system", 20))
        self.card_count_label = Label(self.cardframe,textvariable=self.card_count,font=("system", 20))
#        self.timer_label = Label(self.infoframe,textvariable=self.time_count,font=("system", 20))
#        self.pot_list = Listbox(self.frame,width=18,height=10,selectmode=EXTENDED)
#        self.pot_list.grid(row=0,column=0)
        self.higher = Button(self.frame,text="Higher",command=self.add_higher,fg='red',font=("system", 20))
        self.lower = Button(self.frame,text="Lower",command=self.add_lower,fg='blue',font=("system", 20))
        self.tie = Button(self.frame,text="Tie",command=self.add_tie,fg='orange',font=("system", 20))
#        self.stat.grid(row=1,column=0)
#        self.stat = Button(self.frame,text="Stat",command=self.add_stat,state=ACTIVE)        
        self.pass_button = Button(self.infoframe,text="Pass",state=DISABLED,bg='red',font=("system", 20))
        self.time_button = Button(self.infoframe,bitmap="hourglass",command=self.timer,state=DISABLED,bg='red',font=("system", 20))
        self.pass_button.config(command=self.pass_fun)
        self.reset()
        self.card_up.grid(row=0,column=2,sticky=E)   
        self.pot_size_label.grid(row=1,column=2,sticky=E)
        self.higher.grid(row=0,column=1,sticky=W)
        self.lower.grid(row=1,column=1,sticky=W)
        self.tie.grid(row=0,column=0,rowspan=2,sticky=N+S+E+W)
        self.resultframe.grid(row=2,column=2,sticky=N)
        self.infoframe.grid(row=2,column=0, columnspan=2,sticky=N+E+W)
        self.old_card_label.grid(row=0,column=2,sticky=W)
        self.old_old_card_label.grid(row=0,column=0,sticky=E)
        self.notice_label.grid(row=0,column=1,sticky=W+E+N+S)
        self.pass_button.grid(row=1,column=2,rowspan=2,sticky=N+S+W,padx=40)
        self.time_button.grid(row=3,column=2,rowspan=2,sticky=N+S+W+E)
        self.turnframe.grid(row=1,column=0,sticky=E)
        self.oldturnframe.grid(row=2,column=0,sticky=E)
        self.drinkframe.grid(row=3,column=0,sticky=E)
        self.cardframe.grid(row=4,column=0,sticky=E)
        self.turn_label.pack(side=LEFT)
        self.old_turn_label.pack(side=LEFT)
        self.turn_count_label.pack(side=RIGHT)
        self.old_turn_count_label.pack(side=RIGHT)
        self.drink_label.pack(side=LEFT)
        self.drink_count_label.pack(side=RIGHT)
        self.card_label.pack(side=LEFT)
        self.card_count_label.pack(side=RIGHT)
#        self.timer_label.grid(row=3,column=2,rowspan=2,sticky=N+S+E)
    def shuffle_deck(self):
        pot_index = self.pot_index
        self.master.destroy()
        root = Tk()
        root.geometry("%dx%d+%d+%d" % (750, 1000, 0, 0))
        app=App(root,pot_index,last_card)
        root.mainloop()
    def reset(self):
        self.m,self.n = 0,0
        self.deck = []
        print self.pot_index, "reset"
        for self.key in self.suit.keys():
            for self.index in range(0,len(self.suit[self.key])):
                self.deck.append((self.suit[self.key][self.index],self.key))
        self.card_index = []
        for i in range(len(self.deck)):
            if i not in self.pot_index:
                self.card_index.append(i)
            else:
                print self.deck[i]
        shuffle(self.card_index)
        if len(self.pot_index) != 0:
            self.card_index.append(self.pot_index[-1])
            for index in self.pot_index:
                if index != self.pot_index[-1]:
                    self.card_var_init = self.deck[index]
                    self.card_var = ''
                    for char in self.card_var_init:
                        if char != "'" and char != "(" and char != ")" and char != ',':
                            self.card_var += str(char)
                    Label(self.resultframe, text='%s'%self.card_var,font=("system", 20)).grid(row=self.m,column=self.n,sticky=N)
                    Label(self.resultframe, text='%s'%(self.pot_size.get()+1),font=("system", 20)).grid(row=self.m+1,column=self.n,sticky=N)
                    self.m += 2
                    self.pot_size.set(self.pot_size.get()+1)
        else:
            self.pot_index.append(self.card_index[-1]) 
        self.last_card.set(self.deck[self.card_index[-1]])

        self.pot_size_up.set(self.pot_size.get()+1)
        self.old_card.set('')
        self.old_old_card.set('')
        self.notice.set('')  
        self.pass_button.config(bg='red',state=DISABLED)
    def timer(self):
#        self.time = self.time_count.get()
        self.time = self.old_pot.get()
        for sec in range(0,self.time):
            sleep(0.7)
            self.old_pot.set(self.time-sec-1)
    def record(self):
        self.card_var_init = self.last_card.get()
        self.card_var = ''
        for char in self.card_var_init:
            if char != "'" and char != "(" and char != ")" and char != ',':
                self.card_var += str(char)
        Label(self.resultframe, text='%s'%self.card_var,fg=self.color,font=("system", 20)).grid(row=self.m,column=self.n,sticky=N)
        Label(self.resultframe, text='%s'%(self.pot_size.get()+1),fg=self.scolor,font=("system", 20)).grid(row=self.m+1,column=self.n,sticky=N)
        self.m += 2
    def add_higher(self):
        if self.deck[self.card_index[-1]][0] == 'Ace':
            card1 = 14
        elif self.deck[self.card_index[-1]][0] == 'King':
            card1 = 13
        elif self.deck[self.card_index[-1]][0] == 'Queen':
            card1 = 12
        elif self.deck[self.card_index[-1]][0] == 'Jack':
            card1 = 11
        else:
            card1 = self.deck[self.card_index[-1]][0]
        if self.deck[self.card_index[-2]][0] == 'Ace':
            card2 = 14
        elif self.deck[self.card_index[-2]][0] == 'King':
            card2 = 13
        elif self.deck[self.card_index[-2]][0] == 'Queen':
            card2 = 12
        elif self.deck[self.card_index[-2]][0] == 'Jack':
            card2 = 11
        else:
            card2 = self.deck[self.card_index[-2]][0]
        if int(card1) < int(card2):
            self.color = 'red'
            self.scolor = 'dark green'
            self.old_card.set('')
            self.old_old_card.set('')
            self.notice.set('')       
            self.record()
            self.pot_size.set(self.pot_size.get()+1)
            self.pot_size_up.set(self.pot_size.get()+1)
            self.turn_count.set(self.turn_count.get()+1)
            if self.turn_count.get() > 1:
                self.pass_button.config(bg='green',state=ACTIVE)
            self.time_button.config(bg='red',state=DISABLED)
        elif int(card1) > int(card2):
            self.scolor = 'purple'
            self.color = 'red'
            self.old_card.set(self.deck[self.card_index[-2]])
            self.old_card_label.config(fg='blue')
            self.old_old_card.set(self.deck[self.card_index[-1]])
            self.old_old_card_label.config(fg='red')
            self.old_pot.set(self.pot_size.get()+2)
            self.old_turn_count.set(self.turn_count.get())
            self.pot_size.set(0)
            self.pot_size_up.set(self.pot_size.get()+1)
            self.wrong_flag = 1
            self.notice.set('!')
            self.turn_count.set(0)
            self.pass_button.config(bg='red',state=DISABLED)
            self.time_button.config(bg='green',state=ACTIVE)
        else:
            self.color = 'red'
            self.scolor = 'purple'
            self.old_card.set(self.deck[self.card_index[-2]])
            self.old_card_label.config(fg='orange')
            self.old_old_card.set(self.deck[self.card_index[-1]])
            self.old_old_card_label.config(fg='red')
            self.old_pot.set(self.pot_size.get()+2)
            self.old_turn_count.set(self.turn_count.get())
            self.pot_size.set(0)
            self.pot_size_up.set(self.pot_size.get()+1)
            self.wrong_flag = 1
            self.notice.set('!')
            self.turn_count.set(0)
            self.pass_button.config(bg='red',state=DISABLED)
            self.time_button.config(bg='green',state=ACTIVE)
        self.deck[self.card_index[-1]] 
        self.card_index.pop()
        self.card_count.set(self.card_count.get()-1)
        self.last_card.set(self.deck[self.card_index[-1]])
        self.pot_index.append(self.card_index[-1])
        if len(self.card_index) == 2 and self.wrong_flag == 1:
            self.higher.config(state = DISABLED)
            self.lower.config(state = DISABLED)
            self.tie.config(state = DISABLED)
            self.menubar.entryconfig("Shuffle",state=ACTIVE)
        elif len(self.card_index) == 1 and self.wrong_flag == 0:
            self.higher.config(state = DISABLED)
            self.lower.config(state = DISABLED)
            self.tie.config(state = DISABLED)
            self.menubar.entryconfig("Shuffle",state=ACTIVE)
        if self.wrong_flag == 1:
            self.pot_index = []
            self.resultframe.pack_forget()
            self.resultframe.destroy()
            self.m = 0
            if len(self.card_index) != 1:
                self.card_index.pop()
                self.card_count.set(self.card_count.get()-1)
                self.last_card.set(self.deck[self.card_index[-1]])
                self.pot_index.append(self.card_index[-1])
            else:
                self.higher.config(state = DISABLED)
                self.lower.config(state = DISABLED)
                self.tie.config(state = DISABLED)
                self.menubar.entryconfig("Shuffle",state=ACTIVE)
                self.last_card.set('')
                self.pot_size_up.set('')
            self.resultframe = Frame(self.frame)
            self.resultframe.grid(row=2,column=2)
        self.wrong_flag = 0
    def add_lower(self):
        if self.deck[self.card_index[-1]][0] == 'Ace':
            card1 = 14
        elif self.deck[self.card_index[-1]][0] == 'King':
            card1 = 13
        elif self.deck[self.card_index[-1]][0] == 'Queen':
            card1 = 12
        elif self.deck[self.card_index[-1]][0] == 'Jack':
            card1 = 11
        else:
            card1 = self.deck[self.card_index[-1]][0]
        if self.deck[self.card_index[-2]][0] == 'Ace':
            card2 = 14
        elif self.deck[self.card_index[-2]][0] == 'King':
            card2 = 13
        elif self.deck[self.card_index[-2]][0] == 'Queen':
            card2 = 12
        elif self.deck[self.card_index[-2]][0] == 'Jack':
            card2 = 11
        else:
            card2 = self.deck[self.card_index[-2]][0]
        if int(card1) > int(card2):
            self.scolor = 'dark green'
            self.color = 'blue'
            self.notice.set('')  
            self.old_card.set('')
            self.old_old_card.set('')
            self.record()
            self.pot_size.set(self.pot_size.get()+1)
            self.pot_size_up.set(self.pot_size.get()+1)
            self.turn_count.set(self.turn_count.get()+1)
            if self.turn_count.get() > 1:
                self.pass_button.config(bg='green',state=ACTIVE)
            self.time_button.config(bg='red',state=DISABLED)
        elif int(card1) < int(card2):
            self.scolor = 'purple'
            self.color = 'blue'
            self.old_card.set(self.deck[self.card_index[-2]])
            self.old_card_label.config(fg='red')
            self.old_old_card.set(self.deck[self.card_index[-1]])
            self.old_old_card_label.config(fg='blue')
            self.old_pot.set(self.pot_size.get()+2)
            self.old_turn_count.set(self.turn_count.get())
            self.pot_size.set(0)
            self.pot_size_up.set(self.pot_size.get()+1)
            self.wrong_flag = 1
            self.notice.set('!')
            self.turn_count.set(0)
            self.pass_button.config(bg='red',state=DISABLED)
            self.time_button.config(bg='green',state=ACTIVE)
        else:
            self.scolor = 'purple'
            self.color = 'blue'
            self.old_card.set(self.deck[self.card_index[-2]])
            self.old_card_label.config(fg='orange')
            self.old_old_card.set(self.deck[self.card_index[-1]])
            self.old_pot.set(self.pot_size.get()+2)
            self.old_turn_count.set(self.turn_count.get())
            self.pot_size.set(0) 
            self.pot_size_up.set(self.pot_size.get()+1)
            self.wrong_flag = 1
            self.notice.set('!')
            self.turn_count.set(0)
            self.pass_button.config(bg='red',state=DISABLED)
            self.time_button.config(bg='green',state=ACTIVE)
        self.card_index.pop()
        self.card_count.set(self.card_count.get()-1)
        self.last_card.set(self.deck[self.card_index[-1]])
        self.pot_index.append(self.card_index[-1])
        if len(self.card_index) == 2 and self.wrong_flag == 1:
            self.higher.config(state = DISABLED)
            self.lower.config(state = DISABLED)
            self.tie.config(state = DISABLED)
            self.menubar.entryconfig("Shuffle",state=ACTIVE)
        elif len(self.card_index) == 1 and self.wrong_flag == 0:
            self.higher.config(state = DISABLED)
            self.lower.config(state = DISABLED)
            self.tie.config(state = DISABLED)
            self.menubar.entryconfig("Shuffle",state=ACTIVE)
        if self.wrong_flag == 1:
            self.pot_index = []
            self.resultframe.pack_forget()
            self.resultframe.destroy()
            self.m = 0
            if len(self.card_index) != 1:
                self.card_index.pop()
                self.card_count.set(self.card_count.get()-1)
                self.last_card.set(self.deck[self.card_index[-1]])
                self.pot_index.append(self.card_index[-1])
            else:
                self.higher.config(state = DISABLED)
                self.lower.config(state = DISABLED)
                self.tie.config(state = DISABLED)
                self.menubar.entryconfig("Shuffle",state=ACTIVE)
                self.last_card.set('')
                self.pot_size_up.set('')
            self.resultframe = Frame(self.frame)
            self.resultframe.grid(row=2,column=2)
        self.wrong_flag = 0   
    def add_tie(self):
        if self.deck[self.card_index[-1]][0] == 'Ace':
            card1 = 14
        elif self.deck[self.card_index[-1]][0] == 'King':
            card1 = 13
        elif self.deck[self.card_index[-1]][0] == 'Queen':
            card1 = 12
        elif self.deck[self.card_index[-1]][0] == 'Jack':
            card1 = 11
        else:
            card1 = self.deck[self.card_index[-1]][0]
        if self.deck[self.card_index[-2]][0] == 'Ace':
            card2 = 14
        elif self.deck[self.card_index[-2]][0] == 'King':
            card2 = 13
        elif self.deck[self.card_index[-2]][0] == 'Queen':
            card2 = 12
        elif self.deck[self.card_index[-2]][0] == 'Jack':
            card2 = 11
        else:
            card2 = self.deck[self.card_index[-2]][0]
        if int(card1) == int(card2):
            self.scolor = 'dark green'
            self.color = 'orange'
            self.record()
            self.old_card.set('')
            self.old_old_card.set('')
            self.notice.set('')    
            self.pot_size.set(self.pot_size.get()+1)
            self.pot_size_up.set(self.pot_size.get()+1)
            self.turn_count.set(self.turn_count.get()+1)
            if self.turn_count.get() > 1:
                self.pass_button.config(bg='green',state=ACTIVE)
            self.time_button.config(bg='red',state=DISABLED)
        else:
            self.color = 'orange'
            self.scolor = 'purple'
            #self.record()
            self.old_card.set(self.deck[self.card_index[-2]])
            self.old_old_card.set(self.deck[self.card_index[-1]])
            self.old_old_card_label.config(fg='orange')
            self.old_pot.set(self.pot_size.get()+2)
            self.old_turn_count.set(self.turn_count.get())
            self.pot_size.set(0)
            self.pot_size_up.set(self.pot_size.get()+1)
            self.wrong_flag = 1
            self.notice.set('!')
            self.turn_count.set(0)
            self.pass_button.config(bg='red',state=DISABLED)
            self.time_button.config(bg='green',state=ACTIVE)
        self.card_index.pop()
        self.card_count.set(self.card_count.get()-1)
        self.last_card.set(self.deck[self.card_index[-1]])
        self.pot_index.append(self.card_index[-1])
        if len(self.card_index) == 2 and self.wrong_flag == 1:
            self.higher.config(state = DISABLED)
            self.lower.config(state = DISABLED)
            self.tie.config(state = DISABLED)
            self.menubar.entryconfig("Shuffle",state=ACTIVE)
        elif len(self.card_index) == 1 and self.wrong_flag == 0:
            self.higher.config(state = DISABLED)
            self.lower.config(state = DISABLED)
            self.tie.config(state = DISABLED)
            self.menubar.entryconfig("Shuffle",state=ACTIVE)
        if self.wrong_flag == 1:
            self.pot_index = []
            self.resultframe.pack_forget()
            self.resultframe.destroy()
            self.m = 0
            if len(self.card_index) != 1:
                self.card_index.pop()
                self.card_count.set(self.card_count.get()-1)
                self.last_card.set(self.deck[self.card_index[-1]])
                self.pot_index.append(self.card_index[-1])
            else:
                self.higher.config(state = DISABLED)
                self.lower.config(state = DISABLED)
                self.tie.config(state = DISABLED)
                self.menubar.entryconfig("Shuffle",state=ACTIVE)
                self.last_card.set('')
                self.pot_size_up.set('')
            self.resultframe = Frame(self.frame)
            self.resultframe.grid(row=2,column=2)
        self.wrong_flag = 0
    def add_stat(self):
        if self.deck[self.card_index[-1]][0] == 'Ace':
            card1 = 14
        elif self.deck[self.card_index[-1]][0] == 'King':
            card1 = 13
        elif self.deck[self.card_index[-1]][0] == 'Queen':
            card1 = 12
        elif self.deck[self.card_index[-1]][0] == 'Jack':
            card1 = 11
        else:
            card1 = self.deck[self.card_index[-1]][0]
        total = 0
        for i in range(0,len(self.card_index)):
            if self.deck[self.card_index[i]][0] == 'Ace':
                total += 14
            elif self.deck[self.card_index[i]][0] == 'King':
                total += 13
            elif self.deck[self.card_index[i]][0] == 'Queen':
                total += 12
            elif self.deck[self.card_index[i]][0] == 'Jack':
                total += 11
            else:
                total += int(self.deck[self.card_index[i]][0])
        avg = float(total)/float(len(self.card_index))
        if avg < float(card1):
            self.add_lower()
        elif avg > float(card1):
            self.add_higher()
        else:
            self.add_tie()
    def pass_fun(self):         
        self.old_turn_count.set(self.turn_count.get())
        self.turn_count.set(0)
        self.pass_button.config(bg='red',state=DISABLED)
def save_obj(obj, name):                
    with open(name, 'wb') as f:
        f.write(obj)
        f.close()
def load_obj(name ):
    with open(name, 'r') as f:
        sets = eval(f.read())
        f.close()
        return sets

last_card = ''
pot_index = []
root = Tk()
root.geometry("%dx%d+%d+%d" % (750, 1000, 0, 0))
app=App(root,pot_index,last_card)
root.mainloop()
