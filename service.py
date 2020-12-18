import socket
import threading
import json
from itertools import izip

#headers that are not intended to contain argumnets
skip_headers = ["Accept","Connection","Host","User-Agent","Accept-Encoding","Accept-Language","Referer","Content-Type","Contnet-Length","Access-Control","X-Powered-By", "Content-Length","Cache-Control"]

#tries to parse data into json, on error that means its no json
def parse_json(data):
	try:
		json_dict = json.loads(data)
		return True,json_dict
	except:
		return False,{}
		
#parsing args into one line when there are multiple lines or new lines between the args
'''
ex:
{
	'arg1':'1',

	'arg2':'2'
}

will return:

{'arg1':'1','arg2':'2'}
'''
def parse_args(data): 
	collect = False
	args = ""
	for line in data:
		if collect:
			args += line
		if line == "" or line is None: #for post and response, the arguments start after the "null line"
			collect = True
	return args

#handles the request, prints the endpoint, the method and arguments in the: url,headers,body of post
#prints and returns request type,endpoint and a dict of arguments
def handle_request(data,key): 
	data_arr = data[0].split(" ")
	request_type = data_arr[0] #request type is the first string in http request
	parms = {} #parms dictionary, for 
	args_bool = False
	is_json = False
	raw_args = []
	if "?" in data_arr[1]: #parse arguments in url
		temp = data_arr[1].split("?") #if the arguments look like: /endpoint?search=what+is+http+request
		if "&" in data_arr[1]: #if there are multiple arguments, ex: /endpoint?search=what+is+http+request&help=pls
			raw_args.extend(temp[1].split("&"))
			endpoint = temp[0]
		else: #one argument only
			raw_args.append(temp[1])
			endpoint = temp[0]
		args_bool = True #there are arguments
	#parse arguments in method which doesnt send arguments in url
	else:
		endpoint = data_arr[1]
		
	args = parse_args(data)
	#print(args) #for testing
	if args is None or args == "": #if there are no arguments in the body
		pass
	is_json, json_args = parse_json(args)
	args_bool = is_json
	if not is_json:
		if "=" in args: #if the arguments look like: username=hello&passowrd=world!
			if "&" in args: #if there are multiple arguments, ex: username=hello&passowrd=world!
				raw_args.extend(args.split("&"))
			else: #one argument only like: message=hello%20there
				raw_args.append(args)
			args_bool = True
	
	if len(raw_args): #are there any arguments in the request?
		for arg in raw_args:
			temp = arg.split("=")
			parms[temp[0]]=temp[1]
	if is_json:
		parms.update(json_args)
	
	'''#need to be fixed
	#add arguments from headers, adds H_ for each key for marking as header argument:
	is_json = False
	for line in data[1:]:
		if line == "" or line is None: #for post requests where there is a null line before the body
			break
		header = line.split(": ")
		if header[0] not in skip_headers:
			is_json, raw_args = parse_json(header[1])
			if is_json: #if its a real json, parser thinks integer or a string is a json as well
				try:
					raw_args = dict(("H_{}".format(k),v) for k,v in raw_args.items())
					print(raw_args,is_json)
					parms.update(raw_args) #adds a dict to the old dict
				except:
					pass
			elif "," in header[1]: #headers that thier arguments look like this: word1=hello, word2=world
				args_list = header[1].split(", ")
				for arg in args_list:
					temp = arg.split("=")
					parms["H_"+temp[0]]=temp[1]
			elif ";" in header[1]: #headers that thier arguments look like this: word1=hello; word2=world
				args_list = header[1].split("; ")
				for arg in args_list:
					temp = arg.split("=")
					parms["H_"+temp[0]]=temp[1]
			elif "=" in header[1]: #one argument
				temp = args.split("=")
				parms["H_"+temp[0]]=temp[1]
	'''
				
	print("------------------------------http request %s ------------------------------" %key[-1]) #prints header for making it look nice
	print("Method: %s" %(request_type)) #request type
	print("endpoint: %s" %(endpoint)) #endpoint
	print("arguments: %s" %(parms)) #parms as a dictionary of arguments
	#print("-"*80)
	return request_type,endpoint,parms
	
#handles the response, prints and returns the payload as json
def handle_response(data,key): 
	print("------------------------------http response %s------------------------------" %key[-1]) #prints header for making it look nice
	payload = parse_args(data)
	is_json, json_dict = parse_json(payload)
	if is_json:
		print("response json payload :\n%s" %(json_dict))
		#print("-"*80)
		return json_dict
	print("response payload:\n%s" %(payload))
	#print("-"*80)
	return payload

#handles data from the file, which is
def handle_data(data,key): #check if the data is a request or a response
	if data[0].split(" ")[0] == "HTTP/1.1": #if its a HTTP/1.1 in the beginning, that means its a response
		handle_response(data,key)
	else:
		handle_request(data,key)
	print("\n")

#main for sockets
''' 
def main():
	serv = socket.socket()
	serv.bind(("127.0.0.1",80))
	serv.listen(1)
	while True:
		conn, addr = serv.accept()
		print("conn incoming: %s" % (str(addr)))
		data = conn.recv(1024)
		conn.close()
		if data == "EOF":
			print("----------------------------Thats IT!---------------------------")
			exit(1)
		x = threading.Thread(target=handle_data, args=(data,conn,addr))
		x.start()
'''

def main(): #main function, iteretes in the requests.txt file and parses the lines into a list of headers
	requests_dict = {}
	with open("requests.txt",'r') as requests_file:
		raw_request = []
		for line in requests_file:
			if "-"*80 in line: #each request ends with CR-LF, after that its sends the request that has been colected to the handler and then zero the raw_request parm for new one
				temp = raw_request[1:] #without the request number header
				requests_dict[raw_request[0][:-1]] = temp #the key is the header, which is Req_1,Res_2,Req_3...
				raw_request = [] #zero the array
			else:
				raw_request.append(str(line.rstrip("\n")))
	sorted_requests = sorted(list(requests_dict))
	sorted_requests.sort(key = lambda x: int(x.rsplit('_',1)[1])) #sorts by req,res and their number, ex: req_1, res_1
	for key in sorted_requests:
		handle_data(requests_dict[key],key)
			
if __name__ == "__main__":
	main()
