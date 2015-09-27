#!/usr/bin/env python

#   CVSS v2 calculator. Calculates score from input vector.
#   Copyright (C) 2015  Jakub Svoboda
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Assignment: "Write a CVSSv2 parser.  Something were you  can provide the CVSSv2 metrics and have it calculate the score.  You should be able to provide the metrics as an argument, or interactively enter them." [sic]


# CVSSv2 vectors may look like this:
# AV:A/AC:H/Au:S/C:P/I:P/A:C/E:U/RL:TF/RC:ND/CDP:L/TD:L/CR:ND/IR:ND/AR:ND
# AV:A/AC:M/Au:S/C:P/I:P/A:N


# the number of metrics for the individual groups in the CVSSv2 vector
temp_num_of_metrics = 3
env_num_of_metrics = 5



def parse_cvssv2_vector(cvss_vect_string):
	"""Parses the input string (CVSSv2 vector) into a metric:value dictionary. Returns the dictionary and a multiline string with messages about encountered errors."""

	cvss_vector_values = {} # dict of string:string
	error_messages = ""

	if cvss_vect_string == None:
		return cvss_vector_values, error_messages

	metrics_list = cvss_vect_string.split("/")
	for metric in metrics_list:
		try:
			metric_name, metric_value = metric.split(":", 1)
			cvss_vector_values[metric_name] = metric_value
		except ValueError:
			error_message = "The metric string \"" + metric + "\" cannot be parsed."
			error_messages += error_message + "\n";

	return cvss_vector_values, error_messages  


def validate_metrics(cvss_values, base_valid_metrics):
	"""Validates the provided metrics values (cvss_values dictionary) based on the provided possible legal metrics values (base_valid_metrics dictionary). Returns a list of missing metrics, a list of metrics with invalid/missing values, and a multiline string with messages about encountered errors."""

	missing_list = list() # missing metrics
	error_list = list() # metrics that are either missing or have an invalid value
	error_messages = ""
	for metric in base_valid_metrics:
		if metric in cvss_values:
			if cvss_values[metric] not in base_valid_metrics[metric]:
				error_message = "The metric value \'" + metric + ":" +  cvss_values[metric] + "\' is invalid (valid values are " +  str(base_valid_metrics[metric]) + ")."
				error_messages += error_message + "\n";
				error_list.append(metric)
		else:
			error_message = "The metric \'" + metric + "\':" + str(base_valid_metrics[metric]) + " was not found."
			error_messages += error_message + "\n";
			missing_list.append(metric)
			error_list.append(metric)

	return missing_list, error_list, error_messages


def validate_metrics_base(cvss_values):
	"""Validates the base metrics group. Returns a list of missing metrics, a list of metrics with invalid/missing values, and a multiline string with messages about encountered errors."""

	# Base AV:[L,A,N]/AC:[H,M,L]/Au:[M,S,N]/C:[N,P,C]/I:[N,P,C]/A:[N,P,C]
	base_valid_metrics = {
		"AV":["L","A","N"],  
		"AC":["H","M","L"],
		"Au":["M","S","N"],  
		"C":["N","P","C"],   
		"I":["N","P","C"],   
		"A":["N","P","C"]
	}
	return validate_metrics(cvss_values, base_valid_metrics)


def validate_metrics_temp(cvss_values):
	"""Validates the temporal metrics group. Returns a list of missing metrics, a list of metrics with invalid/missing values, and a multiline string with messages about encountered errors."""

	# Temporal E:[U,POC,F,H,ND]/RL:[OF,TF,W,U,ND]/RC:[UC,UR,C,ND]
	temp_valid_metrics = {
		"E":["U","POC","F","H","ND"],
		"RL":["OF","TF","W","U","ND"],
		"RC":["UC","UR","C","ND"]
	}
	return validate_metrics(cvss_values, temp_valid_metrics)


def validate_metrics_env(cvss_values):
	"""Validates the environmental metrics group. Returns a list of missing metrics, a list of metrics with invalid/missing values, and a multiline string with messages about encountered errors."""

	# Environmental CDP:[N,L,LM,MH,H,ND]/TD:[N,L,M,H,ND]/CR:[L,M,H,ND]/IR:[L,M,H,ND]/AR:[L,M,H,ND]
	env_valid_metrics = {
		"CDP":["N","L","LM","MH","H","ND"],
		"TD":["N","L","M","H","ND"],
		"CR":["L","M","H","ND"],
		"IR":["L","M","H","ND"],
		"AR":["L","M","H","ND"]
	}
	return validate_metrics(cvss_values, env_valid_metrics)

def validate_metrics_all_print_errors(cvss_values, print_errors = True):
	"""Validates all metrics. Prints error messages about encountered errors. Returns information indicating which metrics groups are not fully populated with valid values. The cvss_values parameter is a dictionary of the metric:value pairs from the CVSSv2 vector."""

	missing_list_base, error_list_base, error_messages_base = validate_metrics_base(cvss_values)

	missing_list_temp, error_list_temp, error_messages_temp = validate_metrics_temp(cvss_values)

	missing_list_env, error_list_env, error_messages_env = validate_metrics_env(cvss_values)

	# doesn't print errors for metrics groups that are entirely missing (because they are optional)
	if print_errors:
		if len(error_messages_base) > 0: print error_messages_base
		if (len(missing_list_temp) != temp_num_of_metrics) and (len(error_messages_temp) > 0): print error_messages_temp
		if (len(missing_list_env) != env_num_of_metrics) and (len(error_messages_env) > 0): print error_messages_env
		# prints error if the entire temp group is missing while the env group is specified
		if (len(missing_list_temp) == temp_num_of_metrics) and (len(missing_list_env) != env_num_of_metrics): print "Temporal metrics missing but environmental metrics are specified. Temporal metrics are required for environmental metrics computation."

	base_incomplete = len(error_list_base) > 0
	temp_incomplete = len(error_list_temp) > 0
	env_incomplete = len(error_list_env) > 0

	return base_incomplete, temp_incomplete, env_incomplete
	

def compute_base(cvss_values, validate_input_bool = True, AdjustedImpact = None):
	"""Computes the base group of metrics from the vector. The cvss_values parameter is a dictionary of the metric:value pairs from the CVSSv2 vector."""

	if validate_input_bool:
		missing, errors, error_messages = validate_metrics_base(cvss_values)
		if len(errors)>0:
			return float("NaN"), float("NaN"), float("NaN")

	# Base AV:[L,A,N]/AC:[H,M,L]/Au:[M,S,N]/C:[N,P,C]/I:[N,P,C]/A:[N,P,C]

	# Sources of the equations:
	# - https://nvd.nist.gov/CVSS-v2-Calculator
	# - https://www.first.org/cvss/cvss-v2-guide.pdf

	# AccessComplexity = case AccessComplexity of
	#                         high:   0.35
	#                         medium: 0.61
	#                         low:    0.71
	AccessComplexity = {
	"H": 0.35,
	"M": 0.61,
	"L": 0.71
	}.get(cvss_values["AC"], float("NaN"))

	#  
	# Authentication   = case Authentication of
	#                         Requires no authentication:                    0.704
	#                         Requires single instance of authentication:    0.56
	#                         Requires multiple instances of authentication: 0.45
	Authentication = {
	"M": 0.45,
	"S": 0.56,
	"N": 0.704 
	}.get(cvss_values["Au"], float("NaN"))

	#  
	# AccessVector     = case AccessVector of
	#                         Requires local access:    0.395
	#                         Local Network accessible: 0.646
	#                         Network accessible:       1
	AccessVector = {
	"L": 0.395,
	"A": 0.646,
	"N": 1 
	}.get(cvss_values["AV"], float("NaN"))

	#  
	# ConfImpact       = case ConfidentialityImpact of
	#                         none:             0
	#                         partial:          0.275
	#                         complete:         0.660
	ConfImpact = {
	"N": 0,
	"P": 0.275,
	"C": 0.660 
	}.get(cvss_values["C"], float("NaN"))

	#  
	# IntegImpact      = case IntegrityImpact of
	#                         none:             0
	#                         partial:          0.275
	#                         complete:         0.660
	IntegImpact = {
	"N": 0,
	"P": 0.275,
	"C": 0.660 
	}.get(cvss_values["I"], float("NaN"))

	#  
	# AvailImpact      = case AvailabilityImpact of
	#                         none:             0
	#                         partial:          0.275
	#                         complete:         0.660
	#  
	AvailImpact = {
	"N": 0,
	"P": 0.275,
	"C": 0.660 
	}.get(cvss_values["A"], float("NaN"))


	# Impact = 10.41 * (1 - (1 - ConfImpact) * (1 - IntegImpact) * (1 - AvailImpact))
	Impact = 10.41 * (1 - (1 - ConfImpact) * (1 - IntegImpact) * (1 - AvailImpact))
	
	if AdjustedImpact != None:
		Impact = AdjustedImpact

	# Exploitability = 20 * AccessComplexity * Authentication * AccessVector
	Exploitability = 20 * AccessComplexity * Authentication * AccessVector

	# f(Impact) = 0 if Impact=0; 1.176 otherwise
	f_Impact = 1.176
	if Impact == 0:
		f_Impact = 0

 
	# BaseScore = round_to_1_decimal( (.6*Impact +.4*Exploitability-1.5)*f(Impact) )
	BaseScore = round ( (0.6 * Impact + 0.4 * Exploitability - 1.5) * f_Impact, 1)
	Impact =  round ( Impact, 1)
	Exploitability =  round ( Exploitability, 1)


	return BaseScore, Impact, Exploitability


def compute_temp(cvss_values, BaseScore_in = None, validate_input_bool = True):
	"""Computes the temporal group of metrics from the vector. The cvss_values parameter is a dictionary of the metric:value pairs from the CVSSv2 vector."""

	if validate_input_bool:
		missing, errors, error_messages = validate_metrics_temp(cvss_values)
		if len(errors)>0:
			return float("NaN")

	BaseScore = BaseScore_in

	if BaseScore_in == None:
		BaseScore, imp, exp = compute_base(cvss_values, validate_input_bool)

	# Temporal E:[U,POC,F,H,ND]/RL:[OF,TF,W,U,ND]/RC:[UC,UR,C,ND]

	# Sources of the equations:
	# - https://nvd.nist.gov/CVSS-v2-Calculator
	# - https://www.first.org/cvss/cvss-v2-guide.pdf



	#  
	# Exploitability   = case Exploitability of
	#                         unproven:             0.85
	#                         proof-of-concept:     0.9
	#                         functional:           0.95
	#                         high:                 1.00
	#                         not defined           1.00
	Exploitability = {
	"U": 0.85,
	"POC": 0.9,
	"F": 0.95,
	"H": 1.00,
	"ND": 1.00
	}.get(cvss_values["E"], float("NaN"))

	#                         
	# RemediationLevel = case RemediationLevel of
	#                         official-fix:         0.87
	#                         temporary-fix:        0.90
	#                         workaround:           0.95
	#                         unavailable:          1.00
	#                         not defined           1.00
	RemediationLevel = {
	"OF": 0.87,
	"TF": 0.90,
	"W": 0.95,
	"U": 1.00,
	"ND": 1.00 
	}.get(cvss_values["RL"], float("NaN"))
	# Temporal E:[U,POC,F,H,ND]/RL:[OF,TF,W,U,ND]/RC:[UC,UR,C,ND]

	#  
	# ReportConfidence = case ReportConfidence of
	#                         unconfirmed:          0.90
	#                         uncorroborated:       0.95      
	#                         confirmed:            1.00
	#                         not defined           1.00
	#  
	ReportConfidence = {
	"UC": 0.90,
	"UR": 0.95,
	"C": 1.00,
	"ND":1.00  
	}.get(cvss_values["RC"], float("NaN"))

	# TemporalScore = BaseScore 
	#               * Exploitability 
	#               * RemediationLevel 
	#               * ReportConfidence
	TemporalScore = round ( BaseScore * Exploitability * RemediationLevel * ReportConfidence, 1)

	return TemporalScore



def compute_env(cvss_values, validate_input_bool = True):
	"""Computes the environmental group of metrics from the vector. The cvss_values parameter is a dictionary of the metric:value pairs from the CVSSv2 vector."""

	if validate_input_bool:
		missing, errors, error_messages = validate_metrics_env(cvss_values)
		if len(errors)>0:
			return float("NaN")


	# Environmental CDP:[N,L,LM,MH,H,ND]/TD:[N,L,M,H,ND]/CR:[L,M,H,ND]/IR:[L,M,H,ND]/AR:[L,M,H,ND]

	# Sources of the equations:
	# - https://nvd.nist.gov/CVSS-v2-Calculator
	# - https://www.first.org/cvss/cvss-v2-guide.pdf


	# CollateralDamagePotential = case CollateralDamagePotential of
	#                                  none:            0
	#                                  low:             0.1
	#                                  low-medium:      0.3   
	#                                  medium-high:     0.4
	#                                  high:            0.5      
	#                                  not defined:     0
	CollateralDamagePotential = {
	"N": 0,
	"L": 0.1,
	"LM": 0.3,
	"MH": 0.4,
	"H": 0.5,
	"ND": 0 
	}.get(cvss_values["CDP"], float("NaN"))

	#                                  
	# TargetDistribution        = case TargetDistribution of
	#                                  none:            0
	#                                  low:             0.25
	#                                  medium:          0.75
	#                                  high:            1.00
	#                                  not defined:     1.00
	TargetDistribution = {
	"N": 0,
	"L": 0.25,
	"M": 0.75,
	"H": 1.00,
	"ND": 1.00  
	}.get(cvss_values["TD"], float("NaN"))

	#  
	# ConfReq       = case ConfidentialityImpact of
	#                         Low:              0.5
	#                         Medium:           1
	#                         High:             1.51
	#                         Not defined       1
	ConfReq = {
	"L": 0.5,
	"M": 1,
	"H": 1.51,
	"ND": 1 
	}.get(cvss_values["CR"], float("NaN"))

	#  
	# IntegReq      = case IntegrityImpact of
	#                         Low:              0.5
	#                         Medium:           1
	#                         High:             1.51
	#                         Not defined       1
	IntegReq = {
	"L": 0.5,
	"M": 1,
	"H": 1.51,
	"ND": 1 
	}.get(cvss_values["IR"], float("NaN"))

	#  
	# AvailReq      = case AvailabilityImpact of
	#                         Low:              0.5
	#                         Medium:           1
	#                         High:             1.51
	#                         Not defined       1
	AvailReq = {
	"L": 0.5,
	"M": 1,
	"H": 1.51,
	"ND": 1 
	}.get(cvss_values["AR"], float("NaN"))


	# Base metrics:

	#  
	# ConfImpact       = case ConfidentialityImpact of
	#                         none:             0
	#                         partial:          0.275
	#                         complete:         0.660
	ConfImpact = {
	"N": 0,
	"P": 0.275,
	"C": 0.660 
	}.get(cvss_values["C"], float("NaN"))

	#  
	# IntegImpact      = case IntegrityImpact of
	#                         none:             0
	#                         partial:          0.275
	#                         complete:         0.660
	IntegImpact = {
	"N": 0,
	"P": 0.275,
	"C": 0.660 
	}.get(cvss_values["I"], float("NaN"))

	#  
	# AvailImpact      = case AvailabilityImpact of
	#                         none:             0
	#                         partial:          0.275
	#                         complete:         0.660
	#  
	AvailImpact = {
	"N": 0,
	"P": 0.275,
	"C": 0.660 
	}.get(cvss_values["A"], float("NaN"))


	# back to the Environmental equation:

	#  
	# AdjustedImpact = Min(10, 
	#                      10.41 * (1 - 
	#                                 (1 - ConfImpact * ConfReq) 
	#                               * (1 - IntegImpact * IntegReq) 
	#                               * (1 - AvailImpact * AvailReq)))
	AdjustedImpact = min(10, 10.41 * (1 - (1 - ConfImpact * ConfReq) * (1 - IntegImpact * IntegReq) * (1 - AvailImpact * AvailReq)))

	# AdjustedTemporal = TemporalScore recomputed with the Impact sub-equation 
	#                    replaced with the following AdjustedImpact equation.
	AdjustedBase, imp, exp = compute_base(cvss_values, validate_input_bool, AdjustedImpact)
	AdjustedTemporal = compute_temp(cvss_values, AdjustedBase, validate_input_bool)

	# EnvironmentalScore = (AdjustedTemporal 
	#                         + (10 - AdjustedTemporal) 
	#                         * CollateralDamagePotential) 
	#                      * TargetDistribution
	EnvironmentalScore = round (  (AdjustedTemporal + (10 - AdjustedTemporal) * CollateralDamagePotential) * TargetDistribution, 1)

	return EnvironmentalScore


def interactively_ask_missing(cvss_values):
	"""Interactively asks for missing/wrong values until everything is OK or until the user doesn't want to answer anymore."""

	ask_again = True
	first_run = True

	while ask_again:

		# gather list of errors
		missing_list_base, error_list_base, error_messages_base = validate_metrics_base(cvss_values)
		missing_list_temp, error_list_temp, error_messages_temp = validate_metrics_temp(cvss_values)
		missing_list_env, error_list_env, error_messages_env = validate_metrics_env(cvss_values)
		error_list = error_list_base + error_list_temp + error_list_env

		# print errors
		if len(error_messages_base) > 0:
			print "Base metrics errors:"
			print error_messages_base
		if len(error_messages_temp) > 0:
			print "Temporal metrics errors: (The temporal group is optional.)"
			print error_messages_temp
		if len(error_messages_env) > 0:
			print "Environmental metrics errors: (The environmental group is optional.)"
			print error_messages_env

		# allow cancellation of a repeated input prompt (if there are still unresolved input errors)
		if (len(error_list) > 0) and (not first_run):
			val = raw_input("Do you want to skip the value input and compute what we've got? [Y]")
			# cancel on Enter/Y/y
			if (val == "Y") or (val == "y") or (len(val) == 0):
				ask_again = False
				return

		# ask for the inputs (corrections)
		for metric in error_list:
			val = raw_input("Enter the value for the \'" + metric + "\' metric: ")
			if len(val) > 0:
				cvss_values[metric] = val

		first_run = False

		# do not ask again if everything is resolved
		if len(error_list) == 0:
			ask_again = False
		




def main():
	"""A command line program that calculates CVSS v2 score from a provided vector."""

	# parse arguments
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--vector', help="CVSS v2 vector provided as a single string. See https://www.first.org/cvss/cvss-v2-guide.pdf for the vector format.")
	parser.add_argument('-b', '--bare-output', help="Prints only the resulting scores (number) or \"nan\" to the output.", action='store_true')
	parser.add_argument('-i', '--interactive', help="The program will ask for missing CVSS v2 vector items interactively.", action='store_true')
	args = parser.parse_args()

	if args.bare_output and args.interactive:
		print "The options -b and -i are mutually incompatible."
		return

	# parse the CVSSv2 vector string into a dictionary
	cvss_vector_values, error_messages = parse_cvssv2_vector(args.vector)

	# print parsing errors
	if (not args.bare_output) and (len(error_messages) > 0):
		print error_messages

	# interactively ask for missing values
	if args.interactive:
		interactively_ask_missing(cvss_vector_values) 

	# validate the CVSSv2 vector and detect which groups are incomplete
	base_incomplete, temp_incomplete, env_incomplete = validate_metrics_all_print_errors(cvss_vector_values, (not args.bare_output))

	# compute the scores/numeric values
	BaseScore, Impact, Exploitability = compute_base(cvss_vector_values)
	TemporalScore = compute_temp(cvss_vector_values)
	EnvironmentalScore = compute_env(cvss_vector_values)

	# print results
	if args.bare_output:
		print BaseScore
		print TemporalScore
		print EnvironmentalScore
	else:
		if not base_incomplete:
			print "CVSS Base Score:          {:>4}".format(BaseScore)
			print " Impact Subscore:         {:>4}".format(Impact)
			print " Exploitability Subscore: {:>4}".format(Exploitability)

		if not temp_incomplete:
			print "CVSS Temporal Score:      {:>4}".format(TemporalScore)

		if not env_incomplete:
			print "CVSS Environmental Score: {:>4}".format(EnvironmentalScore)



if __name__ == '__main__':
    main()
