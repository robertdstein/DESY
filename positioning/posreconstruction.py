import array, math
#from scipy.optimize import fmin

def run(t):
	
	n=len(t)
	print n, "Detections"

	for i in range(1,n):
		print i
		eval("x" + str(i) + " = t" + str(i)+ "[0]")
		eval("y" + str(i) + " = t" + str(i) + "[1]")
		eval("a" + str(i) + " = t" + str(i) + "[2]")
		eval("l" + str(i) + " = t" + str(i) + "[3]")
	
	for i in range(n):
		print eval("x"+n), eval("y"+n), eval("a"+n), eval("l"+n)

		def f1 (x,y):
			return (y1-y) + math.tan(a1)*(x-x1) 

	x2 = t2[0]
	y2 = t2[1]
	a2 = t2[2]
	l2 = t2[3]

	def f2(x,y):
		return (y2-y) + math.tan(a2)*(x-x2)

	def f(x,y):		
		print "hello", f1(x,y)*f2(x,y)		
		return f1(x,y)*f2(x,y)

	f(1,2)

t1 = [0,0,2,90]
t2 = [1,1,1,90]

run([t1,t2])

#fmin(run,array.array([0,0]))

