# BamHistogram
A python script to produce a histogram of bam alignment files (requires indexed bam file and index of reference sequence)

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#requirements">Requirements</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- requirements -->
## Requirements

This script has been tested with Python 3.
The script requires the following python package, script, and files.

Packages:<br /><br />
&nbsp;&nbsp;&nbsp;pysam<br />
&nbsp;&nbsp;&nbsp;GeneralWindow (available as a separate file in the repository)<br />
    
Files:<br /><br />
&nbsp;&nbsp;&nbsp;Bam or sam file(s) that you wish to get the average coverage or score for (output: scaffold start end score)<br />
&nbsp;&nbsp;&nbsp;Genome index file (produced by samtools faidx)<br />

<!-- usage -->
## Usage

1) Produce a file with average coverage in windows:<br /><br />
&nbsp;&nbsp;&nbsp;python BamReaderandHistogramv1.0.py -file file.bam -fai Genome.fasta.fai -win 10000 -step 5000 -out cov > Coverage.circos.txt<br /><br />
&nbsp;&nbsp;&nbsp;help (and further explanations): python BamReaderandHistogramv1.0.py -h
    
<!-- license -->
## License 

Distributed under the MIT License.
