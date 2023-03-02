##########################################################
### Import Necessary Modules

import argparse		               #provides options at the command line
import sys		               #take command line arguments and uses it in the script
import gzip		               #allows gzipped files to be read
import re		               #allows regular expressions to be used
import pysam			       #allows sam and bam files to be read
import GeneralWindow                   #generates windows

##########################################################
### Command-line Arguments
parser = argparse.ArgumentParser(description="A script to characterize coverage of a sam or bam alignment file (must be proper pair alignments) as histogram (coverage or alignment score)")
parser.add_argument("-file", help = "The location of the bam or sam file, default=<stdin>, comma-separated for multiple files", nargs='+')
parser.add_argument("-fai", help = "The location of faidx indexed for the reference genome", default=sys.stdin, required=True)
parser.add_argument("-win", help = "The window size, default=1000000", default=1000000)
parser.add_argument("-step", help = "The step size, default=500000", default=500000)
parser.add_argument("-chrom", help = "To specify a specific chromosome or scaffold, default=all", default="all")
parser.add_argument("-minScore", help = "The minimum score to keep stats on alignment, default= 0", default=0)
parser.add_argument("-maxScore", help = "The maximum score to keep stats on alignment, default=100", default=100)
parser.add_argument("-minLen", help = "The minimum query alignment length to keep stats on alignment, default= 0", default=0)
parser.add_argument("-maxLen", help = "The maximum query alignment length to keep stats on alignment, default= 10000", default=10000)
parser.add_argument("-out", help = "Output the average coverage (default) or average score for a region, default= cov, option= score", default="cov")
args = parser.parse_args()

#########################################################
### Global Variables
class Variables():
    window = {}
    scaffoldSizes = {}

#########################################################
### Opening files and functions
class OpenFile():
    def __init__ (self, f, inde):
        """Opens a file -- sam or bam accepted"""
        if re.search(".sam$", f):
            self.aln = pysam.AlignmentFile(f, "r")
            sys.stderr.write("\n\tOpening file {}\n\n".format(f))
            OpenAln(self.aln, inde)
        elif re.search(".bam$", f):
            self.aln = pysam.AlignmentFile(f, "rb")
            sys.stderr.write("\n\tOpening file {}\n\n".format(f))
            OpenAln(self.aln, inde)
        elif re.search(".fai$", f):
            sys.stderr.write("\n\tOpening file {}\n\n".format(f))
            self.filename = open(f, 'r')
            OpenFai(self.filename)
        else:
            sys.stderr.write("\n\tError {}, did not match accepted file extensions (.fai, .bam, and .sam).\n\n".format(f))

class OpenAln():
    def __init__ (self, aln, ind):
        """Reads the alignment file and generate statistics for every window"""
        for self.sequence in Variables.window:
            for self.window in Variables.window[self.sequence]:
                self.startPosition, self.endPosition = self.window.split(":")
                self.inter = aln.fetch(str(self.sequence), int(self.startPosition), int(self.endPosition))
                self.readCount = 0
                self.qualScore = 0
                self.queryLength = 0
                for self.line in self.inter:
                    if (self.line.is_proper_pair and int(self.line.mapping_quality) <= int(args.maxScore) and int(self.line.mapping_quality) >= int(args.minScore) and
                    int(self.line.query_alignment_length) <= int(args.maxLen) and int(self.line.query_alignment_length) >= int(args.minLen)):
                        self.readCount += 1
                        self.qualScore += int(self.line.mapping_quality)
                        self.queryLength += int(self.line.query_alignment_length)
                try:
                    self.qual = float(self.qualScore)/int(self.readCount)
                    self.coverage = float(self.queryLength)/(int(self.endPosition) - int(self.startPosition) + 1)
                except:
                    self.qual = "NA"
                    self.coverage = 0
                self.report = self.coverage
                if args.out == "score":
                    self.report = self.qual
                print("{}\t{}\t{}\t{}".format(self.sequence, self.startPosition, self.endPosition, self.report))


class OpenFai():
    def __init__ (self,f):
        """Opens fai file and returns scaffold and read lengths to a global variable"""
        self.scaffCount = 0
        self.length = 0
        for self.line in f:
            self.line = self.line.rstrip('\n')
            self.scaff, self.len = self.line.split("\t")[0:2]
            if args.chrom == "all" or args.chrom == self.scaff:
                Variables.scaffoldSizes[self.scaff] = self.len
                Variables.window[self.scaff] = GeneralWindow.Window(1, int(self.len), int(args.win), int(args.step))
            self.scaffCount += 1
            self.length += int(self.len)
        f.close()
        sys.stderr.write("\t\t# Seqs in fai file: {}\n".format(self.scaffCount))
        sys.stderr.write("\t\tAvgLength: {}\n\n".format(float(self.length)/self.scaffCount))

#########################################################
###Order of things to be called
if __name__ == '__main__':
    Variables()
    open_file = OpenFile(args.fai, "1")
    if len(args.file) > 0:
        for index, bamFile in enumerate(args.file):
            open_file = OpenFile(bamFile, index)
