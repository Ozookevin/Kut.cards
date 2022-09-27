
from Dependency.Python_imports import *



app = Flask(__name__)

## Main Page
@app.route("/", methods=['POST', 'GET'])
def Home():
    if request.method == 'POST':
        URl = request.form['URL']
        return cardProcess(URl)


    return render_template('index.html')


## Download page for chrome extension

@app.route("/Kut_Extension")                                        
def Kut_Extension():
    return render_template("Download_Extention.html")



## Chrome Extension     

@app.route("/chrome", methods=['POST', 'GET'])
def chrome():
    if request.method == 'POST':
        URl = request.form['URL']
        author = request.form['aName']
        date = request.form['pDate']
        
        return cardProcess(URl)

        #return render_template('Loading.html')
    else:
        return render_template('Chrome.html')
    
    
    return render_template('Chrome.html')

def cardProcess(url):
    
    render_template('Loading.html')
    api_URL = url

    try:
            
        if len(api_URL) < 10:
            return "Request Error #001-- invalid URL"
    except:
        pass
    
# Strip url spaces and charachters
    Url_filename = re.sub(r'[^\w\s]','',api_URL)
    UrlClean = Url_filename
    Url_filename = Url_filename ,".docx"
    Url_filename = str(Url_filename)

# Read data from the past url json file
    with open('Dependency\P_URL.json') as f:
        Url_list = json.load(f)

# Check if user input has been processed before

    if UrlClean in Url_list:
        downloadFile = UrlClean
        # return the file in the download folder
        file_path = r'D:\Cards'
        
        downloadFile = file_path + r'\\'+ downloadFile + ".docx"
        
        try:
            return send_file(downloadFile, as_attachment= True, download_name= "KutCards_Backfile.docx")
        except:
            try:
                downloadFile = downloadFile.replace(" ","")
                return send_file(downloadFile, as_attachment= True, download_name= "KutCards_Backfile.docx")
            except:
                try:
                    downloadFile = file_path + r'\\' + UrlClean + " .docx"
                except:
                    pass 

        #return send_file(Url_filename, as_attachment= True, download_name= "KutCard_Backfile.docx")


    return get_content(api_URL,Url_list)
    
def get_content(url,Url_list):
    url = url 
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    Title = article.title
    Authors = article.authors
    Publication_Date = article.publish_date
    clean_text = article.text
    cites = [Title, Authors, Publication_Date]  

    try:
        ext = tldextract.extract(url)
        publisher = ext.domain.title()
    except: 
        publisher = ''   
    try:
        page=requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        lastname = soup.find("meta",  {"property":"author"})
        lastname = lastname["content"] if lastname else None
        lastname1 = lastname.split()[1]
        lastname1 = re.sub(r'[^\w\s]','',lastname1)
        #lastname1 = str(lastname1)
        #lastname = lastname1
        # Using same method as above answer
        # author = author["content"] if author else None
    except:
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            first_last = article.authors
            try:
                lastname1 = first_last
                lastname1 = lastname1.split()[1]
                lastname1 = re.sub(r'[^\w\s]','',lastname1)
                lastname1 = str(lastname1)
            except:
                lastname1 = lastname
        except:
            lastname = publisher
            lastname1 = publisher

    try:
        cite_Publication_Date = article.publish_date
        date = datetime.strptime(cite_Publication_Date,'%Y-%m-%d %H:%M:%S')
        year = date.strftime("%Y")
        a_string = str(year)
        a_length = len(a_string)
        year = a_string[a_length - 2: a_length]
    except:
        cite_Publication_Date = "Last accessed 2021"
        year = '21'
        date = "Last assessed 2021"

    cite_clean_content = article.text

    template = r"C:\Users\kevoz\OneDrive\NonOrganized\Desktop\Kut_Cards\Dependency\debate_temp.docx"


    # calls to summery api
    response =['https://api.smmry.com/&SM_API_KEY=5BD00B32C7&SM_URL=']
    response.append(url)
    clean_response_no_spaces = ''.join(response)
    content = requests.get(clean_response_no_spaces)
    
    
    # Convert Json into text
    json_response_text = content.text 
    jsonconvert = json.loads(json_response_text)
    clean_summery_content = jsonconvert['sm_api_content']

   
   
    # create summery parsed document that will later be merged

    token_sum = sent_tokenize(clean_summery_content)
    token_full_content = sent_tokenize(cite_clean_content)

    document = Document()

    body = document.add_paragraph(style = 'Body Text')
    for sentences in token_full_content:
        if any(sentences in s for s in token_sum):
            highlighted = body.add_run(sentences)
            highlighted.bold = True
            highlighted.underline = True
            highlighted.font.size = Pt(12)
        else:
            unhighlighted = body.add_run(sentences)
            unhighlighted.bold = False
            unhighlighted.underline = False
            unhighlighted.font.size = Pt(8)

    filenamecontent=  "\\temp_content.docx"
    filenamecite = "\\temp_cite.docx"
    document.save(r'C:\Users\kevoz\OneDrive\NonOrganized\Desktop\Kut_Cards\Dependency' + filenamecontent)
    
    
    # Generate Card Tag:
    sentence_list = nltk.sent_tokenize(clean_summery_content)
    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(clean_summery_content):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
        else:

            maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 50:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(1, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    sum1 = re.sub('[^a-zA-Z]', '', summary)
    cite_tag = summary

    
    
    # applying MailMerge to input varables into word templete
    document = MailMerge(template)   
    document.merge(
        Tag = cite_tag,
        Author = lastname1,
        Date = year,
        Publication_date = date,
        Qual = " ",
        Author_full_name = lastname,
        content = cite_clean_content,
        Publication = publisher,
        URL = url
        )
    document.write(r'C:\Users\kevoz\OneDrive\NonOrganized\Desktop\Kut_Cards\Dependency' + filenamecite)


    # merge documents together:
    # combining documents together

    # Strip url spaces and charachters
    Url_filename = re.sub(r'[^\w\s]','',url)
    URLClean = Url_filename
    file_path = r'D:\Cards'
    Url_filename = Url_filename,".docx"
    Url_filename = str(Url_filename)
    Url_filename = file_path + r'\\' + Url_filename

    try:

        Url_filename = Url_filename.replace("(","")
    except:
        pass

    Url_filename = Url_filename.replace(")","")

    try:
        Url_filename = Url_filename.replace("'","")
    except:
        pass

    try:
        Url_filename = Url_filename.replace(",","")
    except:
        pass

    try:
        Url_filename = Url_filename.repalce(" ","")
    except:
        pass

    master = Document(r"C:\Users\kevoz\OneDrive\NonOrganized\Desktop\Kut_Cards\Dependency\temp_cite.docx")
    composer = Composer(master)
    doc1 = Document(r"C:\Users\kevoz\OneDrive\NonOrganized\Desktop\Kut_Cards\Dependency\temp_content.docx")
    composer.append(doc1)
    try:
        Url_filename = Url_filename.replace(" ","")
    except:
        pass

    composer.save(Url_filename)

    Url_list.append(URLClean)

    with open('Dependency\P_URL.json', 'w') as file_descriptor:
        json.dump(Url_list, file_descriptor)

    
    
    return send_file(Url_filename, as_attachment= True, download_name= "KutCard.docx")
    ## Return code to other python script







if __name__ == "__main__":
    run_simple('0.0.0.0',80, app,)

