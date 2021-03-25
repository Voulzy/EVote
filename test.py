import OpenSSL 
import generateCertif
import argparse



if __name__ == '__main__':
	parser= argparse.ArgumentParser()
	parser.add_argument("--output_file", help="Output file for the certif")
	parser.add_argument('-k',"--key_size", help="KeySize", type=int)
	parser.add_argument('-n', "--number_votant", help="Nombre de votant", type=int)
	options=parser.parse_args()
	print(options)
	#### self signed certificats ####
	ca_key = generateCertif.create_key(options.key_size)
	ca_req = generateCertif.create_request(ca_key,'My Certification Authority')
	ca_cert = generateCertif.create_certificate(ca_req,ca_req,ca_key,0)
	generateCertif.save_key(ca_key,'myCA.key')
	generateCertif.save_certificate(ca_cert,'myCA.cert')
	for i in range(0,options.number_votant):
		key=generateCertif.create_key(options.key_size)
		req=generateCertif.create_request(key,f'Votant n {i}')
		cert=generateCertif.create_certificate(req,ca_req,ca_key,256+i)
		generateCertif.save_key(key,f'Voteur_{i}.key')
		generateCertif.save_certificate(cert,f'Voteur_{i}.cert')
	
