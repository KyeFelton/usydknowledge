import html
import json
import os
import re
import shutil


def is_empty(v):
    '''Checks if a variable is None, an empty dict, an empty list, or an empty string.

    Args:
        v (*): The variable to be inspected.

    Returns
        (bool): True if empty, otherwise False.
    '''
    if v is None:
        return True
    elif type(v) is dict and len(v.keys()) == 0:
        return True
    elif type(v) is list and len(v) == 0:
        return True
    elif type(v) is str and v == '':
        return True
    else:
        return False

class Cleaner():

    def __init__(self, root_dir):
        if not hasattr(self, 'name'):
            raise AttributeError('Cleaner requires a name.')
        self.root_dir = root_dir
        filename = f'{root_dir}/{self.name}/data/scraped.json'
        with open(filename) as f:
            self.data = json.loads(f.read())
        self.pages = []
            

    def clean(self):
        self._parse()
        self._sort()
        
        # Write data to .json file
        json_path = f'{self.root_dir}/{self.name}/data/cleaned.json'
        if os.path.exists(json_path):
            os.remove(json_path)
        with open(json_path, 'w') as f:
            f.write(json.dumps(self.data))
        
        # Create path to write .txt files
        txt_path = f'{self.root_dir}/{self.name}/data/pages/'
        if os.path.exists(txt_path):
            try:
                shutil.rmtree(txt_path)
            except OSError as e:
                print(f'Unable to remove pages folder: {e.filename} - {e.strerror}.')
                exit(3)
        os.mkdir(txt_path)
        
        # Write pages to .txt files
        for page in self.pages:
            for k, v in page.items():
                with open(f'{txt_path}{k.replace(" ", "_")}.txt', 'w') as f:
                    f.write(v)
    
    def _parse(self):

        def parse_struct(data):
            if type(data) is dict:
                res = {}
                for k, v in data.items():
                    if not is_empty(v):
                        parsed = parse_struct(v)
                        if not is_empty(parsed):
                            res[k] = parsed
            elif type(data) is list:
                res = []
                for i in data:
                    if not is_empty(i):
                        parsed = parse_struct(i)
                        if not is_empty(parsed):
                            res.append(parsed)
            else:
                res = self._parse_value(data)
            return res

        self.data = parse_struct(self.data)

    def _parse_value(self, v):
        pass
    
    def _sort(self):
        pass
