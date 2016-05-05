import os
import sys
import lxml.etree as etree
import subprocess
import shutil
import json

apps = []
covert = []
didfail = []

def analyze(path):
  covert_apk_path = '/home/dawn/covert_dist/app_repo/bundle'
  didfail_path = '/root/didfail/toyapps/out/'
  didfail_sh = '/root/didfail/cert/run-didfail.sh'
  didfail_apk = '/root/didfail/toyapps/*.apk'
  didfail_folder = '/root/didfail/toyapps'
  
  # delete any data in covert and didfail folders before starting
  #if os.path.isdir(covert_apk_path):
  #  shutil.rmtree(covert_apk_path)
  #os.makedirs(covert_apk_path)
  #if os.path.isdir(didfail_path):
  #  shutil.rmtree(didfail_path)
  #os.makedirs(didfail_path)
  #for file in os.listdir(didfail_folder):
  #  if file.endswith(".apk"):
  #    os.remove(didfail_folder + '/' + file)

  # run covert  
  for apk_file in os.listdir(path):
    if apk_file.endswith(".apk"):
      new_apk_file = apk_file.replace(' ','_').replace('&','AND').replace('-','_')
      os.rename(path + '/' + apk_file, path + '/' + new_apk_file)
      #if not os.path.isfile(covert_apk_path + '/' + apk_file):
        #shutil.copy(path + '/' + apk_file, covert_apk_path)
  os.chdir('/home/dawn/covert_dist')
  #p = subprocess.Popen(['sh', './covert.sh', 'bundle'])
  #p.communicate()

  # get all apps names and components
  Apps = {}
  app = {}
  components = []
  covert_model = '/home/dawn/covert_dist/app_repo/bundle/analysis/model'
  for xml_file in os.listdir(covert_model):
    if xml_file.endswith(".xml"):
      e = etree.parse(covert_model + '/' + xml_file)
      Apps[e.findall('name')[0].text.replace('-','_').replace(' ','_').replace('&','AND')] = e
      app['name'] = e.findall('name')[0].text.replace('-','_').replace(' ','_').replace('&','AND')
  

  # get covert connections
  filter_component = {}
  intent_component = {}
  for app in Apps:
    for comp in Apps[app].findall('components')[0].findall('Component'):
      components.append(comp.find('name').text)
      
      for filt in comp.findall('IntentFilter')[0].findall('filter'):
        for act in filt.findall('actions'):
          if act.text != 'android.intent.action.MAIN':
            mime = "None"
            if filt.find('data') is not None:
              if filt.find('data').find('mimeType').text is not None:
                mime = filt.find('data').find('mimeType').text
            filters = {}
            filters[act.text] = mime
      filter_component[comp.find('name').text] = filters
    for intent in Apps[app].findall('newIntents')[0].findall('Intent'):
      intents = {}
      mime = 'None'
      if intent.find('action').text:
        if intent.find('dataType').text is not None:
          mime = intent.find('dataType').text
        intents[intent.find('action').text.replace('"','')] = mime.replace('"','')
    intent_component[intent.find('sender').text] = intents
    components.append(comp.find('name').text)
    app['components'] = components
  apps.append(app)
  for key in intent_component:
    for value in intent_component[key]:
      for key2 in filter_component:
        for value2 in filter_component[key2]:
          if value == value2 and intent_component[key][value] == filter_component[key2][value2]:
            same_app = False
            for name in Apps:
              if key.lower().find(name.lower()) != -1 and key2.lower().find(name.lower()) != -1:
                same_app = True
              if not same_app:
                connection = {}
                connection['start'] = key
                connection['end'] = key2
                covert.append(connection)

  # run DidFail
  for apk_file in os.listdir(path):
    if apk_file.endswith(".apk"):
      new_apk_file = apk_file.replace(' ','_').replace('&','AND').replace('-','_')
      os.rename(path + '/' + apk_file, path + '/' + new_apk_file)
      os.chdir('/root/')
      #if not os.path.isfile(didfail_folder + '/' + new_apk_file):
        #shutil.copy(path + '/' + new_apk_file, didfail_folder)
  #p = subprocess.Popen([didfail_sh, didfail_path, didfail_apk])
  #p.communicate()

  # get didfail connections
  epicc = {}
  epicc_action = {}
  buffer = []
  for epicc_file in os.listdir(didfail_path):
    if (epicc_file.endswith(".epicc")):
      open_file = open(didfail_path + '/' + epicc_file)
      txtFound = False
      for line in open_file:
        if txtFound: 
          if '-' in line:
            buffer.append(line.split('- ', 1)[1])
          if 'Action: ' in line:
            buffer.append(line.split(',', 2)[0])
            buffer.append(line.split(',', 2)[1])
            epicc_action[buffer[1].split('Action: ', 1)[1]] = buffer[2].split('Type: ', 1)[1]
            if '(' in buffer[0]:
              epicc[buffer[0].split('(', 1)[0].rsplit('/', 1)[0]] = epicc_action
        if 'The following ICC values were found:' in line:
          txtFound = True

  manifest = {}
  android = '{http://schemas.android.com/apk/res/android}'
  for man_file in os.listdir(didfail_path):
    if (man_file.endswith(".manifest.xml")):
      e = etree.parse(didfail_path + '/' + man_file)
      package = e.getroot().get('package')
      for activity in e.findall('application')[0].findall('activity'):
        for filtr in activity.findall('intent-filter'):
          action = {}
          for act in filtr.findall('action'):
            mime = 'None'
            if filtr.find('data') is not None:
              if filtr.find('data').get(android + 'mimeType') is not None:
                mime = filtr.find('data').get(android + 'mimeType')
          action[act.get(android + 'name')] = mime            
        if activity.get(android + 'name').startswith('.'):
          manifest[package + activity.get(android + 'name')] = action
        else:
          manifest[activity.get(android + 'name')] = action
  for key in epicc:
    for value in epicc[key]:
      for key2 in manifest:
        for value2 in manifest[key2]:
          if value == value2 and epicc[key][value] == manifest[key2][value2]:
            connection = {}
            connection['start'] = key
            connection['end'] = key2
            didfail.append(connection)
  
  output = {}
  output['apps'] = apps
  output['covert'] = covert
  output['didfail'] = didfail
  print(output)
  
  return output
