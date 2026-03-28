#!/usr/bin/env python3
"""
获取B站CC字幕
"""
import requests
import re
import json
import html
import os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64