import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from bayan.alignment import clean,split_sentences,similarity,time_entities
def test_clean(): assert clean("مَرْحَبًا ــ بالعالم")=="مرحبا بالعالم"
def test_split(): assert split_sentences("هذه جملة. وهذه ثانية؟")==["هذه جملة.","وهذه ثانية؟"]
def test_similarity(): assert similarity("Riyadh","Riyadh")>=1
def test_date(): assert any(x[2]=="DATE" for x in time_entities("في عام 2020"))
