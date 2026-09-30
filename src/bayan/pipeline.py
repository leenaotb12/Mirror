# -*- coding: utf-8 -*-
import html,re,sys,torch
from transformers import pipeline,AutoTokenizer,AutoModelForSeq2SeqLM
import spacy
from .alignment import GROUP,clean,split_sentences,time_entities,similarity
MT_MODEL="Helsinki-NLP/opus-mt-ar-en"; AR_NER_MODEL="CAMeL-Lab/bert-base-arabic-camelbert-msa-ner"; THRESHOLD=.35
def arabic_entities(text,ner):
    ents=time_entities(text)
    for r in ner(text):
        s,e=r["start"],r["end"]; g=GROUP.get(r["entity_group"].replace("B-","").replace("I-",""),"MISC")
        if not any(s<e2 and e>s2 for s2,e2,_ in ents): ents.append((s,e,g))
    return sorted(ents)
def english_entities(text,nlp): return [(x.start_char,x.end_char,GROUP[x.label_]) for x in nlp(text).ents if x.label_ in GROUP]
def align(ar_text,ar_ents,en_text,en_ents,translate_batch,cache):
    need=list({ar_text[s:e] for s,e,_ in ar_ents if ar_text[s:e] not in cache})
    if need:
        for k,v in zip(need,translate_batch(need)): cache[k]=v
    scored=[]
    for i,(s,e,g) in enumerate(ar_ents):
        tr=cache[ar_text[s:e]]
        for j,(s2,e2,g2) in enumerate(en_ents):
            if g==g2 or "MISC" in (g,g2):
                sc=similarity(tr,en_text[s2:e2])
                if sc>=THRESHOLD: scored.append((sc,i,j))
    pairs=[]; ui=set(); uj=set()
    for sc,i,j in sorted(scored,reverse=True):
        if i not in ui and j not in uj: ui.add(i); uj.add(j); pairs.append((i,j))
    return pairs
def words_html(text,ents):
    out=[]
    for m in re.finditer(r"\S+",text):
        eid=None
        for s,e,g,i in ents:
            if m.start()<e and m.end()>s: eid=i; break
        w=html.escape(m.group())
        out.append(f'<span class="word entity-word" data-eid="{eid}" onmouseover="hl(\'{eid}\')" onmouseout="unhl()">{w}</span>' if eid else f'<span class="word">{w}</span>')
    return " ".join(out)
PAGE="""<!DOCTYPE html><html lang="ar"><head><meta charset="utf-8"><title>الكيانات العربية ومقابلاتها الإنجليزية</title>
<style>body{font-family:system-ui,sans-serif;background:#f8fafc;margin:0;padding:30px;direction:rtl}.container{max-width:1300px;margin:0 auto;background:#fff;padding:40px;border-radius:16px}.reader-table{width:100%;border-collapse:collapse;table-layout:fixed}.reader-table th,.reader-table td{padding:14px;border:1px solid #e2e8f0}.word{display:inline-block;margin:0 2px;padding:2px 4px}.entity-word{cursor:pointer;border-bottom:2px dotted #94a3b8}.flash-active{font-weight:bold;box-shadow:0 0 10px #fde047}.ar-col{text-align:right;line-height:1.8}.en-col{text-align:left;line-height:1.8;direction:ltr}</style>
<script>function hl(id){document.querySelectorAll('[data-eid="'+id+'"]').forEach(e=>e.classList.add('flash-active'))}function unhl(){document.querySelectorAll('.flash-active').forEach(e=>e.classList.remove('flash-active'))}</script></head><body><div class="container"><h2>نظام تحديد الكيانات العربية ومقابلاتها الإنجليزية</h2><p>مرر الماوس فوق الكلمات المنقطة لترى الوميض على الكيان ومقابله.</p><table class="reader-table"><thead><tr><th>الجملة العربية</th><th>الجملة الإنجليزية</th></tr></thead><tbody>%ROWS%</tbody></table></div></body></html>"""
def main(inp,outp):
    sents=split_sentences(clean(open(inp,encoding="utf-8").read()))
    tok=AutoTokenizer.from_pretrained(MT_MODEL); mt=AutoModelForSeq2SeqLM.from_pretrained(MT_MODEL)
    def translate_batch(xs):
        out=[]
        for i in range(0,len(xs),16):
            b=tok(xs[i:i+16],return_tensors="pt",padding=True,truncation=True,max_length=256)
            with torch.no_grad(): g=mt.generate(**b,max_new_tokens=256,num_beams=4)
            out+=tok.batch_decode(g,skip_special_tokens=True)
        return out
    ner=pipeline("token-classification",model=AR_NER_MODEL,aggregation_strategy="simple"); nlp=spacy.load("en_core_web_sm")
    translations=translate_batch(sents); cache={}; rows=[]; eid=n_ar=n_en=0
    for ar,en in zip(sents,translations):
        ar_e,en_e=arabic_entities(ar,ner),english_entities(en,nlp); n_ar+=len(ar_e); n_en+=len(en_e)
        ar_w=[]; en_w=[]
        for i,j in align(ar,ar_e,en,en_e,translate_batch,cache):
            eid+=1; ar_w.append((ar_e[i][0],ar_e[i][1],ar_e[i][2],f"e{eid}")); en_w.append((en_e[j][0],en_e[j][1],ar_e[i][2],f"e{eid}"))
        rows.append(f'<tr><td class="ar-col">{words_html(ar,ar_w)}</td><td class="en-col">{words_html(en,en_w)}</td></tr>')
    open(outp,"w",encoding="utf-8").write(PAGE.replace("%ROWS%","\n".join(rows))); print(f"sentences={len(sents)} arabic_entities={n_ar} english_entities={n_en} aligned_pairs={eid}")
if __name__=="__main__": main(sys.argv[1],sys.argv[2])
