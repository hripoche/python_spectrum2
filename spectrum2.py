# Author: Hugues Ripoche
# Copyright (c) 2002-2011
# License: BSD Style.
# python version: 2.6

import csv

import math

import matplotlib.pyplot as plt

FILTER_MODE = ["Sum of intensities","Cosine similarity"]

output_file_separator = "\t"

#config_file = "spectrum_config.txt"

#def split_masses(str):
#    """convert a string of floats into a list of floats"""
#    str = str.replace('\"','')
#    str = str.replace(' ','')
#    items = str.split(",")
#    result = []
#    for item in items:
#        item = float(item)
#        result.append(item)
#    return result

#def read_config_file(textfile):
#    """read text config file"""
#    handler = open(textfile,"r")
#    text = handler.read()
#    # eclate le texte en lignes en supprimant les caracteres de fin de ligne
#    lines = text.splitlines(False)
#    hashtable = {}
#    for line in lines:
#        print(line)
#        items = line.split("\t")
#        key = items[0]
#        val = items[1]
#        if key == "delta":
#            val = float(val)
#        if key == "parental_mass":
#            val = float(val)
#        if key == "theoretical_fragment_masses":
#            val = split_masses(val)
#        hashtable[key] = val
#        print(key,val)
#    handler.close()
#    return hashtable

class SpectrumLine():
    def __init__(self):
        self.retention_time = None
        self.polarity = None
        self.ionization_type = None
        self.ms_ms_generation = None
        self.ms_ms_precursor = None
        self.profile_line_spectrum = None
        self.mass_range = None
        self.number_of_points = None
        self.points = None
        self.value_which_match = None
        self.fragments_which_match = None
        
    def not_empty_points(self):
        return self.number_of_points is not None and self.number_of_points != 0 and self.points is not None and len(self.points) > 0

    def has_match(self):
        return len(self.fragments_which_match)>=1

    def xprint(self):
        print "retention_time",self.retention_time
        print "polarity",self.polarity
        print "ionization_type",self.ionization_type
        print "ms_ms_generation",self.ms_ms_generation
        print "ms_ms_precursor",self.ms_ms_precursor
        print "profile_line_spectrum",self.profile_line_spectrum
        print "mass_range",self.mass_range
        print "number_of_points",self.number_of_points
        print "points",self.points
        print "value_which_match",self.value_which_match
        print "fragments_which_match",self.fragments_which_match

def read_csvdatafile(textfile):
    """read ascii csv text file and returns a list of SpectrumLine objects"""
    handler = open(textfile,"r")
    lines = []
    if handler:
        for line in csv.reader(handler):
            spectrumLine = SpectrumLine()
            spectrumLine.retention_time = line[0]
            spectrumLine.polarity = line[1]
            spectrumLine.ionization_type = line[2]
            spectrumLine.ms_ms_generation = line[3]
            spectrumLine.ms_ms_precursor = line[4]
            spectrumLine.profile_line_spectrum = line[5]
            spectrumLine.mass_range = line[6]
            spectrumLine.number_of_points = line[7]
            if spectrumLine.number_of_points.isdigit():
                l = []
                for i in range(0,long(spectrumLine.number_of_points)):
                    l.append(line[8+i].split(" "))
                spectrumLine.points = l
            lines.append(spectrumLine)
        handler.close()
    else:
        print "Error: cannot open: ",textfile
    return lines

def filter_points_sum(theoretical_fragment_masses,points,delta):
    """theoretical_fragment_masses : list of theoretical masses
    points : list of points (where point is : [mass, intensity])
    delta : max difference for match between theoretical and experimental mass
    return a tuple: sum of intensities where there is a match, list of points that match
    """
    sum = 0.0
    l = []
    for point in points:
        m = float(point[0])
        i = float(point[1])
        for tfm in theoretical_fragment_masses:
            diff = abs(m - tfm)
            if diff <= delta:
                sum = sum + i
                l.append(point)
    return (sum,l)

def filter_points_cosine(theoretical_fragment_masses,points,delta):
    """theoretical_fragment_masses : list of theoretical masses
    points : list of points (where point is : [mass, intensity])
    delta : max difference for match between theoretical and experimental mass
    
    return a tuple: cosine, list of points that match
    where cosine is: dot_product / (norm_all * norm_tfm)
    where the dot product is computed for the fragments which match
    and norm_all is the norm over all the points' intensities
    and norm_tfm is the norm over all the theoretical fragments (intensity is considered 1 for each theoretical fragment)
    """
    sum = 0.0
    l = []
    sum_all = 0.0
    for point in points:
        #print "point",point
        m = float(point[0])
        i = float(point[1])
        sum_all = sum_all + i*i
        for tfm in theoretical_fragment_masses:
            diff = abs(m - tfm) 
            if diff <= delta:
                sum = sum + i
                l.append(point)
    norm_all = math.sqrt(sum_all)
    norm_tfm = math.sqrt(len(theoretical_fragment_masses))
    #print("norm_all",norm_all)
    #print("norm_tfm",norm_tfm)
    cosine = float(sum) / (norm_all * norm_tfm)
    #print("cosine",cosine)
    return (cosine,l)

class Fragments(object):
    
    def __init__(self,ascii_file,parental_mass,theoretical_fragment_massses,delta,mode_text):
        self.ascii_file = ascii_file
        self.parental_mass = parental_mass
        self.theoretical_fragment_massses = theoretical_fragment_massses
        self.lines = read_csvdatafile(ascii_file)
        self.delta = delta
        for spectrumLine in self.lines:
            #spectrumLine.xprint()
            if spectrumLine.not_empty_points():
                if mode_text == FILTER_MODE[0]:
                    (value_which_match,fragments_which_match) = filter_points_sum(self.theoretical_fragment_massses,spectrumLine.points,delta)
                elif mode_text == FILTER_MODE[1]:
                    (value_which_match,fragments_which_match) = filter_points_cosine(self.theoretical_fragment_massses,spectrumLine.points,delta)
                else:
                    print "Error: Unknown mode"
                spectrumLine.value_which_match = value_which_match
                spectrumLine.fragments_which_match = fragments_which_match
    
    def print_get_lines(self,output_file):
        handler = open(output_file,"w")
        #print(self.ascii_file,"\n")
        #print("parental_mass=",self.parental_mass,"\n")
        #print("theoretical_fragment_massses=",self.theoretical_fragment_massses,"\n")
        #print("delta=",self.delta,"\n")
        if handler:
            for spectrumLine in self.lines:
                if spectrumLine.not_empty_points() and spectrumLine.has_match():
                    print >>handler, spectrumLine.retention_time, output_file_separator, spectrumLine.value_which_match, output_file_separator, str(len(spectrumLine.fragments_which_match))+" in "+spectrumLine.number_of_points, output_file_separator, spectrumLine.fragments_which_match  
            handler.close()
        else:
            print "Error: cannot open: ",output_file

    def plot_lines(self,img_filename,mode_text):
        for spectrumLine in self.lines:
            if spectrumLine.not_empty_points() and spectrumLine.has_match():
                rt = spectrumLine.retention_time
                plt.plot(rt,spectrumLine.value_which_match,'.')
        plt.title("Parental Mass : " + str(self.parental_mass))
        plt.xlabel("Retention time")
        plt.ylabel(mode_text)
        plt.grid(True)
        plt.savefig(img_filename)
        plt.show()

#def main():
#    hashtable = read_config_file(config_file)
#    delta = 0
#    delta = hashtable["delta"]
#    fragments = Fragments(hashtable["ascii_file"],hashtable["parental_mass"],hashtable["theoretical_fragment_masses"],delta)
#    fragments.print_get_lines(hashtable["output_file"])
#    fragments.plot_lines()

#main()
