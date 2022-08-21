from __future__ import print_function
from mailmerge import MailMerge
from datetime import date
from docx import Document
from docxcompose.composer import Composer
from docx import Document as Document_compose
import KO_Cut
from KO_Cut import citeTag, citeAuthor, citeDate, pubDate, citeQual, citeFullname, citePub, citeURL

# loading Debate templete from root

template = "debate_temp.docx"

# applying MailMerge to input varables into word templete

document = MailMerge(template)

# blank varable are place holder

cardContent = 'none'

def create_doc(document):
    
    document.merge(
    Tag = citeTag,
    Author = citeAuthor,
    Date = citeDate,
    Publication_date = pubDate,
    Qual = citeQual,
    Author_full_name = citeFullname,
    content = cardContent,
    Publication = citePub,
    URL = citeURL
    )
    
    document.write('temp_cite.docx')
    
create_doc(document) # Fucntion call for Document creation. 

def docTitle(citeTag):
    title = citeTag
    title = title[0:30]
    fileEx = ".docx"
    title = title.strip() + fileEx.strip() 

    return title 

title = docTitle(citeTag)
# should put into a def at some point.

# combining documents together
master = Document("temp_cite.docx")
composer = Composer(master)
doc1 = Document("temp_content.docx")
composer.append(doc1)
composer.save(title)


