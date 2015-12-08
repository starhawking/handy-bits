#!/usr/bin/env python

def IPdecimalToBinary( decIP, bits = 8):
    decList = map(lambda x: int(x), decIP.split("."))[::-1]
    return sum([ decList[x] <<  x*8  for x in range(4)])

def IPbinaryToDecimal( binIP, bits=8, octets=4):
    listIP = [ ((2**(bits) -1)<< ( bits * x) & binIP) >> ( bits * x) for x in range(octets) ]
    return ".".join(map(lambda x: str(x), listIP)[::-1])

def IPcidrToBinary(cidr, bits=32):
	return (2**cidr-1)<< (bits-cidr)

def IPbinaryToCidr(binIP):
	return len(filter(lambda x: binIP & 1<<x, range(32)))

def IPisCidr(binIP):
    bitsOn=[ (binIP >> x) & 1 for x in xrange(32) ]
    return bitsOn == sorted(bitsOn)
