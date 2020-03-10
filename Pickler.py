import cPickle as pkl
from os.path import join, normpath
import os
import time


class Pickler(object):
    '''Handles pickling operations'''

    def __init__(self, pkl_filename, pkl_dir, expiry_hrs):
        self.pkl_path = normpath( join(pkl_dir, pkl_filename) )
        # print self.pkl_path
        #pickle file expires after 6 hours
        if not os.path.exists(self.pkl_path):
            self.expired = True
        else:
            # pickled file expires after 6 hours
            if (int(time.time()) - os.path.getmtime(self.pkl_path)) > (expiry_hrs * 3600):
                self.expired = True
            else:
                self.expired = False

    def load(self):
        if not self.expired:
            try:
                data = None
                with open(self.pkl_path, 'rb') as pkl_file:
                    data = pkl.load(pkl_file)
                return data
            except Exception as e:
                # print e
                return None
        else:
            return None

    def dump(self, data):
        pkl_file = open(self.pkl_path, 'wb')
        try:
            with open(self.pkl_path, 'wb') as pkl_file:
                pkl.dump(data, pkl_file, protocol=pkl.HIGHEST_PROTOCOL)
            return True
        except Exception as e:
            print e
            return False