import flask
from flask import request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science -fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.route('/api/v1/resources/timesjobs', methods=['GET'])
def timesjobsearch():
   
    industry_dic = {'AA_text_':"",'Consulting Services jobs' : 42, 'Software Services jobs' : 57, 'Manufacturing/Industrial jobs' : 30, 'Internet/Dot com/ISP jobs' : 54, 'IT-Software jobs' : 28, 'IT-Hardware/Networking jobs' : 27, 'Telecom jobs' : 38, 'Retailing jobs' : 36, 'Banking jobs' : 39, 'Financial Services/Stockbroking jobs' : 22, 'Consumer Durables/FMCG jobs' : 23, 'CRM/CallCentres/BPO/ITES/Med.Trans jobs' : 17, 'Healthcare jobs' : 24, 'Educational/Training jobs' : 18, 'Automobiles/Auto Component/Auto Ancillar... jobs' : 15, 'Engineering/Projects jobs' : 20, 'Biotechnology/Pharmaceutical/Medicine jobs' : 16, 'Hotel/Travel/Tourism/Airlines/Hospitalit... jobs' : 25, 'Recruitment/Placement Agencies jobs' : 19, 'Projects/Infrastructure/Power/Energy jobs' : 56, 'Agriculture/Forestry/Fishing jobs' : 13, 'Petroleum/Oil and Gas/Power jobs' : 33, 'Construction/Cement/Metal/Steel/Iron jobs' : 41, 'Insurance jobs' : 26, 'Advertising/PR/Event Management jobs' : 12, 'Warehousing jobs' : 50, 'Research/Surveyor/MR jobs' : 48, 'Real Estate jobs' : 35, 'Petrochemicals jobs' : 52, 'Accounting-Tax/Consulting jobs' : 11, 'Entertainment/Media jobs' : 21, 'NGO/Social Services jobs' : 31, 'Logistics/Freight Forward/Distribution/C... jobs' : 43, 'Architecture/Interior Design jobs' : 14, 'Apparel/Garments jobs' : 10, 'Marine/Aviation/Military/Mining/Shipping jobs' : 44, 'Law/Legal Firms jobs' : 29, 'Catering/Food Services/Restaurant jobs' : 40, 'Export/Import/Merchandising jobs' : 45, 'Printing/Packaging jobs' : 34, 'Gems & Jewellery jobs' : 55, 'Fashion/Modelling jobs' : 46, 'Security/Law Enforcement jobs' : 37, 'Defence jobs' : 53, 'Sports/Recreation jobs' : 49, 'Government Sector jobs' : 47, }    
    total_jobs = 2
    
    
    if 'total_jobs' in request.args:
       total_jobs = int(request.args['total_jobs'].strip())+1
       
    
    
    links = []
    location = []
    skills = []
    final_url = ''
    			
   
    if 'industry' in request.args:
         industry_no = request.args['industry'].strip()
         if int(industry_no) in industry_dic.values():
            industry_name = list(industry_dic.keys())[list(industry_dic.values()).index(int(industry_no))]
            industry_name  = industry_name.replace(' jobs','')
            industry_name  = industry_name.replace(' ','%20')
            
            base_industry_url = 'https://www.timesjobs.com/candidate/job-search.html?from=submit&searchType=Industry&luceneResultSize=25&postWeek=60&cboIndustry='
            final_url = base_industry_url+industry_no+'&pDate=Y&sequence='
            #print(final_url)        
         else:
            return jsonify(industry_dic)

        
    else:
         if 'skills' in request.args:
            skills.extend(request.args['skills'].split(','))
            base_url = 'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords='
            skills = [s.strip() for s in skills]       
            skills = [s.replace("+",'0PLUS0') for s in skills]
            skills = [s.replace(' ','%20') for s in skills]
            skills = ','.join(skills)

            if 'location' in request.args:
               location.extend(request.args['location'].split(','))
               
          
            if len(location) == 0:
               final_url = base_url+skills+'&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords='+skills+'&pDate=I&sequence='
        
            else:
               locations = '%20,'.join(location)    
               final_url = base_url+skills+'&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&txtLocation='+ locations +'&luceneResultSize=25&postWeek=60&txtKeywords='+skills+'&pDate=I&sequence='
               
            #print(final_url)   
         else:
            return "Error: No skills field provided. Please specify an skills."


    #print(final_url)
    
    for i in range(1,total_jobs):
          final_url_ = final_url+str(i)+'&startPage=1'
          print(final_url_)
          page = requests.get(final_url_)
             
          soup = BeautifulSoup(page.content, 'html.parser')
          for div in soup.find_all('li', attrs={'class':'clearfix job-bx wht-shd-bx'}):
              link = div.find('a')['href']
              link = link.replace(' ','%20')
              links.append(link)
        
    dic = {'link':links}    
    
    return  jsonify(dic)


@app.route('/api/v1/resources/naukri', methods=['GET'])
def naukri_search():    
    total_jobs = 2   
    
    if 'total_jobs' in request.args:
       total_jobs = int(request.args['total_jobs'].strip())+1
    
    links = []
    location = []
    skills = []
    final_url = ''
        
    
    if 'skills' in request.args:
       skills.extend(request.args['skills'].split(','))
       base_url = 'https://www.naukri.com/'
       skills = [s.strip() for s in skills]       
       skills = [s.replace(" ",'-') for s in skills]
       skills = [s.replace('+','-plus') for s in skills]
       skills = '-'.join(skills)

       if 'location' in request.args:
           location.extend(request.args['location'].split(','))
               
          
       if len(location) == 0:
          final_url = base_url+skills+'-jobs'        
       else:
          locations = '-'.join(location)    
          final_url = base_url+skills+"-jobs-in-"+locations
    
            #print(final_url)   
    else:
       return "Error: No skills field provided. Please specify an skills."
       
    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--disable-gpu')    
    driver = webdriver.Chrome(options=opts)
    #html = driver.get(skill_url)
    #html = driver.page_source
        
    #soup = BeautifulSoup(driver.page_source, 'html.parser')
    #for div in soup.find_all('li', attrs={'class':'desig'}):
     #   link = div.find('a')['href']
        #link = link.replace(' ','%20')
      #  links.append(link)
    
  
    #text = soup.body.findAll(text=re.compile('^Apply to '))
    #total_jobs = re.findall(r'\d+',str(text))
    #total_jobs = int(total_jobs[0])
   
    print(type(total_jobs),total_jobs)
    
    #if int(total_jobs/50)+1 > 5:
     #   total_jobs = 5
    #else:
     #   total_jobs = int(total_jobs/50)+1
    html = driver.get(final_url)
    print(final_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    for div in soup.find_all('li', attrs={'class':'desig'}):
        
            link = div.find('a')['href']
            print(link)
            #link = link.replace(' ','%20')
            links.append(link)
    
    for i in range(2,total_jobs): #
        
        #if len(location) == 0:
         #   final_url_ = base_url+skills+'-jobs-'+str(i)
        #else:    
         #   skill_url = base_url+skills+"-jobs-in-"+locations+"-"+str(i)
        
        html = driver.get(final_url+"-"+str(i))
        print(final_url+str(i))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for div in soup.find_all('li', attrs={'class':'desig'}):
            link = div.find('a')['href']
            #link = link.replace(' ','%20')
            links.append(link)
            
    #print(skill_url)
    #print(html)
    
    #print(soup.prettify())
    dic = {'link':links}
    driver.quit()     
    return  jsonify(dic)
    
    #return links
    
@app.route('/api/v1/resources/monster', methods=['GET'])    
def monster_search():       
    industry_dic = {'Automotive' : 'automotive-ancillaries', 'Banking & Financial Services' : 'banking-financial-services', 'Bio Technology' : 'bio-technology-life-sciences', 'Chemicals and Petrochem' : 'chemicals-petrochemicals', 'Construction & Engineering' : 'construction-engineering', 'FMCG' : 'fmcg', 'Education' : 'education', 'Entertainment & Media' : 'entertainment-media-publishing', 'Insurance' : 'insurance', 'ITES and BPO' : 'ites-bpo', 'IT / Computer Hardware' : 'it-computers-hardware', 'IT / Computer Software' : 'it-computers-software', 'KPO and Analytics' : 'kpo-analytics', 'Machinery and Equipment Manufacturing' : 'machinery-equipment-mfg', 'Oil and Gas' : 'oil-gas-petroleum', 'Pharmaceuticals' : 'pharmaceutical', 'Plastics and Rubber' : 'plastic-rubber', 'Power and Energy' : 'power-energy', 'Real Estate' : 'real-estate', 'Recruitment and Staffing' : 'recruitment-staffing-rpo', 'Retailing' : 'retailing', 'Telecom' : 'telecom', 'Advertising/PR/Events' : 'advertising-pr-events', 'Agriculture/Dairy/Forestry/Fishing' : 'agriculture-dairy-forestry-fishing', 'Aviation/Aerospace' : 'aviation-aerospace', 'Wellness/Fitness/Sports' : 'wellness-fitness-sports', 'Beverages/ Liquor' : 'beverages-liquor', 'Cement' : 'cement', 'Ceramics & Sanitary Ware' : 'ceramics-sanitary-ware', 'Consultancy' : 'consultancy', 'Courier/ Freight/ Transportation' : 'courier-freight-transportation', 'Dotcom/Internet/E-commerce' : 'dotcom-internet-e-commerce', 'E-Learning' : 'e-learning', 'Electrical/Switchgear' : 'electrical-switchgear', 'Engineering, Procurement, Construction' : 'engineering-procurement-construction', 'Environmental Service' : 'environmental-service', 'Facility management' : 'facility-management', 'Fertilizer/ Pesticides' : 'fertilizer-pesticides', 'Food & Packaged Food' : 'food-packaged-food', 'Textiles / Yarn / Fabrics / Garments' : 'textiles-yarn-fabrics-garments', 'Gems & Jewellery' : 'gems-jewellery', 'GLASS' : 'glass', 'Government/ PSU/ Defence' : 'government-psu-defence', 'Consumer Electronics/Appliances' : 'consumer-electronics-appliances', 'Hospitals/Healthcare/Diagnostics' : 'hospitals-healthcare-diagnostics', 'HVAC' : 'hvac', 'Hotels/ Restaurant' : 'hotels-restaurant', 'Import / Export' : 'import-export', 'Iron/ Steel' : 'iron-steel', 'ISP' : 'isp', 'Law Enforcement/Security Services' : 'law-enforcement-security-services', 'Leather' : 'leather', 'Market Research' : 'market-research', 'Medical Transcription' : 'medical-transcription', 'Mining' : 'mining', 'NGO/Social Services' : 'ngo-social-services', 'Non-Ferrous Metals (Aluminium, Zinc etc.)' : 'non-ferrous-metals', 'Office Equipment/Automation' : 'office-equipment-automation', 'Paints' : 'paints', 'Paper' : 'paper', 'Printing/ Packaging' : 'printing-packaging', 'Public Relations (PR)' : 'public-relations', 'Semiconductor' : 'semiconductor', 'Shipping/ Marine Services' : 'shipping-marine-services', 'Social Media' : 'social-media', 'Sugar' : 'sugar', 'Travel/ Tourism' : 'travel-tourism', 'Tyres' : 'tyres', 'Wood' : 'wood', 'Other' : 'other', 'Any' : 'any', }
    total_jobs = 2   
    
    if 'total_jobs' in request.args:
       total_jobs = int(request.args['total_jobs'].strip())+1
    
    links = []
    location = []
    skills = []
    final_url = ''
    			
   
    if 'industry' in request.args:
         industry = request.args['industry'].strip()
         print(industry)
         if industry in industry_dic.values():
            base_industry_url = 'https://www.monsterindia.com/'
            final_url = base_industry_url+industry+'-jobs-' #1.html
            #print(final_url)        
         else:
            return jsonify(industry_dic)

        
    else:
         if 'skills' in request.args:
           skills.extend(request.args['skills'].split(','))
           
           skills = [s.strip() for s in skills]
           
           base_url = "https://www.monsterindia.com/"
           
           skills = [s.replace("#",'sharp') for s in skills]
           skills = [s.replace(' ','-') for s in skills]
           skills = '-'.join(skills)
    
    
           if 'location' in request.args:
              location.extend(request.args['location'].split(','))
               
          
           if len(location) == 0:
              final_url = base_url+skills+'-jobs-'
           else:
              locations = '-'.join(location)    
              final_url = base_url+skills+"-jobs-in-"+locations+"-"
            #print(final_url)   
         else:
         
            return "Error: No skills field provided. Please specify an skills."
    
    #base_url = "https://www.monsterindia.com/"
           
    #skills = [s.replace("#",'sharp') for s in skills]
    #skills = [s.replace(' ','-') for s in skills]
    #skills = '-'.join(skills)
    #locations = '-'.join(location)
    #print(location)
    #print(locations)
    
    #if len(location) == 0:
     #   skill_url = base_url+skills+'-jobs.html'        
    #else:    
     #   skill_url = base_url+skills+"-jobs-in-"+locations+'.html' 
    
    
    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--disable-gpu')    
    driver = webdriver.Chrome(options=opts)
    #html = driver.get(skill_url)
    #html = driver.page_source
        
    #soup = BeautifulSoup(driver.page_source, 'html.parser')
    #print(skill_url)
    #for div in soup.find_all('a', attrs={'class':'title_in'}):
        #link = "https:"+div['href']       
        #link = link.replace(' ','%20')
        #links.append(link)
    
  
    #txt = soup.find_all('div',attrs={'class':'count pull-left'})
    #total_jobs = re.findall(r'of \d+',str(txt))
    #total_jobs = re.findall(r'\d+',str(total_jobs))
    
    #text = soup.body.findAll(text=re.compile('Job\(s\)$'))
    #print(soup.prettify())    
    #total_jobs = int(total_jobs[0])
   
    
    #print(type(total_jobs),total_jobs)
    
    #if int(total_jobs/50)+1 > 5:
     #   total_jobs = 5
    #else:
     #   total_jobs = int(total_jobs/50)+1
    
    for i in range(1,total_jobs): #

        final_url_ = final_url+str(i)+".html"     
        print(final_url_)        
        html = driver.get(final_url_)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for div in soup.find_all('a', attrs={'class':'title_in'}):
            link = "https:"+ div['href']
            #print("https:"+div['href'])
            #link = link.replace(' ','%20')
            links.append(link)
            
    #print(skill_url)
    #print(total_jobs)
    
    #print(soup.prettify())
    dic = {'link':links}    
    driver.quit() 
    return  jsonify(dic)


@app.route('/api/v1/resources/iimjobs', methods=['GET'])
def iimjobs_search():    
    total_jobs = 2   
    iimjobs_location_numbering = {'metros' :87, 'anywhere in india' :88, 'overseas/international' :89, 'ahmedabad' :53, 'amritsar' :45, 'andhra pradesh' :34, 'aurangabad' :79, 'bangalore' :3, 'bhubaneshwar' :65, 'bihar' :19, 'chandigarh' :14, 'chennai' :6, 'chhattisgarh' :64, 'cochin/kochi' :70, 'coimbatore' :84, 'cuttack' :86, 'dehradun' :58, 'delhi' :36, 'delhi ncr' :1, 'faridabad' :40, 'gandhinagar' :55, 'ghaziabad' :41, 'goa' :13, 'greater noida' :39, 'gujarat' :8, 'guntur' :77, 'gurgaon/gurugram' :37, 'guwahati' :12, 'haridwar' :57, 'haryana' :16, 'hosur' :71, 'hubli' :72, 'hyderabad' :4, 'jaipur' :11, 'jalandhar' :46, 'jammu' :43, 'jammu & kashmir' :42, 'jamshedpur' :63, 'jharkhand' :20, 'jodhpur' :52, 'karnataka' :31, 'kerala' :17, 'kolkata' :5, 'lucknow' :60, 'ludhiana' :48, 'madurai' :83, 'maharashtra' :9, 'mp' :10, 'mumbai' :2, 'mysore' :73, 'nagpur' :66, 'nasik' :67, 'navi mumbai' :68, 'noida' :38, 'odisha' :18, 'panipat' :50, 'patiala' :47, 'patna' :61, 'pondicherry' :85, 'pune' :7, 'punjab' :15, 'raipur' :74, 'rajasthan' :33, 'rajkot' :80, 'ranchi' :62, 'sonipat' :49, 'srinagar' :44, 'surat' :54, 'tamil nadu' :32, 'telangana' :35, 'thane' :69, 'thiruvananthapuram' :75, 'udaipur' :51, 'up' :21, 'uttarakhand' :59, 'vadodara/baroda' :56, 'varanasi/banaras' :81, 'vijayawada' :76, 'vishakhapatnam/vizag' :78, 'warangal' :82, 'abu dhabi' :100, 'afghanistan' :109, 'africa' :26, 'bahrain' :90, 'bangladesh' :107, 'bhutan' :105, 'china' :108, 'dhaka' :106, 'doha' :98, 'dubai' :91, 'egypt' :113, 'ethiopia' :112, 'eu' :28, 'hong kong' :30, 'indonesia' :103, 'kabul' :92, 'kenya' :114, 'kuwait' :93, 'london' :95, 'malaysia' :27, 'middle east' :25, 'muscat' :97, 'nairobi' :115, 'nepal' :104, 'nigeria' :94, 'oman' :96, 'pakistan' :110, 'philippines' :120, 'qatar' :99, 'riyadh' :102, 'saudi arabia' :101, 'singapore' :24, 'south africa' :117, 'sri lanka' :111, 'tanzania' :116, 'uk' :23, 'us' :22, 'zambia' :119, 'zimbabwe' :118, 'others' :100000, }
    
    if 'total_jobs' in request.args:
       total_jobs = int(request.args['total_jobs'].strip())+1
    
    links = []
    location = []
    count = 0
    skills = []
    final_url = ''
        
    
    if 'skills' in request.args:
       skills.extend(request.args['skills'].split(','))
       base_url = "https://www.iimjobs.com/search/"
       skills = [s.strip() for s in skills]
              
       skills = [s.replace(" ",'%252B') for s in skills]
       skills = [s.replace('+','%252B') for s in skills]
       skills = '%252B'.join(skills)
       print(skills)
       if 'location' in request.args:
           location.extend(request.args['location'].split(','))
               
          
       if len(location) == 0:           
           final_url = base_url+skills+'-0'        
       else:
           print(location)           
           for x in location:
                 if int(x) in iimjobs_location_numbering.values():
                     a=1
                     print('if ' + str(location))
                 else:
                     return jsonify(iimjobs_location_numbering)
                              
           locations = '_'.join(location)    
           final_url = base_url+skills+"-"+locations+'-0' 
    
       #print(skill_url)
    
            #print(final_url)   
    else:
       return "Error: No skills field provided. Please specify an skills."
       
    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--disable-gpu')    
    driver = webdriver.Chrome(options=opts)
    #html = driver.get(skill_url)
    #html = driver.page_source
        
    #soup = BeautifulSoup(driver.page_source, 'html.parser')
    #for div in soup.find_all('li', attrs={'class':'desig'}):
     #   link = div.find('a')['href']
        #link = link.replace(' ','%20')
      #  links.append(link)
    
  
    #text = soup.body.findAll(text=re.compile('^Apply to '))
    #total_jobs = re.findall(r'\d+',str(text))
    #total_jobs = int(total_jobs[0])
   
    print(type(total_jobs),total_jobs)
    
    #if int(total_jobs/50)+1 > 5:
     #   total_jobs = 5
    #else:
     #   total_jobs = int(total_jobs/50)+1
    
    for i in range(1,total_jobs): #
        
        #if len(location) == 0:
         #   final_url_ = base_url+skills+'-jobs-'+str(i)
        #else:    
         #   skill_url = base_url+skills+"-jobs-in-"+locations+"-"+str(i)
         
        final_url_ = final_url+'-'+str(count)+'-0-'+str(i)+'.html'
        count += 100 
        html = driver.get(final_url_)
        print(final_url_)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for div in soup.find_all('a', attrs={'class':'mrmob5 hidden-xs'}):
            link = div['href']
            #link = link.replace(' ','%20')
            links.append(link)
           
    #print(skill_url)
    #print(html)
    
    #print(soup.prettify())
    dic = {'link':links}
    driver.quit()      
    return  jsonify(dic)
    
    #return links
      

app.run(host='0.0.0.0',port=4444,debug=True)
