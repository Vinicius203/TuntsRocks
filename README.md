<h1>TuntsRocks - Tech Challenge</h1>

<h2>Overview</h2>
<p>This repository contains a Python script that interacts with a Google Sheets document containing information about students, including their grades. 
  The script calculates the average grade for each student and determines their academic status based on the calculated average. Possible outcomes include:
  <ul>
    <li>Fail due to Attendance</li>
    <li>Fail due to Low Grades</li>
    <li>Final Exam</li>
    <li>Pass</li>
  </ul>
  The script then updates the Google Sheets document with the student's status. If this status is "Final Exam," it calculates the grade required for a final 
  passing result.</p>

<h2>Requirements</h2>
<p>In order to run the code, you need the following:</p>
<ul>
  <li>Python 3.10.7 or higher </li>
  <li>Google Sheets API Credentials</li>
</ul>
<p>It is necessary to install a few libraries; please run the following commands:</p>
<ul>
  <li>pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib</li>
  <li>pip install pandas</li>
</ul>

<h2>Run the Application</h2>
<p>Since you already have the libraries, do the following:</p>
<ul>
  <li>Navigate to the folder where your file is saved.</li>
  <li>Run the following command in the terminal: python challenge.py</li>
</ul>

<h2>Observation</h2>
<p>Please feel free to modify the spreadsheet and the code. The code assumes that the values for the columns "Situação" and "Nota para Aprovação Final"
  are NOT empty. If you delete these values, also delete the column names in the DataFrame created in the main function. After the first successful run, please place the column
  names again.</p>

<p>Author: [Vinicius Martins Freire](github.com/Vinicius203)</p>
