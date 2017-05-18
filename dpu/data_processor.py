import os.path
import re
import pandas

from constants import HDD_URLS_UNPROC, PA_URLS_PROT, SA_URLS


class DataProcessor(object):
    def process_heart_diseases_dataset(self, url):
        outfile = '/'.join([url[0], url[1], 'hdd_processed', url[3]])
        if os.path.isfile(outfile):
            print("Data set {} already processed".format(url[3]))
        with open('/'.join(url), 'rb') as f:
            current = []
            solution = []
            for line in f:
                line = line.replace(b"\n", b"")
                line = line.decode("utf-8")
                try:
                    line = list(map(float, line.split(" ")))
                    line = list(map(lambda number: 0 if number < 0 else number, line))
                    line = ' '.join(str(number) for number in line).encode('utf-8')
                except ValueError:
                    line = line.split(" ")
                    res = []
                    num_format = re.compile(r'^\-?[1-9][0-9]*\.?[0-9]*')
                    for el in line:
                        if re.match(num_format, el):
                            el = float(el)
                            res.append(0 if el < 0 else el)
                        else:
                            res.append(el)
                    line = ' '.join(str(number) for number in res).encode('utf-8')
                current.append(line.strip())
                if b'name' == line[-4:]:
                    replacement = current[-1].replace(b'name', b'0')
                    current[-1] = replacement
                    solution.append(current)
                    current = []
            with open(outfile, 'w+b') as f:
                f.write(b'\n'.join((b' '.join(part) for part in solution)))
        return outfile

    def process_hdd(self):
        new_urls = []
        for url in HDD_URLS_UNPROC:
            urlx = ['..'] + url
            new_url = self.process_heart_diseases_dataset(urlx)
            new_urls.append(new_url)
        return new_urls

    def process_pamap(self):
        return PA_URLS_PROT

    def process_sa(self):
        return SA_URLS

    def join_hdd(self, urls):
        url = '../ds/hdd_processed/joined.data'
        if os.path.isfile(url):
            print("Data set {} already generated".format(url))
        frames = []
        for url in urls:
            df = pandas.read_csv(url, sep=' ', header=None)
            frames.append(df)
        df = pandas.concat(frames)
        df.to_csv(url, sep=' ')
        return url

    def join_pamap(self, urls):
        url = '../ds/pamap2/joined.data'
        if os.path.isfile(url):
            print("Data set {} already generated".format(url))
            return url
        frames = []
        for url in urls:
            df = pandas.read_csv(url, sep=' ', header=None)
            frames.append(df)
        df = pandas.concat(frames)
        df.to_csv(url, sep=' ')
        return url