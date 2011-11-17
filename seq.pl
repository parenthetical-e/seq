#! usr/bin/perl

# This script takes either a single .txt file or 
# raw excel exported eprime (.edata) and returns 
use strict;

# GLOBALS (subs defined at end)
# ============================
	# A. CONFIGURE this script
	# USER SETTINGS
	# ---------------------
	%seqData				= undef;
	@colNames 			= qw/stim.ACC,stim.RESP,stim.RT/;
	@condNames 			= qw/1.bmp, 2.bmp, 3.bmp/;
	$condColName		= "";
	$dBUG						= 0;							# control debugging
	$vERB						= 0;							# print some useful info to the console
	# ---------------------
	# END USER SETTINGS


	# B. OTHERs
	# ---------
	@files					= ();							# files to process
	@allCols				= ();
	# ---------
# ============================

# THE FLOW:
# 	A. process invocation args
# 	B. parse() (parses ans does the counts)
# 	C. write the results to file

if ($dBUG) {
	open STDERR, ">>seq.log" or die "Could not create the log file: $!\n";
}

# A: PROCESS OPTIONS
# 		Ignore POSIX, allow only short option flags ... 
# 		-r:  recusivly process all .txt files in the PWD.
# 		-h:  help prints a useage guide to STDOUT
# are there flags?

{
	my $tmpfiles = undef;
	
	for(@ARGV) {
		if($_ =~ /^-h/) {
			print "Help invoked.  This script takes a given file (or all the .txt files in the current directory if '-r' is used) and extracts first and second order sequence data in the specified columns.  See the USER GLOBALS (in the script file) for configuration details.\n\n  The first N arguments should be flags (either -h or -r) followed by a filename (or not if -r).\nNOTE: this script expects individual subjects data.  If you are using a merged .edata file it will be treated holistically, ignoring subject specifiers.  This is probably not what you want.\n";
		}
		# -r loop may run a futile cycle, 
		# but this should not matter;
		# help leads to death.
		elsif ($_ =~ /^-r/) {
			# get all the txt files in the PWD
			$tmpfiles = `ls -1 *.txt`;
			if ($tmpfiles =~ /No such file or directory$/) {
				die "-r: the specified directory contained no .txt files.\n";
			} else{
				@files = split(/\n/,$tmpfiles);
			}
		} 
	}
}
	


for my $file (@files) {
	# slurp $file	
	{ 
		local $/ = undef; 
		local *FILE; 
		open FILE, "<$file"; 
		$f = <FILE>; 
		close FILE; 
	}
	
	# FILE PREPROCESSING
	my @rows = split(/\t/,$f); 
	chomp @rows;
	
	# drop the first line 
	# and store the header
	shift @rows;
	my $header = shift @rows;
	
	# find the location 
	# (index) of @colNames
	# in @allCols
	my @allCols = split(/\t/,$header);
	for (@allCols) {
		@colLocations = push(@colLocations, grep(/$_/,@colNames));		
	}
	@condLocation = grep(/$condColName/,@colNames);
	if (@condLocation > 1) {die "Redundant naming with $condColName.\n";}
	
	if (dBUG) {
		print STDERR "Preprocessing is complete.\n";
		print STDERR "Header: @allCols\n";
		print STDERR "Good col locations: @colLocations. \n";
		print STDERR "There are $rows remaining rows in $file. \n";
	}
	if (vERB) {
		print ">>> Preprocessing is complete.";
		print ">>> Starting to gather sequence data on $file.\n";
	}
	# END PREPROCESSING
	
	# GATHER THE SEQ DATA -- 
	# &counT affects globals!
	my $reinit_count = 1;
 	&count($row) for $row (@rows);
	
	# write out the seq data,
	# then clear %seqData
	@seqCondKeys = sort keys %seqData;
	for(@seqCondKeys) {
		open STDOUT, "<$_.${file}.dat" or die "$!\n";
		print "@colNames\n";
		print "$seqData{ $_ }";
		close, STDOUT;
	}
	reset %seqData;
}

# ::SUBS::
# count: actually does work tabulating the data by cond.
sub count {
	# $_ is the arg to count()
	my @rowArray = split $_[0];
	chomp @rowArray;
	
	if ($reinit_count) {
		# this is probably the wrong thing to do...
		# if this is run in for loop what happens?
		my @twoback = undef;
		my @oneback = undef;
		$reinit_count = 0;
	}
	
	my $curr = $rowArray[$condLocation];
	
	$seqData{ $curr } = {
	 $seqData{ $curr } . "@rowArray[@colLocations]" . "\n";
	}
	
	$seqData{ $oneback.$curr } = {
	 $seqData{ $oneback.$curr } . "@rowArray[@colLocations]" . "\n";
	}
	
	$seqData { $twoback.$oneback.$curr } = {
	 $seqData { $twoback.$oneback.$curr } . "@rowArray[@colLocations]" . "\n";
	}
	
	# shift one and twoback over, 
	# in prep for next iteration.
	$twoback = $oneback;
	$oneback = $curr;
}
