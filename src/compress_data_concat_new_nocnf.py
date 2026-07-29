import json
import math
import bz2
import lzma
import gzip

#dir = "Test Suite - TNF Compressed/"
#fn = "test_set_0.15-0.35-1.0.json"


def avblen (text) :
   return 8*len(text)

# each term can be represented with 10 trinary or 16 binary (3^10 < 2^16)
def avterm_compress (text) :
   return 16*text.count('^')

def compress_data_file(fn) :
   print("fn=",fn)
   return compress_data(json.load(open(fn)))

def compress_data(j) :
   nvars = len(j["Variables"])
   N = 2**nvars

   p_sender = j["p_sender"]
   p_query = j["p_query"]
   p_receiver = j["p_receiver"]

   sender_tnf = ""
   query_tnf = ""
   riquery_tnf = ""   


   Ntest = 0

   for case in j["Test Cases"]:
      sender_tnf += case["Sender TNF"]
      query_tnf += case["Query TNF"]
      riquery_tnf += case["Receiver Informed Query TNF"]
      
      Ntest += 1

   bz_sender_tnf = avblen(bz2.compress(bytes(sender_tnf,"utf-8")))
   bz_query_tnf = avblen(bz2.compress(bytes(query_tnf,"utf-8")))
   bz_riquery_tnf = avblen(bz2.compress(bytes(riquery_tnf,"utf-8")))   

   lz_sender_tnf = avblen(lzma.compress(bytes(sender_tnf,"utf-8"),preset=9))
   lz_query_tnf = avblen(lzma.compress(bytes(query_tnf,"utf-8"),preset=9))
   lz_riquery_tnf = avblen(lzma.compress(bytes(riquery_tnf,"utf-8"),preset=9))   

   len_sender_tnf =  len(sender_tnf)
   len_query_tnf = len(query_tnf)
   len_riquery_tnf = len(riquery_tnf)   

   term_compress_sender_tnf = avblen(sender_tnf)/2 # only needs 4 bits per character since uses 0-9 + "v" + "^" + "-", i.e. 13 distinct chars can be represented in 4 bits
   term_compress_query_tnf = avblen(query_tnf)/2
   term_compress_riquery_tnf = avblen(riquery_tnf)/2          

   gz_sender_tnf =  avblen(gzip.compress(bytes(sender_tnf,"utf-8")))
   gz_query_tnf = avblen(gzip.compress(bytes(query_tnf,"utf-8")))
   gz_riquery_tnf = avblen(gzip.compress(bytes(riquery_tnf,"utf-8")))   

   min_tnf = min([bz_sender_tnf, bz_query_tnf, bz_riquery_tnf, lz_sender_tnf, lz_query_tnf, lz_riquery_tnf, gz_sender_tnf, gz_query_tnf, gz_riquery_tnf,
                  term_compress_sender_tnf, term_compress_query_tnf, term_compress_riquery_tnf])

   min_tnf_noriq = min([bz_sender_tnf, bz_query_tnf, lz_sender_tnf, lz_query_tnf, gz_sender_tnf, gz_query_tnf,
                        term_compress_sender_tnf, term_compress_query_tnf])

   lambda_bound = -p_sender * math.log2( p_sender/(p_sender + p_receiver - p_query) ) - (p_receiver-p_query)* math.log2( (p_receiver-p_query)/(p_sender + p_receiver - p_query) )

   return { "len_sender_tnf" : len_sender_tnf/Ntest,
            "len_query_tnf" : len_query_tnf/Ntest,
            "len_riquery_tnf" : len_riquery_tnf/Ntest,             
            "normed_min_sender_tnf" : min([bz_sender_tnf, lz_sender_tnf, gz_sender_tnf, term_compress_sender_tnf])/N/Ntest,
            "normed_min_query_tnf" : min([bz_query_tnf, lz_query_tnf, gz_query_tnf, term_compress_query_tnf])/N/Ntest,
            "normed_min_riquery_tnf" : min([bz_riquery_tnf, lz_riquery_tnf, gz_riquery_tnf, term_compress_riquery_tnf])/N/Ntest,            
            "normed_min_tnf" : min_tnf/N/Ntest,
            "lambda_bound" : lambda_bound }

