import os 
import sys
import secrets
import numpy as np
import pandas as pd
import hashlib as H
from humanfriendly import parse_size,format_size
from concurrent.futures import ThreadPoolExecutor,as_completed
from threading import current_thread
# from threading import cu
from typing import Tuple,Awaitable,List
from scipy import stats
import dotenv

ENV_FILE_PATH = os.environ.get("ENV_FILE_PATH","")
if not len(ENV_FILE_PATH) ==0:
    dotenv.load_dotenv(ENV_FILE_PATH)



def generate_file(output_folder:str,file_id:str,file_size:int ,prefix:str="")->Tuple[str, int, str]:
    thread_name = current_thread().getName()
    size_bytes = int(file_size)
    data       = secrets.token_bytes(size_bytes)
    if prefix == "":
        hasher = H.sha256()
        hasher.update(data)
        file_id = hasher.hexdigest()
    file_path = "{}/{}".format(output_folder,file_id)
    with open(file_path,"wb") as f:
        f.write(data)
        print("{} writes at {} id={} size={}".format(thread_name,file_path,file_id,size_bytes))
    # row.append()
    return [ file_id, size_bytes, file_path]
        # paths.append(file_path)

def generate_files(
        avg_file_size:str = "1MB",
        std_file_size:str = "0.5MB", 
        N:int = 1,
        output_folder:str = "/test/out",
        prefix:str="file",
        separator:str = "-",
        max_threads:int = 2

):
    _avg_file_size = parse_size(avg_file_size)
    _std_file_size = parse_size(std_file_size)
    file_sizes     = np.ceil(np.abs(stats.norm.rvs(loc =_avg_file_size, scale = _std_file_size ,size = N)))
    file_ids       = list(map(lambda x: "{}{}{}".format(prefix,separator,x),range(0,N)))
    if not (os.path.exists(output_folder)):
        os.makedirs(output_folder)

    id_size_zipped = zip(file_ids,file_sizes)
    output_rows:List[Tuple[str,int,str]]        = []
    futures:List[Awaitable[Tuple[str,int,str]]] = []
    with ThreadPoolExecutor(max_workers=max_threads, thread_name_prefix="mictlanx:utils") as executor:
        for file_id,file_size in id_size_zipped:
            fut = executor.submit(generate_file, output_folder = output_folder,file_id=file_id, file_size =file_size,prefix=prefix)
            futures.append(fut)
        for future in as_completed(futures):
            row:Tuple[str,int,str] = future.result()
            output_rows.append(row)

        df = pd.DataFrame(output_rows,columns=["FILE_ID","FILE_SIZE","PATH"])
        df.to_csv("{}/trace.csv".format(output_folder),index=False)
    return df
    
        

if __name__ =="__main__":
    generate_files(
        avg_file_size = os.environ.get("AVG_FILE_SIZE","1MB"),
        std_file_size = os.environ.get("STD_FILE_SIZE","0.5MB"),
        N             = int(os.environ.get("N",100)),
        output_folder = os.environ.get("OUTPUT_FOLDER","/test/out"),
        prefix        = os.environ.get("FILENAME_PREFIX","data"), 
        separator     = os.environ.get("FILENAME_SEPARATOR","-_"),
        max_threads   = int(os.environ.get("MAX_THREADS","2"))
    )