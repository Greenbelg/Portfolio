from pathlib import Path
import time
import binascii


class Cach:
    def __init__(self):
        self.path = Path(__file__).parent.parent.joinpath('cach').joinpath('cach.txt')

    def record_data(self, domain_name, data, ttl):
        file = self.path.open('+rb')
        current_data = file.read()
        file.seek(0)
        file.write(b';'.join(
            [domain_name, binascii.hexlify(data), 
             bytes(str(ttl), encoding='utf-8'), 
             bytes(str(time.time()), encoding='utf-8')]) + b'\n')
        file.write(current_data)
        file.close()
    
    def try_get_record_by_domain_name(self, domain_name):
        file = self.path.open('+rb')
        lines = file.read().split(b'\n')
        file.seek(0)
        file.close()
        for line in lines:
            if len(line) < 1:
                continue
            
            try:
                domain_name_from_file, address, ttl, save_date = map(bytes, line.strip().split(b';'))
            except ValueError:
                continue
            if domain_name_from_file != domain_name:
                continue
            
            if time.time() - float(save_date.decode()) > float(ttl.decode()):
                self.__remove_line_by_domain(domain_name, lines)
                break
            
            return binascii.unhexlify(address)
        
    def __remove_line_by_domain(self, domain_name, lines):
        self.path.open('wb').close()
        file = self.path.open('wb')
        file.write(b'\n'.join(
            [line for line in lines if len(line) > 1 and line.strip().split(b';')[0] != domain_name]))
        print(f'Cach by domain {domain_name.decode()} delete, because TTL is up')
        file.close()
