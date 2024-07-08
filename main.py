import discord
import asyncio
from discord.ext import tasks, commands
import io
import requests
import json



r = []
g = []
g_lines = []
f = []
c = []
m = []
n = []
user = []
file = open("data.json", "r")
data = json.load(file)
for i in range(len(data)):
    r.append(i)
    g.append(i)
    g_lines.append(i)
    f.append(i)
    c.append(i)
    m.append(i)
    n.append(i)
    user.append(i)

    user[i] = data[i]["user_id"]
    r[i] = requests.session()
    r[i].get('https://api.librus.pl/OAuth/Authorization?client_id=46&response_type=code&scope=mydata')
    r[i].post('https://api.librus.pl/OAuth/Authorization/Grant?client_id=46', data={
    'action': 'login',
    'login': data[i]["login"],
    'pass': data[i]["pass"]})
    r[i].get('https://api.librus.pl/OAuth/Authorization/Grant?client_id=46')
    r[i].get('https://synergia.librus.pl/uczen/index')


    txt = r[i].get('https://synergia.librus.pl/przegladaj_oceny/uczen').text
    buf = io.StringIO(txt)
    g_lines[i] = buf.readlines()
    g[i]=0
    for line in g_lines[i]:
        g[i]+=1

    txt = r[i].get('https://synergia.librus.pl/przegladaj_nb/uczen').text
    buf = io.StringIO(txt)
    lines = buf.readlines()
    f[i]=0
    for line in lines:
        f[i]+=1

    txt = r[i].get('https://synergia.librus.pl/terminarz').text
    buf = io.StringIO(txt)
    lines = buf.readlines()
    c[i]=0
    for line in lines:
        c[i]+=1

    txt = r[i].get('https://synergia.librus.pl/wiadomosci').text
    buf = io.StringIO(txt)
    lines = buf.readlines()
    m[i]=None
    for line in lines:
        if '><a href="/wiadomosci/' in line:
            m[i]=line
            break

    txt = r[i].get('https://synergia.librus.pl/ogloszenia').text
    buf = io.StringIO(txt)
    lines = buf.readlines()
    iteration=0
    n[i]=None
    for line in lines:
        iteration+=1
        if '<th>Treść</th>' in line:
            line = lines[iteration]
            n[i] = line
            break


########################

intent = discord.Intents.default()
intent.members = True
client = discord.Client()
bot = commands.Bot(command_prefix='!', intents=intent)

@bot.event
async def on_ready():
    print("Done!")
    librus.start()


@tasks.loop(minutes=10.0)
async def librus():
    for i in range(len(f)):
        global librus_user
        global user
        librus_user = bot.get_user(user[i])
        try:
            txt1 = r[i].get('https://synergia.librus.pl/przegladaj_oceny/uczen').text
            buf1 = io.StringIO(txt1)
            lines = buf1.readlines()
            x1=0
            for line in lines:
                x1+=1
            global g
            x1 += 1
            print(x1)
            print(g[i])
            if g[i] != x1:
                if g[i] > x1:
                    await librus_user.send('Usunięto ocenę...')
                    print(librus_user,"Usunięto ocenę!")
                elif g[i] < x1:
                    iteration = 0
                    for iteration in range(x1):
                        print(iteration)
                        if 'Kategoria:' in x1[iteration]:
                            print("g : ",g[i][iteration])
                            print("x1: ",x1[iteration])
                            if g[i][iteration] != x1[iteration]:
                                line1 = x1[iteration].split("<br>")
                                end = ""
                                for iteration in line1:
                                    end = end + "\n" + iteration
                                str_response = "Dodano ocenę: " + "\n" + end
                                await librus_user.send(str_response)
                                print(librus_user, "Dodano ocenę...")
                            break
                            print(line)

                            break
                    break
                    g[i]=x1

            txt1 = r[i].get('https://synergia.librus.pl/przegladaj_nb/uczen').text
            buf1 = io.StringIO(txt1)
            lines = buf1.readlines()
            x1=0
            for line in lines:
                x1+=1
            #global f
            if f[i] != x1:
                if f[i] < x1:
                    await user.send('Dodano nieobecność...')
                    print(librus_user,'Dodano nieobecność...')
                elif f[i] > x1:
                    await user.send('Usunięto nieobecność...')
                    print(librus_user,'Usunięto nieobecność...')
                f[i]=x1

            txt1 = r[i].get('https://synergia.librus.pl/terminarz').text
            buf1 = io.StringIO(txt1)      #sprawdzanie (dynamic)
            lines = buf1.readlines()
            x1=0
            for line in lines:
                x1+=1
            global c
            if c[i] != x1:
                if c[i] < x1:
                    await user.send('Dodano wydarzenie w terminarzu...')
                    print(librus_user,'Dodano wydarzenie w terminarzu...')
                elif c[i] > x1:
                    await user.send('Usunięto wydarzenie w terminarzu...')
                    print(librus_user,'Usunięto wydarzenie w terminarzu...')
                c[i]=x1

            txt1 = r[i].get('https://synergia.librus.pl/wiadomosci').text
            buf1 = io.StringIO(txt1)      #sprawdzanie (dynamic)
            lines = buf1.readlines()
            x1=None
            for line in lines:
                if '><a href="/wiadomosci/' in line:
                    x1=line
                    break
            global m
            if m[i] != x1:
                await user.send('Nowa wiadomość: '+ m[i])
                print(librus_user,' Nowa wiadomość!')
                m[i]=x1

            txt1 = r[i].get('https://synergia.librus.pl/ogloszenia').text
            buf1 = io.StringIO(txt1)      #sprawdzanie (dynamic)
            lines = buf1.readlines()
            iteration=0
            for line in lines:
                iteration+=1
                if '<th>Treść</th>' in line:
                    line = lines[iteration]
                    x1=line
                    break
            global n
            if n[i] != x1:
                await user.send('Dodano ogłoszenie: '+ n[i])
                print(librus_user,'Dodano ogłoszenie...')
                n[i] = x1
            print(librus_user," Returned!")
        except:
            user = bot.get_user('Moje id')
            await user.send(str(librus_user) + " Error!!!")

bot.run('*secret*')
