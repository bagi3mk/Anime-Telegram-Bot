import os
import re
import threading
from config import bot_token,bot_token_subscribe,api_id,api_hash,username_channel
from pyromod import listen
import requests
from funcs import *
from pyrogram import Client,filters
from pyrogram.types import (InlineKeyboardButton,InlineKeyboardMarkup,Message,CallbackQuery)
import redis,warnings
from helper.funcs import (get_animes,get_espode_dl_links,check_anime,get_espodes,get_from_the_main_page,google_drive,sub,get_upload_info,mp4upload,upbaam,get_select_esp,)
warnings.filterwarnings('ignore')

r = redis.Redis(decode_responses=True,charset='utf-8')

Laksis = Client('Anime4up',in_memory=True,api_hash=api_hash,api_id=api_id,bot_token=bot_token)

copyrights = InlineKeyboardMarkup([[InlineKeyboardButton('Anime World',url=f'https://t.me/{username_channel}')]])

@Laksis.on_message(filters.private & filters.text , group=1)
async def Front_End(c:Client,m:Message):#
    if not sub(m.from_user.id,bot_token,username_channel):
        keys = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('اشترك', url=f"https://t.me/{username_channel}")]
            ]
        )
        await m.reply("- لازم تشترك بقناتنا عشان تقدر تستخدم البوت ياحلو (: .", reply_markup=keys)
        return
    if m.text == "/start":
        keys = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('حلقات الأنمي الأكثر مشاهدة',callback_data="MostEspView"),InlineKeyboardButton('حلقات الأنمي المثبتة',callback_data='PinnedEsp')
                ],
                [
                    InlineKeyboardButton('الأنميات المثبتة',callback_data="PinnedAnimes"),
                ],
                # [
                #     InlineKeyboardButton('آخر الحلقات المضافة',callback_data='RecentEspAdd'),InlineKeyboardButton('آخر الأنميات المضافة',callback_data='RecentAnimesAdd')
                # ],
                [
                    InlineKeyboardButton('شرح البوت',callback_data="explainbot")
                ]
            ]
        )
        await m.reply(f"- أهلا {m.from_user.mention} البوت خاص للانمي تقدر تبحث فيه وتحميل اي انمي تفكر فيه ! .",reply_markup=keys)
    elif re.match('بحث (.*?)$',m.text):
        query = re.match('بحث (.*?)$',m.text).group(1)
        try:
            animes = get_animes(query)
        except:
            return await m.reply('- تعذر العثور على الانمي تأكد من كتابة الاسم بشكل صحيح .')
        keys = []
        where = 0
        for anim in animes:
            try:
                keys.append([InlineKeyboardButton(text=anim,callback_data=f"Search:{where}")])
                r.set(f"SearchResults:{where}:{m.from_user.id}",f"{anim}|{animes[anim]['url']}")
            except:
                pass
            where += 1
        await m.reply("- إليك نتائج بحثك : ",reply_markup=InlineKeyboardMarkup(keys))
def dodo(ca,c,typee):
    other_infos = get_upload_info(r.get(f"DirectDownload:{ca.from_user.id}:{typee}").split('|')[1])
    if typee == "mp4upload":
        check = (mp4upload(filename=f"{other_infos['name']}.mp4",
                           url=r.get(f"DirectDownload:{ca.from_user.id}:{typee}").split('|')[0]))
    elif typee == "google":
        check = (google_drive(filename=f"{other_infos['name']}.mp4",
                           url=r.get(f"DirectDownload:{ca.from_user.id}:{typee}").split('|')[0]))
    elif typee == "upbaam":
        check = (upbaam(filename=f"{other_infos['name']}.mp4",
                           url=r.get(f"DirectDownload:{ca.from_user.id}:{typee}").split('|')[0]))
    if check == 404:
        return c.send_message(ca.message.chat.id, f"- تم حذف الحلقة من السيرفر استخدم سيرفر آخر .")
    elif not check:
        return c.send_message(ca.message.chat.id, f"- تم حذف الحلقة من السيرفر استخدم سيرفر آخر .")
    elif check:
        try:
            open(other_infos['name'] + ".jpg", 'wb').write(requests.get(other_infos['thumbnailUrl']).content)
            c.send_video(ca.message.chat.id, video=open(f'{other_infos["name"]}.mp4', 'rb'), duration=1380,
                               height=int(other_infos['publisher']['logo']['height']),
                               width=int(other_infos['publisher']['logo']['width']), thumb=f"{other_infos['name']}.jpg",
                               caption=other_infos['description'], reply_markup=copyrights)
            c.send_message(ca.message.chat.id, "Enjoy")
            c.send_sticker(ca.message.chat.id, "https://t.me/biiir/3314")
            os.remove(f"{other_infos['name']}.mp4")
            os.remove(f"{other_infos['name']}.jpg")
        except:
            return c.send_message(ca.message.chat.id, f"- تم حذف الحلقة من السيرفر استخدم سيرفر آخر .")
@Laksis.on_callback_query(group=2)
async def Back_End(c:Client,ca:CallbackQuery):
    data = ca.data
    if re.match("Search:(.*?)$",data):
        await ca.answer("- جاري ....")
        where = re.match("Search:(.*?)$",data).group(1)
        infos = r.get(f"SearchResults:{where}:{ca.from_user.id}")
        full = re.match('(.*?)\|(.*?)$',infos)
        get_anime_info = check_anime(full.group(2))
        await ca.message.delete()
        await c.send_message(chat_id=ca.message.chat.id,text=f"\n{get_anime_info['desc']}\nالنوع : {get_anime_info['kind']}",reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('عرض الحلقات' if get_anime_info['kind'] == 'انمي/حلقات متعددة' else 'تحميل الفلم',callback_data=f"ShowAnimeesp:{where}" if get_anime_info['kind'] == 'انمي/حلقات متعددة' else 'DownloadMovie')]
        ]))
    elif re.match("ShowAnimeesp:(.*?)$",data):
        where = re.match("ShowAnimeesp:(.*?)$",data).group(1)
        infos = r.get(f"SearchResults:{where}:{ca.from_user.id}")
        full = re.match('(.*?)\|(.*?)$',infos)
        esps = get_espodes(full.group(2))
        keys = []
        where = 0
        for anim in esps:
            r.set(f"EspodesSearchResults:{where}:{ca.from_user.id}",f"{anim}|{esps[anim]}")
            keys.append([InlineKeyboardButton(text=anim,callback_data=f"DownloadEspodes:{where}")])
            where += 1
        r.set(f"CustomEsp:{where}:{ca.from_user.id}",f"{full.group(2)}")
        keys.append([InlineKeyboardButton(text='حلقة اخرى', callback_data=f"cus:{where}")])
        await ca.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keys))
    elif re.match("DownloadEspodes:(.*?)$",data):
        where = re.match("DownloadEspodes:(.*?)$", data).group(1)
        infos = r.get(f"EspodesSearchResults:{where}:{ca.from_user.id}")
        full = re.match('(.*?)\|(.*?)$',infos)
        await ca.answer('- جاري جلب رابط التحميل يرجى الانتظار ...')
        tt = get_espode_dl_links(full.group(2))
        keys = []
        for gogo in tt:
            if str(gogo).lower().count('google'):
                r.set(f"DirectDownload:{ca.from_user.id}:google",tt[gogo]+"|"+full.group(2))
                keys.append([InlineKeyboardButton(text=str(gogo[:64]),callback_data="DirectDownload:Google")])
            elif str(gogo).lower().count('mp4upload'):
                r.set(f"DirectDownload:{ca.from_user.id}:mp4upload",tt[gogo]+"|"+full.group(2))
                keys.append([InlineKeyboardButton(text=str(gogo[:64]),callback_data="DirectDownload:mp4upload")])
            elif str(gogo).lower().count('upbaam'):
                r.set(f"DirectDownload:{ca.from_user.id}:upbaam",tt[gogo]+"|"+full.group(2))
                keys.append([InlineKeyboardButton(text=str(gogo[:64]),callback_data="DirectDownload:upbaam")])
        await ca.message.edit("- روابط التحميل المتوفرة :",reply_markup=InlineKeyboardMarkup(keys))
    elif data == "DirectDownload:Google":
        await ca.message.delete()
        threading.Thread(target=dodo,args=(ca,c,'google')).start()
    elif data == 'DirectDownload:mp4upload':
        await ca.message.delete()
        threading.Thread(target=dodo,args=(ca,c,'mp4upload')).start()
    elif data== 'DirectDownload:upbaam':
        await ca.message.delete()
        threading.Thread(target=dodo,args=(ca,c,'upbaam')).start()
    elif data == "explainbot":
        new_keys = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('رجوع',callback_data="back")
                ]
            ]
        )
        subject = f"- البوت مبني على السكرابنق على موقع معين تقدر انك تبحث وتحمل فقط عن طريق كتابة كلمة بحث وبجانبها اسم الأنمي .\n\n - البوت تحت تحديث مستمر للسيرفرات وطرق التحميل وحلول للمشاكل الموجودة في البوت .\n\n- أمثلة على طريقة البحث :-\n- بحث conan\n- بحث Undead Girl Murder Farce \n- بحث black colver\nفقط ضع اسم الانمي بعد كلمة بحث مع مراعاة وجود مسافة بين كلمة بحث واسم الانمي .\n\n- واتبع بقية الازرار الموضحه للتحميل .\n\n- اي مشكلة تواجهك تواصل مع المطور لكي يتم حلها ."
        await ca.message.edit_text(subject,reply_markup=new_keys)
    elif data == "back":
        keys = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('قناتنا', url=f'https://t.me/{username_channel}')
                ],
                [
                    InlineKeyboardButton('المطور', url="https://t.me/biiir")
                ],
                [
                    InlineKeyboardButton('موقع البوت', url='https://animelek.me')
                ],
                [
                    InlineKeyboardButton('شرح البوت', callback_data="explainbot")
                ]
            ]
        )
        await ca.message.edit_text(f"- أهلا {ca.from_user.mention} البوت خاص للانمي تقدر تبحث فيه وتحميل اي انمي تفكر فيه ! .",
                      reply_markup=keys)
    elif re.match('cus:(.*?)$',data):
        where = re.match('cus:(.*?)$',data).group(1)
        getit = r.get(f"CustomEsp:{where}:{ca.from_user.id}")
        await ca.message.delete()
        t = await c.ask(ca.message.chat.id,"- قم بأرسال رقم الحلقه (تأكد من انها موجودة) .",timeout=60)
        if not str(t.text).isdigit():
            return await c.send_message(ca.message.chat.id,f"- تنسيق خاطء حاول مره اخرى وارسل رقم الحلقة بشكل صحيح وبالارقام فقط .")
        yt = get_select_esp(url=getit,num=int(t.text))
        tt = get_espode_dl_links(yt[1])
        keys = []
        for gogo in tt:
            if str(gogo).lower().count('google'):
                r.set(f"DirectDownload:{ca.from_user.id}:google",tt[gogo]+"|"+yt[1])
                keys.append([InlineKeyboardButton(text=str(gogo[:64]),callback_data="DirectDownload:Google")])
            elif str(gogo).lower().count('mp4upload'):
                r.set(f"DirectDownload:{ca.from_user.id}:mp4upload",tt[gogo]+"|"+yt[1])
                keys.append([InlineKeyboardButton(text=str(gogo[:64]),callback_data="DirectDownload:mp4upload")])
            elif str(gogo).lower().count('upbaam'):
                r.set(f"DirectDownload:{ca.from_user.id}:upbaam",tt[gogo]+"|"+yt[1])
                keys.append([InlineKeyboardButton(text=str(gogo[:64]),callback_data="DirectDownload:upbaam")])
        await c.send_message(ca.message.chat.id,"- روابط التحميل المتوفرة :",reply_markup=InlineKeyboardMarkup(keys))
    elif data == "MostEspView":
        results = get_from_the_main_page(typ="MostEspView")
        keys = []
        where = 0
        for esp in results:
            r.set(f"EspodesSearchResults:{where}:{ca.from_user.id}", f"{esp}|{results[esp]}")
            keys.append([InlineKeyboardButton(esp,callback_data=f"DownloadEspodes:{where}")])
            where += 1
        await ca.edit_message_text('- الحلقات الاكثر مشاهدة :',reply_markup=InlineKeyboardMarkup(keys))
    elif data == "PinnedEsp":
        results = get_from_the_main_page(typ="PinnedEsp")
        keys = []
        where = 0
        for esp in results:
            r.set(f"EspodesSearchResults:{where}:{ca.from_user.id}", f"{esp}|{results[esp]}")
            keys.append([InlineKeyboardButton(esp,callback_data=f"DownloadEspodes:{where}")])
            where += 1
        await ca.edit_message_text('- الحلقات المثبتة :',reply_markup=InlineKeyboardMarkup(keys))
    elif data == "PinnedAnimes":
        results = get_from_the_main_page(typ="PinnedAnimes")
        keys = []
        where = 0
        for esp in results:
            keys.append([InlineKeyboardButton(text=esp, callback_data=f"Search:{where}")])
            r.set(f"SearchResults:{where}:{ca.from_user.id}", f"{esp}|{results[esp]}")
            where += 1
        await ca.edit_message_text('- الانميات المثبتة :',reply_markup=InlineKeyboardMarkup(keys))
Laksis.run()