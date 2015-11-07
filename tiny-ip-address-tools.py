#!/usr/bin/env python

def IPdecimalToBinary( decIP, bits = 8):
	decList = map(lambda x: int(x), decIP.split("."))
	pairings=[[len(decList) - x -1,x*8 ] for x in range(len(decList))]
	return sum( map(lambda x: decList[x[0]]<<x[1], pairings))

def IPbinaryToDecimal( binIP, bits=8, octets=4):
	maxOctet = reduce( lambda x, y: x+y, map(lambda x: 1<< x, range(bits)))
	offset=[ maxOctet << ( (octets - x -1 )* bits  ) for x in range(0,octets) ]
	pairings = zip(range((octets-1)*bits,-1,-bits),offset)
	almost = [ (binIP & x[1]) >> x[0] for x in pairings ]
	return ".".join(map( lambda x: str(x), almost))

def IPcidrToBinary(cidr, bits=32):
	return (2**cidr-1)<< (bits-cidr)

def IPbinaryToCidr(binIP):
	return len(filter(lambda x: binIP & 1<<x, range(32)))

def increments(bitsOn, bit):
	newBit=bitsOn.pop()
	if newBit + 1 != bit:
		return False
	if len(bitsOn) >= 1:
		return increments(bitsOn, newBit)
	return True

def IPisCidr(binIP):
	bitsOn = filter(lambda x: binIP & 1<<x, range(32))
	bit = bitsOn.pop()
	return increments(bitsOn, bit)
