from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import csv
import sys

#functions to submit jobs to each serveice
def submit_job_NetMHCpan(peptide_sequence, peptide_length,HLA_Class):
    #defines the function which inputs into NetMHCpan
    #Peptide Sequence takes a String
    #Peptide Length an Int which must be one of the options on the website
    #HLA-Class must be the exact text of an option on the dropdown menu. Consider just hard coding this to be our targets of interest

    # find the text area to enter peptide sequence the hard coded sequence
    seqelem = driver.find_element_by_name("SEQPASTE")
    seqelem.clear()
    seqelem.send_keys(peptide_sequence)
    seqelem.send_keys(Keys.RETURN)

    # find the sequence length and set it to that value
    lengthelem = driver.find_element_by_name("len")
    lengthelem.send_keys(peptide_length)
    lengthelem.send_keys(Keys.RETURN)

    # find HLA Class element and select the hard coded HLA class
    HLAclasselem = Select(driver.find_element_by_name("slave0"))
    count = 0
    while (count < 12):
        HLAclasselem.select_by_index(count)
        count = count+1
        driver.implicitly_wait(5)

    # click Submit
    submitbutton = driver.find_element_by_xpath("//input[@type = 'submit'][@value = 'Submit']")
    submitbutton.click()
def submit_job_NetMHC(peptide_sequence, peptide_length,HLA_Class):
    # defines the function which inputs into NetMHC
    # Peptide Sequence takes a String
    # Peptide Length an Int which must be one of the options on the website
    # HLA-Class must be the exact text of an option on the dropdown menu. Consider just hard coding this to be our targets of interest
    # find the text area to enter peptide sequence the hard coded sequence
    seqelem = driver.find_element_by_name("SEQPASTE")
    seqelem.clear()
    seqelem.send_keys(peptide_sequence)

    # find the sequence length and set it to that value
    lengthelem = driver.find_element_by_name("len")
    lengthelem.send_keys(peptide_length)

    # find HLA Class element and select the hard coded HLA class
    HLAclasselem = Select(driver.find_element_by_name("slave0"))
    HLAclasselem.select_by_visible_text(HLA_Class)

    # click Submit
    submitbutton = driver.find_element_by_xpath("//input[@type = 'submit'][@value = 'Submit']")
    submitbutton.click()
def submit_job_SYFPEITHI(peptide_sequence, peptide_length,HLA_Class):
    # defines the function which inputs into SYFPEITHI
    # Peptide Sequence takes a String
    # Peptide Length an Int which must be one of the options on the website
    # HLA-Class must be the exact text of an option on the dropdown menu. Consider just hard coding this to be our targets of interest
    # find the text area to enter peptide sequence the hard coded sequence
    seqelem = driver.find_element_by_name("SEQU")
    seqelem.clear()
    seqelem.send_keys(peptide_sequence)
    seqelem.send_keys(Keys.RETURN)

    # find the sequence length and set it to that value
    lengthelem = Select(driver.find_element_by_name("amers"))
    lengthelem.select_by_value(peptide_length)

    # find HLA Class element and select the hard coded HLA class
    HLAclasselem = Select(driver.find_element_by_name("Motif"))
    HLAclasselem.deselect_all()
    HLAclasselem.select_by_visible_text(HLA_Class)
    #HLAclasselem.send_keys(Keys.RETURN)

    # click Submit
    submitbutton = driver.find_element_by_name("DoIT")
    submitbutton.click()
def submit_job_RANKPEP(peptide_sequence, HLA_class_and_length):
    seqelem = driver.find_element_by_name("sequence")
    seqelem.clear()
    seqelem.send_keys(peptide_sequence)
    seqelem.send_keys(Keys.RETURN)

    # find HLA Class element and select the hard coded HLA class
    HLAclasselem = Select(driver.find_element_by_name("matrixi"))
    HLAclasselem.select_by_visible_text(HLA_class_and_length)

    # click Submit
    submitbutton = driver.find_element_by_xpath("//input[@type = 'SUBMIT'][@value = 'Send']")
    submitbutton.click()
#.split("\n", 14)[14]).rsplit("\n", 8)[0];
def inputdata_from_textfile(input_filename):
    #takes inputs from a text file with peptides on each new line and returns a list with each peptide as a string
    with open(input_filename,"r") as file:
        contents = file.read()
        contents_list = list(contents.rsplit("\n"))
        return contents_list
def scrape_data_NetMHCpan():
    #retrieves data from the NetMHCpan results page as a string sans ancillary lines before and after
    re_text = driver.find_element_by_xpath("/html/body/pre").text

    print(re_text)
    return(re_text)
def text_to_list_NetMHCpan(string):
    #takes input string from scrape_data_NetMHCpan and returns it to a list with each entry as a value
    #Note: removes the BindLevel significance marker, not needed for eventual analysis
    #print(string)
    li = list(string.split())
    li.remove('---------------------------------------------------------------------------------------------------------------------------')
    li.remove('BindLevel')
    try:
        li.remove('<=')
        li.remove('WB')
        li.remove('SB')
    except ValueError:
        pass

    return li
def write_csv_NetMHCpan(input_list):
    #inputs list from text_to_list_NetMHCpan and writes to a csv file of choosing
    list_len = (len(input_list))
    # print(list_len)
    with open('writeData.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        count = 0
        while (count<=list_len):
            writer.writerow(input_list[count:(count+13)])
            count = count+13

#opens new firefox window
driver = webdriver.Firefox()

#navigate to NetMHCpan Website and validate
driver.get('http://www.cbs.dtu.dk/services/NetMHCpan/')
assert "NetMHCpan" in driver.title

#submit job to NetMHCpan, wait, then output the data, if throws error adjust wait time
submit_job_NetMHCpan(inputdata_from_textfile("hervk.txt")[0],9, "HLA-A*02:01 (A2)")
driver.implicitly_wait(20)

#create a csv from the data scraped from NetMHCpan
write_csv_NetMHCpan(
    text_to_list_NetMHCpan(
        scrape_data_NetMHCpan()
    )
)
