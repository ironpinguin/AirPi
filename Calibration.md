# Nitrogen Dioxide

[German toxological information](http://gestis.itrust.de/nxt/gateway.dll/gestis_de/001090.xml?f=templates$fn=default.htm$3.0)

From the MOS datasheet of the MiCS-4514 found at
[Smart Citizen Project](http://futureeverything.org/projects/smart-citizen/)
, you can find a log-log sheet for the
OX sensor. Since there are no data rows, we use this. Measurement on a
re-scaled graph result in a 44.6° measured angle, which is an inclination of
0.992. That results in a formula

__log10(y) = a + 0.992 * log10(x)__

Points (6|40) and (0.01|0.06) can roughly be read from the graph, an a of 0.8 gives a nice fit
Wolfram Alpha resolves this to 

__x = 0.156152 * y ^ 1.00806__

Values need to be factorized with the pulldown resistance of 10000. 
The output from the CSV with the Ohm values can be transformed with awk: 

__cat airpi.csv | cut -d ";" -f 5 | awk '{print 0.156152\*($0 / 10000)^1.00806}'__

Problem: We measure about 0.04 ppm currently, the sensor is said to range from 0.05 to 10 ppm
