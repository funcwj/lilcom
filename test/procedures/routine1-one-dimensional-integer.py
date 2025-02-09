# Signals are supposed to be given as numpy arrays
import numpy
# The main library
import lilcom.lilcom_c_extension as l
# To create random samples for the signal
import random

n_samples = 1000

inputArray = numpy.array([random.randrange(-(2**15), 2**15 - 1) for i in range (n_samples)]).astype(numpy.int16)
outputArray = numpy.zeros((inputArray.shape[0]+4), numpy.int8)
reconstruction = numpy.zeros(inputArray.shape, numpy.int16)

#lilcom.compress_int16(inputArray, outputArray,
#                      lpc_order=5, conversion_exponent=39)

print("Shapes {} {} {} ".format(inputArray.shape, outputArray.shape, reconstruction.shape))
a = l.compress_int16(inputArray, outputArray, lpc_order=5, conversion_exponent=0)
print("Return value = {}".format(a))



c_exponent = l.decompress_int16(outputArray, reconstruction)

print("Return value = {}".format(c_exponent))

for i in range(n_samples):
        print("Sample no ", i , "original number = ", inputArray[i], \
                " compressed = ", outputArray[i], " reconstructed number = ", reconstruction[i])



print ("conversion exponent = ", c_exponent)

