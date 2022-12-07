import requests

import pickle

class Helppy:
  def __init__(self, username):
    self.username = username
    self.KB = None
    if self._check_username_exists(username):
      self._load_KB(username)
  

  def _check_username_exists(self):
    pass
  

  def _send_request(self, command, extra_params):
    requests.post(SECRETS.API_GATEWAY, json={'command':command, 'username':self.username, **extra_params})


  def _load_KB(self):
    '''load the knowledge-base'''
    self._send_request('get_KB')
    self.kb = pickle.loads(res.content)
  

  def add_repo(self, repo_name):
    pass
    

  def refresh_KB(self, extensions=['.md']):
    '''reload the topics of the knowledge-base in case there have been some changes.
    '''
    # send request to AWS Lambda to refresh the KB
    self._send_request('refresh_KB', {'extensions':extensions})
    
  
  def find(self, header_keyword=None, page_path_keyword=None, page_body_keyword=None, results_cap=3):
    '''Search the knowledge-base by providing a keyword that appears in the header of the section,
       or search by providing a keyword that appears in the page.
       In either case, you can optionally provide a keyword for page name (page_path_keyword) to limit the search to those pages.
    '''
    if (header_keyword is None and page_body_keyword is None) or (header_keyword and page_body_keyword):
      print("One of 'header_keyword' or 'page_body_keyword' arguments must to be provided.")
      return

    counter = 0
    if header_keyword:
      for (url, page_path_keywords), (topics, page_body) in self.kb.items():
        if not page_path_keyword or page_path_keyword.lower() in page_path_keywords:  # filter the results by page_path_keyword
          for topic in topics:
            if header_keyword.lower() in topic.title.lower():
              counter += 1
              # print the topic
              print(url + '#' + topic.title.replace(':', '').replace(' ','-') + '\n' + '#' * topic.header_size + ' ' + topic.title + '\n' + topic.body)
              # print the sub-topics of the current topic (if any)
              for sub_topic in topic.sub_topics:
                print(url + '#' + sub_topic.title.replace(':', '').replace(' ','-') + '\n' + '#' * sub_topic.header_size + ' ' + sub_topic.title + '\n' + sub_topic.body)
              if results_cap != 0 and counter >= results_cap:
                print("\nBy default at most three results are shown. You can change it by passing a different number to the 'results_cap' parameter (pass 0 for no cap).")
                break

    else:  # page_body_keyword is provided instead of header_keyword
      for (url, page_path_keywords), (topics, page_body) in self.kb.items():
        if not page_path_keyword or page_path_keyword.lower() in page_path_keywords:  # filter the results by page_path_keyword
          if page_body_keyword.lower() in page_body:
            print(url)