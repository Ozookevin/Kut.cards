
# imports that are need to run Kutcards API 

import flask
from flask import Flask, request
from newspaper import Article
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from flask import Blueprint, render_template, send_from_directory, send_file
from flask.templating import render_template_string
import pandas as pd
import requests
import json
from mailmerge import MailMerge
from datetime import date
from docx import Document
from docxcompose.composer import Composer
from docx import Document as Document_compose
import articleDateExtractor
import tldextract 
from docx import Document
from docx.shared import Length
from docx.shared import Inches, Pt
from docx.shared import RGBColor
from docx.text.run import Font, Run
import nltk
#from website import Flask, create_app 
#nltk.download()
from nltk.tokenize import sent_tokenize, word_tokenize
import re
import heapq
from datetime import datetime, date
import ctypes
import json

from flask import Flask 
from flask import render_template
from flask import request
from flask import flash
import requests
#from crypt import methods
from werkzeug.serving import run_simple
from werkzeug.serving import make_ssl_devcert