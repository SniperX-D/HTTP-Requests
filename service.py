import socket
import threading
import json
from itertools import izip

#headers that are not intended to contain argumnets
skip_headers = ["HOST","Accept","Connection","Host","User-Agent","Accept-Encoding","Accept-Language","Referer","Content-Type","Contnet-Length","Access-Control","X-Powered-By", "Content-Length","Cache-Control"]

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
def handle_request(data): 
	data_arr = data[0].split(" ")
	request_type = data_arr[0] #request type is the first string in http request
	parms = {} #parms dictionary, for 
	args_bool = False
	is_json = False
	raw_args = []
	if "?" in data_arr[1]: #parse arguments in url
		temp = data_arr[1].split("?") #if the arguments look like: /endpoint?search=what+is+http+request , /endpoint?Test=True&message=hello
		raw_args.extend(temp[1].split("&"))
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
			raw_args.extend(args.split("&"))
			args_bool = True
	
	if len(raw_args): #are there any arguments in the request?
		for arg in raw_args:
			temp = arg.split("=")
			parms[temp[0]]=temp[1]
	if is_json:
		parms.update(json_args)
	
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
			elif "=" in header[1]: #one argument, had to do that because there are arguments without "=" and arent really usful
				temp = args.split("=")
				parms["H_"+temp[0]]=temp[1]
				
	print("------------------------------http request------------------------------") #prints header for making it look nice
	print("Method: %s" %(request_type)) #request type
	print("endpoint: %s" %(endpoint)) #endpoint
	print("arguments: %s" %(parms)) #parms as a dictionary of arguments
	#print("-"*80)
	return request_type,endpoint,parms
	
#handles the response, prints and returns the payload as json
def handle_response(data): 
	print("------------------------------http response------------------------------") #prints header for making it look nice
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
#main function, iteretes in the requests.txt file and parses the lines into a list of headers. the function collects requests by line order and then searchs for the next response
def main(): 
	is_request = True #boolean variable to collect requests and not responses
	is_response = False
	skip_responses = 0 #how much responses to skip till next response
	with open("requests.txt",'r') as requests_file:
		raw_request = [] #saves raw requests and raw responses...
		lines = requests_file.readlines() #lines from the file "loaded" into memory (could use another file description but had to skip some amount of files)
		for line_num,line in enumerate(lines):
			if "HTTP" in line and not line.startswith("HTTP") and not is_request: #is it a request?
				is_request = True #read it!
			elif "HTTP" in line and line.startswith("HTTP") and skip_responses > 0: #skips responses what were already printed, ex: (">" is where the loop is) req_1,req_2,res_1,>res_2,req_3,res_3 and skip_responses = 1, so it decrices skip_response by one so it wont skip res_3 later
				skip_responses -=1
			if is_request:
				if "-"*80 in line: #each request ends with CR-LF, after that its sends the request that has been colected to the handler and then zero the raw_request parm for new one
					handle_request(raw_request)
					raw_request = [] #zero the array
					for res_line_index in range(line_num+1, len(lines)):
						if "HTTP" in lines[res_line_index] and lines[res_line_index].startswith("HTTP") and not is_response:
							if skip_responses <= 0: #skips http responses, ex: (">" where is the loop pointer and "--" what needs to printed) >req_2,req_3,res_1,--res_2,res_3, loop read and printed req_2, needs to skip res_1 to read res_2 
								is_response = True #you can read the response and not skip to the next one
							else:
								skip_responses -= 1 #the loop already read a response, need to skip to the next
						elif is_response:
							if "-"*80 in lines[res_line_index]: #CR-LF after responses
								handle_response(raw_request)
								raw_request = []
								is_response = False
								skip_responses += 1 #means the loop needs to skip 1 response so it will print the next response right after this one
								break
							elif is_response: #append the lines into raw_request
								raw_request.append(lines[res_line_index].rstrip("\n"))
					is_request = False #incase of next http payload is a response so it wont collect it
				else:
					raw_request.append(str(line.rstrip("\n")))

			
if __name__ == "__main__":
	main()
