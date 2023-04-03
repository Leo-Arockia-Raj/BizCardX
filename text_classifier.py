import re


def text_classifier(result):
    """ returns the extracted information after classification using regular expression as company_name,
        card_holder_name, designation, mobile_number, email_address, website_URL, area, city,
        state, pin_code"""
    text_data = []
    extracted_info = {'company_name': "-",
                      'card_holder_name': "-",
                      'designation': "-",
                      'mobile_number': "-",
                      'email_address': "-",
                      'website_URL': "-",
                      'area': "-",
                      'city': "-",
                      'state': "-",
                      'pin_code': "-"
                      }
    company = ['Digitals', 'Insurance', 'Airlines', 'Restaurant', 'Electricals', 'Company', 'Firm', 'Organization']
    designation = ['CEO', 'CFO', 'COO', 'CIO', 'CTO', 'Director', 'Manager', 'Assistant', 'Analyst', 'Engineer',
                   'Developer', 'Designer', 'Consultant', 'Sales', 'Marketing', 'HR', 'Legal', 'Operations',
                   'Administration', 'Finance', 'Executive']
    city = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune",
            "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Visakhapatnam", "Bhopal", "Patna", " Ludhiana", "Agra",
            "Nashik", "Vadodara", "Faridabad", "Madurai", "Varanasi", "Jamshedpur", "Srinagar", "Amritsar",
            "Raipur", "Allahabad", "Coimbatore", "Jodhpur", "Rajkot", "Thiruvananthapuram",
            "Gwalior", "Guwahati", "Chandigarh", "Solapur", "Hubli-Dharwad", "Mysore", "Tiruchirappalli",
            "Bareilly", "Aligarh", "Tiruppur", "Gurgaon", "Moradabad", "Jalandhar", "Bhubaneswar", "Warangal",
            "Mangalore", "Bhiwandi", "Pondicherry", "Dehradun", "Salem", "Asansol", "Nanded-Waghala", "Kolhapur",
            "Ajmer", "Gulbarga", "Jamnagar", "Ujjain", "Loni", "Siliguri", "Jhansi", "Ulhasnagar", "Nellore",
            "Jammu", "Sangli-Miraj & Kupwad", "Belgaum", "Mangaluru", "Ambattur", "Tirunelveli", "Malegaon",
            "Gaya", "Jalgaon", "Udaipur", "Maheshtala", 'Erode']

    states = ["Andhra Pradesh", "Arunachal Pradesh ", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
              "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
              "Maharashtra",
              "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
              "TamilNadu",
              "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
              "Chandigarh", "Dadra and Nagar Haveli", "Daman and Diu", "Lakshadweep",
              "National Capital Territory of Delhi",
              "Puducherry"]
    extras = ['WWW', 'Erode,', 'GLOBAL', 'St ,', 'BORCELLE', 'Family']
    remaining = []
    for text in result:
        text_data.append(text.strip())
        word = text.strip()
        if any(substring.lower() in word.lower() for substring in company):
            extracted_info['company_name'] = word
            print("company_name:", word)
        elif re.fullmatch("^[A-Z][A-Za-z&. ]{1,}[^.com]$", word) and\
                word not in states and word not in city and word not in extras:
            if any(substring.lower() in word.lower() for substring in designation):
                extracted_info['designation'] = word
                print("designation:", word)
            else:
                extracted_info['card_holder_name'] = word
                print("card_holder_name:", word)
        elif re.match("[0-9\- +]{9,13}", word):
            if extracted_info['mobile_number'] != '-':
                word = extracted_info['mobile_number'] + ", " + word
            extracted_info['mobile_number'] = word
            print("mobile_number:", word)
        elif re.match("[A-Za-z_0-9]{1,}[@][A-Za-z0-9]{1,}[.][A-Za-z]{2,3}", word):
            if extracted_info['email_address'] != '-':
                word = extracted_info['email_address'] + ", " + word
            extracted_info['email_address'] = word
            print("email_address:", word)
        elif re.match("^(https://|www).*", word.lower()):
            extracted_info['website_URL'] = word
            print("website_URL:", word)
        elif re.match(".*(St).*", word):
            if re.match(".*[S][t][A-Za-z ,]{3,}", word):
                extracted_info['area'] = re.findall("(.*St)", word)[0]
                print("area:", re.findall("(.*St)", word)[0])
                # extracted_info['area'] = word
                if any(substring.lower() in re.findall("St(.*)", word)[0].lower() for substring in states):
                        city_state = re.findall("St(.*)", word)[0].strip(" ,;").split(" ")
                        city_extract = (city_state[0])
                        extracted_info['city'] = city_extract
                        print("city:", city_extract)
                        state_extract = (city_state[1])
                        extracted_info['state'] = state_extract
                        print("state:", state_extract)
                else:
                    city_extract = (re.findall("St(.*)", word)[0]).strip(" ,;")
                    extracted_info['city'] = city_extract
                    print("city:", city_extract)

            else:
                extracted_info['area'] = word
        elif any(substring.lower() in word.lower() for substring in city):
            extracted_info['city'] = word
            print("city:", word)
        elif any(substring.lower() in word.lower() for substring in states):
            if re.match(".*[0-9]", word):
                state_extract = re.findall("[A-za-z]+", word)[0]
                extracted_info['state'] = state_extract
                print("state:", state_extract)
                pincode_extract = re.findall("([\d]+)", word)[0]
                extracted_info['pin_code'] = pincode_extract
                print("pin_code:", pincode_extract)
            else:
                extracted_info['state'] = word
                print("state:", word)
        elif re.match("[0-9]{6,7}", word):
            extracted_info['pin_code'] = word
            print("pin_code:", word)

    return (extracted_info['company_name'], extracted_info['card_holder_name'], extracted_info['designation'],
            extracted_info['mobile_number'], extracted_info['email_address'], extracted_info['website_URL'],
            extracted_info['area'], extracted_info['city'], extracted_info['state'], extracted_info['pin_code'])
