from flask import *
from project import db
from project.forms import QueryForm, NewDocForm
from project.indexer import InvertedIndex
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from project.model import Documents


admin = Blueprint('admin',__name__)

# db = Database()
invertedIndex = InvertedIndex()


@admin.route('/', methods=['POST', 'GET'])
def landingPage():
    form = QueryForm()
    if form.validate_on_submit():
        query = form.query.data
        if query:
            return redirect(url_for('admin.resultPage', query=query, invertedIndex=invertedIndex))
    return render_template('index.html', form=form, Documents=Documents)


@admin.route('/add-new', methods=['GET', 'POST'])
def addNewPage():
    return render_template('add-new.html')

@admin.route('/load-new-doc', methods=['POST', 'GET'])
def loadNewDocPage():
    queryForm = QueryForm()
    newDocForm = NewDocForm()
    if newDocForm.validate_on_submit():
        document = newDocForm.document.data
        if document:
            documents = []
            document = document.replace('\r', '').split('\n\n')
            for document in document:
                documents.append(document)
            for eachDocument in documents:
                invertedIndex.index_document(eachDocument)
            return redirect(url_for('admin.landingPage'))
    return render_template('load-new-doc.html', form=newDocForm)


@admin.route('/load-new-pdf', methods=['POST', 'GET'])
def loadNewPdfPage():
    def convert_pdf_to_txt(path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)
        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
        return text
    text = ''
    if request.method == "POST":
        print('aaa')
        print(request.files['file'])
        f = request.files['file']
        f.save(f.filename)
        text = convert_pdf_to_txt(f.filename)
    if text:
        invertedIndex.index_document(text, True)
    return redirect(url_for('admin.landingPage'))


@admin.route('/<query>/search-results', methods=['POST', 'GET'])
def resultPage(query):
    searchResults = []
    result = invertedIndex.lookup_query(query)
    if result[0]:
        for term in result[1].keys():
            for appearance in result[1][term]:
                document = Documents.query.filter_by(id=appearance.docId)[0].text              
                searchResults.append(document)
    else:
        print('No documents match your search')
    searchResults = list(set(searchResults))
    form = QueryForm()
    form.query.render_kw={"placeholder":query}
    if searchResults:
        return render_template('search-results.html', form=form, searchResults=searchResults)
    else:
        return render_template('no-docs-found.html')


@admin.route('/view-all-docs', methods=['POST', 'GET'])
def viewAllDocs():
    searchResults = []
    allDocs = Documents.query.all()
    for doc in allDocs:
        if doc.text:
            searchResults.append(doc.text)
    searchResults = list(set(searchResults))
    print(searchResults)
    if searchResults:
        return render_template('view-all-docs.html', searchResults=searchResults)
    else:
        return render_template('no-docs-found.html')

@admin.route('/erase-all-docs', methods=['POST', 'GET'])
def eraseAllDocs():
    Documents.query.delete()
    db.session.commit()
    return render_template('erase-all-docs.html')