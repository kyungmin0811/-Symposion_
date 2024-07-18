import pymupdf
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import nltk
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import word_count



word_count.analyze_question()