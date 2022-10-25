# -*- coding: utf-8 -*-
import time
import csv

def main():

    try:
        csvfile = "historico-nombres.csv" #"prueba.csv"
        with open(csvfile) as f:
            names_csv = csv.reader(f)
            names_list = []
            
            for row in names_csv:
                names_list.append(row[0])
            
            print(len(names_list))

    except Exception:
        print("Error")
    #    removeConnection(celularRed)

main()