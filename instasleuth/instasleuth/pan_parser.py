def parse_pan(uploaded_image):
	print uploaded_image,"uploaded_image"
	import numpy as np
	threshold = 200     #the average of the darkest values must be _below_ this to count (0 is darkest, 255 is lightest)
	obviousness = 50    #how many of the darkest pixels to include (1 would mean a single dark pixel triggers it)

	from PIL import Image
	from pytesseract import image_to_string
	from PIL import ImageFilter
	def find_line(vals):
	    #implement edge detection once, use many times 
	    for i,tmp in enumerate(vals):
	        tmp.sort()
	        average = float(sum(tmp[:obviousness]))/len(tmp[:obviousness])
	        if average <= threshold:
	            return i
	    return i    #i is left over from failed threshold finding, it is the bounds

	def getbox(img):
	    #get the bounding box of the interesting part of a PIL image object
	    #this is done by getting the darekest of the R, G or B value of each pixel
	    #and finding were the edge gest dark/colored enough
	    #returns a tuple of (left,upper,right,lower)

	    width, height = img.size    #for making a 2d array
	    retval = [0,0,width,height] #values will be disposed of, but this is a black image's box 

	    pixels = list(img.getdata())
	    vals = []                   #store the value of the darkest color
	    for pixel in pixels:
	        vals.append(min(pixel)) #the darkest of the R,G or B values

	    #make 2d array
	    vals = np.array([vals[i * width:(i + 1) * width] for i in xrange(height)])

	    #start with upper bounds
	    forupper = vals.copy()
	    retval[1] = find_line(forupper)

	    #next, do lower bounds
	    forlower = vals.copy()
	    forlower = np.flipud(forlower)
	    retval[3] = height - find_line(forlower)

	    #left edge, same as before but roatate the data so left edge is top edge
	    forleft = vals.copy()
	    forleft = np.swapaxes(forleft,0,1)
	    retval[0] = find_line(forleft)

	    #and right edge is bottom edge of rotated array
	    forright = vals.copy()
	    forright = np.swapaxes(forright,0,1)
	    forright = np.flipud(forright)
	    retval[2] = width - find_line(forright)

	    if retval[0] >= retval[2] or retval[1] >= retval[3]:
	        print "error, bounding box is not legit"
	        return None
	    return tuple(retval)

	def crop_image(image_name):
	    print "here crop image", image_name
	    
	    image = Image.open(image_name)
	    image = image.filter(ImageFilter.SHARPEN)
	    print "here", image
	    box = getbox(image)
	    #print "result is: ",box
	    result = image.crop(box)
	    t = image_name.split('/')
	    cropped_image_name = "/".join(t[0:-1]+['cropped', '']) + t[-1]
	    print result, cropped_image_name
	    result.save(cropped_image_name)
	    #result.show()
	    ratio = (box[2] - box[0])/float(box[3]-box[1])
	    return (cropped_image_name, ratio)


	image_to_process, ratio = crop_image(uploaded_image)

	print image_to_process, "image_to_process", ratio
	if ratio < 1:
	    img = Image.open(image_to_process)
	    img2 = img.rotate(90, expand=True)
	    img2.save(image_to_process)
	    print "here"
	t = Image.open(image_to_process)
	print "here2222"
	text_from_image = image_to_string(t, lang='eng')
	print text_from_image,"text_from_image"


	if "INCOME" in text_from_image or "GOVT" in text_from_image:
	    pass
	else:
		print "okay"
	    img = Image.open(image_to_process)
	    print "not kay"
	    img2 = img.rotate(180, expand=True)
	    img2.save(image_to_process)
	    t = Image.open(image_to_process)
	    text_from_image = image_to_string(t, lang='eng')

	list_of_words = text_from_image.split('\n')


	cleaned_words = []
	for word in list_of_words:
	    stripped_word = word.strip()
	    if len(stripped_word)>1:
	        cleaned_words.append(stripped_word)


	user_name = cleaned_words[2]
	fathers_name = cleaned_words[3]
	dob = cleaned_words[4].replace(' ', '')
	pan_card_no = cleaned_words[6].replace(' ', '')
	return (user_name, fathers_name, dob, pan_card_no)