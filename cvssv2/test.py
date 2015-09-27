#!/usr/bin/env python

#   Tests of the CVSS v2 calculator.
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


import unittest
import os
import cvssv2
 
class Cvssv2Unittest(unittest.TestCase):


	def test01(self):
		"""The 3.3.1 CVE-2002-0392 example from https://www.first.org/cvss/cvss-v2-guide.pdf"""
		cvss_vector = "AV:N/AC:L/Au:N/C:N/I:N/A:C/E:F/RL:OF/RC:C/CDP:H/TD:H/CR:M/IR:M/AR:H"
		cvss_vector_values, error_messages = cvssv2.parse_cvssv2_vector(cvss_vector)
		BaseScore, Impact, Exploitability = cvssv2.compute_base(cvss_vector_values)
		TemporalScore = cvssv2.compute_temp(cvss_vector_values)
		EnvironmentalScore = cvssv2.compute_env(cvss_vector_values)
		self.assertEqual(BaseScore, 7.8)
		self.assertEqual(Impact, 6.9)
		self.assertEqual(Exploitability, 10.0)
		self.assertEqual(TemporalScore, 6.4)
		self.assertEqual(EnvironmentalScore, 9.2)

	def test02(self):
		"""The 3.3.2 CVE-2003-0818 example from https://www.first.org/cvss/cvss-v2-guide.pdf"""
		cvss_vector = "AV:N/AC:L/Au:N/C:C/I:C/A:C"
		cvss_vector_values, error_messages = cvssv2.parse_cvssv2_vector(cvss_vector)
		BaseScore, Impact, Exploitability = cvssv2.compute_base(cvss_vector_values)
		TemporalScore = cvssv2.compute_temp(cvss_vector_values)
		EnvironmentalScore = cvssv2.compute_env(cvss_vector_values)
		self.assertEqual(BaseScore, 10.0)
		self.assertEqual(Impact, 10.0)
		self.assertEqual(Exploitability, 10.0)

	def test03(self):
		"""The 3.3.3 CVE-2003-0062 example from https://www.first.org/cvss/cvss-v2-guide.pdf"""
		cvss_vector = "AV:L/AC:H/Au:N/C:C/I:C/A:C"
		cvss_vector_values, error_messages = cvssv2.parse_cvssv2_vector(cvss_vector)
		BaseScore, Impact, Exploitability = cvssv2.compute_base(cvss_vector_values)
		TemporalScore = cvssv2.compute_temp(cvss_vector_values)
		EnvironmentalScore = cvssv2.compute_env(cvss_vector_values)
		self.assertEqual(BaseScore, 6.2)
		self.assertEqual(Impact, 10.0)
		self.assertEqual(Exploitability, 1.9)


	def test04(self):
		cvss_vector = "AV:L/AC:L/Au:N/C:N/I:P/A:C/E:U/RL:W/RC:UR/CDP:L/TD:M/CR:L/IR:H/AR:L"
		cvss_vector_values, error_messages = cvssv2.parse_cvssv2_vector(cvss_vector)
		BaseScore, Impact, Exploitability = cvssv2.compute_base(cvss_vector_values)
		TemporalScore = cvssv2.compute_temp(cvss_vector_values)
		EnvironmentalScore = cvssv2.compute_env(cvss_vector_values)
		self.assertEqual(BaseScore, 5.6)
		self.assertEqual(Impact, 7.8)
		self.assertEqual(Exploitability, 3.9)
		self.assertEqual(TemporalScore, 4.3)
		self.assertEqual(EnvironmentalScore, 3.1)


	def test05(self):
		cvss_vector = "AV:A/AC:L/Au:S/C:P/I:C/A:N/E:POC/RL:U/RC:UC/CDP:H/TD:ND/CR:H/IR:L/AR:M"
		cvss_vector_values, error_messages = cvssv2.parse_cvssv2_vector(cvss_vector)
		BaseScore, Impact, Exploitability = cvssv2.compute_base(cvss_vector_values)
		TemporalScore = cvssv2.compute_temp(cvss_vector_values)
		EnvironmentalScore = cvssv2.compute_env(cvss_vector_values)
		self.assertEqual(BaseScore, 6.2)
		self.assertEqual(Impact, 7.8)
		self.assertEqual(Exploitability, 5.1)
		self.assertEqual(TemporalScore, 5)
		self.assertEqual(EnvironmentalScore, 7.0) # value differs from https://nvd.nist.gov/cvss.cfm?calculator&version=2 by 0.1, probably because of different floating point arithmetics


	def test06(self):
		cvss_vector = "AV:A/AC:M/Au:M/C:P/I:P/A:C/E:U/RL:TF/RC:UR/CDP:LM/TD:L/CR:M/IR:M/AR:L"
		cvss_vector_values, error_messages = cvssv2.parse_cvssv2_vector(cvss_vector)
		BaseScore, Impact, Exploitability = cvssv2.compute_base(cvss_vector_values)
		TemporalScore = cvssv2.compute_temp(cvss_vector_values)
		EnvironmentalScore = cvssv2.compute_env(cvss_vector_values)
		self.assertEqual(BaseScore, 5.9)
		self.assertEqual(Impact, 8.5)
		self.assertEqual(Exploitability, 3.5)
		self.assertEqual(TemporalScore, 4.3)
		self.assertEqual(EnvironmentalScore, 1.3)



# runs the test suite if run as a standalone program
if __name__ == '__main__':
    unittest.main()

