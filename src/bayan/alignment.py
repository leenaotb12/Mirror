# -*- coding: utf-8 -*-
import re
from difflib import SequenceMatcher
GROUP={"PER":"PER","PERSON":"PER","LOC":"LOC","GPE":"LOC","FAC":"LOC","ORG":"ORG","MISC":"MISC","NORP":"MISC","EVENT":"MISC","PRODUCT":"MISC","WORK_OF_ART":"MISC","LAW":"MISC","LANGUAGE":"MISC","DATE":"DATE","TIME":"DATE"}
MONTHS="يناير|فبراير|مارس|أبريل|ابريل|إبريل|مايو|يونيو|يونيه|يوليو|يوليه|أغسطس|اغسطس|سبتمبر|أكتوبر|اكتوبر|نوفمبر|ديسمبر|كانون الثاني|كانون الأول|شباط|آذار|نيسان|أيار|حزيران|تموز|آب|أيلول|تشرين الأول|تشرين الثاني|محرم|صفر|ربيع الأول|ربيع الآخر|جمادى الأولى|جمادى الآخرة|رجب|شعبان|رمضان|شوال|ذو القعدة|ذو الحجة"
DAYS="الأحد|الاثنين|الإثنين|الثلاثاء|الأربعاء|الخميس|الجمعة|السبت"
ORD="الأول|الثاني|الثالث|الرابع|الخامس|السادس|السابع|الثامن|التاسع|العاشر|الحادي عشر|الثاني عشر|الثالث عشر|الرابع عشر|الخامس عشر|السادس عشر|السابع عشر|الثامن عشر|التاسع عشر|العشرين|الحادي والعشرين"
TIME_PATTERNS=[rf"(?:(?:يوم\s+)?(?:{DAYS})\s+)?(?:\d{{1,2}}\s+)?(?:شهر\s+)?(?:{MONTHS})(?:\s+(?:من\s+)?(?:عام|سنة)?\s*\d{{3,4}}(?:\s*(?:م|هـ|ه))?)?",rf"القرن\s+(?:{ORD})(?:\s+(?:الميلادي|الهجري|قبل الميلاد))?",rf"(?:عام|سنة)\s+\d{{3,4}}(?:\s*(?:م|هـ|ه))?",rf"\b(?:{DAYS})\b",r"\b(?:1[0-9]{3}|20[0-9]{2})\b(?:\s*(?:م|هـ))?"]
def clean(text):
    text=re.sub(r"[ً-ْٰ]","",text); text=text.replace("ـ","")
    text=re.sub(r"[​-‏‪-‮﻿]","",text); text=re.sub(r"https?://\S+"," ",text)
    text=re.sub(r"[ \t\r\n]+"," ",text); text=re.sub(r"\s+([.،؛:!؟?])",r"\1",text)
    return text.strip()
def split_sentences(text):
    return [p.strip() for p in re.split(r"(?<=[.!؟?])(?<!\d\.)\s+",text) if len(p.strip())>1]
def time_entities(text):
    out=[]
    for p in TIME_PATTERNS:
        for m in re.finditer(p,text):
            s,e=m.span()
            if e>s and not any(s<e2 and e>s2 for s2,e2,_ in out): out.append((s,e,"DATE"))
    return out
def norm(s): return re.sub(r"[^\w\s]","",s.lower()).strip()
def similarity(a,b):
    a,b=norm(a),norm(b)
    if not a or not b:return 0
    ta,tb=set(a.split()),set(b.split()); jac=len(ta&tb)/len(ta|tb); seq=SequenceMatcher(None,a,b).ratio()
    dig=.3 if set(re.findall(r"\d+",a))&set(re.findall(r"\d+",b)) else 0
    return max(jac,seq)+dig
