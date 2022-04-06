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
    def __init__(self,id_c,firstname,surname,score,user):
        self.fname = firstname
        self.sname = surname
        self.score = 0
        self.user = user
        self.id_st = id_c
        self.perm = False

bot = telebot.TeleBot(os.environ['TBOTTOKEN'])
connection = modelstickers.create_connection(os.environ['DBPATH'])
students = {}
limit = 0
def show():
    f=[]
    stc = "Top students. \n"
    for i in students:
        f.append(students[i])
    f.sort(key = lambda x:x.score)
    f.reverse()
    for x in range(len(f)):
        stc+=str(x+1)+". "+f[x].fname+" "+f[x].sname+" "+str(f[x].score)+". \n"
    return stc
def isUnique(studentId):
    global students
    flag = True
    for student in students:
        if student == studentId:
            flag = False;
            break;
    return flag;
def makeUp():
    zhopa = modelstickers.getStudents(connection,message.chat.id)
    if not zhopa == None:
        for i in zhopa:
            students[i[0]] = Student(i[0],i[1],i[2],i[3],i[4])
@bot.message_handler(commands=['start'])
def startBot(message):
    global students
    perem = modelstickers.createTable(connection,message.chat.id)
    print(perem)
    if perem==None:
        zhopa = modelstickers.getStudents(connection,message.chat.id)
        if not zhopa == None:
            for i in zhopa:
                students[i[0]] = Student(i[0],i[1],i[2],i[3],i[4])
    bot.send_message(message.chat.id, "Welcome to stickers bot, write /help command to know more about this bot")
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,"You have this list of commands.\nStudent can write this commands\n/add {number of stickers} #this command add number of stickers\n/reg {firstname} {surname} #this command registrate student \n /stat #show statistics of students!!!Allows to teacher!!!\n /rename {firstname} {surname} #rename student name\n Teacher commnads\n /startcount #allows to student write message to add their number of stickers\n /endcount #disallow to students add their number of stickers\n /limit {limit of stickers} #create limit of stickers that students can not overcome\n /addStudent {student username} {number of stickers} #teacher can add stickers to student or remove if write negative number",parse_mode="html")

@bot.message_handler(commands=['startcount','endcount','limit','addStudent'])
def startcount(message):
    if bot.get_chat_member(message.chat.id,message.from_user.id).status in ['administrator','creator']:
        if "/startcount" in message.text:
            send_mess = f"{message.from_user.username} allow to write your amount of stickers. You can ONE time. So, be carefully and write stickers correctly"
            for i in students:
                students[i].perm=True
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
        if isUnique(message.from_user.id):
            students[message.from_user.id] = Student(message.from_user.id,st[1],st[2],0,message.from_user.username)
            perem =modelstickers.insertStudent(connection,message.chat.id,message.from_user.id,students[message.from_user.id].fname,students[message.from_user.id].sname,students[message.from_user.id].score,students[message.from_user.id].user)
            if perem == None:
                bot.send_message(message.chat.id,f"Congratulations! {st[1]} {st[2]} was joined to our group")
                makeUp()
            else:
                bot.send_message(message.chat.id,perem)

        else:
            bot.send_message(message.chat.id,f"{message.from_user.username} already was registrated")
    else:
        bot.send_message(message.chat.id,"Please write your firstname and surname fully")

@bot.message_handler(commands=['add'])
def addStudent(message):
    mark = message.text.split()
    if mark[1].isdigit() and message.from_user.id in list(students.keys()):
        if  students[message.from_user.id].perm == True:
            if int(mark[1])>=0 and int(mark[1])<=limit:
                bot.send_message(message.chat.id, f"Congratulatons! You achieve +{mark[1]} stickers")
                students[message.from_user.id].addSticker(int(mark[1]))
                el = modelstickers.updateScore(connection,message.chat.id,message.from_user.id,students[message.from_user.id].score)
                print(el)
                students[message.from_user.id].perm=False
                makeUp()
            else:
                bot.send_message(message.chat.id, "Write not negative numbers, write again")
        else:
            bot.send_message(message.chat.id, "Sorry you use your chance. If you less more than you have or vice versa, please ask from teacher that you write wrong number and teacher can write correctly")
    else:
        if not(message.from_user.id in students.keys()):
            bot.send_message(message.chat.id, "Please register into the group")
        else:
            bot.send_message(message.chat.id, "Please write numbers")

def addTeacher(message):
    u = message.text.split()
    f={}
    for i in students:
        f[students[i].user]=students[i].id_st
    if len(u) == 3:
        print(u[1], list(f.keys()))
        if (("-" in u[2] and u[2][1:len(u[2])].isdigit()) or u[2].isdigit()) and (u[1] in list(f.keys())):
            if int(u[2])>=0:
                bot.send_message(message.chat.id, f"{u[1]} achieve {u[2]} stickers by teacher")
                students[f[u[1]]].addSticker(int(u[2]))
                modelstickers.updateScore(connection,message.chat.id,message.from_user.id,students[message.from_user.id].score)
            else:
                bot.send_message(message.chat.id, f"{u[1]} lost {u[2]} stickers by teacher")
                students[f[u[1]]].addSticker(int(u[2]))
                modelstickers.updateScore(connection,message.chat.id,message.from_user.id,students[message.from_user.id].score)
            makeUp()
        else:
            bot.send_message(message.chat.id, f"You write wrong number or student username")
    else:
        bot.send_message(message.chat.id, f"Please write fully student username and number of stickers")


def endCount(message):
    send_mess = f"{message.from_user.username} close access to write your amount of stickers. You can write your stickers next time"
    for i in students:
        students[i].perm=False
    bot.send_message(message.chat.id, send_mess)
def limitState(message):
    d = message.text.split()
    if d[1].isdigit():
        global limit
        bot.send_message(message.chat.id, f"Teacher set limit of stickers.Limit of stickers is {d[1]}")
        limit=int(d[1])
    else:
        bot.send_message(message.chat.id, "Please write numbers")
@bot.message_handler(commands=['stat'])
def TopStudent(message):
    makeUp()
    bot.send_message(message.chat.id, show())
@bot.message_handler(commands=['rename'])
def rename(message):
    g = message.text.split()
    if len(g)==3:
        modelstickers.updateName(connection,message.chat.id,message.from_user.id,g[1],g[2])
        zhopa = modelstickers.getStudents(connection,message.chat.id)
        makeUp()
        bot.send_message(message.chat.id, f"Now you are {g[1]} {g[2]}")
    else:
        bot.send_message(message.chat.id, f"Please write fully student firstname and surname")
bot.polling(none_stop=True)
