# CVSS v2 Calculator

Computes CVSS v2 score based on the input CVSS v2 vector.

[Read more about CVSS v2 (PDF)](https://www.first.org/cvss/cvss-v2-guide.pdf).

## Examples

```
$ python cvssv2.py --help
usage: cvssv2.py [-h] [-v VECTOR] [-b] [-i]

optional arguments:
  -h, --help            show this help message and exit
  -v VECTOR, --vector VECTOR
                        CVSS v2 vector provided as a single string. See
                        https://www.first.org/cvss/cvss-v2-guide.pdf for the
                        vector format.
  -b, --bare-output     Prints only the resulting scores (number) or "nan" to
                        the output.
  -i, --interactive     The program will ask for missing CVSS v2 vector items
                        interactively.
```


Input can be provided on command line:

```
$ python cvssv2.py -v AV:N/AC:L/Au:N/C:N/I:N/A:C/E:F/RL:OF/RC:C/CDP:N/TD:N/CR:M/IR:M/AR:H
CVSS Base Score:           7.8
 Impact Subscore:          6.9
 Exploitability Subscore: 10.0
CVSS Temporal Score:       6.4
CVSS Environmental Score:  0.0
```

The -b switch suppresses all output except for the three CVSS scores (Base, Temporal, Environmental). In this mode, the output always consists of 3 lines. Values that cannot be calculated contain "nan" (not a number).
```
$ python cvssv2.py -v AV:N/AC:L/Au:N/C:N/I:N/A:C/E:F/RL:OF/RC:C/CDP:N/TD:N/CR:M/IR:M -b
7.8
6.4
nan
```

In interactive mode, the program asks for values that are missing or invalid:
```
$ python cvssv2.py -v "AV:A/AC:M/Au:S/C:P/I:P/A:N/E:U/RL:OF/RC:C/CR:L/TD:L/IR:M/CDP:L/AR:MX/AR:Mx" -i
Environmental metrics errors: (The environmental group is optional.)
The metric value 'AR:Mx' is invalid (valid values are ['L', 'M', 'H', 'ND']).

Enter the value for the 'AR' metric: M
CVSS Base Score:           3.8
 Impact Subscore:          4.9
 Exploitability Subscore:  4.4
CVSS Temporal Score:       2.8
CVSS Environmental Score:  0.8
```

Non-interactive mode prints error messages and calculates all values that can be calculated. The Environmental Score is missing here because it cannot be calculated due to an invalid input value.
```
$ python cvssv2.py -v "AV:A/AC:M/Au:S/C:P/I:P/A:N/E:U/RL:OF/RC:C/CR:L/TD:L/IR:M/CDP:L/AR:MX/AR:Mx"
The metric value 'AR:Mx' is invalid (valid values are ['L', 'M', 'H', 'ND']).

CVSS Base Score:           3.8
 Impact Subscore:          4.9
 Exploitability Subscore:  4.4
CVSS Temporal Score:       2.8

```

