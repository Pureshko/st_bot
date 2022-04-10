import telebot
from telebot import types
import modelstickers
import os
class Student():
    def openPerm():
        self.perm = True
    def closePerm():
        self.perm = False
    def addSticker(self,stickers):
        self.score+=stickers
    def __init__(self,id_c,firstname,surname,score,user,permis):
        self.fname = firstname
        self.sname = surname
        self.score = score
        self.user = user
        self.id_st = id_c
        self.perm = permis


bot = telebot.TeleBot('5268370640:AAGLuB_lWaM70mS4bOGb8YHDP4q60qp-Atw')
connection = modelstickers.create_connection('class.db')
limit = {}
def show(mes):
    zhopa = modelstickers.getStudents(connection,mes)
    f=[]
    stc = "Top students. \n"
    if zhopa == []:
        return stc
    elif 'no such table' in zhopa:
        return "You must write /start command"
    else:
        for i in zhopa:
            f.append(Student(i[0],i[1],i[2],i[3],i[4],i[5]))
        f.sort(key = lambda x:x.score)
        f.reverse()
        for x in range(len(f)):
            stc+=str(x+1)+". "+f[x].fname+" "+f[x].sname+" "+str(f[x].score)+". \n"
        return stc

def isUnique(mes,studentId):
    zhopa = modelstickers.getStudents(connection,mes)
    flag = True
    if 'no such table' in zhopa:
        bot.send_message(mes, "You must write /start command")
    else:
        for student in zhopa:
            if student[0] == studentId:
                flag = False;
                break;
        return flag;
def idNameUnique(mes,fname,sname):
    zhopa = modelstickers.getStudents(connection,mes)
    flag = True
    if 'no such table' in zhopa:
        bot.send_message(mes, "You must write /start command")
    else:
        for student in zhopa:
            if student[1] == fname and student[2] == sname:
                flag = False;
                break;
        return flag;
    
def setStudents(mes):
    djaga = {}
    students = modelstickers.getStudents(connection,mes)
    if students == []:
        return {}
    elif 'no such table' in students:
        bot.send_message(mes, "You must write /start command")
        return {}
    else:
        for i in students:
            djaga[i[0]] = Student(i[0],i[1],i[2],i[3],i[4],i[5])
        return djaga
def setUser(mes):
    djaga = {}
    students = modelstickers.getStudents(connection,mes)
    if students == []:
        return {}
    elif 'no such table' in students:
        bot.send_message(mes, "You must write /start command")
        return {}
    else:
        for i in students:
            djaga[i[1]+i[2]] = Student(i[0],i[1],i[2],i[3],i[4],i[5])
        return djaga
@bot.message_handler(commands=['start'])
def startBot(message):
    perem = modelstickers.createTable(connection,message.chat.id)
    print(perem)
    bot.send_message(message.chat.id, "Welcome to stickers bot, write /help command to know more about this bot")
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,"You have this list of commands.\nStudent can write this commands\n/add {number of stickers} #this command add number of stickers\n/reg {firstname} {surname} #this command registrate student \n /stat #show statistics of students!!!Allows to teacher!!!\n /rename {firstname} {surname} #rename student name\n Teacher commnads\n /startcount #allows to student write message to add their number of stickers\n /endcount #disallow to students add their number of stickers\n /limit {limit of stickers} #create limit of stickers that students can not overcome\n /addStudent {student firstname} {student surname} {number of stickers} #teacher can add stickers to student or remove if write negative number",parse_mode="html")

@bot.message_handler(commands=['startcount','endcount','limit','addStudent'])
def startcount(message):
    if bot.get_chat_member(message.chat.id,message.from_user.id).status in ['administrator','creator']:
        if "/startcount" in message.text:
            send_mess = f"{message.from_user.username} allow to write your amount of stickers. You can ONE time. So, be carefully and write stickers correctly"
            zhopa = modelstickers.getStudents(connection,message.chat.id)
            if 'no such table' in zhopa:
                bot.send_message(message.chat.id, "You must write /start command")
            else:
                for i in zhopa:
                    modelstickers.openPermis(connection, message.chat.id,i[0])
                bot.send_message(message.chat.id, send_mess)

        elif "/endcount" in message.text:
            endCount(message)
        elif "/limit" in message.text:
            limitState(message)
        elif "/addStudent" in message.text:
            addTeacher(message)
    else:
        bot.send_message(message.chat.id, "You are not allowed to write this command")
@bot.message_handler(commands=['reg'])
def registrate(message):
    st = message.text.split()
    if len(st)==3:
        text = isUnique(message.chat.id,message.from_user.id)
        if text:
            if idNameUnique(message.chat.id,st[1],st[2]):
                perem =modelstickers.insertStudent(connection,message.chat.id,message.from_user.id,st[1],st[2],0,message.from_user.username,0)
                if perem == None:
                    bot.send_message(message.chat.id,f"Congratulations! {st[1]} {st[2]} was joined to our group")
                else:
                    bot.send_message(message.chat.id,perem)
            else:
                bot.send_message(message.chat.id, f"This name already registered")
        elif text == False:
            bot.send_message(message.chat.id,f"{message.from_user.username} already was registrated")
    else:
        bot.send_message(message.chat.id,"Please write your firstname and surname fully")

def addTeacher(message):
    u = message.text.split()
    f = setUser(message.chat.id)
    if len(u) == 4:
        if (("-" in u[3] and u[3][1:len(u[3])].isdigit()) or u[3].isdigit()) and ((u[1]+u[2]) in list(f.keys())):
            if int(u[3])>=0:
                bot.send_message(message.chat.id, f"{u[1]} {u[2]} achieve {u[3]} stickers by teacher")
                modelstickers.updateScore(connection,message.chat.id,f[u[1]+u[2]].id_st,f[u[1]+u[2]].score+int(u[3]))
            else:
                bot.send_message(message.chat.id, f"{u[1]} {u[2]} lost {u[3]} stickers by teacher")
                modelstickers.updateScore(connection,message.chat.id,f[u[1]+u[2]].id_st,f[u[1]+u[2]].score+int(u[3]))
        else:
            bot.send_message(message.chat.id, f"You write wrong number or student username")
    else:
        bot.send_message(message.chat.id, f"Please write fully student username and number of stickers")

def endCount(message):
    send_mess = f"{message.from_user.username} close access to write your amount of stickers. You can write your stickers next time"
    zhopa = modelstickers.getStudents(connection,message.chat.id)
    if 'no such table' in zhopa:
        bot.send_message(message.chat.id, "You must write /start command")
    else:
        for i in zhopa:
            modelstickers.closePermis(connection, message.chat.id,i[0])
        bot.send_message(message.chat.id, send_mess)


def limitState(message):
    d = message.text.split()
    if d[1].isdigit():
        bot.send_message(message.chat.id, f"Teacher set limit of stickers.Limit of stickers is {d[1]}")
        limit[message.chat.id]=int(d[1])
    else:
        bot.send_message(message.chat.id, "Please write numbers")

@bot.message_handler(commands=['add'])
def addStudent(message):
    global limit
    mark = message.text.split()
    f = setStudents(message.chat.id)
    if len(mark) == 2:
        if mark[1].isdigit() and message.from_user.id in list(f.keys()):
            if f[message.from_user.id].perm == 1 and message.chat.id in list(limit.keys()):
                if int(mark[1])>=0 and int(mark[1])<=limit[message.chat.id]:
                    bot.send_message(message.chat.id, f"Congratulatons! You achieve +{mark[1]} stickers")
                    modelstickers.updateScore(connection,message.chat.id,message.from_user.id,f[message.from_user.id].score+int(mark[1]))
                    modelstickers.closePermis(connection,message.chat.id,message.from_user.id)
                else:
                    bot.send_message(message.chat.id, f"Please write number of stickers from 0 to {limit[message.chat.id]}")
            else:
                if f[message.from_user.id].perm == 0:
                    bot.send_message(message.chat.id, "Sorry you use your chance. If you less more than you have or vice versa, please ask from teacher that you write wrong number and teacher can write correctly")
                elif message.chat.id not in list(limit.keys()):
                    bot.send_message(message.chat.id, "Teacher, please set limit of number of stickers")
        else:
            if not(message.from_user.id in f.keys()):
                bot.send_message(message.chat.id, "Please register into the group")
            else:
                bot.send_message(message.chat.id, "Please write numbers")
    else:
        bot.send_message(message.chat.id, "Please, fully write yout achieved number of stickers")
@bot.message_handler(commands=['stat'])
def TopStudent(message):
    bot.send_message(message.chat.id, show(message.chat.id))

@bot.message_handler(commands=['rename'])
def rename(message):
    g = message.text.split()
    f = setStudents(message.chat.id)
    if len(g)==3:
        if message.from_user.id in list(f.keys()):
            if idNameUnique(message.chat.id, g[1],g[2]):
                modelstickers.updateName(connection,message.chat.id,message.from_user.id,g[1],g[2])
                bot.send_message(message.chat.id, f"Now you are {g[1]} {g[2]}")
            else:
                bot.send_message(message.chat.id, f"This name already registered")
        else:
            bot.send_message(message.chat.id, "Please register into the group")
    else:
        bot.send_message(message.chat.id, f"Please write fully student firstname and surname")
bot.polling(none_stop=True)
