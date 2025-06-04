#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Azərbaycan Söz Ovçusu - 4x4 şəbəkədən Azərbaycan sözləri tapır
"""

import pandas as pd
import os
from colorama import init, Fore, Back, Style

# Colorama-nı başlat
init(autoreset=True)

class AzerbaijaniGridWordHunter:
    def __init__(self, excel_file="words.xlsx"):
        self.words = set()
        self.grid = []
        self.directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        self.load_words(excel_file)
    
    def load_words(self, excel_file):
        """Excel faylından sözləri yüklə"""
        try:
            if not os.path.exists(excel_file):
                print(f"{Fore.RED}❌ {excel_file} tapılmadı!")
                return
            
            print(f"{Fore.CYAN}📂 {excel_file} faylı oxunur...")
            
            ext = excel_file.split('.')[-1].lower()
            engine = 'xlrd' if ext == 'xls' else 'openpyxl' if ext == 'xlsx' else None
            
            if engine:
                df = pd.read_excel(excel_file, engine=engine)
            else:
                df = pd.read_csv(excel_file)
            
            for word in df.iloc[:, 0]:
                if pd.notna(word):
                    clean = self.normalize_az(str(word).strip())
                    if len(clean) >= 2:
                        self.words.add(clean)
            
            print(f"{Fore.GREEN}✅ {len(self.words)} söz yükləndi")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Xəta: {e}")
    
    def normalize_az(self, text):
        """Azərbaycan hərflərini normallaşdır"""
        az_chars = {
            'ə': 'ə', 'ı': 'ı', 'ö': 'ö', 'ü': 'ü', 'ç': 'ç', 'ğ': 'ğ', 'ş': 'ş',
            'Ə': 'ə', 'I': 'ı', 'Ö': 'ö', 'Ü': 'ü', 'Ç': 'ç', 'Ğ': 'ğ', 'Ş': 'ş'
        }
        
        result = []
        for char in text:
            if char in az_chars:
                result.append(az_chars[char])
            elif char.isalpha():
                result.append(char.lower())
        
        return ''.join(result)
    
    def create_grid(self, letters):
        """16 hərfdən 4x4 şəbəkə"""
        if len(letters) != 16:
            return False
        
        letters = self.normalize_az(letters)
        self.grid = [[letters[i*4+j] for j in range(4)] for i in range(4)]
        return True
    
    def print_grid(self):
        """Şəbəkəni göstər"""
        print(f"\n{Fore.YELLOW}🔤 Şəbəkə:")
        for row in self.grid:
            colored_row = " ".join(f"{Back.BLUE}{Fore.WHITE} {c.upper()} {Style.RESET_ALL}" for c in row)
            print(f"  {colored_row}")
    
    def find_word(self, word, row, col, pos, used):
        """Sözü şəbəkədə tap (rekursiv)"""
        if pos == len(word):
            return True
        
        if (row < 0 or row >= 4 or col < 0 or col >= 4 or 
            (row, col) in used or self.grid[row][col] != word[pos]):
            return False
        
        used.add((row, col))
        
        if pos == len(word) - 1:
            used.remove((row, col))
            return True
        
        for dr, dc in self.directions:
            if self.find_word(word, row + dr, col + dc, pos + 1, used):
                used.remove((row, col))
                return True
        
        used.remove((row, col))
        return False
    
    def can_make_word(self, word):
        """Sözün şəbəkədə olub-olmadığını yoxla"""
        word = self.normalize_az(word)
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == word[0]:
                    if self.find_word(word, i, j, 0, set()):
                        return True
        return False
    
    def find_all_words(self):
        """Bütün sözləri tap"""
        found = {}
        
        for word in self.words:
            if self.can_make_word(word):
                length = len(word)
                if length not in found:
                    found[length] = []
                found[length].append(word)
        
        return found

def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}🎯 Azərbaycan 4x4 Şəbəkə Söz Ovçusu")
    print(f"{Fore.CYAN}{'=' * 40}")
    
    hunter = AzerbaijaniGridWordHunter("words.xlsx")
    
    if not hunter.words:
        print(f"{Fore.RED}❌ Söz bazası yüklənmədi!")
        return
    
    while True:
        print(f"\n{Fore.MAGENTA}🔤 16 hərf daxil edin (çıxış üçün '{Fore.RED}q{Fore.MAGENTA}'):")
        letters = input(f"{Fore.YELLOW}➤ {Style.RESET_ALL}").strip()
        
        if letters.lower() == 'q':
            print(f"{Fore.GREEN}👋 Görüşənədək!")
            break
        
        if not hunter.create_grid(letters):
            print(f"{Fore.RED}❌ 16 hərf lazımdır!")
            continue
        
        hunter.print_grid()
        found_words = hunter.find_all_words()
        
        if found_words:
            total = sum(len(words) for words in found_words.values())
            print(f"\n{Fore.GREEN}📝 Tapılan sözlər: {Style.BRIGHT}{total}")
            print(f"{Fore.CYAN}{'-' * 30}")
            
            for length in sorted(found_words.keys()):
                words = found_words[length]
                colored_words = f"{Fore.CYAN}{Style.BRIGHT}, ".join(words)
                print(f"\n{Fore.YELLOW}{length} hərfli ({Fore.CYAN}{len(words)}{Fore.YELLOW}): {Fore.CYAN}{Style.BRIGHT}{colored_words}")
        else:
            print(f"\n{Fore.RED}❌ Söz tapılmadı!")

if __name__ == "__main__":
    main()