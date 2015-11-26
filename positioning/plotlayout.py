import argparse, math, random
import csv
#import matplotlib.pyplot as plt
import generate as g
import lightdensity as ld
import circleoverlap as co

parser = argparse.ArgumentParser(description='Create a canvas for positions of telescopes')
parser.add_argument("-s", "--source", default="five")
parser.add_argument("-o", "--output", default="default")
parser.add_argument("-t", "--text", action="store_true")
parser.add_argument("-g", "--graph", action="store_true")
parser.add_argument("-n", "--number", default=1)
cfg = parser.parse_args()

eff = 1.0

with open("output/" + cfg.output + ".csv", 'wb') as csvout:
    	writer = csv.writer(csvout, delimiter=',', quotechar='|')
	writer.writerow(["Event Number", "Category", "Xpos", "Ypos", "Photon Count", "Illuminated Area"])

	for i in range (0, int(cfg.number)):
		#if cfg.graph:
			#fig = plt.figure()

		rayxpos, rayypos, epsilon, rayradius, Energy, major, e, Z = g.run(text=cfg.text)
		
		#if cfg.graph:
			#circle=plt.Ellipse((rayxpos,rayypos),rayradius,color='black')
			#fig.gca().add_artist(circle)

		if cfg.text:
			print "Cosmic Ray centre at", rayxpos, rayypos

		with open("orientations/"+ cfg.source +".csv", 'rb') as csvfile:
    			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    			for row in reader:
        			category = row[0]
        			xpos = float(row[1])
        			ypos = float(row[2])
        			if category == "lst":
        	        		diameter = 23
        	        		colour = 'r'
        			elif category == "mst":
        	        		diameter = 12
        	        		colour = 'b'
        			elif category == "sst":
        	        		diameter = 4
        	        		colour = 'g'
		
				dangle = math.atan((rayypos - ypos)/(rayxpos - xpos))

				angle = math.pi + epsilon - dangle

				r = major * (1-(e**2))/(1 + (e*math.cos(angle)))        	
		
				radius = diameter/2
            
        			distance = math.sqrt((rayxpos - xpos)**2 + (rayypos - ypos)**2)
            
				density, bkgd = ld.run(distance, Energy, Z)
		
				area = (radius**2) * math.pi
		
				if distance < (radius + r):
					#if cfg.graph:
						#circle=plt.Circle((xpos,ypos),radius,color='magenta')
						#fig.gca().add_artist(circle)
		
					if distance < (r- radius):
						litarea=area
						rawsigcount = density*litarea*eff
						sigcount = int(random.gauss(rawsigcount, math.sqrt(rawsigcount)))
						bkgcount = int(bkgd*area*eff)
						count = sigcount+bkgcount
	
					else:
						litarea = co.run(radius, r, distance)		
						if cfg.text:
							print "PARTIAL ILLUMINATION!!!!!", 
						rawsigcount = density*litarea*eff				
						sigcount = int(random.gauss(rawsigcount, math.sqrt(rawsigcount)))
						bkgcount = int(bkgd*area*eff)
						count = sigcount+bkgcount
			
					if cfg.text:
						print "Angle of location", math.degrees(dangle)
						print "Radius of ring at this angle is", r
						print "Detection!", xpos, ypos, "Distance = " + str(distance), "Illuminated area is", litarea
						print "Density is", density, ", Photon Count is", count
						print "Signal accounts for", rawsigcount, "Smeared to", sigcount, "Background accounts for", bkgcount
					
				    	#if cfg.graph:
						#circle=plt.Circle((xpos,ypos),radius,color=colour)
					    	#fig.gca().add_artist(circle)
				
				else:
					sigcount = 0
					bkgcount = 0
					litarea=0
					count = sigcount+bkgcount
				
				writer.writerow([i+1, category, xpos, ypos, count, litarea])					
			    
				#if cfg.graph:
					#plt.xlim(-200, 200)
					#plt.ylim(-200, 200)
					#plt.show()
					#raw_input("prompt")
