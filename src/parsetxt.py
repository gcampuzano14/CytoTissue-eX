import os
import re
import csv
import json
from datetime import datetime
import appmodules.open_diff_os as open_diff_os

# force_encoding('iso8859-1').encode('utf-8')


def cleaner(case_dict, choice_site):
    clean_case_dict = {}
    for e in case_dict:
        #print e
        clean_case_dict[e]=[]
        for c in case_dict[e]:

            case_in = c
            case_in['diagnosis'] = re.sub(r'\n', ' ', case_in['diagnosis'].strip())
            if choice_site == 'UM':
                case_in['diagnosis'] = re.sub(r'Selection\sCriteria:\sAccession\sDate:\s\d+/\d+/\d{4}\s\d+:\d+\sTo\s\d+/\d+/\d{4}\s\d+:\d+\sTarget\sSpec\.\s'
                                              'Class:.+?Related\sSpec\.\sClass:\s.+?Rel\.\sDays\sFrom/To\sTarg\.:\s\d+\sTo\s\d+\sCytology/Surgical\s'
                                              'Correlation\s.+?\sDate/Time\sPrinted:\s\d+/\d+/\d{4}\s\d+:\d+', ' ', case_in['diagnosis'])

                case_in['diagnosis'] = re.sub(r'University\sof\sMiami:\sMiller\sSchool\sof\sMedicine\sPage\s\d+\sof\s\d+', ' ', case_in['diagnosis'])
            elif choice_site == 'JHS':
                case_in['diagnosis'] = re.sub(r'Cytology\/Surgical\sCorrelation\s.+?\sDate\/Time\sPrinted:\s\d+/\d+/\d{4}\s\d+:\d+\sSelection\sCriteria:\s'
                                              'Accession\sDate:\s\d+/\d+/\d{4}\s\d+:\d+\sTo\s\d+/\d+/\d{4}\s\d+:\d+\sTarget\sSpec\.\sClass:\s.+?\sRelated\s'
                                              'Spec\.\sClass:\s.+?\sRel\.\sDays\sFrom\/To\sTarg\.:\s\d+\sTo\s\d+', ' ', case_in['diagnosis'])
                case_in['diagnosis'] = re.sub(r'Jackson\sMemorial\sHospital\sPage\s\d+\sof\s\d+', ' ', case_in['diagnosis'])
            clean_case_dict[e].append(case_in)
    return clean_case_dict


def encode_decode(my_str):
    unicode_str = my_str.decode('latin')
    dx = unicode_str.encode("utf8")
    return dx


def cyto_tissue_extract(params):

    now = "".join([str(datetime.now())[0:4],str(datetime.now())[5:7],
         str(datetime.now())[8:10],str(datetime.now())[11:13],
         str(datetime.now())[14:16],str(datetime.now())[17:19],
         str(datetime.now())[20:len(str(datetime.now()))-1]])

    openfile = params['openfile']
    out_dir = '_'.join([params['out_dir'], now])
    choice_site = params['choice_site']

    with open(openfile, "r") as txt_body:
        txt_body = txt_body.read()

    os.mkdir(out_dir)
    print txt_body[:1000]
    if choice_site == 'UM':
        allcases = re.findall(r'([A-Z]+(?:-\w+)*,\s[A-Z\s]+)\nSpecimen\sNumber\sAccession\sDate\sTarget\sor\sRelated\sFinal\sDiagnosis\n'
                              'DOB:\s\d+\/\d+\/\d{4}\sMRN:\s\w+\n([A-Z]{1,2}\d{2}-\d+\s\d+\/\d+\/\d{4}\s\d+:\d{2}\s'
                              '(Target|Related).+?\n)(?=[A-Z]+(?:-\w+)*,\s[A-Z\s]+\nSpecimen\sNumber\sAccession\sDate\sTarget\sor\s'
                              'Related\sFinal\sDiagnosis\nDOB:\s\d+\/\d+\/\d{4}\sMRN:\s\w+\n)', txt_body, re.S)
    elif choice_site == 'JHS':
        allcases = re.findall(r'([A-Z]+(?:-\w+)*,[A-Z\s]+)\nSpecimen\sNumber\sAccession\sDate\sTarget\sor\sRelated\sFinal\sDiagnosis\n([A-Z]{1,2}\d{2}-\d+\s'
                              '\d+\/\d+\/\d{4}\s\d+:\d{2}\s(Target|Related).+?\n)(?=[A-Z]+(?:-\w+)*,[A-Z\s]+\nSpecimen\sNumber\sAccession\sDate\sTarget\sor\s'
                              'Related\sFinal\sDiagnosis\n)', txt_body, re.S)

    case_dict = {}
    for case in allcases:

        all_subcases  = re.findall(r'([A-Z]{1,2}\d{2}-\d+)\s(\d+\/\d+\/\d{4})\s\d+:\d{2}\s(Target|Related)(.*?)\n'
                                   '(?=$|[A-Z]{1,2}\d{2}-\d+\s\d+\/\d+\/\d{4}\s\d+:\d{2}\s(?:Target|Related).*\n)', case[1], re.S)

        all_subcases = [{'accession_number':x[0], 'accession_date':x[1], 'case_type':x[2], 'diagnosis':encode_decode(x[3])} for x in all_subcases]
        if case[0] in case_dict:
            for c in all_subcases:
                case_dict[case[0]].append(c)
        else:
            case_dict[case[0]] = all_subcases


    case_dict = cleaner(case_dict, choice_site)

    with open(os.path.join(out_dir, 'out_multiple_row.csv'), 'wb') as out_file:
        fileWriter = csv.writer(out_file)
        row = ['NAME', 'ACCESSION_DATE', 'TYPE', 'ACCESSION_NUMBER', 'DIAGNOSIS', 'EVENT_FILTER_1','EVENT_FILTER_2']
        fileWriter.writerow(row)
        count = 0
        for e in case_dict:
            for c in case_dict[e]:

                row = [e]+[c[x].strip() for x in c] + [''.join(["=IF(ISERROR(SEARCH(F$1,$E", str(count+2), ",1)),0,1)"]), ''.join(["=IF(ISERROR(SEARCH(G$1,$E", str(count+2), ",1)),0,1)"])]
                fileWriter.writerow(row)
                count += 1

    with open(os.path.join(out_dir,'out_single_row.csv'), 'wb') as out_file:
        fileWriter = csv.writer(out_file)
        for e in case_dict:
            row_blob = [e]
            for c in case_dict[e]:
                 row_blob = row_blob + [c[x].strip() for x in c]

            fileWriter.writerow(row_blob)

    with open(os.path.join(out_dir, 'out_data_elastic.json'), 'wb') as out_file:
        json_str = json.dumps(case_dict)
        out_file.write(json_str)

    open_diff_os.openFolder(out_dir)

if __name__ == '__main__':
    with open('um cases.txt', 'r') as txt_raw:
        txt_body = txt_raw.read()
    cyto_tissue_extract(txt_body,'UM')
