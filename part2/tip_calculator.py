from optparse import OptionParser #import the OptionParser object from this module

parser = OptionParser()

parser.add_option("-m", "--meal",
	dest="meal", help="your meal cost",
	type="float")

parser.add_option("-x", "--tax",
	dest="tax", help="the tax rate",
	type="float")

parser.add_option("-p", "--tip",
	dest="tip", help="the percentage to tip",
	default=.15, type="float")

(options, args) = parser.parse_args()

if not(options.meal and options.tax):
	parser.error("You need to enter a correct value for the meal and/or tax rate!")

meal = options.meal
tax = options.tax
tip = options.tip

tax_value = meal*tax
meal_with_tax = meal + tax_value
tip_value = meal_with_tax*tip  #raw val of tip given meal_with_tax

total = tip_value + meal_with_tax #cost of meal_with_tax + tip_value

print "Base cost of meal: ${:.2f}".format(meal)  
print "Dollar value of tax on the meal based on a tax rate of {:.2%}: ${:.2f}".format(tax, tax_value)
print "Dollar value given you tip {:.2%}: ${:.2f}".format(tip, tip_value)
print "Grand total for the meal(including tax & tip): ${:.2f}".format(total)