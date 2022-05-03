import pandas as pd
import requests
from bs4 import BeautifulSoup

list_of_member_details = []
for i in range(1, 38):  # to get all pages from 1 to 37 so range will go from 1 to 38 that will be 37
    data = {
        'PhysicianSearch$FTR01$PagingID': i
    }
    URL = "https://www.stfrancismedicalcenter.com/find-a-provider/"
    response = requests.post(URL, data=data)
    sf_web_page = response.text

    soup = BeautifulSoup(sf_web_page, "html.parser")
    # print(soup.prettify())

    for a in soup.find_all("a", href=True)[66:78]:
        mem_url = f"https://www.stfrancismedicalcenter.com{a['href']}"
        response = requests.get(mem_url)
        mem_web_page = response.text

        soup = BeautifulSoup(mem_web_page, "html.parser")
        for prac in soup.findAll("div", attrs={'class': 'physician-locations'}):
            for div in soup.findAll("div", attrs={'class': 'two-thirds'}):
                mem_name = soup.find("title").getText()
                mem_speciality = div.getText().strip()
                full_add = prac.getText().split("Locations")[1].split("\n\n\n")[1].split("Get Directions")[0]
                full_addre = full_add.strip().split("\n\t\t\t\t")

                phone_no = full_add.split()[-1]
                zip = full_add.split()[-2]
                practice = \
                    prac.getText().split("Locations")[1].split("\n\n\n")[1].split("Get Directions")[0].split("\n")[
                        0]
                state = \
                    prac.getText().split("Locations")[1].split("\n\n\n")[1].split("Get Directions")[0].split("\n")[
                        1].split()[-2]
                mem_add = \
                    prac.getText().split("Locations")[1].split("\n\n\n")[1].split("Get Directions")[0].split("\n")[
                        1]
                try:
                    city = \
                        prac.getText().split("Locations")[1].split("\n\n\n")[1].split("Get Directions")[0].split(
                            "\n")[
                            1].split()[-3].split(",")[0]
                except IndexError:
                    city = prac.getText()

            for span in soup.findAll("span", attrs={'class': 'two-thirds'})[1::20]:
                lst_lang = ['Farsi', 'Spanish, English', 'English', 'Male', 'Arabic', 'Female',
                            'Nigerian, Spanish', 'English, Persian', 'Spanish', 'Hindi, Gujrati',
                            'Cantonese, Spanish', 'English, Nippongo, Tagalog', 'Male',
                            'Tagalog', 'French, Arabic', 'Korean, Spanish, Tagalog', 'Spanish, Korean',
                            'Romanian', 'Spanish, Hindu, English', 'Tagalog, Hispanic', 'Armenian, English',
                            'Spanish, Filipino (Tagalog), English, Filipino', 'English, Persian',
                            'English, Nippongo, Tagalog', 'English, Spanish', 'Punjabi, English',
                            'English, Spanish, Hindi, Punjabi', 'Korean, English', 'Mandarin, Taiwanese, English',
                            'Gujarati', 'Spanish, Tagalog', 'Vietnamese',
                            'English, Hindi, Gujrati', 'English, Farsi', 'English, Arabic, French',
                            'Arabic, French', 'Punjabi', 'English, Polish', 'English, Cantonese',
                            'Korean, Portuguese, English, Portugese', 'English, Vietnamese', 'Hindi, Punjabi',
                            'Farsi, English',
                            'English, Japanese', 'Hindi, English, Gujarati', 'English, German',
                            'Spanish, Farsi, English', 'Urdu', 'Romanian', 'Armenian, English',
                            'English, Nippongo, Tagalog', 'English, Burmese', 'Chinese']
                if full_addre[0]:
                    full_address = " ".join(full_addre[0].split("\n"))

                    add_speciality = span.getText().strip()
                    if add_speciality not in lst_lang:
                        j = {
                            "\nFull_Name": mem_name,
                            "Speciality": mem_speciality,
                            "Add_Speciality": add_speciality,
                            "Full_Address": full_address,
                            "Practice": practice,
                            "Address": mem_add,
                            "City": city,
                            "State": state,
                            "Zip": zip,
                            "Phone": phone_no,
                            "URL": mem_url,
                            '\n': "\n"

                        }

                        list_of_member_details.append(j)
                    elif add_speciality in lst_lang:
                        j = {
                            "\nFull_Name": mem_name,
                            "Speciality": mem_speciality,
                            "Add_Speciality": "      ",
                            "Full_Address": full_address,
                            "Practice": practice,
                            "Address": mem_add,
                            "City": city,
                            "State": state,
                            "Zip": zip,
                            "Phone": phone_no,
                            "URL": mem_url,
                            '\n': "\n"
                        }

                        list_of_member_details.append(j)
    print(list_of_member_details)
    print(pd.DataFrame(list_of_member_details))
    pd.DataFrame(list_of_member_details).to_csv("output_doctors_details.csv", header=True, line_terminator="\t",
                                                mode="w", index_label=None, index=False)
